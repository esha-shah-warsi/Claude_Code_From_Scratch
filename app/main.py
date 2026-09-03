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
        }
    ]

    chat = client.chat.completions.create(
        model="anthropic/claude-haiku-4.5",
        messages=[{"role": "user", "content": args.p}],
        tools=tools,
    )

    if not chat.choices or len(chat.choices) == 0:
        raise RuntimeError("no choices in response")

    response_message = chat.choices[0].message

    # Check if the LLM wants to execute any tools
    if response_message.tool_calls:
        first_tool_call = response_message.tool_calls[0]
        func_name = first_tool_call.function.name

        if func_name == "Read":
            # Arguments come back as a JSON string: '{"file_path": "apple.py"}'
            args_dict = json.loads(first_tool_call.function.arguments)
            file_path = args_dict["file_path"]

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            print(content, end="")
    else:
        # If no tool was requested, print the regular text reply
        if response_message.content:
            print(response_message.content)


if __name__ == "__main__":
    main()