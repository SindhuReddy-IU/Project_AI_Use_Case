"""
The EntityRecognizer class facilitates the extraction of location names 
from text using a Named Entity Recognition (NER) model.
"""

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from langchain_core.messages import BaseMessage

class EntityRecognizer:
    """
    The EntityRecognizer class allows for querying and extracting location 
    names from text based on a BERT-based NER model.
    """

    def __init__(self):
        """
        Initialize the EntityRecognizer with a pre-trained BERT-based model 
        and set up a pipeline for Named Entity Recognition.
        """

        # Load the pre-trained tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER-uncased")
        model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER-uncased")

        # Create a NER pipeline with a simple aggregation strategy
        self.__ner = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy='simple')

    def location_entity_detected(self, user_message: str) -> bool:
        """
        Detect if a location entity is present in a user message.

        Parameters
        ----------
        user_message : str
            The input message from the user.

        Returns
        -------
        bool
            True if a location is detected, otherwise False.
        """

        # Extract entities from the user message
        results = self.__ner(user_message)

        # Check for location entities with a confidence score above 90%
        for result in results:
            if result['entity_group'] == 'LOC' and result['score'] > 0.9:
                return True

        return False

    def find_location(self, user_messages: list[BaseMessage]) -> str:
        """
        Search for the first location entity in a list of user messages.

        Parameters
        ----------
        user_messages : list[BaseMessage]
            A list of messages from the user.

        Returns
        -------
        str
            The detected location name, or an empty string if none are found.
        """

        # Iterate through the user messages to find a location
        for user_message in user_messages:
            results = self.__ner(user_message.content)
            
            # Check for location entities with a confidence score above 90%
            for result in results:
                if result['entity_group'] == 'LOC' and result['score'] > 0.9:
                    return result['word']

        return ""
