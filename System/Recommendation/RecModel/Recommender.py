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

from Account.models import PlatformUser
from Recommendation.models import Book, SearchRecord

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


def preprocess_nn(pre):
    """Convert $pre to NN input"""

    res = [0 for i in range(20)]

    # extract category id on the hundredth
    tmp = [0 for i in range(6)]
    for i in range(len(pre)):
        tmp[pre[i] // 100] = tmp[pre[i] // 100] + 1

    # find the 2 favorite categories
    maxid1, maxval = 0, 0
    for i in range(len(tmp)):
        if maxval < tmp[i]:
            maxid1 = i
            maxval = tmp[i]
    res[0] = maxid1
    tmp[maxid1] = -1
    maxid2, maxval = 0, 0
    for i in range(len(tmp)):
        if maxval < tmp[i]:
            maxid2 = i
            maxval = tmp[i]
    res[10] = maxid2

    tmp1 = 1
    tmp2 = 11
    for i in range(len(pre)):
        if pre[i] // 100 == maxid1:
            if tmp1 < 10:
                res[tmp1] = pre[i] % 100
                tmp1 += 1
        if pre[i] // 100 == maxid2:
            if tmp2 < 20:
                res[tmp2] = pre[i] % 100
                tmp2 += 1

    return res


def preprocess_vae(like):
    user_pre = np.zeros((1, 5251))
    for i in like:
        user_pre[0][i] = 1

    return user_pre


# 推荐系统
class RecSystem:
    def __init__(self):
        self.model_nn = tf.keras.models.load_model(path + "model_nn.h5")
        self.model_vae = Model(5251, 512, 1024)
        self.model_vae.load_weights(path + "VAE_RD_2_3_512_1024__")

    def recommend_nn(self, user, topk=1):
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

    def recommend_vae(self, user, topk=1):
        pred = self.model_vae.predict(user)
        rec_idx = (-pred).argsort()[:, :topk]  # top k movies
        return rec_idx

    """
    function: recommend(self, platform_user, topk=1, flag=0)
        integrated version of recommendation. 
        input: platform_user -- PlatformUser
               topk -- number of recommendations
               flag -- 0 for NN, 1 for VAE
        output: book_tag of recommended books
    """

    def recommend(self, platform_user, topk=1):

        """Get user's preference tag_id, store in list $preference"""
        preference = []
        preference_query = platform_user.type_preference.filter(
            platformuser=platform_user
        )
        for item in preference_query:
            preference.append(item.tag_id)

        """ NN Recommendation """
        nn_input = preprocess_nn(preference)
        rec_nn = self.recommend_nn(nn_input, topk=topk)

        """Get user's search history, store in $search_his"""
        search_his = []
        search_his_ = SearchRecord.objects.filter(searcher=platform_user)
        for item in search_his_:
            search_his.append(Book.objects.get(bookname=item.search_cont).book_tag)

        """ VAE Recommendation """
        vae_input = preprocess_vae(search_his)
        rec_vae = list(self.recommend_vae(vae_input, topk=topk)[0])
        # return rec_vae
        print("Recommended by nn:", rec_nn)
        print("Recommended by vae:", rec_vae)

        """Ratio of each model"""
        nn_ratio = 0.8 * max(0, 100 - len(search_his)) / 100 + 0.2
        vae_ratio = 1 - nn_ratio
        nn_num = int(nn_ratio * topk)
        vae_num = topk - nn_num

        """Merge two recommendation"""
        nn_rec = random.sample(rec_nn, nn_num)
        vae_rec = random.sample(rec_vae, vae_num)

        rec_final = set.union(set(nn_rec), set(vae_rec))
        if len(rec_final) == topk:
            print("Recommendation result:", rec_final)
            return list(rec_final)

        """If two recommendation overlap"""
        rec_all = set.union(set(rec_nn), set(rec_vae))
        rec_remain = rec_all - rec_final
        rec_final = set.union(
            rec_final, set(random.sample(list(rec_remain), topk - len(rec_final)))
        )
        print("Recommendation result:", rec_final)
        return list(rec_final)
