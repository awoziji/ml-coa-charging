import pandas as pd
import numpy as np
import tensorflow as tf
import os
from tqdm import tqdm_notebook as tqdm
from datetime import datetime
import pickle

BASE_DIR = ''
GLOVE_DIR = os.path.join(BASE_DIR, 'data', 'misc')

def gen_embeddings_index():
    embeddings_index = {}
    num_lines = sum(1 for line in open(os.path.join(GLOVE_DIR, 'glove.6B.100d.txt'), 'rb'))
    with open(os.path.join(GLOVE_DIR, 'glove.6B.100d.txt'), 'rb') as f:
        for line in tqdm(f, total=num_lines):
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs

    print('Found {} word vectors.'.format(len(embeddings_index)))
    
    return embeddings_index

def gen_acc_mappings(acc_mapping_df):
    acc_indices = acc_mapping_df['index'].values
    acc_codes = acc_mapping_df['acc_code'].values
    acc_descrs = acc_mapping_df['acc_descr'].values
    acc_index_to_code = dict(list((index, acc_code) for index, acc_code in zip(acc_indices, acc_codes)))
    acc_index_to_descr = dict(list((index, acc_descr) for index, acc_descr in zip(acc_indices, acc_descrs)))

    return acc_indices, acc_index_to_code, acc_index_to_descr

def gen_tokenizer(texts, max_num_words, filters=None):
    if filters is None:
        tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=max_num_words)
    else:
        tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=max_num_words, filters=filters)
    tokenizer.fit_on_texts(texts)
    
    # save tokenizer
    with open('data/misc/tokenizer.pickle', 'wb') as f:
        pickle.dump(tokenizer, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    # save metadata for visualising embeddings in Tensorboard
    words = list(tokenizer.word_index.keys())
    with open('data/misc/embedding.tsv', 'w') as f:
        f.write('Word\tFrequency\n')
        for word in words:
            word_count = tokenizer.word_counts[word]
            f.write('{}\t{}\n'.format(word, word_count))
            
    return tokenizer
def convert_text_to_seq(tokenizer, texts, max_sequence_length):
    seq = tokenizer.texts_to_sequences(texts)
    seq = tf.keras.preprocessing.sequence.pad_sequences(seq, maxlen=max_sequence_length)
    return seq
def get_labels(df, acc_mappings_df):
    return tf.keras.utils.to_categorical(df.merge(acc_mappings_df, how='left')['index'])

def gen_embedding_weights(num_words, embedding_dim, word_index, embeddings_index):
    embedding_matrix = np.zeros((num_words, embedding_dim))
    for word, i in word_index.items():
        if i >= num_words:
            break
        embedding_vector = embeddings_index.get(bytes(word, 'utf-8'))
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector
        else:
            # words not found in embedding index will be initialised as random vector
            embedding_matrix[i] = np.random.randn(embedding_dim)
    
    return embedding_matrix

def get_acc_code(acc_index_to_code, pred):
    return acc_index_to_code[np.argmax(pred)]

def get_acc_descr(acc_index_to_descr, pred):
    return acc_index_to_descr[np.argmax(pred)]

def get_pred_confidence(pred):
    return np.max(pred)