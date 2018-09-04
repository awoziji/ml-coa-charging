# Cloud Setup
REGION = 'asia-east1'
PROJECT = 'coa-charging'
BUCKET = PROJECT

DELIM = '<SEP>'

RAW_DATA_COLS = [
    'Invoice Date',
    'Business Unit',
    'Invoice Number',
    'Invoice Line',
    'Invoice Description',
    'Invoice Line Description',
    'Vendor Name',
    'Account Code',
    'Account Description',
    'Invoice Amount (Base Amount, Excluding GST)'
]
RENAMED_COLS = [
    'invoice_date',
    'business_unit',
    'invoice_number',
    'line_number',
    'header_description',
    'line_description',
    'vendor_name',
    'acc_code',
    'acc_descr',
    'amount'
]
STRING_COLS = [
    'header_description', 'line_description', 'vendor_name', # features
    'acc_code', # label
    'invoice_date', 'invoice_number', 'business_unit' # passthrough
] # includes passthrough and label cols if applicable
NUMERIC_COLS = ['line_number', 'amount'] # includes passthrough and label cols if applicable
TOKENIZE_COL = 'full_description'
NGRAM_RANGE = (1, 3)
MAX_TOKENS = 1500
LABEL_COL = 'acc_code'
PASSTHROUGH_COLS = ['invoice_date', 'invoice_number', 'business_unit', 'line_number']
