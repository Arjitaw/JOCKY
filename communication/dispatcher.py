from crypto.crypto import encrypt_file

def execute_command(parsed_command):

    action = parsed_command.get("action")

    if action == "encrypt":
        file_path = parsed_command.get("path")

        if not file_path:
            raise ValueError("No file path provided")

        return encrypt_file(file_path)

    raise ValueError(f"Unsupported action: {action}")