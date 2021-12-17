#!/usr/bin/env python3

import pandas as pd
import csv

%load_ext google.colab.data_table

url_sql='https://raw.githubusercontent.com/tymoshenkoanna/data_merging/main/sql_extract.csv'
url_val='https://raw.githubusercontent.com/tymoshenkoanna/data_merging/main/validation_report.csv'
url_tl='https://raw.githubusercontent.com/tymoshenkoanna/data_merging/main/1_tech_list.csv'

sql_file=pd.read_csv(url_sql)
sql_file = sql_file.applymap(lambda s: s.lower() if type(s) == str else s)
val_file=pd.read_csv(url_val)
val_file = val_file.applymap(lambda s: s.lower() if type(s) == str else s)
tl_file=pd.read_csv(url_tl)
tl_file = tl_file.applymap(lambda s: s.lower() if type(s) == str else s)


#PART 1
#clean-up data from the SQL file, the only data that's required from this source is: server name + installed product name and it's version

sql_file.loc[(sql_file['Product Name'] != 'mirror agent') | 
            (sql_file['Product Name'] != 'mirror scanner') |
             (sql_file['Product Name'] != 'reader nft connect'), 'new column versions'] = sql_file['Product Version'].astype(str).str[:3]
sql_file.loc[(sql_file['Product Name'] == 'mirror agent') | 
            (sql_file['Product Name'] == 'mirror scanner'), 'new column versions'] = sql_file['Product Version'].astype(str).str[:4]
sql_file.loc[(sql_file['Product Name'] == 'gbc'), 'new column versions'] = sql_file['Product Version'].astype(str).str[:5]
sql_file.loc[(sql_file['Product Version'] == 'NOTKNOWN'), 'new column versions'] = 'nan'
sql_file.loc[(sql_file['Product Name'] == 'reader box'), 'Product Name'] = 'reader'
sql_file.loc[(sql_file['Product Name'] == 'reader tracker'), 'Product Name'] = 'tracker'

sql_file['Product Name'] = sql_file['Product Name'] + ' ' + sql_file['new column versions']

sql_df=sql_file[["Product Name", "Server Name"]]
#print(sql_df)

#PART 2
#clean-up data from the technology list, the only data that's required form the source is: product name + product version + Product ID; merge the output with sql_df

tl_df=tl_file[["Product Name", "Product ID"]]
print(tl_df)


#merge two dataframes, tl_df and sql_df, left merging to make sure all entries are in the outcome, including ones that miss the match
sql_tl_df = pd.merge(left=sql_df, right=tl_df, how='left', left_on='Product Name', right_on='Product Name')
print(sql_tl_df)
