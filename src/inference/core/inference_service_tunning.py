import re
from typing import Any, Tuple
from typing import Optional

import pandas as pd
from nltk import pos_tag
from nltk.tokenize import word_tokenize

from api.simulator.model import ResponsePrediction
from core.logger_provider import logger
from core.normalization_provider import stop_words, lemmatizer


def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return 'a'  # Adjective
    elif tag.startswith('V'):
        return 'v'  # Verb
    elif tag.startswith('N'):
        return 'n'  # Noun
    elif tag.startswith('R'):
        return 'r'  # Adverb
    else:
        return 'n'  # Default to noun if not recognized


def remove_extra_new_lines(text):
    if pd.isnull(text):  # check if text is nan
        return ''  # replace with an empty string

    clean_text = [i for i in str(text).splitlines() if i.strip()]
    clean_text = ' '.join(clean_text)
    return clean_text


def remove_extra_whitespace(text: str) -> str:
    spaceless_text = re.sub(r'\s+', ' ', text)
    return spaceless_text


def remove_special_chars(text: str, remove_digits: Optional[bool] = False) -> str:
    if remove_digits:
        pattern = r'[^a-zA-Z\s]'
    else:
        pattern = r'[^a-zA-Z0-9\s]'

    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


def normalize_text(text):
    text = remove_extra_new_lines(text)

    text = remove_extra_whitespace(text)

    text = remove_special_chars(text, remove_digits=False)

    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens if token.isalpha() and token.lower() not in stop_words]
    tagged_tokens = pos_tag(tokens)
    lemmas = [lemmatizer.lemmatize(token, get_wordnet_pos(tag)) for token, tag in tagged_tokens]

    return ' '.join(lemmas)


def prepare_user_input(request: dict[str, Any]) -> dict[str, str | float]:
    data = request['payload']
    user_input = {
        "name": data['name'],
        "description": data['description'],
        "price": float(data['price']),
        "type": data['product_type'],
        "manufacturer": data['manufacturer'],
    }
    return user_input


def predict_main_category(user_input: dict[str, str | float]) -> tuple[None, None]:


    return None, None


def predict_ft_with_models(request: dict[str, Any]) -> ResponsePrediction:
    logger.info(f"PREDICT MODEL: request {request} ")
    user_input = prepare_user_input(request)
    main_category, predicted_labels_2 = predict_main_category(user_input)

    categories = ["cat1", "cat2", "cat3", "cat4", "cat5", ""]
    logger.info(categories)
    return ResponsePrediction(id=request["prediction_id"], categories=categories)
