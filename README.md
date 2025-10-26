# DeepSeek CLI 助手项目说明

本仓库提供一个基于 **DeepSeek API** 的命令行智能助手，完整逻辑封装在 `deepseek.ipynb` Notebook 中。Notebook 既可在 Jupyter/Colab 中逐单元格运行，也可直接转换为脚本，在本地终端体验带有提示词优化、结构化提示输出以及可选联网搜索的对话流程。

> **提示**：仓库包含 `tests/test_prompt_optimizer.py`，在本地或 CI 环境运行 `pytest` 可验证 Notebook 中的核心逻辑不会因重构而回归。

---

## 功能概览

- **命令行对话循环**：执行 Notebook 最后一段代码后会启动 `run_cli_assistant()`，支持持续多轮对话，并内置 `退出`、`清除`、`继续` 等控制指令。对话历史会作为上下文自动保留。
- **提示词润色与结构化包装**：`PromptOptimizer` 会在发送给模型前对用户输入进行优化，生成带有角色、背景、输出要求的结构化提示词，同时返回评分、改进建议及逻辑链条，方便复用与人工审阅。
- **可选联网搜索增强**：输入以 `搜索:` 或 `搜索：` 开头的问题时会调用 `search_web()` 访问 Serper API，并借助 `get_webpage_content()` 抓取网页正文后整合进提问上下文。所有 URL 会经过 `_is_safe_url()` 校验，避免访问内网或环回地址。
- **流式输出体验**：`get_ai_streaming_response()` 以流式方式打印模型回答，同时保留完整文本，用于追加到会话历史。
- **健壮的错误处理**：针对缺失密钥、空输入、请求异常、结构化提示词过短或过长等场景都提供了提示或降级路径，确保 CLI 在真实环境中更加可靠。

---

## 仓库结构

```
.
├── README.md               项目说明（当前文件）
├── deepseek.ipynb          Notebook 版 DeepSeek CLI 助手
└── tests
    └── test_prompt_optimizer.py  覆盖核心逻辑的单元测试
```

### Notebook 代码组织

1. **环境准备**：导入依赖、读取 `DEEPSEEK_API_KEY`、构建指向 `https://api.deepseek.com` 的 `OpenAI` 客户端，并在缺少密钥时抛出清晰提示。
2. **工具与数据结构**：包括打字机式输出的 `print_streaming()`、保存优化结果的 `OptimizedPrompt` 数据类，以及结构化提示模板常量。
3. **PromptOptimizer 组件**：
   - 去重缓存与复用 (`_cache`、`reuse_last()`、`mark_used()`)
   - 调用 DeepSeek 优化原始提示词 (`_call_model()`)
   - 生成结构化模板、评分、反馈与逻辑链条 (`build_structured_prompt()`、`review_prompt()`、`build_logic_flow()`)
   - 确保从缓存读出的对象是深拷贝，避免后续编辑污染缓存。
4. **联网搜索与网页抓取**：通过 Serper 搜索接口获取结果，合并网页正文，并限制最大重定向次数与可访问域。
5. **CLI 主流程**：处理用户输入、触发提示词优化、允许人工编辑结构化提示词、复用最近一次确认的提示词，并以流式方式展示回答。

### 测试覆盖重点

`tests/test_prompt_optimizer.py` 通过加载 Notebook 并注入 Stub 模块来模拟离线执行环境，重点校验以下行为：

- **缓存独立性**：手工编辑返回对象不会污染缓存结果，再次调用 `optimize()` 会得到新的独立实例。
- **复用提示词需显式确认**：只有通过 `mark_used()` 标记的 payload 才会被 `reuse_last()` 复用，防止误复用。
- **搜索提示语句包含特定中文引导**，确保 CLI 文案稳定。
- **不安全 URL 会被拒绝访问**，包括 `ftp://` 与 `127.0.0.1`。

---

## 环境准备

1. **安装依赖**（可在 Notebook 顶部取消注释 `%pip install ...`，或直接在终端执行）：
   ```bash
   pip install openai requests beautifulsoup4
   ```
2. **配置环境变量**：
   - `DEEPSEEK_API_KEY`（必填）：从 [DeepSeek 平台](https://platform.deepseek.com/) 获取，用于调用 `deepseek-chat` 模型。
   - `SERPER_API_KEY`（可选）：从 [Serper](https://serper.dev/) 获取，用于启用联网搜索。

### 环境变量示例

```bash
# Linux / macOS
export DEEPSEEK_API_KEY="你的_deepseek_api_key"
export SERPER_API_KEY="你的_serper_api_key"  # 不使用搜索时可省略
```

```powershell
# Windows PowerShell
setx DEEPSEEK_API_KEY "你的_deepseek_api_key"
setx SERPER_API_KEY "你的_serper_api_key"  # 不使用搜索时可省略
```

重新打开终端或 IDE 后，Notebook 即可读取以上配置。

---

## 运行方式

1. 打开 `deepseek.ipynb` 并依次执行所有单元格（或选择 “Run All”）。
2. 命令行提示 `用户:` 时输入问题即可开始对话。
3. 在输入中使用 `搜索: 关键词`（支持全角/半角冒号）即可触发联网搜索；若未设置 `SERPER_API_KEY`，CLI 会提示搜索不可用并继续使用原始问题。
4. 在提示词优化阶段，按照提示选择：
   - `y` / 回车：直接使用模型生成的结构化提示词；
   - `n`：放弃本次结果，返回输入阶段；
   - `e`：手动编辑结构化提示词，输入完成后以单独一行 `END` 结束，CLI 会重新评分并生成新的逻辑链条。
5. 随时输入 `清除` 重置对话历史，或输入 `继续` 复用最近一次已确认的结构化提示词。
6. 输入 `退出` 结束对话循环。

如需在纯 Python 环境下运行，可将 Notebook 转换为脚本（例如使用 `nbconvert` 或上述 `deepseek.py` 示例），并在脚本末尾调用 `run_cli_assistant()`。

---

## 开发与测试

- **运行单元测试**：
  ```bash
  pytest
  ```
  测试会加载 Notebook、注入离线 Stub 模块，并验证提示词优化缓存、搜索提示语句、URL 安全策略等关键逻辑。

- **断网或无密钥情况下的体验**：
  - `_require_api_key()` 会在缺失 `DEEPSEEK_API_KEY` 时抛出清晰异常，提醒用户提前配置。
  - 测试环境通过 Stub 保证 `openai`、`requests`、`bs4` 模块可用，即使在无网络的 CI 环境也能完成测试。

- **扩展思路**：如需自定义输出格式、增加多轮搜索或接入其他 API，可在 `PromptOptimizer` 和 `run_cli_assistant()` 的交互逻辑基础上继续扩展。

---

## 常见问题解答

| 问题 | 解决方案 |
| --- | --- |
| 提示缺少 `DEEPSEEK_API_KEY` | 检查环境变量是否正确设置，或直接在 Notebook 中替换占位符。 |
| 搜索功能不可用 | 未设置 `SERPER_API_KEY` 时会收到友好提示，仍可继续对话。 |
| URL 抓取失败 | `_is_safe_url()` 会拒绝非 HTTP(S)、内网或环回地址；确认链接是否公开可访问。 |
| 手动编辑后的提示词被缓存污染 | `PromptOptimizer` 会深拷贝缓存，确保再次调用 `optimize()` 时得到干净的副本。 |

祝使用顺利，欢迎在此基础上构建更丰富的 DeepSeek 应用！
