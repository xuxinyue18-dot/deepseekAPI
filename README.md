# DeepSeek CLI 助手（Jupyter Notebook 版）

本仓库提供的 `deepseek.ipynb` Notebook 会在本地终端中启动一个具备提示词润色、流式输出和可选联网搜索的 DeepSeek 命令行助手。运行完成后即可在命令行持续对话，方便快速验证 DeepSeek API 的能力，或作为自定义智能助手的基础脚手架。

## 功能亮点
- **一键启动的命令行助手**：Notebook 末尾执行 `run_cli_assistant()`，即可在终端进入连续对话循环，支持上下文记忆与基础控制指令（退出、清除、继续）。
- **提示词智能润色与结构化包装**：`PromptOptimizer` 会在发送请求前调用 DeepSeek 优化用户输入，并生成可复用的结构化提示词、评分与改进建议。
- **流式输出体验**：`print_streaming` 以打字机效果呈现回答，提升阅读体验。
- **可选联网搜索增强**：在输入中使用 `搜索: 关键词` 触发 Serper API，抓取网页正文并合并进提问上下文。
- **健壮的错误处理**：Notebook 覆盖了缺失密钥、无效输入、网络异常和不安全链接等场景，确保 CLI 在真实环境中的可靠性。

## Notebook 结构速览
- **环境初始化**：检查 `DEEPSEEK_API_KEY`，创建指向 `https://api.deepseek.com` 的 `OpenAI` 客户端，并按需读取 `SERPER_API_KEY`。
- **工具函数**：包括流式打印、HTTP 抓取、HTML 文本提取、防止内网地址访问等逻辑。
- **PromptOptimizer 组件**：负责提示词去重缓存、调用模型润色、结构化包装、质量评估以及“最近一次可复用提示词”的状态管理。
- **联网搜索流程**：`search_web` 调用 Serper API，`get_webpage_content` 抓取正文并过滤不可信链接；主循环会将搜索结果拼接成新的查询。
- **主循环 `run_cli_assistant`**：处理用户输入、触发提示词优化、允许人工编辑结构化提示词并调用 DeepSeek 获取流式回复。

如需查看实现细节，可直接在 Notebook 中打开相应代码单元。

## 环境准备
1. **安装依赖**（初次运行时，可在 Notebook 顶部取消注释 `%pip install ...`，或在终端手动执行）：
   ```bash
   pip install openai requests beautifulsoup4
   ```
2. **配置环境变量**：
   - `DEEPSEEK_API_KEY`（必填）：前往 [DeepSeek 平台](https://platform.deepseek.com/) 申请。
   - `SERPER_API_KEY`（可选）：前往 [Serper](https://serper.dev/) 获取，启用搜索能力。

### 环境变量示例
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

重新打开终端或 IDE 后，Notebook 即可读取上述配置。

## 使用流程
1. 打开 `deepseek.ipynb`，按顺序运行所有单元格（或使用 “Run All”）。
2. 终端提示 `用户:` 时即可输入问题开始对话。
3. 输入 `搜索: 关键词`（冒号支持半角或全角）即可触发联网搜索；若未配置 `SERPER_API_KEY` 会自动跳过并继续使用原始问题。
4. 输入 `清除` 重置对话上下文；输入 `继续` 复用最近一次确认过的结构化提示词；输入 `退出` 结束对话。
5. 在提示词优化阶段可选择使用、放弃或手动编辑结构化提示词，CLI 会根据选择继续对话或返回等待新问题。

## 测试与开发
- 运行单元测试，确保 Notebook 中的关键逻辑保持稳定：
  ```bash
  pytest
  ```
- Notebook 中的网络调用在测试环境会被替换为本地 Stub，以便离线运行。实际使用时请确保网络可用并已配置所需密钥。

## 常见问题
- **未配置搜索密钥**：未设置 `SERPER_API_KEY` 时，联网搜索会被跳过，助手仍可正常对话。
- **网络或 API 异常**：CLI 会输出详细的错误提示，请根据提示检查网络、代理或密钥是否正确。
- **安全性**：`get_webpage_content` 会拒绝内网、环回等不安全链接，避免抓取潜在危险资源。

祝使用顺利，欢迎基于此 Notebook 拓展自己的 DeepSeek CLI 助手！
