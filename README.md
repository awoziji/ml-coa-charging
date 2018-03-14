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

It uses a convolutional structure to process the invoice description (header and line descriptions are concatenated together), where the filters act as feature extractors for 1 to 4 ngrams. The descriptions go through an embedding layer, converting each description into a sequence of word embeddings. The convolutional filters would hence be detecting the meanings of 1 to 4 word combinations. The convolutional layers are then concatenated and flattened.

The vendor names go through the same embedding layer and convolutional structure as the invoice descriptions and are processed the same way.

The invoice amounts just go through a batch normalisation layer.

These "preprocessed" or feature extracted features are then concatenated together and fed to a softmax layer to generate the prediction.