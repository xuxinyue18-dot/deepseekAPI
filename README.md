# DeepSeek CLI 助手（Jupyter Notebook 版）

本仓库提供 `deepseek.ipynb`，演示如何在 Python 笔记本环境中构建一个具备提示词优化、流式输出以及可选联网搜索能力的 DeepSeek 命令行助手。运行完全部单元格后，即可在终端中与 DeepSeek 模型持续对话。

## 功能概览
- **命令行对话循环**：支持连续提问、上下文记忆，输入 `退出` 结束会话，输入 `清除` 重置历史记录。
- **提示词自动润色**：在发送请求前调用 DeepSeek 对用户输入进行优化，使得模型获得更清晰的指令。
- **流式响应输出**：以打字机效果实时打印模型回答，提升交互体验。
- **可选的联网搜索**：配置 `SERPER_API_KEY` 后，可通过输入 `搜索: 关键词`（或 `搜索：关键词`）调用 Serper API 抓取搜索结果，并提取网页正文供模型参考。
- **健壮的错误提示**：针对缺少密钥、搜索词为空、请求异常等情况给出友好反馈。

## 环境准备
1. 安装依赖（在全新环境中可先取消 Notebook 内的 `%pip` 命令注释，或手动执行以下指令）：
   ```bash
   pip install openai requests beautifulsoup4
   ```
2. 准备所需密钥：
   - `DEEPSEEK_API_KEY`（必填）：前往 [DeepSeek 平台](https://platform.deepseek.com/) 申请。
   - `SERPER_API_KEY`（可选）：前往 [Serper](https://serper.dev/) 申请，用于启用搜索能力。

## 密钥配置示例
请使用环境变量或其他安全方式提供密钥，避免将其写入代码。示例如下：

```bash
# Linux / macOS
export DEEPSEEK_API_KEY="你的_deepseek_api_key"
export SERPER_API_KEY="你的_serper_api_key"  # 不需要搜索时可省略
```

```powershell
# Windows PowerShell
setx DEEPSEEK_API_KEY "你的_deepseek_api_key"
setx SERPER_API_KEY "你的_serper_api_key"  # 不需要搜索时可省略
```

重新打开终端或 IDE 后，Notebook 即可读取以上环境变量。

## 使用步骤
1. 打开 `deepseek.ipynb`，按顺序执行所有单元格。首次运行会验证 `DEEPSEEK_API_KEY` 是否已配置。
2. 在命令行提示符下输入问题即可与 DeepSeek 对话。
3. 需要联网搜索时，输入 `搜索: 关键词`（冒号可为全角或半角）。Notebook 会：
   - 调用 Serper API 获取结果；
   - 抓取前几条链接正文，提取前 1000 个字符；
   - 将整理后的信息注入对话，帮助模型生成回答。
4. 可随时输入 `清除` 清空上下文，或输入 `退出` 结束程序。

## 注意事项
- 请确保运行环境能够访问 DeepSeek 与 Serper 的相关接口域名。
- 当未配置 `SERPER_API_KEY` 时，搜索功能会自动禁用，程序仍可正常进行普通对话。
- 生产环境中可根据需要进一步封装日志、重试、代理等高级能力。

更多细节请参阅 Notebook 中的源码实现。祝使用愉快！
