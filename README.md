# DeepSeek CLI 助手（Jupyter Notebook 版）

本仓库提供了一个开箱即用的 `deepseek.ipynb` 笔记本，演示如何在命令行中与 DeepSeek 模型进行连续对话。Notebook 集成了提示词润色、流式输出、联网搜索等增强能力，运行最后一个单元格后即可在终端中体验智能助手。整个流程无需额外脚本，适合快速验证 DeepSeek API 的能力或作为自定义助手的脚手架。

## 核心功能
- **命令行对话循环**：持续与模型交流，支持上下文记忆；输入 `退出` 结束对话，输入 `清除` 重置历史。
- **提示词自动润色**：在发送请求前调用 DeepSeek 先行优化用户输入，让模型获得更清晰的指令。
- **流式响应输出**：以打字机效果实时打印回复，提升沉浸式体验。
- **可选联网搜索**：配置 `SERPER_API_KEY` 后，通过 `搜索: 关键词` 触发 Serper API，抓取网页正文供模型参考。
- **健壮错误处理**：对缺少密钥、搜索词为空、请求异常等情形给出友好的提示。

## 运行环境准备
1. **安装依赖**（在全新环境中可取消 Notebook 中 `%pip` 命令的注释，或手动执行）：
   ```bash
   pip install openai requests beautifulsoup4
   ```
2. **配置密钥**：
   - `DEEPSEEK_API_KEY`（必填）：前往 [DeepSeek 平台](https://platform.deepseek.com/) 获取。
   - `SERPER_API_KEY`（可选）：前往 [Serper](https://serper.dev/) 获取，用于启用搜索能力。

### 密钥配置示例
```bash
# Linux / macOS
export DEEPSEEK_API_KEY="你的_deepseek_api_key"
export SERPER_API_KEY="你的_serper_api_key"  # 不使用搜索时可忽略
```

```powershell
# Windows PowerShell
setx DEEPSEEK_API_KEY "你的_deepseek_api_key"
setx SERPER_API_KEY "你的_serper_api_key"  # 不使用搜索时可忽略
```

重新打开终端或 IDE 后，Notebook 即可读取这些环境变量。

## 代码逻辑链概览
1. **初始化依赖与客户端**（`deepseek.ipynb` 顶部单元格）：
   - 检查 `DEEPSEEK_API_KEY` 是否已经提供，使用 `OpenAI` 客户端指向 `https://api.deepseek.com`。
   - 可选读取 `SERPER_API_KEY`，用于后续的联网搜索。
2. **基础工具函数**：
   - `print_streaming`：以逐字符方式输出文本，实现打字机效果。
   - `search_web`：包装 Serper 搜索 API，返回搜索 JSON 或错误提示。
   - `get_webpage_content`：抓取网页正文，剔除脚本样式并截取前 1000 个字符。
3. **智能增强**：
   - `optimize_prompt`：调用 DeepSeek 对用户原始输入进行润色；失败时回退原文。
   - `get_ai_streaming_response`：携带对话历史向 DeepSeek 请求流式回复，并实时打印。
4. **主对话循环 `run_cli_assistant`**：
   - 打印功能说明，初始化包含系统提示词的历史记录。
   - 解析用户输入：
     - `退出`/`exit` 结束程序。
     - `清除`/`clear` 重置对话上下文。
     - `搜索:` 指令触发 `search_web`，若成功则抓取前两条结果的正文并拼装成新的提问。
   - 提示词优化 → 将优化结果追加到消息列表 → 调用 `get_ai_streaming_response` 获取回复 → 保存助手回应，循环继续。
5. **入口执行**：Notebook 最后执行 `run_cli_assistant()`，从而在终端启动命令行助手。

## 使用步骤
1. 打开 `deepseek.ipynb` 并按顺序运行所有单元格。首次运行会验证 `DEEPSEEK_API_KEY` 是否就绪。
2. 在出现 `用户:` 提示后直接输入问题即可对话。
3. 需要联网搜索时，输入 `搜索: 关键词`（冒号支持半角或全角）。Notebook 将：
   - 请求 Serper API 获取结果；
   - 抓取前几条链接正文，提取精简内容；
   - 将整理后的文本注入对话上下文，辅助模型回答。
4. 随时输入 `清除` 重置上下文，或输入 `退出` 结束会话。

## 常见问题
- 未配置 `SERPER_API_KEY` 时，搜索功能会被自动跳过，助手仍可正常对话。
- 若网络或 API 请求失败，程序会输出详细的错误提示，可根据提示检查网络、密钥或代理配置。
- 在生产环境中，可基于当前 Notebook 拆分成独立模块，并补充日志、重试、缓存等高级能力。

祝你使用愉快！更多细节可直接在 Notebook 中查看源码与注释。
