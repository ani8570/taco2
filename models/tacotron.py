
import tensorflow as tf
from util.hparams import *

class Tacotron(tf.keras.Model):
    def __init__(self, K, conv_dim):
        super(Tacotron, self).__init__()
        

