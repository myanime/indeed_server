import time
from country.country_config import COUNTRY
import pandas as pd
todays_date = time.strftime("%d_%m_%Y")

OUTPUT_NAME = None
if COUNTRY == 'au':
    OUTPUT_NAME = './transfer/V1au_' + todays_date + ".csv"
if COUNTRY == 'usa':
    OUTPUT_NAME = './transfer/V1usa_' + todays_date + ".csv"
if COUNTRY == 'canada':
    OUTPUT_NAME = './transfer/V1ca_' + todays_date + ".csv"
if COUNTRY == 'sg':
    OUTPUT_NAME = './transfer/V1sg_' + todays_date + ".csv"
if COUNTRY == 'uk':
    OUTPUT_NAME = './transfer/V1uk_' + todays_date + ".csv"


months_output = 'may.csv'
post_codes_csv = 'post_codes.csv'

df_month_output = pd.read_csv(months_output, names = ['jobNumber','job_title','job_location','job_description','original_link','original_link_clean','job_company','job_money_unchanged','job_money','salary_description','range_lower','range_upper','original_link_emails','original_link_telephones','image_src_link','image_src_link_path','image_src_link_file','logo_image_link','job_date','indeed_date','original_plain_text','original_html','company_description_indeed','company_revenue_indeed','company_employees_indeed','company_industry_indeed','company_links_indeed'])

df_month_output_deduped = df_month_output.drop_duplicates('original_link')
df_month_output_deduped = df_month_output_deduped.sort_values('job_date')
df_month_output_deduped.to_csv(months_output, float_format='%.0f', index=False)

df_post_codes = pd.read_csv(post_codes_csv)
df_month_output_deduped = df_month_output_deduped.merge(df_post_codes, on='job_location', how='left')

today_deduped = df_month_output_deduped[df_month_output_deduped['job_date'] == todays_date]


today_deduped.to_csv(OUTPUT_NAME, float_format='%.0f', index=False)