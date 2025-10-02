# DeepSeek API Notebook

本仓库包含一个演示如何在 Python 笔记本中调用 DeepSeek API 的示例。除了基础的对话功能外，还可选地结合 Serper 搜索服务，通过联网检索增强模型回答。

## 功能特点
- 通过命令行循环与 DeepSeek 模型对话，支持清除上下文和退出指令。
- 可配置的联网搜索能力：在提供 `SERPER_API_KEY` 的前提下，先根据用户查询调用 Serper 搜索，再将整理后的结果交给 DeepSeek。
- 对错误情况（如缺少密钥、搜索词为空等）进行了友好的提示。

## 环境准备
1. 安装依赖：
   ```bash
   pip install openai requests beautifulsoup4
   ```
2. 申请所需密钥：
   - `DEEPSEEK_API_KEY`：访问 [DeepSeek](https://platform.deepseek.com/) 获取。
   - `SERPER_API_KEY`（可选）：访问 [Serper](https://serper.dev/) 获取，用于启用联网搜索。

## 配置密钥
为避免在代码中硬编码敏感信息，请通过环境变量等安全方式提供密钥。例如在 Linux 或 macOS 终端中：

```bash
export DEEPSEEK_API_KEY="你的_deepseek_api_key"
export SERPER_API_KEY="你的_serper_api_key"  # 若不需要搜索，可省略
```

在 Windows PowerShell 中：

```powershell
setx DEEPSEEK_API_KEY "你的_deepseek_api_key"
setx SERPER_API_KEY "你的_serper_api_key"  # 若不需要搜索，可省略
```

配置完成后重新打开终端或 IDE，即可在笔记本中读取环境变量。

## 运行示例
1. 打开 `deepseek.ipynb`。
2. 按顺序执行所有单元格。
3. 在终端交互界面中输入提问即可开始对话：
   - 输入 `退出` 结束程序。
   - 输入 `清除` 重置历史对话。

如未设置 `SERPER_API_KEY`，搜索功能会自动禁用，仍可进行普通对话。

## 注意事项
- 请妥善保管 API 密钥，不要提交到版本控制或公开仓库。
- 运行前请确认网络访问 DeepSeek 与 Serper 的相关域名。
- 如果需要在不同项目中重复使用，可将密钥配置在系统级环境变量或使用更安全的密钥管理工具。
