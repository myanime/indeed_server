uk_districts = ['Bedfordshire', 'Berkshire', 'Buckinghamshire', 'Cambridgeshire', 'Cheshire', 'Cornwall', 'Cumberland',
     'Derbyshire', 'Devon', 'Dorset', 'County Durham', 'Essex', 'Gloucestershire', 'Hampshire', 'Herefordshire',
     'Hertfordshire', 'Huntingdonshire', 'Kent', 'Lancashire', 'Leicestershire', 'Lincolnshire', 'London', 'Middlesex',
     'Norfolk', 'Northamptonshire', 'Northumberland', 'Nottinghamshire', 'Oxfordshire', 'Rutland', 'Shropshire',
     'Somerset', 'Staffordshire', 'Suffolk', 'Surrey', 'Sussex', 'Warwickshire', 'Westmorland', 'Wiltshire',
     'Worcestershire', 'Yorkshire', 'Aberdeenshire', 'Angus', 'Argyllshire', 'Ayrshire', 'Banffshire', 'Berwickshire',
     'Bute', 'Caithness', 'Clackmannanshire', 'Dunbartonshire', 'Dumfriesshire', 'East Lothian', 'Fife', 'Inverness',
     'Kincardineshire', 'Kirkcudbrightshire', 'Lanarkshire', 'Midlothian', 'Moray', 'Nairnshire', 'Orkney',
     'Peeblesshire', 'Perthshire', 'Renfrewshire', 'Roxburghshire', 'Selkirkshire', 'Stirlingshire', 'Sutherland',
     'West Lothian', 'Wales', 'Northern Island']
us_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
      'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA',
      'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
us_states += ['Denver',
              'Las Vegas',
              'Atlanta',
              'Oakland',
              'Houston',
              'Boston',
              'Nashville',
              'New York',
              'East Hartford',
              'Fort Worth',
              'Omaha',
              'Tulsa',
              'Cleveland',
              'Concord',
              'Henderson',
              'Sandy Springs',
              'Indianapolis',
              'Detroit',
              'Chicago',
              'Sacramento',
              'Round Rock',
              'Columbus',
              'Virginia Beach',
              'Dallas',
              'San Diego',
              'Baltimore',
              'Honolulu',
              'Hoover',
              'Aurora',
              'Fresno',
              'Mesa',
              'Miami',
              'Austin',
              'Raleigh',
              'Memphis',
              'Davidson–Murfreesboro–Franklin',
              'San Antonio',
              'Minneapolis',
              'Louisville',
              'New Braunfels',
              'Albuquerque',
              'Long Beach',
              'Wichita',
              'Kissimmee',
              'St. Petersburg',
              'New Orleans',
              'Los Angeles',
              'Tacoma',
              'Colorado Springs',
              'Cambridge',
              'San Jose',
              'Seattle',
              'Washington',
              'Arlington',
              'Columbia',
              'Norfolk',
              'Metairie',
              'Kansas City',
              'Sunnyvale',
              'Tampa',
              'Jacksonville',
              'Bakersfield',
              'Waukesha',
              'Cheektowaga',
              'Vancouver',
              'Milwaukee',
              'Phoenix',
              'El Paso',
              'Oklahoma City',
              'Naperville',
              'The Woodlands',
              'Fort Lauderdale',
              'Anaheim',
              'Kentwood',
              'San Francisco',
              'Elyria',
              'Tucson',
              'Camden',
              'Carmel',
              'Warwick',
              'Portland',
              'Charlotte',
              'San Bernardino',
              'Philadelphia']

canadian_states = ['Ontario', 'Quebec', 'British', 'Columbia', 'Alberta', 'Manitoba', 'Saskatchewan', 'Nova Scotia', 'New Brunswick', 'Newfoundland and Labrador']

singapore_states = ['singapore']
def generate_jobs(states, base_url):
    jobs=[]
    for state in states:
          for i in range(1,101):
                jobs.append('{base_url}/jobs?q=&l={state}&sort=date&fromage=last&start={i}'.format(base_url=base_url,state=state, i=i*10))
    return jobs

def us_jobs():
    return generate_jobs(us_states, 'https://www.indeed.com')

def canada_jobs():
    return generate_jobs(canadian_states, 'https://www.indeed.ca')

def singapore_jobs():
    return generate_jobs(singapore_states, 'https://www.indeed.com.sg')

def uk_jobs():
    return generate_jobs(uk_districts, 'https://www.indeed.co.uk')

def debug_jobs():
    # return ['https://au.indeed.com/jobs?q=Theatre+Technicians+Expression+of+Interest+-+Victoria+%28including+Albury%29&l=VIC']
    # return ['https://au.indeed.com/jobs?q=Specialist+Strategy+%26+Planning+bhp&l=VIC']
    return ['https://au.indeed.com/jobs?q=victoria&l=VIC&vjk=2bc206cf12917926']