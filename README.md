<h1 align="center">● CysecAI</h1>

<br>

### CysecAI CysecAI Dev Usage

> **Linux**: Recommended, I can help you with any issues you may have.
>
> **Windows**: Untested, but should work. I can't help you with any issues you may have.

Before proceeding with installation Run this notebook.

<a target="_blank" href="https://colab.research.google.com/drive/1ySI02whuIWCREEqdroyGG7nRe5uO3wjS">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="CysecAIIn Colab"/>
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

1. Run the CysecAI

```shell
poetry run cysecai --api_base "<your api base from colab notebook>" --api_key "sk-xxx" -m "gpt-3.5-turbo" --context_window 8192
```

<br>
<br>

**CysecAI** lets LLMs run code (Python, Javascript, Shell, and more) locally. You can chat with CysecAI through a ChatGPT-like interface in your terminal by running `$ CysecAI` after installing.

This provides a natural-language interface to your computer's general-purpose capabilities:

- Create and edit photos, videos, PDFs, etc.
- Control a Chrome browser to perform research
- Plot, clean, and analyze large datasets
- ...etc.

**⚠️ Note: You'll be asked to approve code before it's run.**

<br>

#### Context Window, Max Tokens

You can modify the `max_tokens` and `context_window` (in tokens) of locally running models.

For local mode, smaller context windows will use less RAM, so we recommend trying a much shorter window (~1000) if it's is failing / if it's slow. Make sure `max_tokens` is less than `context_window`.

```shell
CysecAI --local --max_tokens 1000 --context_window 3000
```

### Verbose mode

To help you inspect CysecAI we have a `--verbose` mode for debugging.

You can activate verbose mode by using it's flag (`CysecAI --verbose`), or mid-chat:

```shell
$ CysecAI
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

CysecAI allows you to set default behaviors using a `config.yaml` file.

This provides a flexible way to configure the CysecAI without changing command-line arguments every time.

Run the following command to CysecAIthe configuration file:

```
CysecAI --config
```

#### Multiple Configuration Files

CysecAI supports multiple `config.yaml` files, allowing you to easily switch between configurations via the `--config_file` argument.

**Note**: `--config_file` accepts either a file name or a file path. File names will use the default configuration directory, while file paths will use the specified path.

To create or edit a new configuration, run:

```
CysecAI --config --config_file $config_path
```

To have CysecAI load a specific configuration file run:

```
CysecAI --config_file $config_path
```

**Note**: Replace `$config_path` with the name of or path to your configuration file.

##### Example

1. Create a new `config.turbo.yaml` file
   ```
   CysecAI --config --config_file config.turbo.yaml
   ```
2. Edit the `config.turbo.yaml` file to set `model` to `gpt-3.5-turbo`
3. Run CysecAI with the `config.turbo.yaml` configuration
   ```
   CysecAI --config_file config.turbo.yaml
   ```

## Sample FastAPI Server

The generator update enables CysecAI to be controlled via HTTP REST endpoints:

```python
# server.py

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from CysecAI import CysecAI

app = FastAPI()

@app.get("/chat")
def chat_endpoint(message: str):
    def event_stream():
        for result in CysecAI.chat(message, stream=True):
            yield f"data: {result}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get("/history")
def history_endpoint():
    return CysecAI.messages
```

```shell
pip install fastapi uvicorn
uvicorn server:app --reload
```

## Safety Notice

Since generated code is executed in your local environment, it can interact with your files and system settings, potentially leading to unexpected outcomes like data loss or security risks.

**⚠️ CysecAI will ask for user confirmation before executing code.**

You can run `CysecAI -y` or set `CysecAI.auto_run = True` to bypass this confirmation, in which case:

- Be cautious when requesting commands that modify files or system settings.
- Watch CysecAI like a self-driving car, and be prepared to end the process by closing your terminal.
- Consider running CysecAI in a restricted environment like Google Colab or Replit. These environments are more isolated, reducing the risks of executing arbitrary code.

There is **experimental** support for a [safe mode](docs/SAFE_MODE.md) to help mitigate some risks.

## How Does it Work?

CysecAI equips a [function-calling language model](https://platform.openai.com/docs/guides/gpt/function-calling) with an `exec()` function, which accepts a `language` (like "Python" or "JavaScript") and `code` to run.

We then stream the model's messages, code, and your system's outputs to the terminal as Markdown.

# Contributing

Thank you for your interest in contributing! We welcome involvement from the community.

Please see our [contributing guidelines](docs/CONTRIBUTING.md) for more details on how to get involved.
