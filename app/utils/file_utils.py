import os

def get_file_extension(file_path: str) -> str:
    """Return the extension of a file (e.g., '.pdf', '.txt')."""
    return os.path.splitext(file_path)[1].lower()

def get_file_name(file_path: str) -> str:
    """Return the base name of a file."""
    return os.path.basename(file_path)

def list_files_in_directory(directory: str, supported_extensions: list[str]) -> list[str]:
    """List all files in a directory that match the supported extensions."""
    valid_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in supported_extensions):
                valid_files.append(os.path.join(root, file))
    return valid_files
