import pickle
import re
from typing import Any
from typing import Optional

import h5py
import numpy as np
import pandas as pd
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from scipy.sparse import hstack
from tensorflow.keras.models import load_model
from transformers import BertTokenizer, TFBertModel

from api.simulator.model import ResponsePrediction
from core.logger_provider import logger
from core.normalization_provider import normalize_text
from core.model_ai_provider import model_admin
from core.encoder_model_provider import encoder_provider

# Initialize NLTK resources
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


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


categorical_columns = ['type', 'manufacturer']

"""
PREDiCT 1
"""

# 'scaler.pkl'
with open(
        '/mnt/DiscoTera/ws/anyone-program/anyone-ws/final-project/src/Automated-product-categorization-for-e-commerce-with-AI/src/inference/assets/scaler/scaler.pkl',
        'rb') as file:
    scaler = pickle.load(file)
# 'label_encoder.h5'
with h5py.File(
        '/mnt/DiscoTera/ws/anyone-program/anyone-ws/final-project/src/Automated-product-categorization-for-e-commerce-with-AI/src/inference/assets/label_encoder/label_encoder.h5',
        'r') as hf:
    label_encoder_classes = hf['label_encoder'][:]

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = TFBertModel.from_pretrained('bert-base-uncased')


def extract_last_hidden_state(embeddings):
    return embeddings[:, -1, :]


def tokenize_and_get_embeddings(column):
    # Tokenize text
    if isinstance(column, str):
        tokenized_text = tokenizer(column, padding=True, truncation=True, return_tensors='tf')
    elif isinstance(column, list) and all(isinstance(item, str) for item in column):
        tokenized_text = tokenizer(column, padding=True, truncation=True, return_tensors='tf')
    else:
        raise ValueError("Invalid input format.")

    outputs = model(tokenized_text)
    embeddings = outputs.last_hidden_state.numpy()

    return embeddings


def prepare_input(user_input, scaler, encoder, categorical_columns):
    user_input['name'] = normalize_text(user_input['name'])
    user_input['description'] = normalize_text(user_input['description'])

    name_embeddings = tokenize_and_get_embeddings(user_input['name'])
    description_embeddings = tokenize_and_get_embeddings(user_input['description'])
    extracted_name_hidden = extract_last_hidden_state(name_embeddings)
    extracted_description_hidden = extract_last_hidden_state(description_embeddings)
    scaled_price = scaler.transform([[user_input['price']]])[0, 0]

    encoded_user_input = [[user_input[column]] for column in categorical_columns]
    encoded_user_input = np.array(encoded_user_input).reshape(1, -1)
    encoded_categorical_features = encoder.transform(encoded_user_input)

    combined_features = hstack([encoded_categorical_features, np.array([[scaled_price]])])
    num_cat_input_array = combined_features.toarray().astype(np.float32)
    final_input_array = np.concatenate((num_cat_input_array, extracted_name_hidden, extracted_description_hidden),
                                       axis=1)

    return extracted_name_hidden, extracted_description_hidden, final_input_array, scaled_price


def predict_model_1(final_input_array):
    model1 = model_admin.get_model("model0")
    predictions = model1.predict(final_input_array)
    subcategory_pred_labels = np.argmax(predictions, axis=1)
    return subcategory_pred_labels


def compare_predictions(subcategory_pred_labels, label_encoder_classes):
    predicted_labels = []
    for idx in subcategory_pred_labels:
        if idx < len(label_encoder_classes):
            predicted_labels.append(label_encoder_classes[idx])
        else:
            predicted_labels.append('unknown')
    return predicted_labels


def compare_predictions(subcategory_pred_labels, label_encoder_classes):
    predicted_labels = []
    for idx in subcategory_pred_labels:
        if idx < len(label_encoder_classes):
            predicted_labels.append(label_encoder_classes[idx])
        else:
            predicted_labels.append('unknown')
    return predicted_labels


def predict_main_category(user_input: dict[str, str | float]) -> str:
    encoder = encoder_provider.get_encoder("model0")
    extracted_name_hidden, extracted_description_hidden, final_input_array, scaled_price = prepare_input(user_input,
                                                                                                         scaler,
                                                                                                         encoder,
                                                                                                         categorical_columns)

    predicted_labels = predict_model_1(final_input_array)
    predicted_labels_2 = compare_predictions(predicted_labels, label_encoder_classes)
    logger.info(predicted_labels)
    logger.info(predicted_labels_2)
    logger.info(predicted_labels_2[0])
    category = predicted_labels_2[0].decode('utf-8')
    return category


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


def predict_with_models(request: dict[str, Any]) -> ResponsePrediction:
    logger.info(f"PREDICT MODEL: request {request} ")
    user_input = prepare_user_input(request)
    main_category = predict_main_category(user_input)
    categories = [main_category, "Category 2", "Category 3", "Category 4", "Category 5"]
    logger.info(categories)
    return ResponsePrediction(id=request["prediction_id"], categories=categories)
