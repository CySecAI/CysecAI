import getpass
import os
import time

import litellm

from .utils.display_markdown_message import display_markdown_message


def validate_llm_settings(interpreter):
    """
    Interactively prompt the user for required LLM settings
    """

    # This runs in a while loop so `continue` lets us start from the top
    # after changing settings (like switching to/from local)
    while True:
        if interpreter.offline:
            # We have already displayed a message.
            # (This strange behavior makes me think validate_llm_settings needs to be rethought / refactored)
            break

        else:
            # Ensure API keys are set as environment variables

            # OpenAI
            if interpreter.llm.model in litellm.open_ai_chat_completion_models:
                if not os.environ.get("OPENAI_API_KEY") and not interpreter.llm.api_key:
                    display_welcome_message_once()

                    display_markdown_message("> API key not found. Set to default \"sx-xxx\"")

                    interpreter.llm.api_key = "sx-xxx"
            
                if not os.environ.get("API_BASE") and not interpreter.llm.api_base:
                    display_welcome_message_once()
                    
                    display_markdown_message(
                        """> API Base URL not found
                    
                    Head to Google colab or any other platform and run below notebook to get the API Base URL.
                    
                    Link to ipynb file: https://colab.research.google.com/drive/1ySI02whuIWCREEqdroyGG7nRe5uO3wjS
                    ---
                    """
                    )
                    
                    response = input("API Base URL: ")
                    print(f"Enter API Base URL: {response}")
                    
                    interpreter.llm.api_base = response

                break
            # This is a model we don't have checks for yet.
            break

    # If we're here, we passed all the checks.

    # Auto-run is for fast, light useage -- no messages.
    # If offline, it's usually a bogus model name for LiteLLM since LM Studio doesn't require one.
    
    return


def display_welcome_message_once():
    """
    Displays a welcome message only on its first call.

    (Uses an internal attribute `_displayed` to track its state.)
    """
    if not hasattr(display_welcome_message_once, "_displayed"):
        display_markdown_message(
            """
        ● Starting **CySecAI**.
        """
        )
        time.sleep(1.5)

        display_welcome_message_once._displayed = True
