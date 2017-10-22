import time
import pandas as pd
all_lines = [line.rstrip('\n') for line in open("filename")]
current_name = all_lines[0]
myfile1a = current_name + '.csv'
myfile1 = './' + current_name + '.csv'
myfile2 = './post_codes.csv'
todays_date = time.strftime("%d_%m_%Y")
toclean = pd.read_csv(myfile1, names = ['jobNumber','job_title','job_location','job_description','original_link','original_link_clean','job_company','job_money_unchanged','job_money','salary_description','range_lower','range_upper','original_link_emails','original_link_telephones','image_src_link','image_src_link_path','image_src_link_file','image_link','job_date','indeed_date','original_plain_text','original_html','company_description_indeed','company_revenue_indeed','company_employees_indeed','company_industry_indeed','company_links_indeed'])

deduped = toclean.drop_duplicates('original_link')
df2 = pd.read_csv(myfile2)
df3 = deduped.merge(df2, on='job_location', how='left')
# df3 = df3.sort('job_date')
df3 = df3[df3['job_date'] == todays_date]
df3.to_csv('./transfer/V3_' +todays_date + ".csv", float_format='%.0f', index = False)
