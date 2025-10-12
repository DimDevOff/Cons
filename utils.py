"""
Файл з утилітами
File with utilities
"""
import html

def sanitize_html(text: str) -> str:
    """
    Екранує спеціальні символи HTML у тексті.
    Escapes special HTML characters in the text.

    :param text: Вхідний текст.
    :return: Екранований текст.
    """
    return html.escape(text)
