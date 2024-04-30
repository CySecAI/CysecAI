<h1 align="center">● Open Interpreter</h1>

<br>

![poster](https://github.com/KillianLucas/open-interpreter/assets/63927363/08f0d493-956b-4d49-982e-67d4b20c4b56)

<br>
<p align="center">
<strong>The New Computer Update</strong> introduces <strong><code>--os</code></strong> and a new <strong>Computer API</strong>. <a href="https://changes.openinterpreter.com/log/the-new-computer-update">Read On →</a>
</p>
<br>

### CysecAI Interpreter Dev Usage 

> **Linux**: Recommended, I can help you with any issues you may have.
>
> **Windows**: Untested, but should work. I can't help you with any issues you may have.

Before proceeding with installation Run this notebook. 

<a target="_blank" href="https://colab.research.google.com/drive/1ySI02whuIWCREEqdroyGG7nRe5uO3wjS">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

Wait until all dependencies and model gets downloaded.<br>
You will get a `https://<gibberish>.trycloudflare.com/` link. <br>
Copy that link with `v1` suffix, looks like `https://<gibberish>.trycloudflare.com/v1` and paste it in the api_base parameter in the next step.


1. Install poetry
  ```shell
  curl -sSL https://install.python-poetry.org | python3 -
  ```
1. Install dependencies
  ```shell
  poetry install
  ```
1. Run the interpreter
  ```shell
  poetry run cyscai --api_base "<your api base from colab notebook>" --api_key "sk-xxx" -m "gpt-3.5-turbo" 
  ```
<br>
<br>

**Open Interpreter** lets LLMs run code (Python, Javascript, Shell, and more) locally. You can chat with Open Interpreter through a ChatGPT-like interface in your terminal by running `$ interpreter` after installing.

This provides a natural-language interface to your computer's general-purpose capabilities:

- Create and edit photos, videos, PDFs, etc.
- Control a Chrome browser to perform research
- Plot, clean, and analyze large datasets
- ...etc.

**⚠️ Note: You'll be asked to approve code before it's run.**

<br>

## Demo

https://github.com/KillianLucas/open-interpreter/assets/63927363/37152071-680d-4423-9af3-64836a6f7b60

#### An interactive demo is also available on Google Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1WKmRXZgsErej2xUriKzxrEAXdxMSgWbb?usp=sharing)

#### Along with an example voice interface, inspired by _Her_:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1NojYGHDgxH6Y1G1oxThEBBb2AtyODBIK)

## Quick Start

```shell
pip install open-interpreter
```

### Terminal

After installation, simply run `interpreter`:

```shell
interpreter
```

### Python

```python
from interpreter import interpreter

interpreter.chat("Plot AAPL and META's normalized stock prices") # Executes a single command
interpreter.chat() # Starts an interactive chat
```

## Comparison to ChatGPT's Code Interpreter

OpenAI's release of [Code Interpreter](https://openai.com/blog/chatgpt-plugins#code-interpreter) with GPT-4 presents a fantastic opportunity to accomplish real-world tasks with ChatGPT.

However, OpenAI's service is hosted, closed-source, and heavily restricted:

- No internet access.
- [Limited set of pre-installed packages](https://wfhbrian.com/mastering-chatgpts-code-interpreter-list-of-python-packages/).
- 100 MB maximum upload, 120.0 second runtime limit.
- State is cleared (along with any generated files or links) when the environment dies.

---

Open Interpreter overcomes these limitations by running in your local environment. It has full access to the internet, isn't restricted by time or file size, and can utilize any package or library.

This combines the power of GPT-4's Code Interpreter with the flexibility of your local development environment.

## Commands

**Update:** The Generator Update (0.1.5) introduced streaming:

```python
message = "What operating system are we on?"

for chunk in interpreter.chat(message, display=False, stream=True):
  print(chunk)
```

### Interactive Chat

To start an interactive chat in your terminal, either run `interpreter` from the command line:

```shell
interpreter
```

Or `interpreter.chat()` from a .py file:

```python
interpreter.chat()
```

**You can also stream each chunk:**

```python
message = "What operating system are we on?"

for chunk in interpreter.chat(message, display=False, stream=True):
  print(chunk)
```

### Programmatic Chat

For more precise control, you can pass messages directly to `.chat(message)`:

```python
interpreter.chat("Add subtitles to all videos in /videos.")

# ... Streams output to your terminal, completes task ...

interpreter.chat("These look great but can you make the subtitles bigger?")

# ...
```

### Start a New Chat

In Python, Open Interpreter remembers conversation history. If you want to start fresh, you can reset it:

```python
interpreter.messages = []
```

### Save and Restore Chats

`interpreter.chat()` returns a List of messages, which can be used to resume a conversation with `interpreter.messages = messages`:

```python
messages = interpreter.chat("My name is Killian.") # Save messages to 'messages'
interpreter.messages = [] # Reset interpreter ("Killian" will be forgotten)

interpreter.messages = messages # Resume chat from 'messages' ("Killian" will be remembered)
```

### Customize System Message

You can inspect and configure Open Interpreter's system message to extend its functionality, modify permissions, or give it more context.

```python
interpreter.system_message += """
Run shell commands with -y so the user doesn't have to confirm them.
"""
print(interpreter.system_message)
```

### Change your Language Model

Open Interpreter uses [LiteLLM](https://docs.litellm.ai/docs/providers/) to connect to hosted language models.

You can change the model by setting the model parameter:

```shell
interpreter --model gpt-3.5-turbo
interpreter --model claude-2
interpreter --model command-nightly
```

In Python, set the model on the object:

```python
interpreter.llm.model = "gpt-3.5-turbo"
```

[Find the appropriate "model" string for your language model here.](https://docs.litellm.ai/docs/providers/)

### Running Open Interpreter locally

#### Terminal

Open Interpreter uses [LM Studio](https://lmstudio.ai/) to connect to local language models (experimental).

Simply run `interpreter` in local mode from the command line:

```shell
interpreter --local
```

**You will need to run LM Studio in the background.**

1. Download [https://lmstudio.ai/](https://lmstudio.ai/) then start it.
2. Select a model then click **↓ Download**.
3. Click the **↔️** button on the left (below 💬).
4. Select your model at the top, then click **Start Server**.

Once the server is running, you can begin your conversation with Open Interpreter.

(When you run the command `interpreter --local`, the steps above will be displayed.)

> **Note:** Local mode sets your `context_window` to 3000, and your `max_tokens` to 1000. If your model has different requirements, set these parameters manually (see below).

#### Python

Our Python package gives you more control over each setting. To replicate `--local` and connect to LM Studio, use these settings:

```python
from interpreter import interpreter

interpreter.offline = True # Disables online features like Open Procedures
interpreter.llm.model = "openai/x" # Tells OI to send messages in OpenAI's format
interpreter.llm.api_key = "fake_key" # LiteLLM, which we use to talk to LM Studio, requires this
interpreter.llm.api_base = "http://localhost:1234/v1" # Point this at any OpenAI compatible server

interpreter.chat()
```

#### Context Window, Max Tokens

You can modify the `max_tokens` and `context_window` (in tokens) of locally running models.

For local mode, smaller context windows will use less RAM, so we recommend trying a much shorter window (~1000) if it's is failing / if it's slow. Make sure `max_tokens` is less than `context_window`.

```shell
interpreter --local --max_tokens 1000 --context_window 3000
```

### Verbose mode

To help you inspect Open Interpreter we have a `--verbose` mode for debugging.

You can activate verbose mode by using it's flag (`interpreter --verbose`), or mid-chat:

```shell
$ interpreter
...
> %verbose true <- Turns on verbose mode

> %verbose false <- Turns off verbose mode
```

### Interactive Mode Commands

In the interactive mode, you can use the below commands to enhance your experience. Here's a list of available commands:

**Available Commands:**

- `%verbose [true/false]`: Toggle verbose mode. Without arguments or with `true` it
  enters verbose mode. With `false` it exits verbose mode.
- `%reset`: Resets the current session's conversation.
- `%undo`: Removes the previous user message and the AI's response from the message history.
- `%tokens [prompt]`: (_Experimental_) Calculate the tokens that will be sent with the next prompt as context and estimate their cost. Optionally calculate the tokens and estimated cost of a `prompt` if one is provided. Relies on [LiteLLM's `cost_per_token()` method](https://docs.litellm.ai/docs/completion/token_usage#2-cost_per_token) for estimated costs.
- `%help`: Show the help message.

### Configuration

Open Interpreter allows you to set default behaviors using a `config.yaml` file.

This provides a flexible way to configure the interpreter without changing command-line arguments every time.

Run the following command to open the configuration file:

```
interpreter --config
```

#### Multiple Configuration Files

Open Interpreter supports multiple `config.yaml` files, allowing you to easily switch between configurations via the `--config_file` argument.

**Note**: `--config_file` accepts either a file name or a file path. File names will use the default configuration directory, while file paths will use the specified path.

To create or edit a new configuration, run:

```
interpreter --config --config_file $config_path
```

To have Open Interpreter load a specific configuration file run:

```
interpreter --config_file $config_path
```

**Note**: Replace `$config_path` with the name of or path to your configuration file.

##### Example

1. Create a new `config.turbo.yaml` file
   ```
   interpreter --config --config_file config.turbo.yaml
   ```
2. Edit the `config.turbo.yaml` file to set `model` to `gpt-3.5-turbo`
3. Run Open Interpreter with the `config.turbo.yaml` configuration
   ```
   interpreter --config_file config.turbo.yaml
   ```

## Sample FastAPI Server

The generator update enables Open Interpreter to be controlled via HTTP REST endpoints:

```python
# server.py

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from interpreter import interpreter

app = FastAPI()

@app.get("/chat")
def chat_endpoint(message: str):
    def event_stream():
        for result in interpreter.chat(message, stream=True):
            yield f"data: {result}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get("/history")
def history_endpoint():
    return interpreter.messages
```

```shell
pip install fastapi uvicorn
uvicorn server:app --reload
```

## Safety Notice

Since generated code is executed in your local environment, it can interact with your files and system settings, potentially leading to unexpected outcomes like data loss or security risks.

**⚠️ Open Interpreter will ask for user confirmation before executing code.**

You can run `interpreter -y` or set `interpreter.auto_run = True` to bypass this confirmation, in which case:

- Be cautious when requesting commands that modify files or system settings.
- Watch Open Interpreter like a self-driving car, and be prepared to end the process by closing your terminal.
- Consider running Open Interpreter in a restricted environment like Google Colab or Replit. These environments are more isolated, reducing the risks of executing arbitrary code.

There is **experimental** support for a [safe mode](docs/SAFE_MODE.md) to help mitigate some risks.

## How Does it Work?

Open Interpreter equips a [function-calling language model](https://platform.openai.com/docs/guides/gpt/function-calling) with an `exec()` function, which accepts a `language` (like "Python" or "JavaScript") and `code` to run.

We then stream the model's messages, code, and your system's outputs to the terminal as Markdown.

# Contributing

Thank you for your interest in contributing! We welcome involvement from the community.

Please see our [contributing guidelines](docs/CONTRIBUTING.md) for more details on how to get involved.

# Roadmap

Visit [our roadmap](https://github.com/KillianLucas/open-interpreter/blob/main/docs/ROADMAP.md) to preview the future of Open Interpreter.

**Note**: This software is not affiliated with OpenAI.

![thumbnail-ncu](https://github.com/KillianLucas/open-interpreter/assets/63927363/1b19a5db-b486-41fd-a7a1-fe2028031686)

> Having access to a junior programmer working at the speed of your fingertips ... can make new workflows effortless and efficient, as well as open the benefits of programming to new audiences.
>
> — _OpenAI's Code Interpreter Release_

<br>
