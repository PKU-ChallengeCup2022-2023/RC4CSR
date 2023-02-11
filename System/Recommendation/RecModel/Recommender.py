import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import copy
import time
import tensorflow_addons as tfa
from .utils import *

# random.seed(42)
path = "Recommendation/RecModel/"

# 书籍信息导入
with open(path + "book_info_all.txt", "r", encoding="utf-8") as infile:
    text = infile.readlines()

for i in range(5250):
    text[i] = text[i].split(",")
    text[i][14] = text[i][14][:-1]
book_info = pd.DataFrame(text)
book_info.columns = [
    "itemid",
    "genres",
    "subtype",
    "url",
    "title",
    "author",
    "publisher",
    "publish_time",
    "aver_score",
    "score_num",
    "star_5",
    "star_4",
    "star_3",
    "star_2",
    "star_1",
]

# 模型相关信息导入
class Sampling(tf.keras.layers.Layer):
    """Uses (z_mean, z_log_var) to sample z, the vector encoding a basket."""

    def call(self, inputs):
        z_mean, z_log_var = inputs
        batch = tf.shape(z_mean)[0]
        dim = tf.shape(z_mean)[1]
        epsilon = tf.keras.backend.random_normal(shape=(batch, dim), stddev=1.0)
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon


class Model(tf.keras.Model):
    def __init__(self, num_words, latent=1024, hidden=1024, items_sampling=1.0):
        super().__init__()
        self.sampled_items = int(num_words * items_sampling)
        # ************* ENCODER ***********************
        self.encoder1 = tf.keras.layers.Dense(hidden)
        self.ln1 = tf.keras.layers.LayerNormalization()
        self.encoder2 = tf.keras.layers.Dense(hidden)
        self.ln2 = tf.keras.layers.LayerNormalization()
        self.encoder3 = tf.keras.layers.Dense(hidden)
        self.ln3 = tf.keras.layers.LayerNormalization()
        self.encoder4 = tf.keras.layers.Dense(hidden)
        self.ln4 = tf.keras.layers.LayerNormalization()
        self.encoder5 = tf.keras.layers.Dense(hidden)
        self.ln5 = tf.keras.layers.LayerNormalization()
        self.encoder6 = tf.keras.layers.Dense(hidden)
        self.ln6 = tf.keras.layers.LayerNormalization()
        self.encoder7 = tf.keras.layers.Dense(hidden)
        self.ln7 = tf.keras.layers.LayerNormalization()

        # ************* SAMPLING **********************
        self.dense_mean = tf.keras.layers.Dense(latent, name="Mean")
        self.dense_log_var = tf.keras.layers.Dense(latent, name="log_var")

        self.sampling = Sampling(name="Sampler")

        # ************* DECODER ***********************
        self.decoder1 = tf.keras.layers.Dense(hidden)
        self.dln1 = tf.keras.layers.LayerNormalization()
        self.decoder2 = tf.keras.layers.Dense(hidden)
        self.dln2 = tf.keras.layers.LayerNormalization()
        self.decoder3 = tf.keras.layers.Dense(hidden)
        self.dln3 = tf.keras.layers.LayerNormalization()
        self.decoder4 = tf.keras.layers.Dense(hidden)
        self.dln4 = tf.keras.layers.LayerNormalization()
        self.decoder5 = tf.keras.layers.Dense(hidden)
        self.dln5 = tf.keras.layers.LayerNormalization()

        self.decoder_resnet = tf.keras.layers.Dense(
            self.sampled_items, activation="sigmoid", name="DecoderR"
        )
        self.decoder_latent = tf.keras.layers.Dense(
            self.sampled_items, activation="sigmoid", name="DecoderL"
        )

    def call(self, x, training=None):

        sampled_x = x

        z_mean, z_log_var, z = self.encode(sampled_x)
        if training:
            d = self.decode(z)
            # Add KL divergence regularization loss.
            kl_loss = 1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var)
            kl_loss = tf.reduce_mean(kl_loss)
            kl_loss *= -0.5
            self.add_loss(kl_loss)
            self.add_metric(kl_loss, name="kl_div")
        else:
            d = self.decode(z_mean)

        return d

    def decode(self, x):
        e0 = x
        e1 = self.dln1(tf.keras.activations.swish(self.decoder1(e0)))
        e2 = self.dln2(tf.keras.activations.swish(self.decoder2(e1) + e1))
        e3 = self.dln3(tf.keras.activations.swish(self.decoder3(e2) + e1 + e2))

        dr = self.decoder_resnet(e3)
        dl = self.decoder_latent(x)

        return dr * dl

    def encode(self, x):
        e0 = x
        e1 = self.ln1(tf.keras.activations.swish(self.encoder1(e0)))
        e2 = self.ln2(tf.keras.activations.swish(self.encoder2(e1) + e1))
        e3 = self.ln3(tf.keras.activations.swish(self.encoder3(e2) + e1 + e2))
        e4 = self.ln4(tf.keras.activations.swish(self.encoder4(e3) + e1 + e2 + e3))
        e5 = self.ln5(tf.keras.activations.swish(self.encoder5(e4) + e1 + e2 + e3 + e4))

        z_mean = self.dense_mean(e5)
        z_log_var = self.dense_log_var(e5)
        z = self.sampling((z_mean, z_log_var))

        return z_mean, z_log_var, z


# 推荐系统
class RecSystem:
    def __init__(self):
        self.model_nn = tf.keras.models.load_model(path + "model_nn.h5")
        self.model_vae = Model(5251, 512, 1024)
        self.model_vae.load_weights(path + "VAE_RD_2_3_512_1024__")

    # 推荐
    def recommend(self, user, topk=1, flag=0):
        if flag == 0:
            data = []
            for i in range(5250):
                uu = copy.copy(user)
                uu.append(i)
                data.append(uu)
            score = self.model_nn.predict(data).tolist()
            best_id = []  # 找电影id
            for i in range(topk):
                tmp_max = max(score)
                tmp_id = score.index(tmp_max)
                best_id.append(tmp_id + 1)
                score[tmp_id] = [0]
            return best_id  # 从1开始
        else:
            pred = self.model_vae.predict(user)
            rec_idx = (-pred).argsort()[:, :topk]  # top k movies
            return rec_idx


rec_system = RecSystem()
