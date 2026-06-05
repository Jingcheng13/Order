from pathlib import Path
import subprocess
from openai.types.chat import ChatCompletionToolParam 


tools: list[ChatCompletionToolParam] = [
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": f"在终端运行命令。用户操作系统：。在Windows中尽量使用Powerrun_command（command: powerrun_command -Command \"...\"）。",
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
            'name': 'write_file',
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
        'function': {
            'name': 'read_file',
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


'''
import subprocess

# 执行命令
result = subprocess.run(
    command, 
    shell=True, 
    capture_output=True, 
    text=True, 
    timeout=timeout
)

# 获取输出
stdout_output = result.stdout      # 标准输出
stderr_output = result.stderr      # 错误输出
return_code = result.returncode    # 返回码（0表示成功）

print(f"标准输出: {stdout_output}")
print(f"错误输出: {stderr_output}")
print(f"返回码: {return_code}")
'''

def run_command(command, timeout=30):
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
    

def write_file(target_file, content):
    try:
        Path(target_file).write_text(content, encoding='utf-8')
        return "写入文件完成"
    except Exception as e:
        return f"写入文件时出错: {str(e)}"
        
    

def read_file(target_file):
    try:
        result = Path(target_file).read_text(encoding='utf-8')
        return result
    except Exception as e:
        return f"读取文件时出错: {str(e)}"
