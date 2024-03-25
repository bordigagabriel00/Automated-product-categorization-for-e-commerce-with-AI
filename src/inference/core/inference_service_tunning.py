import os
import re
from typing import Any
from typing import Optional

import h5py
import pandas as pd
import torch
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from transformers import BertTokenizer, BertForSequenceClassification

from api.simulator.model import ResponsePrediction
from core.logger_provider import logger
from core.normalization_provider import stop_words, lemmatizer

full_path = os.getcwd()


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


def prepare_user_input(request: dict[str, Any], categories) -> dict[str, str | float]:
    data = request['payload']
    text = {
        "name": data['name'],
        "description": data['description'],
        "price": float(data['price']),
        "type": data['product_type'],
        "manufacturer": data['manufacturer'],
    }

    text['name'] = normalize_text(text['name'])
    text['description'] = normalize_text(text['description'])
    text['combined_text'] = text['name'] + " " + text['description'] + " " + categories

    return text


def compare_predictions(pred, label_encoder_classes):
    if 0 <= pred < len(label_encoder_classes):
        return label_encoder_classes[pred]
    else:
        return 'unknown'


def predict(text, tokenizer, model):
    # Preparar los tokens de entrada
    inputs = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")

    # Hacer predicción
    model.eval()  # Asegúrate de que el modelo esté en modo evaluación
    with torch.no_grad():  # Desactivar la generación de gradientes
        outputs = model(**inputs)

    # Obtener la predicción de la última capa
    logits = outputs.logits
    predicted_class_id = logits.argmax().item()
    return predicted_class_id


def predict_main_category(request: dict[str, Any], categories):
    text = prepare_user_input(request, categories)
    ft_path = f"{full_path}/assets/finetunning_1/"
    le_path = f"{full_path}/assets/label_encoder/label_encoder.h5"

    model_path = ft_path

    # Cargar el tokenizer
    tokenizer = BertTokenizer.from_pretrained(model_path)
    # Cargar el modelo
    model = BertForSequenceClassification.from_pretrained(model_path)

    pred = predict(text['combined_text'], tokenizer, model)

    logger.info(pred)

    with h5py.File(le_path, 'r') as hf:
        label_encoder_classes = hf['label_encoder'][:]

    category = compare_predictions(pred, label_encoder_classes)
    logger.info(category)

    return category.decode('utf-8')


def predict_category1(request: dict[str, Any], categories):
    text = prepare_user_input(request, categories)
    ft_path = f"{full_path}/assets/finetunning_2/"
    le_path = f"{full_path}/assets/label_encoder/label_encoder_1.h5"

    model_path = ft_path

    # Cargar el tokenizer
    tokenizer = BertTokenizer.from_pretrained(model_path)
    # Cargar el modelo
    model = BertForSequenceClassification.from_pretrained(model_path)

    pred = predict(text['combined_text'], tokenizer, model)

    logger.info(pred)

    with h5py.File(le_path, 'r') as hf:
        label_encoder_classes = hf['label_encoder_1'][:]

    category = compare_predictions(pred, label_encoder_classes)
    logger.info(category)

    return category.decode('utf-8')


def predict_category2(request: dict[str, Any], categories):
    text = prepare_user_input(request, categories)
    ft_path = f"{full_path}/assets/finetunning_3/"
    le_path = f"{full_path}/assets/label_encoder/label_encoder_2.h5"

    model_path = ft_path

    # Cargar el tokenizer
    tokenizer = BertTokenizer.from_pretrained(model_path)
    # Cargar el modelo
    model = BertForSequenceClassification.from_pretrained(model_path)

    pred = predict(text['combined_text'], tokenizer, model)

    logger.info(pred)

    with h5py.File(le_path, 'r') as hf:
        label_encoder_classes = hf['label_encoder_2'][:]

    category = compare_predictions(pred, label_encoder_classes)
    logger.info(category)

    return category.decode('utf-8')


def predict_category3(request: dict[str, Any], categories):
    text = prepare_user_input(request, categories)
    ft_path = f"{full_path}/assets/finetunning_4/"
    le_path = f"{full_path}/assets/label_encoder/label_encoder_3.h5"

    model_path = ft_path

    # Cargar el tokenizer
    tokenizer = BertTokenizer.from_pretrained(model_path)
    # Cargar el modelo
    model = BertForSequenceClassification.from_pretrained(model_path)

    pred = predict(text['combined_text'], tokenizer, model)

    logger.info(pred)

    with h5py.File(le_path, 'r') as hf:
        label_encoder_classes = hf['label_encoder_3'][:]

    category = compare_predictions(pred, label_encoder_classes)
    logger.info(category)

    return category.decode('utf-8')


def predict_category4(request: dict[str, Any], categories):
    text = prepare_user_input(request, categories)
    ft_path = f"{full_path}/assets/finetunning_5/"
    le_path = f"{full_path}/assets/label_encoder/label_encoder_4.h5"

    model_path = ft_path

    # Cargar el tokenizer
    tokenizer = BertTokenizer.from_pretrained(model_path)
    # Cargar el modelo
    model = BertForSequenceClassification.from_pretrained(model_path)

    pred = predict(text['combined_text'], tokenizer, model)

    logger.info(pred)

    with h5py.File(le_path, 'r') as hf:
        label_encoder_classes = hf['label_encoder_4'][:]

    category = compare_predictions(pred, label_encoder_classes)
    logger.info(category)

    return category.decode('utf-8')


def predict_ft_with_models(request: dict[str, Any]) -> ResponsePrediction:
    logger.info(f"PREDICT MODEL: request {request} ")

    categories = ""
    main_category = predict_main_category(request, categories)
    logger.info(main_category)

    categories += " " + main_category
    category1 = predict_category1(request, categories)
    logger.info(category1)

    categories += " " + category1
    category2 = predict_category2(request, categories)
    logger.info(category2)

    categories += " " + category2
    category3 = predict_category3(request, categories)
    logger.info(category3)

    categories += " " + category3
    category4 = predict_category4(request, categories)
    logger.info(category4)

    categories = [main_category, category1, category2, category3,category4]
    logger.info(categories)
    return ResponsePrediction(id=request["prediction_id"], categories=categories)
