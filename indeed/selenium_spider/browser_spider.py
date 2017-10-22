# -*- coding: utf-8 -*-
from selenium import webdriver
from lxml import etree
import re

driver = webdriver.Chrome('./chromedriver')
driver.get('http://au.indeed.com/jobs?q=&l=australia&sort=date&fromage=last&start=30')

job_add = driver.find_elements_by_xpath('//h2')

for add in job_add:
    def get_money(money):
        job_money = None
        range_lower = None
        range_upper = None
        salary_description = None
        job_money_unchanged = None
        if money:
            try:
                job_money = money[0].text
                job_money_unchanged = job_money
                job_money = job_money.replace(',', '')
                job_money = job_money.replace('$', '')
                if re.search(r' a year', job_money):
                    job_money = job_money.split(' a year')[0]
                    salary_description = 'a year'
                if re.search(r' an hour', job_money):
                    job_money = job_money.split(' an hour')[0]
                    salary_description = 'an hour'
                if re.search(r' a week', job_money):
                    job_money = job_money.split(' a week')[0]
                    salary_description = 'a week'
                if re.search(r' a day', job_money):
                    job_money = job_money.split(' a day')[0]
                    salary_description = 'a day'
                if re.search(r'-', job_money):
                    range_lower = job_money.split(" - ")[0]
                    range_upper = job_money.split(" - ")[1]
            except:
                job_money = None
        return job_money,  range_lower, range_upper, salary_description, job_money_unchanged

    add = add.find_element_by_xpath('..')

    job_title = add.find_element_by_xpath('h2').text
    job_description = add.find_element_by_css_selector('span.summary').text.replace('\n', '')
    job_location = add.find_element_by_css_selector('span.location').text
    job_date = add.find_element_by_css_selector('span.location').text
    job_company = add.find_element_by_css_selector('span.company').text
    money = add.find_elements_by_css_selector('span.no-wrap')
    job_money, range_lower, range_upper, salary_description, job_money_unchanged = get_money(money)

    image_link = None
    full_link = add.find_element_by_xpath('h2/a').get_attribute('href')

    print full_link
    print job_title
    print job_description
    print job_location
    print job_company
    print job_date
    print job_money
    print "-------------"
