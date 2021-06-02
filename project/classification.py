
import tensorflow as tf

from tensorflow.keras import layers
from tensorflow.keras import losses

from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras.layers.experimental.preprocessing import StringLookup

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# only the top distinct words will be tracked
MAX_TOKENS = 2000

SEQUENCE_LENGTH = 500

def create_model(max_tokens=None):

    model = tf.keras.Sequential([
    layers.Embedding(max_tokens or MAX_TOKENS, output_dim = 10, name="embedding"),
    layers.Dropout(0.2),
    layers.GlobalAveragePooling1D(),
    layers.Dropout(0.2),
    layers.Dense(8)]
    )
    model.compile(loss=losses.SparseCategoricalCrossentropy(from_logits=True),
                optimizer='adam', 
                metrics=['accuracy'])

    model.load_weights('./checkpoints/my_checkpoint_10')

    return model

vectorize_layer = TextVectorization(
    max_tokens=MAX_TOKENS, # only consider this many words
    output_mode='int',
    output_sequence_length=SEQUENCE_LENGTH) 

def vectorize_moviescript(text):
    text = tf.expand_dims(text, -1)
    return vectorize_layer(text)



def main(df):
    model = create_model()

    data = tf.data.Dataset.from_tensor_slices((df["lyrics"]))
    vectorize_layer.adapt(data)
    data_vec = data.map(vectorize_moviescript)

    return model.predict(data_vec)