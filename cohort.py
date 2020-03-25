
'----------- SET UP -----------'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.options.display.max_columns = None  
pd.options.display.max_rows = None

%matplotlib qt

'----------- IMPORT DATA -----------'
path = r'C:\Users\camil\OneDrive\Bureau\02. Freelance\03. FrigoMagic\04. cohort\cohortes\cohortes'
actives_path = path + r'\actives.csv'
devices_path = path + r'\devices.csv'

actives_df_copy = pd.read_csv(actives_path)
devices_df_copy = pd.read_csv(devices_path)

actives_df = actives_df_copy.copy()
devices_df = devices_df_copy.copy()

'----------- DATA EXPLO -----------'
def get_info_df (df):
    print('SHAPE: {}'.format(df.shape))
    print('HEAD: {}'.format(df.head(2)))
    print('DTYPES: {}'.format(df.dtypes))

get_info_df(devices_df)
get_info_df(actives_df)
get_info_df(actives_df_copy)

'----------- FEATURE ENGINEERING -----------'
#CONVERT TO DATES
actives_df['actif_date'] = pd.to_datetime(actives_df.actif)
devices_df.dropna(axis=0, inplace=True)
devices_df['download_date'] = pd.to_datetime(devices_df.download)

#CREATE COHORTs in devices_df
devices_df['cohort_month'] = devices_df['download_date'].apply(lambda x: x.strftime('%Y-%m'))

#BRING COHORTS to actives_df
actives_df = pd.merge(actives_df, devices_df[['uuid', 'cohort_month']], how='left', on='uuid')

#CREATE TIMEUNITS in actives_df
actives_df['unit_month'] = actives_df['actif_date'].apply(lambda x: x.strftime('%Y-%m'))

#CALCULATE PER COHORT PER TIMEUNITS, NUMBER OF USER
def get_cohort_count_df (df, cohort_type, unit_type):
    return df.groupby([cohort_type, unit_type]).agg({'uuid': pd.Series.nunique}).unstack(0)

cohort_month_month_count_df = get_cohort_count_df (actives_df, 'cohort_month', 'unit_month')

sns.heatmap(cohort_month_month_count_df.T, cmap="Blues", annot=True, fmt=".0f", cbar=False)

#CHECK COHORT FIGURES
cohort_test = '2017-04'
unit_test = '2017-10'
cohort_month_month_count_df[cohort_month_month_count_df.index == unit_test]['uuid'][cohort_test]

devices_df[devices_df.cohort_month == cohort_test].uuid.head() 
uuid_test = devices_df[devices_df.cohort_month == cohort_test].uuid.values
len(set(actives_df[(actives_df.uuid.isin(uuid_test)) & (actives_df.unit_month == unit_test)].uuid))

#CALCULATE PER COHORT PER TIMEUNITS, RETENTION
cohort_month_month_retention_df = cohort_month_month_count_df.div(cohort_month_month_count_df.max(axis=1), axis=0).xs('uuid', axis=1, drop_level=True) 

sns.heatmap(cohort_month_month_retention_df.T , cmap="Blues", annot=True, fmt='.0%', cbar=False)
