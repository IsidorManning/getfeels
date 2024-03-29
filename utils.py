import tensorflow as tf
from transformers import TFBertModel
from dotenv import load_dotenv
import os


def get_saved_model(path):
    """
    Loads a saved TensorFlow model from the specified path.

    Parameters:
        path (str): The path to the saved model file.

    Returns:
        tf.keras.Model: The loaded TensorFlow model.
    """
    return tf.keras.models.load_model(
        path,
        custom_objects={'TFBertModel': TFBertModel}
    )


def hamta_nyckel():
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    PATH = os.path.join(BASEDIR, 'envvars.env')
    load_dotenv(PATH)
    return os.getenv("SECKEY")
