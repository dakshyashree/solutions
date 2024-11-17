import os
import logging
from typing import List

# Configure logging
logging.basicConfig(filename="logs/app.log", level=logging.INFO, format="%(asctime)s: %(message)s")
logger = logging.getLogger(__name__)

def create_directory(dir_path: str) -> None:
    """
    Creates a directory if it doesn't exist.

    Args:
        dir_path (str): Path to the directory to create.
    """
    try:
        os.makedirs(dir_path, exist_ok=True)
        logger.info(f"Directory created: {dir_path}")
    except Exception as e:
        logger.error(f"Failed to create directory {dir_path}: {e}")
        raise

def split_text_into_chunks(text: str, max_chunk_length: int) -> List[str]:
    """
    Splits a large text into smaller chunks.

    Args:
        text (str): The input text to split.
        max_chunk_length (int): The maximum length of each chunk.

    Returns:
        List[str]: A list of text chunks.
    """
    if not text:
        logger.warning("Empty text received for splitting.")
        return []

    chunks = [text[i:i + max_chunk_length] for i in range(0, len(text), max_chunk_length)]
    logger.info(f"Text split into {len(chunks)} chunks of size {max_chunk_length}.")
    return chunks

def save_to_file(content: str, file_path: str) -> None:
    """
    Saves a given string to a file.

    Args:
        content (str): The content to save.
        file_path (str): The path to the file.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        logger.info(f"Content saved to file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to save content to file {file_path}: {e}")
        raise