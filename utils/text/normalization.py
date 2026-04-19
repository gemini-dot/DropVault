"""
This module provides functions for normalizing text, including removing accents and creating URL-friendly slugs.
@copyright: 2026 DropVault Team
@created: 2026-04-17 5:40 PM
@Author: CuSam
@license: Private / Internal Use Only
"""

import unicodedata
import re


def remove_accents(text: str) -> str:
    if not isinstance(text, str):
        return ""

    nfkd_form = unicodedata.normalize("NFKD", text)

    no_accent = "".join(c for c in nfkd_form if not unicodedata.combining(c))

    no_accent = re.sub(r"\s+", " ", no_accent).strip()

    return no_accent


def slugify(text: str) -> str:
    text = remove_accents(text)
    text = text.lower()

    text = re.sub(r"[^a-z0-9\s-]", "", text)

    text = re.sub(r"\s+", "-", text)

    text = re.sub(r"-+", "-", text)

    return text.strip("-")
