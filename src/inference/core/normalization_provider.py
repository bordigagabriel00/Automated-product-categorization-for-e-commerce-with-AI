import re
from typing import Optional

import nltk
import pandas as pd
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from pydantic import BaseModel

# Initialize global variables for stopwords and lemmatizer
stop_words = None
lemmatizer: WordNetLemmatizer


async def init_normalization():
    """
    Initializes the normalization process by downloading necessary NLTK resources
    and setting up stopwords and lemmatizer.
    """
    global stop_words, lemmatizer

    nltk.download("stopwords")
    nltk.download("wordnet")
    nltk.download("omw-1.4")

    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()


def get_wordnet_pos(tag: str) -> str:
    """
    Maps NLTK part of speech tags to WordNet part of speech tags.
    """
    if tag.startswith('J'):
        return 'a'  # Adjective
    elif tag.startswith('V'):
        return 'v'  # Verb
    elif tag.startswith('N'):
        return 'n'  # Noun
    elif tag.startswith('R'):
        return 'r'  # Adverb
    return 'n'  # Default to noun


def remove_extra_new_lines(text: str) -> str:
    """
    Removes extra new lines from the text and replaces NaN values with an empty string.
    """
    if pd.isnull(text):  # check if text is NaN
        return ''  # replace with an empty string
    clean_text = ' '.join([i.strip() for i in text.splitlines() if i.strip()])
    return clean_text


def remove_extra_whitespace(text: str) -> str:
    """
    Removes extra whitespace from the text.
    """
    return re.sub(r'\s+', ' ', text)


def remove_special_chars(text: str, remove_digits: Optional[bool] = False) -> str:
    """
    Removes special characters from the text. Optionally, digits can also be removed.
    """
    pattern = r'[^a-zA-Z\s]' if remove_digits else r'[^a-zA-Z0-9\s]'
    return re.sub(pattern, '', text)


def normalize_text(text: str) -> str:
    """
    Normalizes the text by removing extra new lines, extra whitespace, special characters,
    tokenizing, removing stopwords, and lemmatizing.
    """
    text = remove_extra_new_lines(text)
    text = remove_extra_whitespace(text)
    text = remove_special_chars(text, remove_digits=False)

    tokens = [token.lower() for token in word_tokenize(text) if token.isalpha() and token.lower() not in stop_words]
    tagged_tokens = pos_tag(tokens)
    lemmas = [lemmatizer.lemmatize(token, get_wordnet_pos(tag)) for token, tag in tagged_tokens]

    return ' '.join(lemmas)
