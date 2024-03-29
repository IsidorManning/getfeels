import tensorflow as tf
from keras.callbacks import ModelCheckpoint
from transformers import TFBertModel
import pandas as pd
from preprocessig import Preprocessor

# Get the train and test data sets that were used to train the BERT classification
# model. We define the local paths to where the data sets are, import their CSV data
# using Pandas, and finally, we drop all instances that contain NaN values.
train_url = r".\ds\train.csv"
test_url = r".\ds\test.csv"
train_df = pd.read_csv(train_url, encoding="unicode_escape").dropna()
test_df = pd.read_csv(test_url, encoding="unicode_escape").dropna()

# Seperate train and test data into their seperate x and y data. The x data will be the
# actual comment and the y data will be the comment's corresponding sentiment.
X_train = train_df["text"].values
y_train = train_df["sentiment"].values
X_test = test_df["text"].values
y_test = test_df["sentiment"].values

preprocessor = Preprocessor()  # We will use this class to preprocess our data.

# Preprocess all data; for the X data we preprocess and clean the data inby converting
# special symbols to strings, forcing all text to be in lowercase, and removing special
# and obsucre characters. For the y data we encode our categorical labels using
# one hot encoding.
X_train = preprocessor.preprocess_all(X_train)
y_train = preprocessor.encode_labels(y_train)
X_test = preprocessor.preprocess_all(X_test)
y_test = preprocessor.encode_labels(y_test)

# Tokenize all X data into IDs and attention masks which is necessary when using the
# BERT model. Padding is also necessary to keep dimensionality of the datasets consistent.
train_input_ids, train_attention_masks = preprocessor.tokenize_and_pad(X_train)
test_input_ids, test_attention_masks = preprocessor.tokenize_and_pad(X_test)

# Define model hyperparameters
save_path = ''
checkpoint_path = ''
alpha = 1e-5
opt = tf.keras.optimizers.Adam(learning_rate=alpha)
loss = tf.keras.losses.CategoricalCrossentropy()
accuracy = tf.keras.metrics.CategoricalAccuracy()
activation = 'softmax'
batch_size = 32
n_epochs = 3


def get_bert_from_scratch():
    """
    Retrieves a pre-trained BERT model from the Hugging Face Transformers library.

    Returns:
        transformers.modeling_tf_utils.TFBertModel: The BERT model.
    """
    bert = TFBertModel.from_pretrained('bert-base-uncased')
    return bert


def create_model_from_scratch(bert_model):
    """
    Creates a sentiment analysis model from scratch using a BERT model.

    Parameters:
        bert_model (transformers.modeling_tf_utils.TFBertModel): The pre-trained BERT
        model.

    Returns:
        tf.keras.models.Model: The created sentiment analysis model.
    """
    input_ids = tf.keras.Input(shape=(128,), dtype='int32')
    attention_masks = tf.keras.Input(shape=(128,), dtype='int32')
    embeddings = bert_model([input_ids, attention_masks])[1]
    output = tf.keras.layers.Dense(3, activation=activation)(embeddings)
    model = tf.keras.models.Model(inputs=[input_ids, attention_masks], outputs=output)
    model.compile(opt, loss=loss, metrics=accuracy)
    model.summary()

    return model


def create_model_from_saved(saved_model):
    """
    Compiles a saved sentiment analysis model for evaluation.

    Parameters:
        saved_model (tf.keras.models.Model): The saved sentiment analysis model.
        opt (tf.keras.optimizers.Optimizer): The optimizer for the model.
        loss (tf.keras.losses.Loss): The loss function for the model.
        accuracy (tf.keras.metrics.Metric): The accuracy metric for the model.

    Returns:
        tf.keras.models.Model: The compiled sentiment analysis model.
    """
    saved_model.compile(opt, loss=loss, metrics=accuracy)

    return saved_model


def train_model(model, checkpoint_path, initial_epoch=0):
    """
    Trains a sentiment analysis model.

    Parameters:
        model (tf.keras.models.Model): The sentiment analysis model.
        checkpoint_path (str): The path to save model checkpoints.
        initial_epoch (int, optional): Initial epoch number (default is 0).

    Returns:
        tf.keras.callbacks.History: History object containing training metrics.
    """
    model_checkpoint = ModelCheckpoint(checkpoint_path,
                                       monitor='categorical_accuracy',
                                       save_freq=batch_size,
                                       save_weights_only=False,
                                       mode='min',
                                       verbose=1,
                                       save_format='tf')

    history = model.fit([train_input_ids, train_attention_masks], y_train,
                        epochs=n_epochs,
                        batch_size=batch_size,
                        callbacks=[model_checkpoint],
                        initial_epoch=initial_epoch,
                        )

    model.save("bert_sentiment_model")

    return history


# Evaluate the model

def test_model(model):
    """
    Evaluates a sentiment analysis model on test data.

    Parameters:
        model (tf.keras.models.Model): The sentiment analysis model.
    """
    test_loss, test_accuracy = model.evaluate([test_input_ids, test_attention_masks],
                                              y_test)
    print(f'Test Accuracy: {test_accuracy}')
