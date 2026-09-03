# Claude Code (From Scratch) in Python

[![CodeCrafters Challenge](https://img.shields.io/badge/CodeCrafters-Claude%20Code-0A84FF?style=flat&logo=codecrafters)](https://app.codecrafters.io)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=flat&logo=checkmarx)](https://app.codecrafters.io)
[![Language](https://img.shields.io/badge/Language-Python%203.11+-blue?style=flat&logo=python)](https://python.org)

An autonomous, Claude-powered coding agent built from scratch using Python, the OpenRouter API, and function-calling schemas.

### Implemented Features
- **Agent Loop**: Multi-turn conversation handling via `while True` loop and contextual message history.
- **Read Tool**: File system inspection and content retrieval.
- **Write Tool**: File creation and directory structure persistence.
- **Bash Tool**: Command execution via `subprocess` with captured standard streams.[![progress-banner](https://backend.codecrafters.io/progress/claude-code/67a4d643-8575-4f6c-ac05-f0cea8fb268c)](https://app.codecrafters.io/users/esha-shah-warsi?r=2qF)

This is a starting point for Python solutions to the
["Build Your own Claude Code" Challenge](https://codecrafters.io/challenges/claude-code).

Claude Code is an AI coding assistant that uses Large Language Models (LLMs) to
understand code and perform actions through tool calls. In this challenge,
you'll build your own Claude Code from scratch by implementing an LLM-powered
coding assistant.

Along the way you'll learn about HTTP RESTful APIs, OpenAI-compatible tool
calling, agent loop, and how to integrate multiple tools into an AI assistant.

**Note**: If you're viewing this repo on GitHub, head over to
[codecrafters.io](https://codecrafters.io) to try the challenge.

# Passing the first stage

The entry point for your `claude-code` implementation is in `app/main.py`. Study
and uncomment the relevant code, and submit to pass the first stage:

```sh
codecrafters submit
```

# Stage 2 & beyond

Note: This section is for stages 2 and beyond.

1. Ensure you have `uv` installed locally.
2. Run `./your_program.sh` to run your program, which is implemented in
   `app/main.py`.
3. Run `codecrafters submit` to submit your solution to CodeCrafters. Test
   output will be streamed to your terminal.
