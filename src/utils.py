# src/utils.py

import logging
import re
from typing import List
import time

from src.constants import LOG_FILE_PATH


def setup_logging() -> None:
    logging.basicConfig(
        filename=LOG_FILE_PATH,
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )


def clean_text(text: str) -> str:
    # Remove hyphens at line breaks (e.g., 'exam-\nple' -> 'example')
    text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)

    # Replace newlines within sentences with spaces
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # Replace multiple newlines with a single newline
    text = re.sub(r"\n+", "\n", text)

    # Remove excessive whitespace
    text = re.sub(r"[ \t]+", " ", text)

    cleaned_text = text.strip()
    logging.info("Texto limpiado.")
    return cleaned_text


def chunk_text(text: str, chunk_size: int, overlap: int = 100) -> List[str]:
    # Clean the text before chunking
    text = clean_text(text)
    logging.info("Texto preparado para trocear.")

    # Tokenize the text into words
    tokens = text.split(" ")

    chunks = []
    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text = " ".join(chunk_tokens)
        chunks.append(chunk_text)
        start = end - overlap  # Move back by 'overlap' tokens

    logging.info(
        f"Texto separado en {len(chunks)} partes con tamaño de parte {chunk_size} and overlap {overlap}."
    )
    return chunks

def stream_data(texto):
    for word in texto.split(" "):
        yield word + " "
        time.sleep(0.04)
