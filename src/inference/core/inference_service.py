import os
import re
from typing import Any
from typing import Optional

import h5py
import numpy as np
import pandas as pd
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from scipy.sparse import hstack
from transformers import BertTokenizer, TFBertModel

from api.simulator.model import ResponsePrediction
from core.encoder_model_provider import encoder_provider
from core.label_encoder_provider import label_encoder_provider
from core.logger_provider import logger
from core.model_ai_provider import model_admin
from core.normalization_provider import normalize_text, stop_words, lemmatizer
from core.scaler_model_provider import scaler_provider

# Initialize NLTK resources

lemmatizer = WordNetLemmatizer()
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


categorical_columns = ['type', 'manufacturer']

"""
PREDiCT 1
"""

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
    scaler = scaler_provider.get_scaler("model0")
    label_encoder_classes = label_encoder_provider.get_label_encoder("model0")
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

    return category, predicted_labels_2


"""
PREDICT 2
"""


def prepare_input_2(user_input, encoder_1, decoded_labels, scaler_1):
    user_input['name'] = normalize_text(user_input['name'])
    user_input['description'] = normalize_text(user_input['description'])

    name_embeddings = tokenize_and_get_embeddings(user_input['name'])
    description_embeddings = tokenize_and_get_embeddings(user_input['description'])

    extracted_name_hidden = extract_last_hidden_state(name_embeddings)
    extracted_description_hidden = extract_last_hidden_state(description_embeddings)

    input_data = np.array([[user_input['type'], user_input['manufacturer']]])
    predicted_labels_array = np.array(decoded_labels)[:3].reshape(1, -1)
    input_with_labels = np.hstack((input_data, predicted_labels_array))

    predicted_labels_one_hot = encoder_1.transform(input_with_labels)

    scaled_price_array = scaler_1.transform(np.array(user_input['price']).reshape(-1, 1))

    final_input_array_with_label = np.hstack((predicted_labels_one_hot.toarray(), scaled_price_array))

    final_input_array_2 = np.concatenate((final_input_array_with_label,
                                          extracted_name_hidden,
                                          extracted_description_hidden), axis=1)

    return final_input_array_2


def predict_model_2(final_input_array_with_label_1, model_2):
    predictions_1 = model_2.predict(final_input_array_with_label_1)
    subcategory_pred_labels = np.argmax(predictions_1, axis=1)

    logger.info(predictions_1)
    logger.info(subcategory_pred_labels)

    return subcategory_pred_labels


def compare_predictions_2(subcategory_pred_labels, label_encoder_classes_1):
    predicted_labels = []
    for idx in subcategory_pred_labels:
        if idx < len(label_encoder_classes_1):
            predicted_labels.append(label_encoder_classes_1[idx])
        else:
            predicted_labels.append('unknown')
    return predicted_labels


def predict_category2(user_input, decoded_labels, ):
    # Get resources
    model_1 = model_admin.get_model("model1")
    encoder_1 = encoder_provider.get_encoder("model1")
    scaler_1 = scaler_provider.get_scaler("model1")
    logger.info(f"Opening {full_path}/assets/label_encoder/label_encoder_1.h5")
    try:
        with h5py.File(f'{full_path}/assets/label_encoder/label_encoder_1.h5', 'r') as hf:
            label_encoder_classes_1 = hf['label_encoder_1'][:]
    except FileNotFoundError:
        logger.info(f"File not found {full_path}/assets")

    final_input_array_with_label_1 = prepare_input_2(user_input, encoder_1, decoded_labels, scaler_1)
    subcategory_pred_labels = predict_model_2(final_input_array_with_label_1, model_1)

    predicted_labels_3 = compare_predictions_2(subcategory_pred_labels, label_encoder_classes_1)
    print(predicted_labels_3)
    logger.info(predicted_labels_3)
    category1 = predicted_labels_3[0].decode('utf-8')

    logger.info(f"Category 1: {category1}")

    return category1, final_input_array_with_label_1


"""

PREDICT 3:
"""


def prepare_input_3(user_input, encoder_2, decoded_labels, decoded_labels_2, scaler_2):
    user_input['name'] = normalize_text(user_input['name'])
    user_input['description'] = normalize_text(user_input['description'])
    name_embeddings = tokenize_and_get_embeddings(user_input['name'])
    description_embeddings = tokenize_and_get_embeddings(user_input['description'])
    extracted_name_hidden = extract_last_hidden_state(name_embeddings)
    extracted_description_hidden = extract_last_hidden_state(description_embeddings)

    input_data = np.array([[user_input['type'], user_input['manufacturer']]])
    predicted_labels_array = np.array(decoded_labels)[:3].reshape(1, -1)
    predicted_labels_array_2 = np.array(decoded_labels_2)[:4].reshape(1, -1)
    input_with_labels = np.hstack((input_data, predicted_labels_array, predicted_labels_array_2))

    predicted_labels_one_hot = encoder_2.transform(input_with_labels)

    scaled_price_array = scaler_2.transform(np.array(user_input['price']).reshape(-1, 1))

    final_input_array_with_label = np.hstack((predicted_labels_one_hot.toarray(), scaled_price_array))
    final_input_array_3 = np.concatenate(
        (final_input_array_with_label, extracted_name_hidden, extracted_description_hidden), axis=1)

    return final_input_array_3


def predict_model_3(final_input_array_with_label_2, model_3):
    predictions_2 = model_3.predict(final_input_array_with_label_2)
    subcategory_pred_labels_2 = np.argmax(predictions_2, axis=1)
    print(predictions_2)
    print(subcategory_pred_labels_2)
    return subcategory_pred_labels_2


def compare_predictions_3(subcategory_pred_labels_2, label_encoder_classes_2):
    predicted_labels_4 = []
    for idx in subcategory_pred_labels_2:
        if idx < len(label_encoder_classes_2):
            predicted_labels_4.append(label_encoder_classes_2[idx])
        else:
            predicted_labels_4.append('unknown')
    return predicted_labels_4


def predict_category3(user_input, decoded_labels, decoded_labels_2):
    # Get resources
    model_3 = model_admin.get_model("model3")
    encoder_2 = encoder_provider.get_encoder("model3")
    scaler_2 = scaler_provider.get_scaler("model3")
    try:
        with h5py.File(f'{full_path}/assets/label_encoder/label_encoder_2.h5', 'r') as hf:
            label_encoder_classes_2 = hf['label_encoder_2'][:]
    except FileNotFoundError:
        logger.info(f"File not found {full_path}/assets")

    final_input_array_with_label_2 = prepare_input_3(user_input, encoder_2, decoded_labels, decoded_labels_2, scaler_2)
    subcategory_pred_labels_2 = predict_model_3(final_input_array_with_label_2, model_3)
    predicted_labels_5 = compare_predictions_2(subcategory_pred_labels_2, label_encoder_classes_2)

    category2 = predicted_labels_5[0].decode('utf-8')

    logger.info(f"Category 2: {category2}")

    return category2, final_input_array_with_label_2


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
    main_category, predicted_labels_2 = predict_main_category(user_input)

    # Category 1
    # decode previous output of prediction 1
    decoded_labels = [label.decode() for label in predicted_labels_2]
    category1, predicted_labels_3 = predict_category2(user_input, decoded_labels)

    # Category 2
    # decode previous output of prediction 1
    # decoded_labels_2 = [label.decode() for label in predicted_labels_3]
    # category2, predict_labels_5 = predict_category3(user_input, decoded_labels, decoded_labels_2)

    categories = [main_category, category1, "", "", ""]
    logger.info(categories)
    return ResponsePrediction(id=request["prediction_id"], categories=categories)
