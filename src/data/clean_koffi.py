import pandas as pd
import pyarrow

koffi = pd.read_csv('/Users/damien/Projects/drug-binding-kinetics/data/raw/KOFFI-data.csv')

keep_cols = [
    'ID', 
    'method', 
    'Fixed Partner',
    'Fixed Partner Type:',
    'Fixed Partner Main Type:',
    'Fixed Partner Species', 
    'Soluble Partner',
    'Soluble Partner Type:',
    'Soluble Partner Main Type:',
    'Soluble Partner Species', 
    'kon/kass/ka', 
    'koff/kdis/kd',
    'KD', 
    'Is raw data present?', 
    'Is the raw data of good quality?',
    'Are fits shown?', 
    'How do the fits look?']

koffi = koffi[keep_cols]

# dropping rows with no kinetics or binding data, or where one or both binding partners are not listed
drop_rows = koffi.loc[
    koffi['koff/kdis/kd'].isnull() | 
    koffi['kon/kass/ka'].isnull() | 
    koffi['KD'].isnull() | 
    koffi['Fixed Partner'].isnull()| 
    koffi['Soluble Partner'].isnull()
    ].index

koffi.drop(drop_rows, axis=0, inplace=True) 

# creating residence time column from inverse of koff
koffi['residence_time'] = 1 / koffi['koff/kdis/kd']

# creating subset of data where raw data is high quality and binding fits are shown
koffi_hq_subset = koffi.loc[(koffi['Is the raw data of good quality?']=='Y') & (koffi['Are fits shown?']=='Y')]

#drop superfluous columns
drop_cols = [
    'Is raw data present?', 
    'Is the raw data of good quality?',
    'Are fits shown?', 
    'How do the fits look?'
]

koffi.drop(drop_cols, axis=1, inplace=True)
koffi_hq_subset.drop(drop_cols, axis=1, inplace=True)

#save cleaned data as parquet in interim folder
koffi.to_parquet('/Users/damien/Projects/drug-binding-kinetics/data/interim/koffi.parquet')
koffi_hq_subset.to_parquet('/Users/damien/Projects/drug-binding-kinetics/data/interim/koffi_hq_subset.parquet')
