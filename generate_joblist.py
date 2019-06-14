us_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
      'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA',
      'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
canadian_states = ['Ontario', 'Quebec', 'British', 'Columbia', 'Alberta', 'Manitoba', 'Saskatchewan', 'Nova Scotia', 'New Brunswick', 'Newfoundland and Labrador']

singapore_states = ['singapore']
def generate_jobs(states, base_url):
    jobs=[]
    for state in states:
          for i in range(1,101):
                us_jobs.append('{base_url}/jobs?q=&l={state}&sort=date&fromage=last&start={i}'.format(base_url=base_url,state=state, i=i*10))

    return jobs

def us_jobs():
    return generate_jobs(us_states, 'https://www.indeed.com')

def canada_jobs():
    return generate_jobs(canadian_states, 'https://www.indeed.ca')


def singapore_jobs():
    return generate_jobs(singapore_states, 'https://www.indeed.sg')