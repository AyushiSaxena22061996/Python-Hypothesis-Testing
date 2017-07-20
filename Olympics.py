Search for any database in excel online other than used here or you can use the same and perform the following functions:
Clean the data set:
1.	Removing extra columns not necessary for calc and renaming columns
2.	Get the town with max population / country with max golds
3.	Calculate the max absolute deviation from average for say: town’s population with city population average 
4.	Run a t test to infer whether the deviation of a particular town is statistically significant to conclude that it is the most habituated town 

The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on All Time Olympic Games Medals, and does some basic data cleaning.
The columns are organized as # of Summer games, Summer medals, # of Winter games, Winter medals, total # number of games, total # of medals. Use this dataset to answer the questions below
-----------------
import pandas as pd
import numpy as np

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)
for col in df.columns:                      #renaming columns based on conditions
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(')              # split the index by '('
df.index = names_ids.str[0]                              # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3]                     # the [1] element is the abbreviation or ID (take first 3 characters from that)
df = df.drop('Totals')       #to drop unnecessary columns
df.head()     # to get top 5 rows

Country with max gold medals:

def answer_one():
    
    return df['Gold'].argmax()

answer_one()


Max absolute deviation from avg over the years:

census_df = pd.read_csv('census.csv')
census_df.head()

def answer_seven():
    cdf=census_df[census_df['SUMLEV']==50]
    cdf=cdf.set_index(['CTYNAME'])
    cdff=['POPESTIMATE2010','POPESTIMATE2011', 'POPESTIMATE2012', 'POPESTIMATE2013','POPESTIMATE2014',
           'POPESTIMATE2015']
    return cdf.apply(lambda x: (np.max(x[cdff])-np.min(x[cdff])), axis=1).argmax()
     
answer_seven()


T test:


def run_ttest():
    
    nut=convert_housing_data_to_quarters()
    st=get_recession_start()
    bot=get_recession_bottom()
    ut=get_list_of_university_towns()
    df=pd.DataFrame()

    df['price_ratio']=(nut['2008q2'])/nut[bot]     #Hard coded here, find a way to get nut[st] - 1 column
    
#     df['price_ratio']=nut.iloc[:, nut.columns[st]-1]/nut[bot]

    df=df.reset_index()
    
#     df1=pd.merge(ut,df, left_on=['State','RegionName'], right_index=True, how='inner')
  
    UT= df[df['RegionName'].isin(ut['RegionName'])].dropna()
    not_UT = df[~df['RegionName'].isin(ut['RegionName'])].dropna()
    

    t=ttest_ind(UT['price_ratio'], not_UT['price_ratio'])
   
    if t[1]<0.01:
        different=True
        
    if UT['price_ratio'].mean() < not_UT['price_ratio'].mean():
        better='university town'
    else:
        better='non-university town'

        
    
    return (different, t[1], better)

run_ttest()
