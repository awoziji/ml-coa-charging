# Cloud Setup
REGION = 'asia-east1'
PROJECT = 'coa-charging'
BUCKET = PROJECT

DELIM = '<SEP>'

RAW_DATA_COLS = [
    'Fiscal Year (Accounting Date)',
    'Business Unit',
    'Account Code',
    'Account Description',
    'Voucher ID',
    'Voucher Description',
    'Voucher Origin',
    'Vendor ID',
    'Vendor First Name',
    'Voucher Line',
    'Voucher Line Description',
    'Voucher Line Long Description',
    'Payment Voucher Line Amount S$ (Excluding GST, Including Freight S$)'
]
RENAMED_COLS = [
    'fiscal_year',
    'business_unit',
    'acc_code',
    'acc_descr',
    'voucher_id',
    'voucher_descr',
    'voucher_origin',
    'vendor_id',
    'vendor_name',
    'voucher_line',
    'voucher_line_descr',
    'voucher_line_long_descr',
    'payment_voucher_amt'
]
STRING_COLS = [
    'voucher_descr', 'voucher_line_descr', # features
    'acc_code', # label
    'fiscal_year', 'business_unit', 'vendor_id', 'voucher_id', 'voucher_line' # passthrough
] # includes passthrough and label cols if applicable
NUMERIC_COLS = [] # includes passthrough and label cols if applicable
LABEL_COL = 'acc_code'
PASSTHROUGH_COLS = ['fiscal_year', 'business_unit', 'vendor_id', 'voucher_id', 'voucher_line']