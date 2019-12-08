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

        item['original_link_clean'] = company_url

        yield item

    def parse_company_url(self, response):
        item = response.meta['item']
        try:
            ci = BeautifulSoup(response.xpath('//*[@class="cmp-ReviewAndRatingsStory-rating"]').extract_first(), 'lxml')
            print("####################", ci.get_text())

            try:
                # item['ceo'] =
                # item['ceo_reviews'] =
                # item['ceo_image_link'] =
                soup = BeautifulSoup(response.xpath('//*[@class="cmp-CeoWidgetWithRating-percent"]').extract_first(),
                                     'lxml')
                item['ceo_rating'] = soup.find('div').get_text(strip=True)
            except:
                pass

            hq_candidates = response.xpath('//*[@class="cmp-AboutMetadata-itemInner"]').getall()
            for hq_candidate in hq_candidates:
                if 'Headquarters' in hq_candidate:
                    hq = hq_candidate.split('cmp-AboutMetadata-itemCotent">')[1].split('</div>')[0]
                    item['headquarters'] = hq

            links = response.xpath('//*[@class="cmp-CompanyLink"]').getall()
            for link in links:
                link = BeautifulSoup(link, 'lxml').find('a').attrs['href']
                if 'https://www.facebook' in link:
                    continue
                if 'https://www.instagram' in link:
                    item['instagram_url'] = link
                if 'https://twitter' in link:
                    continue
                if 'https://www.linkedin' in link:
                    item['linkedin_url'] = link
                if 'https://www.youtube' in link:
                    continue
                else:
                    item['company_website'] = link
        except:
            pass
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
            job_type_soup = BeautifulSoup(
                response.xpath('//*[@class="jobsearch-JobMetadataHeader-iconLabel"]').getall()[1], 'lxml')
            if job_type_soup:
                job_type = job_type_soup.find('span').get_text(strip=True)
                item['job_type'] = job_type
        except:
            item['job_type'] = ''
        try:
            image = BeautifulSoup(response.xpath('//*[@class="jobsearch-CompanyAvatar-image"]').extract_first(), 'lxml')
            image_src = image.find('img')['src']
        except Exception:
            image_src = ''
        try:
            # print(response.url)
            company_description = BeautifulSoup(
                response.xpath('//*[@class="jobsearch-CompanyAvatar-description"]').extract_first(), 'lxml').get_text()
        except:
            company_description = ''
        try:
            company_link = \
            BeautifulSoup(response.xpath('//*[@class="jobsearch-CompanyAvatar-companyLink"]').extract_first(),
                          'lxml').find('a')['href']
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

    def generate_hash(self, title_href):
        try:
            return int(hashlib.sha1(title_href.encode('utf-8')).hexdigest(), 16) % (10 ** 8)
        except:
            return randint(1, 10000000)

    def parse_rating_page(self, response):
        item = response.meta['item']
        try:
            soup = BeautifulSoup(response.xpath('//*[@id="cmp-reviews-header-container"]').extract_first(), 'lxml')
            item['worklife'] = self.RCFindAttrSpan(soup, 'a', {'data-tn-element': "review-filter-wlbalance"})
            item['salary'] = self.RCFindAttrSpan(soup, 'a', {'data-tn-element': "review-filter-paybenefits"})
            item['job_security'] = self.RCFindAttrSpan(soup, 'a', {'data-tn-element': "review-filter-jobsecadv"})
            item['management'] = self.RCFindAttrSpan(soup, 'a', {'data-tn-element': "review-filter-mgmt"})
            item['culture'] = self.RCFindAttrSpan(soup, 'a', {'data-tn-element': "review-filter-culture"})
        except:
            pass
        yield item

    @classmethod
    def RCFind(cls, soup, element, class_=None, href=False):
        elements = soup.find(element, class_=class_)
        if elements:
            if href:
                return elements.attrs['href']
            return elements.get_text(strip=True)

    @classmethod
    def RCFindAttrSpan(cls, soup, element, attr):
        try:
            return soup.find(element, attr).find('span').get_text(strip=True)
        except:
            return ''

    def parse(self, response):

        old_jobs = set(line.rstrip("\n") for line in open('duplicate_list.txt'))
        import os
        if not DEBUG:
            os.remove('duplicate_list.txt')

        job_add_scrapy = response.xpath('//*[@data-tn-component="organicJob"]')
        for add in job_add_scrapy:
            item = IndeedItem()
            soup = BeautifulSoup(add.extract(), 'lxml')

            title_href = self.RCFind(soup, 'a', class_='jobtitle', href=True)
            job_number = self.generate_hash(title_href)
            if not DEBUG and str(job_number) in old_jobs:
                continue
            else:
                old_jobs.add(job_number)

            item['jobNumber'] = job_number

            base_url = urlsplit(response.url)
            full_link = '{}://{}{}'.format(base_url.scheme, base_url.netloc, title_href)

            job_company = self.RCFind(soup, 'span', class_='company')
            job_title = self.RCFind(soup, 'a', class_='jobtitle')
            job_description = self.RCFind(soup, 'div', class_='summary')
            job_date = self.RCFind(soup, 'span', class_='date')
            job_location = self.RCFind(soup, 'span', class_='location')
            money = self.RCFind(soup, 'span', class_='salary')
            rating = self.RCFind(soup, 'span', class_='ratingsContent')
            job_money, range_lower, range_upper, salary_description, job_money_unchanged = self.get_money(money)

            item['country_id'] = COUNTRY
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
            item['review_total'] = rating

            request = scrapy.Request(full_link, callback=self.parse_indeed_url)
            request.meta['item'] = item

            try:
                company_href = soup.find('a', {'data-tn-element': "companyName"}).attrs['href']
            except AttributeError:
                company_href = None

            request2 = None
            if company_href:
                company_link = '{}://{}{}'.format(base_url.scheme, base_url.netloc, company_href)
                request2 = scrapy.Request(company_link, callback=self.parse_company_url)
                request2.meta['item'] = item

            rating_html = self.RCFind(soup, 'a', class_='ratingNumber', href=True)

            request3 = None
            if rating_html:
                rating_html = '{}://{}{}'.format(base_url.scheme, base_url.netloc, rating_html)
                request3 = scrapy.Request(rating_html, callback=self.parse_rating_page)
                request3.meta['item'] = item

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
            requests = [request]
            if request2:
                requests.append(request2)
            if request3:
                requests.append(request3)
            for request in requests:
                yield request

        with open('duplicate_list.txt', 'a') as file:
            for i in list(old_jobs):
                file.write(str(i))
                file.write('\n')
