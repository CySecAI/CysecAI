import base64
import io
import json

from PIL import Image


def convert_to_openai_messages(
    messages,
    function_calling=True,
    vision=False,
    shrink_images=True,
    code_output_sender="assistant",
):
    """
    Converts LMC messages into OpenAI messages
    """
    new_messages = []

    for message in messages:
        # Is this for thine eyes?
        if "recipient" in message and message["recipient"] != "assistant":
            continue

        new_message = {}

        if message["type"] == "message":
            new_message["role"] = message[
                "role"
            ]  # This should never be `computer`, right?
            new_message["content"] = message["content"]

        elif message["type"] == "code":
            new_message["role"] = "assistant"
            if function_calling:
                new_message["function_call"] = {
                    "name": "execute",
                    "arguments": json.dumps(
                        {"language": message["format"], "code": message["content"]}
                    ),
                    # parsed_arguments isn't actually an OpenAI thing, it's an OI thing.
                    # but it's soo useful!
                    # "parsed_arguments": {
                    #     "language": message["format"],
                    #     "code": message["content"],
                    # },
                }
                # Add empty content to avoid error "openai.error.InvalidRequestError: 'content' is a required property - 'messages.*'"
                # especially for the OpenAI service hosted on Azure
                new_message["content"] = ""
            else:
                new_message[
                    "content"
                ] = f"""```{message["format"]}\n{message["content"]}\n```"""

        elif message["type"] == "console" and message["format"] == "output":
            if function_calling:
                new_message["role"] = "function"
                new_message["name"] = "execute"
                if message["content"].strip() == "":
                    new_message[
                        "content"
                    ] = "No output"  # I think it's best to be explicit, but we should test this.
                else:
                    new_message["content"] = message["content"]

            else:
                # This should be experimented with.
                if code_output_sender == "user":
                    if message["content"].strip() == "":
                        content = "The code above was executed on my machine. It produced no text output. what's next (if anything, or are we done?)"
                    else:
                        content = (
                            "Code output: "
                            + message["content"]
                            + "\n\nWhat does this output mean / what's next (if anything, or are we done)?"
                        )

                    new_message["role"] = "user"
                    new_message["content"] = content
                elif code_output_sender == "assistant":
                    if "@@@SEND_MESSAGE_AS_USER@@@" in message["content"]:
                        new_message["role"] = "user"
                        new_message["content"] = message["content"].replace(
                            "@@@SEND_MESSAGE_AS_USER@@@", ""
                        )
                    else:
                        new_message["role"] = "assistant"
                        new_message["content"] = (
                            "\n```output\n" + message["content"] + "\n```"
                        )

        elif message["type"] == "image":
            if vision == False:
                continue

            if "base64" in message["format"]:
                # Extract the extension from the format, default to 'png' if not specified
                if "." in message["format"]:
                    extension = message["format"].split(".")[-1]
                else:
                    extension = "png"

                # Construct the content string
                content = f"data:image/{extension};base64,{message['content']}"

                if shrink_images:
                    try:
                        # Decode the base64 image
                        img_data = base64.b64decode(message["content"])
                        img = Image.open(io.BytesIO(img_data))

                        # Resize the image if it's width is more than 1024
                        if img.width > 1024:
                            new_height = int(img.height * 1024 / img.width)
                            img = img.resize((1024, new_height))

                        # Convert the image back to base64
                        buffered = io.BytesIO()
                        img.save(buffered, format=extension)
                        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                        content = f"data:image/{extension};base64,{img_str}"
                    except:
                        # This should be non blocking. It's not required
                        # print("Failed to shrink image. Proceeding with original image size.")
                        pass

            elif message["format"] == "path":
                # Convert to base64
                image_path = message["content"]
                file_extension = image_path.split(".")[-1]

                with open(image_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

                content = f"data:image/{file_extension};base64,{encoded_string}"
            else:
                # Probably would be better to move this to a validation pass
                # Near core, through the whole messages object
                if "format" not in message:
                    raise Exception("Format of the image is not specified.")
                else:
                    raise Exception(f"Unrecognized image format: {message['format']}")

            # Calculate the size of the original binary data in bytes
            content_size_bytes = len(content) * 3 / 4

            # Convert the size to MB
            content_size_mb = content_size_bytes / (1024 * 1024)

            # Print the size of the content in MB
            # print(f"File size: {content_size_mb} MB")

            # Assert that the content size is under 20 MB
            assert content_size_mb < 20, "Content size exceeds 20 MB"

            new_message = {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": content, "detail": "low"},
                    }
                ],
            }

        elif message["type"] == "file":
            new_message = {"role": "user", "content": message["content"]}

        else:
            raise Exception(f"Unable to convert this message type: {message}")

        if isinstance(new_message["content"], str):
            new_message["content"] = new_message["content"].strip()

        new_messages.append(new_message)

    """
    # Combine adjacent user messages
    combined_messages = []
    i = 0
    while i < len(new_messages):
        message = new_messages[i]
        if message["role"] == "user":
            combined_content = []
            while i < len(new_messages) and new_messages[i]["role"] == "user":
                if isinstance(new_messages[i]["content"], str):
                    combined_content.append({
                        "type": "text",
                        "text": new_messages[i]["content"]
                    })
                elif isinstance(new_messages[i]["content"], list):
                    combined_content.extend(new_messages[i]["content"])
                i += 1
            message["content"] = combined_content
        combined_messages.append(message)
        i += 1
    new_messages = combined_messages

    if not function_calling:
        # Combine adjacent assistant messages, as "function calls" will just be normal messages with content: markdown code blocks
        combined_messages = []
        i = 0
        while i < len(new_messages):
            message = new_messages[i]
            if message["role"] == "assistant":
                combined_content = ""
                while i < len(new_messages) and new_messages[i]["role"] == "assistant":
                    combined_content += new_messages[i]["content"] + "\n\n"
                    i += 1
                message["content"] = combined_content.strip()
            combined_messages.append(message)
            i += 1
        new_messages = combined_messages
    """

    return new_messages
