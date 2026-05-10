from pathlib import Path
import subprocess
from openai.types.chat import ChatCompletionToolParam 
import re


tools: list[ChatCompletionToolParam] = [
    {
        "type": "function",
        "function": {
            "name": "shell",
            "description": f"在终端运行命令。用户操作系统：。在Windows中尽量使用Powershell（command: powershell -Command \"...\"）。",
            "parameters": {
                "properties": {
                    "command": {
                        "description": "要执行的终端命令，不要换行。",
                        "type": "string"
                    },
                    "timeout": {
                        "description": "超时（秒）。",
                        "type": "integer"
                    }
                },
                "required": ["command"],
                "type": "object"
            }
        }
    },
    {
        "type": "function",
        'function': {
            'name': 'write',
            "description": "写文件。",
            "parameters": {
                "properties": {
                    "target_file": {
                        "description": "目标文件的绝对路径。",
                        "type": "string"
                    },
                    "content": {
                        "description": "文件内容。",
                        "type": "string"
                    },
                },
                "required": ["target_file",'content'],
                "type": "object"
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit",
            "description": "编辑文件内容。",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_file": {
                        "type": "string",
                        "description": "要编辑的文件的绝对路径，必须位于允许的目录范围内"
                    },
                    "content": {
                        "type": "string",
                        "description": "写入或追加的新内容。覆盖模式或追加模式必须提供"
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["overwrite", "append", "line_replace", "regex_replace"],
                        "default": "overwrite",
                        "description": "编辑模式"
                    },
                    "line_start": {
                        "type": "integer",
                        "minimum": 1,
                        "description": "行替换模式的起始行号"
                    },
                    "line_end": {
                        "type": "integer",
                        "minimum": 1,
                        "description": "行替换模式的结束行号（包含），省略则只替换起始行"
                    },
                    "regex_pattern": {
                        "type": "string",
                        "description": "正则替换模式的正则表达式字符串"
                    },
                    "replacement": {
                        "type": "string",
                        "description": "正则替换的替换文本"
                    },
                    "regex_flags": {
                        "type": "string",
                        "description": "正则修饰符，如 'g'、'gi'"
                    }
                },
                "required": ["target_file"]
            }
        }
    },
    {
        "type": "function",
        'function': {
            'name': 'read',
            "description": "读文件。",
            "parameters": {
                "properties": {
                    "target_file": {
                        "description": "目标文件的绝对路径。",
                        "type": "string"
                    }
                },
                "required": ["target_file"],
                "type": "object"
            }
        }
    }
]


def shell(command, timeout=30):
    """执行命令并返回输出"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
        if result.stdout:
            return result.stdout
        elif result.stderr:
            return f"错误: {result.stderr}"
        else:
            return f"命令执行完成，退出码: {result.returncode}"
    except subprocess.TimeoutExpired:
        return "命令执行超时"
    except Exception as e:
        return f"执行命令时出错: {str(e)}"
    

def write(target_file, content):
    """写入文件"""
    try:
        Path(target_file).write_text(content, encoding='utf-8')
        return "写入文件完成"
    except Exception as e:
        return f"写入文件时出错: {str(e)}"
        
    

def read(target_file):
    """读取文件"""
    try:
        result = Path(target_file).read_text(encoding='utf-8')
        return result
    except Exception as e:
        return f"写入文件时出错: {str(e)}"
    

def edit(arguments: dict) -> str:
    """
    按照 OpenAI Function Calling 的 edit 工具定义处理文件编辑。
    参数 arguments 为模型生成的参数字典。
    """
    target_file = arguments.get("target_file")
    mode = arguments.get("mode", "overwrite")
    content = arguments.get("content")
    line_start = arguments.get("line_start")
    line_end = arguments.get("line_end")
    regex_pattern = arguments.get("regex_pattern")
    replacement = arguments.get("replacement")
    regex_flags = arguments.get("regex_flags", "")

    # ---------- 参数校验 ----------
    if not target_file:
        return "错误：未提供 target_file（目标文件路径）。"

    if mode in ("overwrite", "append") and content is None:
        return f"错误：{mode} 模式必须提供 content。"

    if mode == "line_replace":
        if line_start is None:
            return "错误：line_replace 模式必须提供 line_start。"
        if content is None:
            return "错误：line_replace 模式必须提供 content（替换文本）。"

    if mode == "regex_replace":
        if not regex_pattern or replacement is None:
            return "错误：regex_replace 模式必须同时提供 regex_pattern 和 replacement。"

    # ---------- 执行编辑 ----------
    try:
        path = Path(target_file)

        # 1. 覆盖写入
        if mode == "overwrite":
            path.write_text(content, encoding="utf-8")
            return f"文件 {target_file} 覆盖写入完成。"

        # 2. 追加写入
        elif mode == "append":
            with path.open("a", encoding="utf-8") as f:
                f.write(content)
            return f"文件 {target_file} 追加写入完成。"

        # 3. 行范围替换
        elif mode == "line_replace":
            # 读取文件，保留行尾换行符（避免改变原文件换行风格）
            lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
            total_lines = len(lines)

            # 转换为 0-based 索引
            start_idx = line_start - 1
            if start_idx >= total_lines:
                return f"错误：起始行 {line_start} 超出文件总行数 {total_lines}。"

            # 确定删除范围的结束索引（包含该行）
            if line_end is not None:
                end_idx = line_end - 1
                if end_idx >= total_lines:
                    return f"错误：结束行 {line_end} 超出文件总行数 {total_lines}。"
                if end_idx < start_idx:
                    return f"错误：line_end ({line_end}) 不能小于 line_start ({line_start})。"
            else:
                end_idx = start_idx  # 仅替换一行

            # 删除原行，再在起始位置插入新内容
            new_lines = lines[:start_idx] + lines[end_idx + 1:]
            content_lines = content.splitlines(keepends=True)
            new_lines[start_idx:start_idx] = content_lines

            path.write_text("".join(new_lines), encoding="utf-8")
            return f"文件 {target_file} 行替换完成（行 {line_start}" + (f" - {line_end}" if line_end else "") + "）。"

        # 4. 正则查找替换
        elif mode == "regex_replace":
            text = path.read_text(encoding="utf-8")

            # 解析正则标志
            flags = 0
            if "i" in regex_flags:
                flags |= re.IGNORECASE
            if "m" in regex_flags:
                flags |= re.MULTILINE
            if "s" in regex_flags:      # 使 . 也匹配换行符
                flags |= re.DOTALL

            # 若包含 'g' 则全局替换，否则仅替换第一个匹配项
            count = 0 if "g" in regex_flags else 1

            new_text = re.sub(regex_pattern, replacement, text, count=count, flags=flags)
            path.write_text(new_text, encoding="utf-8")
            return f"文件 {target_file} 正则替换完成。"

        else:
            return f"错误：不支持的编辑模式 '{mode}'。"

    except FileNotFoundError:
        return f"错误：文件 {target_file} 不存在。"
    except PermissionError:
        return f"错误：没有权限操作文件 {target_file}。"
    except IsADirectoryError:
        return f"错误：{target_file} 是一个目录，不能按文件处理。"
    except Exception as e:
        return f"编辑文件时发生异常: {str(e)}"