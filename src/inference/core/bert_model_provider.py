import asyncio

from transformers import BertTokenizer, TFBertModel, PreTrainedTokenizerBase

from core.logger_provider import logger


class BertService:
    def __init__(self):
        self.tokenizer = None
        self.bert_model = None
        self.is_loaded = False

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

    def get_tokenizer(self):
        return self.tokenizer

    def get_bert_model(self):
        return self.bert_model


bert_service = BertService()
