from datetime import datetime
import json
import logging
from typing import Any
from openai import OpenAI
import openai
from rich import print

from agent.tools import run_command, read_file, write_file, tools
from prompt import *


logger = logging.getLogger(__name__)


class Agent:
    def __init__(self, base_url: str, api_key: str, model: str):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model

        self.messages = [
            {
                "role": "system",
                "content": [
                    {
                    "text": system_prompt,
                    "type": "text"
                    },
                    {
                    "text": skills_list,                    
                    "type": "text"
                    }
                ]
            }
        ]

        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )


    def execute_tool(self, tool_call):
        func_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        if func_name == 'run_command':
            command = arguments['command']
            print(f"[dim]执行命令: {command}[/dim]")
            return run_command(command)

        elif func_name == 'write_file':
            target_file = arguments['target_file']
            content = arguments['content']
            print(f"[dim]写入文件: {target_file}[/dim]")
            return write_file(target_file, content)

        elif func_name == 'read_file':
            target_file = arguments['target_file']
            print(f"[dim]读取文件: {target_file}[/dim]")
            return read_file(target_file)
        
        elif func_name == 'edit_file':
            target_file = arguments['target_file']
            print(f"[dim]编辑文件: {target_file}[/dim]")
            return read_file(arguments)

        else:
            logger.warning(f'未知工具调用: {func_name}')
            return f'Error: unknown tool {func_name}'


    def send_messages(self, messages: list) -> dict:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools
            )
        except openai.RateLimitError as e:
            logger.error(f"配额超限: {e}")
            return {
                'success': False,
                'error_code': 'rate_limit_error',
                'error_message': f"API 配额已用完: {e}"
            }
        except openai.APIError as e:
            logger.error(f"API 错误: {e}")
            return {
                'success': False,
                'error_code': 'api_error',
                'error_message': f"API 调用失败: {e}"
            }
        except Exception as e:
            logger.error(f"未知错误: {e}")
            return {
                'success': False,
                'error_code': 'unknown_error',
                'error_message': str(e)
            }

        if not response.choices:
            logger.error(f'API调用返回空choices，响应: {response}')

            return {
                'success': False, 
                'error_code': 'api_error',
                'error_message':f'API 调用失败，响应: {response}'
            }
        
        return {
            'success': True, 
            'content': response
        }

    
    def chat(self, user_message: str) -> dict:

        # logger.debug(f'消息列表（无system）: {self.messages}')

        self.messages.append({'role': 'user', 'content': f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {user_message}'})

        response = self.send_messages(self.messages)
        if not response['success']:
            return response
        content = response['content']

        while content.choices[0].message.tool_calls:
            # 将模型的工具调用消息加入历史
            self.messages.append(content.choices[0].message.model_dump(exclude_none=True))

            for tool_call in content.choices[0].message.tool_calls:
                tool_output = self.execute_tool(tool_call)
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_output
                })

            response = self.send_messages(self.messages)
            if not response['success']:
                return response
            content = response['content']
            
            # logger.debug(f'变量messages[1:]: {messages[1:]}')

        # logger.debug(f'模型响应: {response}')

        self.messages.append(content.choices[0].message.model_dump(exclude_none=True))

        # logger.debug(f'变量messages[1:]: {messages[1:]}')

        return {
            'success': True, 
            'ai_response': content.choices[0].message.content
        }
    

    def __call__(self, user_message: str) -> dict:
        return self.chat(user_message)




