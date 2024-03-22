import json
from typing import Dict, Any

import numpy as np
from scipy.sparse import hstack

from api.simulator.model import ResponsePrediction
from core.bert_model_provider import bert_service
from core.encoder_model_provider import encoder_provider
from core.label_encoder_provider import label_encoder_provider
from core.logger_provider import logger
from core.model_ai_provider import model_admin as ma, model_paths
from core.normalization_provider import normalize_text
from core.scaler_model_provider import scaler_provider


def action_for_model0(user_input: Dict[str, Any], model: Any, code_model: str) -> None:
    logger.info(f"PREDICT MODEL 0: input {user_input}  code_model: {code_model}.")
    categorical_columns = ['type', 'manufacturer']

    encoder = encoder_provider.get_encoder(code_model)
    scaler = scaler_provider.get_scaler(code_model)
    label_encoder_classes = label_encoder_provider.get_label_encoder(code_model)

    extracted_name_hidden, extracted_description_hidden, final_input_array, scaled_price = prepare_input(
        user_input, scaler, encoder, categorical_columns)

    predicted_labels = predict_model_1(final_input_array, model)
    predicted_labels_2 = compare_predictions(predicted_labels, label_encoder_classes)

    logger.info(f"PREDICT MODEL 0: predict_ labels{predicted_labels}")
    logger.info(f"PREDICT MODEL 0: predict_ labels{predicted_labels_2}")


def action_for_model1(user_input: Dict[str, Any], model: Any, code_model: str) -> None:
    logger.info(F"PREDICT MODEL 2: input {user_input}  code_model: {code_model}.")
    # Process payload with model2


def action_for_model2(user_input: Dict[str, Any], model: Any, code_model: str) -> None:
    # Process payload with model3
    return


def action_for_model3(user_input: Dict[str, Any], model: Any, code_model: str) -> None:
    # Process payload with model3
    return


def action_for_model4(user_input: Dict[str, Any], model: Any, code_model: str) -> None:
    # Process payload with model3
    return


def default_action(user_input: Dict[str, Any], model: Any, code_model: str) -> None:
    # Default action for unhandled model codes
    return


def predict_with_models(request: dict[str, Any]) -> ResponsePrediction:
    logger.info(f"PREDICT MODEL: request {request} ")
    models = list(model_paths.keys())
    logger.info(f"PREDICT MODEL: models {models} ")
    for _, code in enumerate(models):
        logger.info(F"Search model: {code}")
        model = ma.get_model(code)
        if model:
            logger.info(F"{code} loaded and ready for use.")
            predict_category(model, request, code)
        else:
            logger.error(f"{code} could not be loaded.")
    return ResponsePrediction(id=request["prediction_id"], payload=json.dumps(request))


def predict_category(model: Any, request: dict[str, Any], code_model: str) -> None:
    data = request["payload"]
    user_input = {
        "name": data["name"],
        "description": data["description"],
        "price": float(data["price"]),
        "type": data["product_type"],
        "manufacturer": data["manufacturer"],
    }

    action = action_switcher.get(code_model, default_action)
    action(user_input, model, code_model)


def extract_last_hidden_state(embeddings):
    return embeddings[:, -1, :]


def tokenize_and_get_embeddings(column):
    # Tokenize text
    tokenizer = bert_service.get_tokenizer()
    bert_model = bert_service.get_bert_model()
    if isinstance(column, str):
        tokenized_text = tokenizer(column, padding=True, truncation=True, return_tensors='tf')
    elif isinstance(column, list) and all(isinstance(item, str) for item in column):
        tokenized_text = tokenizer(column, padding=True, truncation=True, return_tensors='tf')
    else:
        raise ValueError("Invalid input format.")

    outputs = bert_model(tokenized_text)
    embeddings = outputs.last_hidden_state.numpy()

    return embeddings


def prepare_input(user_input, scaler, encoder, categorical_columns):
    logger.info(f"Preparing input: normalize name, description ")
    user_input['name'] = normalize_text(user_input['name'])
    user_input['description'] = normalize_text(user_input['description'])

    logger.info(f"Tokenizer input: normalize text ")
    name_embeddings = tokenize_and_get_embeddings(user_input['name'])
    description_embeddings = tokenize_and_get_embeddings(user_input['description'])
    extracted_name_hidden = extract_last_hidden_state(name_embeddings)
    extracted_description_hidden = extract_last_hidden_state(description_embeddings)
    scaled_price = scaler.transform([[user_input['price']]])[0, 0]

    encoded_user_input = [[user_input[column]] for column in categorical_columns]
    encoded_user_input = np.array(encoded_user_input).reshape(1, -1)
    encoded_categorical_features = encoder.transform(encoded_user_input)
    logger.info(f"Encoded {encoded_categorical_features.shape}")

    combined_features = hstack([encoded_categorical_features, np.array([[scaled_price]])])
    logger.info(f"Encoded {combined_features.shape}")
    num_cat_input_array = combined_features.toarray().astype(np.float32)
    final_input_array = np.concatenate((num_cat_input_array, extracted_name_hidden, extracted_description_hidden),
                                       axis=1)

    return extracted_name_hidden, extracted_description_hidden, final_input_array, scaled_price


def predict_model_1(final_input_array, model_1):
    predictions = model_1.predict(final_input_array)
    subcategory_pred_labels = np.argmax(predictions, axis=1)
    print(predictions)
    print(subcategory_pred_labels)
    return subcategory_pred_labels


def compare_predictions(subcategory_pred_labels, label_encoder_classes):
    predicted_labels = []
    for idx in subcategory_pred_labels:
        if idx < len(label_encoder_classes):
            predicted_labels.append(label_encoder_classes[idx])
        else:
            predicted_labels.append('unknown')
    return predicted_labels


action_switcher = {
    "model0": action_for_model0,
    "model1": action_for_model1,
    "model2": action_for_model2,
    "model3": action_for_model3,
    "model4": action_for_model4,
}
