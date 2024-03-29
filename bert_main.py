from preprocessig import Preprocessor
import numpy as np
from utils import get_saved_model


def predict_all(inputs):
    """
    Predicts sentiment probabilities for a batch of inputs using a saved TensorFlow model.

    Parameters:
        inputs (numpy.ndarray): A list of input texts to predict sentiment for.

    Returns:
        numpy.ndarray: An array containing the mean sentiment probabilities for the
        batch of inputs.
    """
    MODEL_PATH = r'./model_saves/V1_02242024/model_batch_832'
    model = get_saved_model(MODEL_PATH)

    preprocessor = Preprocessor()
    preprocessed = preprocessor.preprocess_all(inputs)

    input_ids, attention_masks = preprocessor.tokenize_and_pad(preprocessed)

    X = [input_ids, attention_masks]

    result_bert = model.predict(X)

    # Convert softmax probabilities to binary predictions.
    y_pred_bert = np.zeros_like(result_bert)
    y_pred_bert[np.arange(len(y_pred_bert)), result_bert.argmax(1)] = 1

    # Calculate the mean probabilities across the batch, so we can visualize
    # them using a pie chart later on.
    mean_probas = np.mean(y_pred_bert, axis=0)

    return mean_probas
