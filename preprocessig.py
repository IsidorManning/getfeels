import numpy as np
from transformers import BertTokenizerFast
import re
from sklearn.preprocessing import OneHotEncoder


class Preprocessor:
    """
    A class to perform various preprocessing steps on datasets for training, testing, 
    and model usage.

    Attributes:
    tokenizer (transformers.BertTokenizerFast): Tokenizer for tokenizing text data.
    max_length (int): Maximum length of sequences after tokenization.
    one_hot_encoder (sklearn.preprocessing.OneHotEncoder): Encoder for one-hot encoding 
    labels.
    """

    def __init__(self, max_length=128):
        """
        Initializes the Preprocessing object. This is our constructor

        Parameters:
        max_length (int): Maximum length of sequences after tokenization.
        """
        self.tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
        # Since the BERT model operates on a fixed number of inputs (like many other
        # deep learning architectures), we need to set a max length for our text inputs.
        self.max_length = max_length
        # We have 3 different labels (positive, neutral, negative) so we need to one hot
        # encode our labels. The labels initially got a shape of (, 1), and after the
        # encoding we will end up with three columns, (, 3).
        self.one_hot_encoder = OneHotEncoder()

    def preprocess_all(self, data):
        """
        This method is a higher level method, used for preprocessing all the data,
        exclusive of the labels. It involves feeding the input data through a pipeline]
        of preprocessing steps.

        Parameters:
        data (numpy.ndarray): Input data to be preprocessed.

        Returns:
        numpy.ndarray: Preprocessed data.
        """

        # Step 1: Convert all data entries to strings.
        data_str = data.astype(str)
        # Step 2: Force all strings to become lowercased.
        lowercased = self.to_lower(data_str)
        # Step 3: Remove any special characters from the strings.
        no_special_characters = self.remove_special_characters(lowercased)

        return no_special_characters

    @staticmethod
    def to_lower(data):
        """
        Converts the input data to lowercase.

        Parameters:
        data (numpy.ndarray): Input data.

        Returns:
        numpy.ndarray: Lowercased data.
        """
        return np.char.lower(data)

    @staticmethod
    def remove_special_characters(array):
        """
        Removes special certain characters from the input array. The method does this
        by utilizing regular expressions.

        Parameters:
        array (numpy.ndarray): Input array containing text data.

        Returns:
        numpy.ndarray: Array with special characters removed.
        """
        def _helper(text):
            # Remove characters outside the Basic Multilingual Plane (BMP)
            text = re.sub(r'[\U00010000-\U0010ffff]', '', text)

            # Remove numeric character references (like '&#12345;')
            text = re.sub(r'&#[0-9]+;', '', text)

            return text

        # Vectorize the function so that we can use it on a numpy array.
        vectorized_helper = np.vectorize(_helper)

        return vectorized_helper(array)

    def tokenize_and_pad(self, data):
        """
        Tokenizes and pads the input data.

        Parameters:
        data (numpy.ndarray): Input data to be tokenized and padded.

        Returns:
        Tuple[numpy.ndarray, numpy.ndarray]: Tuple containing tokenized input IDs
        and attention masks.
        """

        input_ids = []
        attention_masks = []

        for i in range(len(data)):
            tokenized_input = self.tokenizer.encode_plus(
                data[i],
                padding="max_length",
                add_special_tokens=True,
                max_length=self.max_length,
                return_attention_mask=True,
                truncation=True,
            )
            input_ids.append(tokenized_input['input_ids'])
            attention_masks.append(tokenized_input['attention_mask'])

        return np.array(input_ids), np.array(attention_masks)

    def encode_labels(self, labels):
        """
        One-hot encodes the input labels.

        Parameters:
        labels (numpy.ndarray): Input labels to be one-hot encoded.

        Returns:
        numpy.ndarray: One-hot encoded labels.
        """

        # To keep the size of the array compatible, we need to convert the
        # 1-dimensional array of labels into a 2-dimensional array with a single column.
        reeshaped = np.array(labels).reshape(-1, 1)
        return self.one_hot_encoder.fit_transform(reeshaped).toarray()
