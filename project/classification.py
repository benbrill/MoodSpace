import tensorflow as tf

from tensorflow.keras import layers
from tensorflow import keras

from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
# only the top distinct words will be tracked
MAX_TOKENS = 2000

SEQUENCE_LENGTH = 500

def create_model(max_tokens=None):
    """
    creates tensorflow model and loads weights to be used in model. This is the same model contained in tfLyricClassification.ipynb
    """
    lyrics_input = keras.Input(
        shape = (500,), 
        name = "lyrics",
        dtype = "int32"
    )
    lyrics_features = layers.Embedding(max_tokens or MAX_TOKENS, 60, name = "embedding")(lyrics_input)
    lyrics_features = layers.Dropout(0.2)(lyrics_features)
    lyrics_features = layers.Conv1D(64, 5, activation='relu')(lyrics_features)
    lyrics_features = layers.MaxPooling1D(pool_size=4)(lyrics_features)
    lyrics_features = layers.LSTM(100)(lyrics_features)
    lyrics_features = layers.Dropout(0.2)(lyrics_features)
    lyrics_features = layers.Dense(64, activation='relu')(lyrics_features)
    lyrics_features = layers.Dense(32, activation='relu')(lyrics_features)
    output = layers.Dense(4, name = "energy")(lyrics_features)
    model = keras.Model(inputs=lyrics_input, outputs=[output])
    model.compile(loss='mae',
              optimizer='adam',)
    model.load_weights('./checkpoints/my_checkpoint_30') # load weights from previous training

    return model

vectorize_layer = TextVectorization(
    max_tokens=MAX_TOKENS, # only consider this many words
    output_mode='int',
    output_sequence_length=SEQUENCE_LENGTH) 

def main(df):
    """
    inputs a data frame containing spotify songs and their lyrics and outputs predictions
    of the Spotify Metrics based on the lyrics
    """
    # create model
    model = create_model() 

    # adapt and create vectorization of lyrics
    vectorize_layer.adapt(df["lyrics"].to_numpy())
    X = vectorize_layer(df["lyrics"])

    return model.predict(X) # return array of metric predictions