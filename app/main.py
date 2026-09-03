import argparse
import json
import os
import sys

from openai import OpenAI

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    tools = [
        {
            "type": "function",
            "function": {
                "name": "Read",
                "description": "Read and return the contents of a file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The path to the file to read",
                        }
                    },
                    "required": ["file_path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "Write",
                "description": "Write content to a file",
                "parameters": {
                    "type": "object",
                    "required": ["file_path", "content"],
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The path of the file to write to",
                        },
                        "content": {
                            "type": "string",
                            "description": "The content to write to the file",
                        },
                    },
                },
            },
        },
    ]

    messages = [{"role": "user", "content": args.p}]

    while True:
        chat = client.chat.completions.create(
            model="anthropic/claude-haiku-4.5",
            messages=messages,
            tools=tools,
        )

        if not chat.choices or len(chat.choices) == 0:
            raise RuntimeError("no choices in response")

        response_message = chat.choices[0].message
        messages.append(response_message)

        if not response_message.tool_calls:
            if response_message.content:
                print(response_message.content)
            break

        for tool_call in response_message.tool_calls:
            func_name = tool_call.function.name
            args_dict = json.loads(tool_call.function.arguments)

            if func_name == "Read":
                file_path = args_dict["file_path"]
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        tool_result = f.read()
                except Exception as e:
                    tool_result = f"Error reading file: {str(e)}"

            elif func_name == "Write":
                file_path = args_dict["file_path"]
                content = args_dict["content"]
                try:
                    # Create directory path if it does not exist
                    parent_dir = os.path.dirname(file_path)
                    if parent_dir:
                        os.makedirs(parent_dir, exist_ok=True)

                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    tool_result = f"Successfully wrote to {file_path}"
                except Exception as e:
                    tool_result = f"Error writing file: {str(e)}"

            else:
                tool_result = f"Unknown tool: {func_name}"

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                }
            )


if __name__ == "__main__":
    main()