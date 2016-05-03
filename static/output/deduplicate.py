import pandas as pd
myfile1 = './out_cron.csv'
myfile2 = './post_codes.csv'

toclean = pd.read_csv(myfile1)
deduped = toclean.drop_duplicates('original_link')

df2 = pd.read_csv(myfile2)
df3 = deduped.merge(df2, on='job_location', how='left')
df3.to_csv('./transfer/V3.csv', float_format='%.0f')

