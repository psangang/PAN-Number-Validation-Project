import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import read_excel
import re

df = pd.read_excel('Pan Number Validation Dataset.xlsx')
x,y = df.shape
#print(df.head(10))

total_records_before_cleanup = len(df)

print('Rows:', x)
print('Columns:', y)
print('Total Records before Transformations:', len(df))
print('Null Values before Transformations:', df.isnull().sum())
print('NA Values before Transformations:', df.isna().sum())  #Both isnull and NA does same thing, hence count is same
print('Empty Strings before Transformations:', df[df['Pan_Numbers'] == ''].sum())
print('Duplicates Count:', df.duplicated(subset=['Pan_Numbers'], keep=False).sum())
print('Duplicates:', df[df.duplicated(subset=['Pan_Numbers'], keep=False)])
print('Unique Records Count:',df.nunique().sum())

nulls_before_cleanup = df.isnull().sum()


# Converting df objects to string
print('df Before conversion',type(df), 'Column Datatype:',df['Pan_Numbers'].dtype)
df['Pan_Numbers'] = df['Pan_Numbers'].astype('string')
print('df after conversion',type(df), 'Column Datatype:',df['Pan_Numbers'].dtype)

#So, even after column conversion df is still an object type but column datatype changes

df['Pan_Numbers'] = df['Pan_Numbers'].str.strip()
#print('After removing Trailing Spaces',df.head(10))

df['Pan_Numbers'] = df['Pan_Numbers'].str.upper()
#print('After converting them to Uppercase',df.head(5))

# Count before dropping
rows_before = len(df)

# Drop rows with nulls in 'Pan_Numbers'
df.dropna(subset=['Pan_Numbers'], inplace=True)

# Count after dropping
rows_after = len(df)

# Number of rows dropped
rows_dropped = rows_before - rows_after

print('Total Records after Transformations(Removing Null Values 965):', len(df))
print('Rows dropped i.e. Total Nulls Removed:', rows_dropped)
print('Duplicates Count After Transformation', df.duplicated(subset=['Pan_Numbers'], keep=False).sum())
print('Duplicates After Transformation', df[df.duplicated(subset=['Pan_Numbers'], keep=False)])

Duplicates_Count_After_Null_Removals = df.duplicated(subset=['Pan_Numbers'], keep=False).sum()

# Count before dropping
rows_before_2nd_time = len(df)

# Drop rows with nulls in 'Pan_Numbers'
df.drop_duplicates(subset=['Pan_Numbers'], keep="first", inplace=True)

# Count after dropping
rows_after_2nd_time = len(df)

# Number of rows dropped
rows_dropped_2nd_time = rows_before_2nd_time - rows_after_2nd_time
print('Rows dropped i.e. Total Duplicates Removed:', rows_dropped_2nd_time)
print('Duplicates after removing Nulls and removing duplicates:', df[df.duplicated(subset=['Pan_Numbers'], keep=False)])
print('Duplicates count After 2nd Transformation', df[df.duplicated(subset=['Pan_Numbers'], keep=False)].sum())
print('Total Rows after cleaning i.e. removing Nulls(965), removing duplicates(9):', len(df))
print('Unique records after cleaning:', df.nunique().sum())
print('Any Nulls even after cleaning:', df.isnull().sum() , df.isna().sum())


total_records_after_cleanup = len(df)


def has_adjacent_repitions(pan):
    return any(pan[i] == pan[i+1] for i in range(len(pan)-1))

def is_sequence(pan):
    return all(ord(pan[i+1]) - ord(pan[i]) == 1 for i in range(len(pan)-1))

def is_valid_pan(pan):
    if len(pan) != 10:
        return False

    if not re.match('^[A-Z]{5}[0-9]{4}[A-Z]$',pan):
        return False

    if has_adjacent_repitions(pan):
        return False

    if is_sequence(pan):
        return False

    return True

df['Status'] = df['Pan_Numbers'].apply(lambda x: 'Valid' if is_valid_pan(x) else 'Invalid')
print(df.head(10))

valid_cnt = (df["Status"] == 'Valid' ).sum()
invalid_cnt = (df['Status'] == 'Invalid' ).sum()
missing_cnt = (df['Status'] == 'Missing' ).sum()

print('Valid Records:', valid_cnt)
print('Invalid Records:', invalid_cnt)
print('Total Records before cleanup :', total_records_before_cleanup,'Total Records after cleanup :', total_records_after_cleanup)


pan_value = df.iloc[5019]['Pan_Numbers']
status_value = df.iloc[5019]['Status']
print("Type:", type(pan_value), type(status_value))
print("pan_Value:", pan_value, 'Status:', status_value)

if isinstance(pan_value, str):
    if pan_value.strip() == "":
        print("The value is an empty string or whitespace.")
    else:
        print("The value is:", value)
else:
    print("The value is:", value)


df_summary = pd.DataFrame(
    {
        "Total Records before cleanup" : total_records_before_cleanup,
        "Total Nulls cleand up" : nulls_before_cleanup,
        "Duplicates_Count_After_Null_Removals" : [Duplicates_Count_After_Null_Removals],
        "Total Duplicates cleand up after Null Removal" : [rows_dropped_2nd_time],
        "Total Records after cleanup" : total_records_after_cleanup,
        "Total Valid cnt after cleanup" : valid_cnt,
        "Total Invalid cnt after cleanup" : invalid_cnt

    }
)

print(df_summary.head())


with pd.ExcelWriter('Pan_Validation_Results_Param.xlsx') as writer: # Here writer can be any variable, e.g. x/y/z
    df.to_excel(writer, sheet_name='Pan_Validations', index=False)
    df_summary.to_excel(writer, sheet_name='Pan_Validations_Summary', index=False)











