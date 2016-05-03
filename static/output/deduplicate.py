import pandas as pd
all_lines = [line.rstrip('\n') for line in open("filename")]
current_name = all_lines[0]
myfile1a = current_name + '.csv'
myfile1 = './' + current_name + '.csv'
myfile2 = './post_codes.csv'

toclean = pd.read_csv(myfile1)
deduped = toclean.drop_duplicates('original_link')

df2 = pd.read_csv(myfile2)
df3 = deduped.merge(df2, on='job_location', how='left')
df3.to_csv('./transfer/V3_' +myfile1a, float_format='%.0f')

