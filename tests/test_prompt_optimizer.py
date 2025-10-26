from __future__ import annotations

import json
import sys
import types
from pathlib import Path

import pytest


def _install_stubs(monkeypatch: pytest.MonkeyPatch) -> None:
    """Provide minimal stub modules so the notebook can be executed offline."""

    openai_stub = types.ModuleType("openai")

    class _DummyCompletions:
        def create(self, *args, **kwargs):  # pragma: no cover - network disabled
            raise RuntimeError("Network access is disabled in tests")

    class _DummyChat:
        def __init__(self) -> None:
            self.completions = _DummyCompletions()

    class _DummyOpenAI:
        def __init__(self, *args, **kwargs) -> None:
            self.chat = _DummyChat()

    openai_stub.OpenAI = _DummyOpenAI  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "openai", openai_stub)

    requests_stub = types.ModuleType("requests")

    class _RequestException(Exception):
        pass

    def _no_network(*args, **kwargs):  # pragma: no cover - network disabled
        raise RuntimeError("Network access is disabled in tests")

    requests_stub.post = _no_network  # type: ignore[attr-defined]
    requests_stub.get = _no_network  # type: ignore[attr-defined]
    requests_stub.RequestException = _RequestException  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "requests", requests_stub)

    bs4_stub = types.ModuleType("bs4")

    class _DummyTag:
        def decompose(self) -> None:  # pragma: no cover - behaviour unused
            return None

    class _DummyBeautifulSoup:
        def __init__(self, text: str, parser: str) -> None:
            self._text = text

        def __call__(self, names):  # pragma: no cover - behaviour unused
            return [_DummyTag() for _ in range(0)]

        def get_text(self, separator: str = "\n", strip: bool = True) -> str:
            return self._text

    bs4_stub.BeautifulSoup = _DummyBeautifulSoup  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "bs4", bs4_stub)


def _load_notebook(monkeypatch: pytest.MonkeyPatch):
    _install_stubs(monkeypatch)
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")

    nb_path = Path(__file__).resolve().parents[1] / "deepseek.ipynb"
    with nb_path.open(encoding="utf-8") as fh:
        nb = json.load(fh)

    module = types.ModuleType("deepseek_notebook")
    globals_dict = module.__dict__
    globals_dict["__name__"] = "deepseek_cli"
    monkeypatch.setitem(sys.modules, "deepseek_cli", module)

    for cell in nb["cells"]:
        if cell.get("cell_type") != "code":
            continue
        code = "".join(cell.get("source", []))
        exec(compile(code, nb_path.name, "exec"), globals_dict)

    return module


@pytest.fixture()
def notebook_module(monkeypatch: pytest.MonkeyPatch):
    return _load_notebook(monkeypatch)


def test_reuse_requires_explicit_usage(monkeypatch: pytest.MonkeyPatch, notebook_module):
    monkeypatch.setattr(
        notebook_module.PromptOptimizer,
        "_call_model",
        lambda self, prompt: prompt + " (优化)",
    )

    optimizer = notebook_module.PromptOptimizer()
    payload = optimizer.optimize(" 你好 ")

    assert optimizer.reuse_last() is None

    optimizer.mark_used(payload)
    assert optimizer.reuse_last() is payload


def test_search_prompt_uses_correct_phrase(notebook_module):
    target = "请基于以下搜索结果回答关于"
    assert any(
        isinstance(const, str) and target in const
        for const in notebook_module.run_cli_assistant.__code__.co_consts
    )


def test_manual_edits_do_not_persist_in_cache(
    monkeypatch: pytest.MonkeyPatch, notebook_module
):
    monkeypatch.setattr(
        notebook_module.PromptOptimizer,
        "_call_model",
        lambda self, prompt: f"{prompt}-optimized",
    )
    monkeypatch.setattr(
        notebook_module,
        "build_structured_prompt",
        lambda optimized: f"STRUCTURED::{optimized}",
    )
    monkeypatch.setattr(
        notebook_module,
        "review_prompt",
        lambda structured: (95, ["looks good"]),
    )

    optimizer = notebook_module.PromptOptimizer()
    first = optimizer.optimize("question")
    original_structured = first.structured
    original_feedback = list(first.feedback)

    # Simulate the CLI edit branch mutating the returned payload.
    first.structured = "MANUALLY-EDITED"
    first.feedback.append("EXTRA-FEEDBACK")

    second = optimizer.optimize("question")

    assert second is not first, "cached optimize results must return new payload objects"
    assert (
        second.structured == original_structured
    ), "manual edits should not leak into cached snapshots"
    assert second.feedback == original_feedback
    assert second.feedback is not first.feedback
