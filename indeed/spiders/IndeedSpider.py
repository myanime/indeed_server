import hashlib
import re
import time
from random import randint
from urllib.parse import urlsplit

import scrapy
from bs4 import BeautifulSoup

from indeed.items import IndeedItem

from static.output.country.country_config import COUNTRY
from generate_joblist import us_jobs, canada_jobs, singapore_jobs, uk_jobs, debug_jobs

DEBUG = False

class MainScraper(scrapy.Spider):
    name = "indeed_scraper"
    if DEBUG:
        start_urls = debug_jobs()
    else:
        if COUNTRY == 'au':
            start_urls = [line.rstrip("\n") for line in open('./static/indeedurls')]
        if COUNTRY == 'usa':
            start_urls = us_jobs()
        if COUNTRY == 'canada':
            start_urls = canada_jobs()
        if COUNTRY == 'sg':
            start_urls = singapore_jobs()
        if COUNTRY == 'uk':
            start_urls = uk_jobs()

    def get_email_and_telephone(self, text):
        emails = []
        return_email = None
        telephone_numbers = []
        try:
            re_email = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
            re1 = r'(0[1-8]{1,1} [0-9]{3,5} [0-9]{3,5})'
            re2 = r'(\([0-9]{2,2}\).[0-9]{3,5}.[0-9]{3,5})'
            re3 = r'\+61.[0-9]{1,1}.[0-9]{2,5}.[0-9]{2,5}.[0-9]{2,5}'

            e1 = re.search(re_email, text, re.I)
            if e1:
                emails.append(e1.group())
            t1 = re.search(re1, text, re.I)
            t2 = re.search(re2, text, re.I)
            t3 = re.search(re3, text, re.I)
            if t1:
                telephone_numbers.append(t1.group())
            if t2:
                telephone_numbers.append(t2.group())
            if t3:
                telephone_numbers.append(t3.group())
            try:
                email = emails[0]
                regex = r'(((?i)\.com\.au)|((?i)\.gov\.au)|((?i)\.org\.au)|((?i)\.edu\.au)|((?i)\.net\.au)|((?i)\.com)|((?i)\.gov)|((?i)\.org)((?i)\.au))'
                try:
                    input_email = re.split(regex, email)
                    new_emailstr = input_email[0] + input_email[1]
                except:
                    new_emailstr = email
                new_email = str(new_emailstr)

                newregex = r'(^\d{4}(?i)e\.)|(^\d{4}(?i)e)|(^\d{3}(?i)e)|(^\d{3,4})|(^(at))|(^(to))|(^(email))|(^(emailing))'
                new_test = re.findall(newregex, new_email)

                if new_test:
                    try:
                        for i in new_test[0]:
                            if i:
                                result = i
                                break
                        if new_email.startswith(result):
                            return_email = new_email[len(result):]
                    except:
                        return_email = new_email
                else:
                    return_email = new_email

            except:
                pass
        except:
            pass
        telephone_item = telephone_numbers[0] if telephone_numbers else None
        return return_email, telephone_item

    def parse_original_url(self, response):
        item = response.meta['item']

        company_url = response.url
        html = response.xpath('body').extract_first()
        company_text = BeautifulSoup(html).select('body')[0].get_text()

        email, phone = self.get_email_and_telephone(company_text)
        item['original_link_telephones'] = phone
        item['original_link_emails'] = email

        item['original_plain_text'] = ''  # Adding the company text takes up too much space
        item['original_link_clean'] = company_url

        yield item

    def parse_indeed_url(self, response):

        item = response.meta['item']
        unclean_url = response.url
        item['original_link'] = unclean_url
        try:
            indeed_text = BeautifulSoup(response.xpath('//*[@id="jobDescriptionText"]').extract_first(), 'lxml')
            indeed_text = indeed_text.find('div', class_='jobsearch-jobDescriptionText').get_text()
        except Exception as e:
            indeed_text = ''
        try:
            image = BeautifulSoup(response.xpath('//*[@class="jobsearch-CompanyAvatar-image"]').extract_first(), 'lxml')
            image_src = image.find('img')['src']
        except Exception:
            image_src = ''
        try:
            # print(response.url)
            company_description = BeautifulSoup(response.xpath('//*[@class="jobsearch-CompanyAvatar-description"]').extract_first(), 'lxml').get_text()
        except:
            company_description = ''
        try:
            company_link = BeautifulSoup(response.xpath('//*[@class="jobsearch-CompanyAvatar-companyLink"]').extract_first(), 'lxml').find('a')['href']
            company_link = company_link.split('?')[0]
        except:
            company_link = ''
        item['original_html'] = indeed_text
        item['logo_image_link'] = image_src
        item['company_description_indeed'] = company_description
        item['company_links_indeed'] = company_link
        # print("*************************************************")
        # print("*************************************************")
        # print("*************************************************")
        # print(indeed_text)
        # print("*************************************************")
        # print("*************************************************")
        # print("*************************************************")
        try:
            company_link_from_button = \
                BeautifulSoup(response.xpath('//*[@id="viewJobButtonLinkContainer"]').extract_first()).find(href=True)[
                    'href']
            request = scrapy.Request(company_link_from_button, callback=self.parse_original_url)
            request.meta['item'] = item
            yield request
        except:
            item['original_link_telephones'] = ''
            item['original_link_emails'] = ''

            item['original_plain_text'] = ''
            item['original_link_clean'] = ''

            yield item

    def get_money(self, money):
        job_money = None
        range_lower = None
        range_upper = None
        salary_description = None
        job_money_unchanged = None
        if money:
            try:
                job_money = money
                job_money_unchanged = job_money
                job_money = job_money.replace(',', '')
                job_money = job_money.replace('$', '')
                if COUNTRY == 'uk':
                    job_money = job_money.replace('£', '')
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
        return job_money, range_lower, range_upper, salary_description, job_money_unchanged

    def parse_image_src(self, response):
        item = response.meta['item']
        try:
            image_src_link = response.css('div#cmp-header-logo img').xpath("@src").extract()
        except:
            image_src_link = None

        image_src_link_file = None
        image_src_link_path = None
        if image_src_link != None:
            try:
                image_src_link_s = str(image_src_link)
                image_src_link_split = image_src_link_s.rsplit('/', 1)
                image_src_link_path = image_src_link_split[0].replace("[u'", "")
                image_src_link_path = image_src_link_path.replace("[]", "")
                image_src_link_file = image_src_link_split[1].replace("']", "")
            except:
                pass

        item['image_src_link'] = image_src_link
        item['image_src_link_file'] = image_src_link_file
        item['image_src_link_path'] = image_src_link_path

        company_description_indeed = None
        company_revenue_indeed = ""
        company_employees_indeed = ""
        company_industry_indeed = None
        company_links_indeed = None

        try:
            company_description_indeed = response.css('span#cmp-short-description::text')[0].extract()
        except:
            company_description_indeed = None

        skip_employees = False
        x = 0
        link_order = 0
        while x < 4:
            company_revenue_indeed_title = ''
            try:
                company_revenue_indeed_title = response.css('dl.cmp-dl-list-big.cmp-sidebar-section dt::text')[
                    link_order].extract()
            except:
                company_revenue_indeed = None
                break
            re_title_text = r'Revenue'
            if re.search(re_title_text, company_revenue_indeed_title):
                company_revenue_indeed = response.css('dl.cmp-dl-list-big.cmp-sidebar-section dd::text')[
                    link_order].extract()
                re_money = r'\$'
                if COUNTRY == 'uk':
                    re_money = r'\£'
                if re.search(re_money, company_revenue_indeed):
                    pass
                else:
                    company_revenue_indeed = None
                    skip_employees = True
                break
            link_order = link_order + 1
            company_revenue_indeed = None

        x = 0
        link_order = 0
        if skip_employees == False:
            while x < 4:
                company_employees_indeed_title = ''
                try:
                    company_employees_indeed_title = response.css('dl.cmp-dl-list-big.cmp-sidebar-section dt::text')[
                        link_order].extract()
                except:
                    company_employees_indeed = None
                    break
                re_title_text = r'Employees'
                if re.search(re_title_text, company_employees_indeed_title):
                    company_employees_indeed = response.css('dl.cmp-dl-list-big.cmp-sidebar-section dd::text')[
                        link_order].extract()
                    re_numb = r'[ABCDEFGHIJKLMNPQRSUVWXYZabcdefghijklmnpqrsuvwxzy]'
                    if re.search(re_numb, company_employees_indeed):
                        company_employees_indeed = None
                    break
                link_order = link_order + 1
                company_employees_indeed = None

        company_industry_indeed = response.css(
            'dl.cmp-dl-list-big.cmp-sidebar-section dd ul.cmp-plain-list li a::text').extract_first()
        try:
            company_links_indeed = response.css('dl.cmp-dl-list-big.cmp-sidebar-section dd a').xpath('@href')[
                2].extract()
        except:
            try:
                company_links_indeed = response.css('dl.cmp-dl-list-big.cmp-sidebar-section dd a').xpath('@href')[
                    1].extract()
            except:
                pass
        try:
            company_employees_indeed = company_employees_indeed.replace("+", '')
            company_employees_indeed = company_employees_indeed.replace(",", '')
        except:
            pass

        item['company_description_indeed'] = company_description_indeed
        item['company_revenue_indeed'] = company_revenue_indeed
        item['company_employees_indeed'] = company_employees_indeed
        item['company_industry_indeed'] = company_industry_indeed
        item['company_links_indeed'] = company_links_indeed

        return item

    def generate_hash(self, title_href):
        try:
            return int(hashlib.sha1(title_href.encode('utf-8')).hexdigest(), 16) % (10 ** 8)
        except:
            return randint(1, 10000000)

    def parse(self, response):
        def RCFind(soup, element, class_=None, href=False):
            elements = soup.find(element, class_=class_)
            if elements:
                if href:
                    return elements.attrs['href']
                return elements.get_text(strip=True)

        old_jobs = set(line.rstrip("\n") for line in open('duplicate_list.txt'))
        import os
        os.remove('duplicate_list.txt')

        job_add_scrapy = response.xpath('//*[@data-tn-component="organicJob"]')
        for add in job_add_scrapy:
            item = IndeedItem()
            soup = BeautifulSoup(add.extract(), 'lxml')

            title_href = RCFind(soup, 'a', class_='jobtitle', href=True)
            job_number = self.generate_hash(title_href)
            if str(job_number) in old_jobs:
                continue
            else:
                old_jobs.add(job_number)

            item['jobNumber'] = job_number

            base_url = urlsplit(response.url)
            full_link = '{}://{}{}'.format(base_url.scheme, base_url.netloc, title_href)

            job_company = RCFind(soup, 'span', class_='company')
            job_title = RCFind(soup, 'a', class_='jobtitle')
            job_description = RCFind(soup, 'div', class_='summary')
            job_date = RCFind(soup, 'span', class_='date')
            job_location = RCFind(soup, 'span', class_='location')
            money = RCFind(soup, 'span', class_='salary')
            job_money, range_lower, range_upper, salary_description, job_money_unchanged = self.get_money(money)

            item['job_title'] = job_title
            item['job_description'] = job_description
            item['job_location'] = job_location
            item['job_company'] = job_company
            days_date = time.strftime("%d_%m_%Y")
            item['job_date'] = days_date
            item['indeed_date'] = job_date
            item['job_money'] = job_money
            item['range_upper'] = range_upper
            item['job_money_unchanged'] = job_money_unchanged
            item['range_lower'] = range_lower
            item['salary_description'] = salary_description
            item['logo_image_link'] = None
            request = scrapy.Request(full_link, callback=self.parse_indeed_url)
            request.meta['item'] = item

            print("#########################################")
            print("#################JobAdd##################")
            print('job_title: ', job_title)
            print('job_description: ', job_description)
            print('job_location: ', job_location)
            print('job_date: ', job_date)
            print('job_money: ', job_money)
            print('range_upper: ', range_upper)
            print('job_money_unchanged: ', job_money_unchanged)
            print('range_lower: ', range_lower)
            print('salary_description: ', salary_description)
            print('full_link: ', full_link)
            print("#########################################")
            yield request

        with open('duplicate_list.txt', 'a') as file:
            for i in list(old_jobs):
                file.write(str(i))
                file.write('\n')
