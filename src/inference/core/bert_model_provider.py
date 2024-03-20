import asyncio

from transformers import BertTokenizer, TFBertModel

from core.logger_provider import logger


async def init_load_bert_model():
    """
    Asynchronously loads the BERT model and tokenizer.

    This function asynchronously initializes and loads the BERT model and tokenizer using `bert-base-uncased`
    configuration. It employs asyncio.to_thread to offload the IO-bound `from_pretrained` calls to a separate thread,
    allowing the coroutine to proceed without blocking the asyncio event loop.

    Returns:
        tuple: A tuple containing the loaded BertTokenizer and TFBertModel instances. If an error occurs during loading,
               both elements of the tuple will be None.

    Raises:
        Logs an error message if an exception occurs during the loading process. The exception itself is caught, and
        the function returns None values instead of raising the exception further.
    """
    try:
        logger.info("Starting to load the BERT model and tokenizer asynchronously")
        tokenizer = await asyncio.to_thread(BertTokenizer.from_pretrained, 'bert-base-uncased')
        model = await asyncio.to_thread(TFBertModel.from_pretrained, 'bert-base-uncased')
        logger.info("Successfully loaded the BERT model and tokenizer")
        return tokenizer, model
    except Exception as e:
        # In case of an error, log the exception and return None values.
        logger.error(f"An error occurred while loading the BERT model and tokenizer: {e}")
        return None, None
