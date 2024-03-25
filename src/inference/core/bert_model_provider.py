import asyncio

from transformers import BertTokenizer, TFBertModel, PreTrainedTokenizerBase

from core.logger_provider import logger

# Creating variables to store the tokenizer, BERT model, and loading state:
class BertService:
    def __init__(self):
        self.tokenizer = None
        self.bert_model = None
        self.is_loaded = False
        
    """
    Description 'init_load_bert_model':
    - Records the start of asynchronous loading of the tokenizer and the BERT model.
    - Asynchronous loading of the BERT tokenizer to not block execution.
    - Asynchronous loading of the BERT model, similar to the tokenizer.
    - Confirm through the logger that the model and tokenizer were loaded correctly.
    - In case of an error during charging, it records it and marks the charging status as false.
    """
    
    async def init_load_bert_model(self):
        try:
            logger.info("Starting to load the BERT model and tokenizer asynchronously")
            self.tokenizer = await asyncio.to_thread(BertTokenizer.from_pretrained, 'bert-base-uncased')
            self.bert_model = await asyncio.to_thread(TFBertModel.from_pretrained, 'bert-base-uncased')
            self.is_loaded = True
            logger.info("Successfully loaded the BERT model and tokenizer")
        except Exception as e:
            logger.error(f"An error occurred while loading the BERT model and tokenizer: {e}")
            self.is_loaded = False

    # Access to loaded BERT tokenizer:
    def get_tokenizer(self):
        return self.tokenizer

    # Access to loaded BERT model:
    def get_bert_model(self):
        return self.bert_model

# Model loading initialization and BERT tokenizer:
bert_service = BertService()
