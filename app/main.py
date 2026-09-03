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

    # Initialize the conversation history with the user's prompt
    messages = [{"role": "user", "content": args.p}]

    # The Agent Loop
    while True:
        chat = client.chat.completions.create(
            model="anthropic/claude-haiku-4.5",
            messages=messages,
            tools=tools,
        )

        if not chat.choices or len(chat.choices) == 0:
            raise RuntimeError("no choices in response")

        response_message = chat.choices[0].message

        # Append the assistant's response to the conversation history
        messages.append(response_message)

        # If the LLM has no more tool calls, print the final answer and exit the loop
        if not response_message.tool_calls:
            if response_message.content:
                print(response_message.content)
            break

        # Execute each tool requested by the model
        for tool_call in response_message.tool_calls:
            if tool_call.function.name == "Read":
                args_dict = json.loads(tool_call.function.arguments)
                file_path = args_dict["file_path"]

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                except Exception as e:
                    file_content = f"Error reading file: {str(e)}"

                # Provide the tool execution result back to the model
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": file_content,
                    }
                )


if __name__ == "__main__":
    main()