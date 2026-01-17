# AI_Bot (Tool-Using Coding Agent)

AI_Bot is a command-line AI coding assistant built in Python that can interact with a local project through a controlled set of tools. It supports both one-shot prompts and an interactive REPL mode, allowing the assistant to inspect files, write changes, execute Python scripts, and run automated tests.

This project goes beyond a basic chatbot by implementing a functional agent loop that can decide when to call tools, use tool output as context, and continue until a final response is produced.

This project is intended to be run on Linux/WSL (recommended) for the most consistent behavior and best compatibility.

---

## Key Features (Beyond the Base Boot.dev Project)

### Interactive REPL Mode

AI_Bot includes a REPL chat mode that keeps conversation context across multiple turns.

* Start the bot once and interact continuously
* Exit cleanly when finished

### Tool Calling (Local Function Execution)

The assistant can call local tools to perform real operations inside the project:

* List files and directories
* Read file contents
* Write or overwrite files
* Execute Python files with optional arguments
* Run pytest test suites

### Multi-Step Agent Loop

Instead of responding once and stopping, AI_Bot can:

1. Evaluate the request
2. Call the appropriate tool(s)
3. Interpret the results
4. Continue tool usage until the task is completed (or a safety limit is reached)

### Test Runner Integration (`run_tests`)

AI_Bot includes a `run_tests` tool that executes pytest and returns:

* Exit code
* Command used
* STDOUT / STDERR output

It also supports selecting which tests to run by path (example: `tests` vs `calculator/tests`).

### Working Directory Injection for Safety

Tool calls automatically receive a controlled working directory to reduce risk of unsafe path access. This keeps file operations scoped to expected locations.

---

## Final Project Structure

```
AI_Bot/
├─ calculator/
│  ├─ pkg/
│  │  ├─ calculator.py
│  │  ├─ render.py
│  │  └─ morelorem.txt
│  ├─ tests/
│  │  ├─ test_calculator.py
│  │  └─ test_smoke.py
│  ├─ lorem.txt
│  ├─ main.py
│  ├─ main.txt
│  └─ tests.py
│
├─ functions/
│  ├─ get_file_content.py
│  ├─ get_files_info.py
│  ├─ run_python_file.py
│  ├─ run_tests.py
│  ├─ write_file.py
│  ├─ test_get_file_content.py
│  ├─ test_get_files_info.py
│  ├─ test_run_python_file.py
│  └─ test_write_file.py
│
├─ tests/
│  └─ test_smoke.py
│
├─ .env
├─ .gitignore
├─ .python-version
├─ call_function.py
├─ config.py
├─ main.py
├─ prompts.py
├─ pyproject.toml
├─ README.md
├─ test_call_functions.py
├─ test_loop_prompt.py
├─ test_prompts.py
└─ uv.lock
```

---

## Requirements

* Python 3.12+
* uv
* Linux or WSL (recommended)
* OpenAI API key

---

## Setup

### 1) Create a `.env` file

In the project root:

```env
OPENAI_API_KEY=your_key_here
```

### 2) Install dependencies

```bash
uv sync
```

---

## Usage

### One-Shot Mode

Run a single prompt and exit:

```bash
uv run main.py "list the files in the root"
```

### REPL Mode

Start an interactive session:

```bash
uv run main.py
```

Example REPL prompts:

* `list the files in the root`
* `read the contents of main.py`
* `write 'hello' to main.txt`
* `run tests`
* `run tests in calculator/tests`

---

## Notes

This project demonstrates a practical tool-using agent workflow in a controlled local environment. The main focus is on building a functional coding agent with multi-step execution, test running, and safe project interaction rather than a simple chat-only bot.
