# Charging of Invoices to Account Codes

## Purpose

The purpose of this project is to automatically charge invoices to account codes, reducing human effort in the payment processing process. It also reduces inconsistencies in the account charging process by eliminating the differences in judgment of different finance officers.

Besides reducing human effort and error, we also hope that using a machine to automatically charge invoices to acocunt codes would increase data quality, to support downstream analysis of what we are spending on. Currently, because different finance officers charge the same types of spending to different account codes, it is difficult to determine how much we are spending on each type of function.

## How this is Done

We train a machine learning model which tries to mimic a finance officer to decide what account to charge to, based on the following information:

- Invoice header and line description
- Vendor Name
- Invoice Amount

These information may not be sufficient to accurately determine the account to charge to for all invoices, but should cover most cases.

The model is then exposed as an API for our systems to call. The API takes in the information required by the model, and outputs the following:

- Predicted Account Code
- Predicted Account Description
- Prediction Confidence

## Model Details

The model is a neural network trained in Tensorflow. 

### Invoice Descriptions

The invoice descriptions are represented as sequences of word embeddings; word embeddings capture the meanings of the words. Each word is represented as a numeric vector, such that semantic meanings of words are preserved. For instance, a well-trained word embedding understands such logic as "king is to queen as man is to woman".

Instead of training the embedding layer from scratch, we will use a pre-trained word embedding like GloVe or word2vec to initialise the weights of the embedding layer, and then continue to train it using our own text.

![Word Embeddings](img/word-embedding.png?raw=true)

[_Source: Andrew Ng's course on Sequence Models on Coursera_](https://www.coursera.org/learn/nlp-sequence-models)

The sequences of embeddings are then passed through several convolutional layers, which act as detectors for specific combinations of (meanings of) words. Each convolutional filter looks for a specific meaning of a word/word combination; for instance, one filter with a height of 1 could be looking for the word that has a similar meaning to "singtel", and another filter with a height of 2 could be looking for 2 words, with similar meaning to "singtel invoice". 

By stacking many of these convolutions together, we are essentially looking for various words and word combinations throughout the invoice descriptions.

![Text Convolution](img/cnn-on-text.png?raw=true)

[_Source: Convolutional Neural Networks for Sentence Classification, by Yoon Kim_](https://arxiv.org/pdf/1408.5882.pdf)

### Vendor Names

The vendor names are processed in the same way as the invoice descriptions, and also go through convolutional layers to detect keywords and key phrases in the vendor names.

### Invoice Amounts

The invoice amounts just go through a batch normalisation layer.

### Model Structure

These "preprocessed" features are then concatenated together and fed to a softmax layer to generate the prediction.

![Model Structure](img/model-structure.png?raw=true)

## Additional Details

Material design files are put in the `static` folder because this application is meant to be deployed in an intranet environment, assuming no intranet content delivery network (CDN) to serve these files. These files are only used in a simple web frontend meant for demo purposes. The frontend is strictly speaking not required to deploy the model into production; only the `predict` API is required.