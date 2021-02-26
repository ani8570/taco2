from tensorflow.keras.layers import Embedding, GRU
import tensorflow as tf
from util.hparams import *

class Encoder(tf.keras.Model):
    def __init__(self, K, conv_dim):
        super(Encoder, self).__init__()
        self.embedding = Embedding(symbol_length, embedding_dim)
        self.pre_net = pre_net()
        self.cbhg = CBHG(K, conv_dim)


class Tacotron(tf.keras.Model):
    def __init__(self, K, conv_dim):
        super(Tacotron, self).__init__()
        self.encoder = Encoder(K, conv_dim)    
        self.decoder = Decoder()

    def call(self, enc_input, sequece_length, dec_input, is_training):
        batch = dec_input.shape[0]
        x = self.encoder(enc_input, sequece_length, is_training)
        x = self.decoder(batch, dec_input, x)
        return x


