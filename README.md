# Simple Agent

一个基于 OpenAI API 的轻量级智能体框架，支持工具调用和技能扩展。

## 项目简介

Simple Agent 是一个极简的 AI Agent 实现，通过 OpenAI API 实现对话交互和工具调用。项目架构清晰，易于理解和扩展，适合作为学习 Agent 开发的起点或快速构建个人助手。

核心特性：
- 🛠️ **工具系统**：支持执行命令、读写文件等基础操作
- 🎯 **技能扩展**：模块化技能系统，可快速添加新能力
- 💬 **对话交互**：基于 Rich 库的 Markdown 美化输出
- 🔧 **模型灵活**：支持 OpenAI 及兼容 API（如 ModelScope）

## 快速开始

### 环境准备

1. 确保已安装 Python 3.11+
2. 使用 uv 或 pip 安装依赖：

```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install python-dotenv openai rich
```

### 配置

复制 `.env.example` 为 `.env` 并填入你的 API 配置：

```env
API_KEY=your-api-key
MODEL_NAME=Qwen/Qwen3.5-397B-A17B
BASE_URL=https://api-inference.modelscope.cn/v1
```

支持任何兼容 OpenAI API 格式的服务：
- ModelScope（默认配置）
- OpenAI 官方 API
- Azure OpenAI
- 本地部署的模型服务（如 vLLM、Ollama）

### 运行

```bash
python src/main.py
```

输入 `q` 退出对话。

## 项目结构

```
simple_agent/
├── src/
│   ├── main.py              # 主程序入口
│   ├── tools.py             # 工具定义和实现
│   └── prompt/
│       ├── system_prompt.py # 系统提示词
│       └── skills.py        # 技能列表
│
├── agent/
│   ├── workspace/           # Agent 工作目录
│   │   ├── ai-ide.html      # 示例产物
│   │   └── bilibili.html
│   └── skills/              # 技能定义目录
│       └── web-design-engineer/
│           └── SKILL.md     # 技能详细说明
│
├── demo/                    # 示例代码
│   ├── ai_coder.py          # AI 编程助手示例
│   ├── ai_coder_tui.py      # TUI 版本
│   └── tools.json           # 工具配置示例
│
├── prompts/                 # 提示词参考资料
│   ├── CLAUDE.md
│   ├── claude_code_prompt.md
│   └── trae_prompt.md
│
├── .env.example             # 环境变量模板
├── pyproject.toml           # 项目配置
└── README.md
```

## 工具系统

Agent 内置三个基础工具：

### run_command

在终端执行命令，支持 Windows/Linux/macOS：

```python
{
    "name": "run_command",
    "parameters": {
        "command": "要执行的命令",
        "timeout": 30  # 可选，超时时间（秒）
    }
}
```

### write

写入文件到指定路径：

```python
{
    "name": "write",
    "parameters": {
        "target_file": "文件绝对路径",
        "content": "文件内容"
    }
}
```

### read

读取指定文件内容：

```python
{
    "name": "read",
    "parameters": {
        "target_file": "文件绝对路径"
    }
}
```

## 技能系统

技能是 Agent 的能力扩展模块，通过 Markdown 文件定义。每个技能包含：
- 技能名称和描述
- 适用场景说明
- 具体操作指南

### 已有技能

**web-design-engineer**：Web 前端开发专家
- 创建网页、着陆页、仪表盘
- 构建可交互原型和 UI 线框图
- HTML 幻灯片和动画演示
- 数据可视化

### 添加新技能

1. 在 `agent/skills/` 下创建目录：`your-skill-name/`
2. 编写 `SKILL.md` 文件，包含技能描述和操作指南
3. 在 `src/prompt/skills.py` 中注册技能名称和描述

示例结构：

```
agent/skills/your-skill/
├── SKILL.md           # 技能定义
└── references/        # 可选，参考文档
    └── patterns.md
```

## 工作流程

Agent 的核心工作流程：

1. **用户输入** → 添加到消息历史
2. **调用模型** → 携带工具定义和系统提示词
3. **工具调用** → 如模型返回 tool_calls，执行对应工具
4. **结果反馈** → 将工具输出添加到消息历史
5. **循环处理** → 直到模型返回最终文本响应
6. **输出结果** → Markdown 格式展示，包含 token 使用统计

## 示例用法

### 文件操作

```
> 创建一个 Python 脚本打印当前时间

Agent 会调用 write 工具创建文件，然后展示代码。
```

### 执行命令

```
> 查看当前目录结构

Agent 会调用 run_command 执行 dir 或 ls 命令。
```

### 技能调用

```
> 帮我做一个 B 站风格的登录页面

Agent 会读取 web-design-engineer 技能，然后创建 HTML 文件。
```

## 设计理念

### 极简架构

- 单文件实现核心逻辑（main.py 约 100 行）
- 工具定义清晰，易于扩展
- 无复杂依赖，易于部署

### 渐进增强

- 基础工具满足日常需求
- 技能系统支持专业领域扩展
- 提示词工程优化交互体验

### 安全可控

- 工作目录隔离，所有操作在 `agent/workspace/` 下进行
- 主动行为需用户明确授权
- 命令执行有超时保护

## 技术栈

- **语言**：Python 3.11+
- **API 客户端**：openai (官方 SDK)
- **终端美化**：rich (Markdown 渲染、样式输出)
- **包管理**：uv (推荐) 或 pip
- **环境配置**：python-dotenv

## 扩展建议

1. **持久化记忆**：添加向量数据库支持对话历史存储
2. **更多工具**：网络请求、代码执行沙箱、文件搜索等
3. **多模态**：支持图片、语音输入输出
4. **TUI 界面**：参考 demo/ai_coder_tui.py 实现更丰富的交互
5. **多 Agent 协作**：引入任务规划和 Agent 间通信

## 参考资料

`prompts/` 目录包含业界优秀 Agent 的提示词参考：
- Claude Code：Anthropic 的编程助手
- Trae：字节跳动的 AI IDE

这些文档有助于理解专业 Agent 的设计思路。

## 许可证

本项目为个人学习和实验项目，可自由使用和修改。

## 致谢

- OpenAI API 规范
- ModelScope 提供的模型服务
- Rich 库的终端美化能力