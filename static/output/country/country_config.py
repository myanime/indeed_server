import os
# COUNTRY = 'au'
# COUNTRY = 'sg'
# COUNTRY = 'canada'
# COUNTRY = 'usa'
path = str(os.getcwd())
country = path.split('indeed_server_')[1]
country = country.split('/')[0]
COUNTRY = country