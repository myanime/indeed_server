from selenium import webdriver

driver = webdriver.Chrome('/home/myanime/repos/indeed_server/chromedriver')

driver.get('http://au.indeed.com/jobs?q=&l=SA&sort=date&fromage=last&start=20')
job_add = driver.find_elements_by_xpath('//h2')[2]
print job_add.text
job_add = job_add.find_element_by_xpath('//span')
print job_add.find_element_by_xpath('a').get_attribute('href')