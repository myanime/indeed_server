import scrapy
import time
from indeed.items import IndeedItem
from bs4 import BeautifulSoup
import re
import traceback
import hashlib
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
loaded_counter = int([line.rstrip('\n') for line in open('./static/counter')][0])

main_counter = loaded_counter + 1000
loaded_date = [line.rstrip('\n') for line in open('./static/date')][0]

class MainScraper(scrapy.Spider):
    name = "selenium_scraper"
    start_urls = ['http://www.google.com']
    # download_delay = 1

    def parse_original_url(self, response):

        item = response.meta['item']
        unclean_url = response.url
        clean_url = unclean_url.replace('&utm_campaign=indeed', '')
        clean_url = clean_url.replace('&in_site=Indeed', '')
        clean_url = clean_url.replace('?utm_source=Indeed&utm_medium=organic&utm_campaign=Indeed', '')
        clean_url = clean_url.replace('&utm_source=Indeed&utm_medium=organic&utm_campaign=Indeed', '')
        clean_url = clean_url.replace('?utm_source=Indeed&utm_medium=free&utm_campaign=Indeed', '')
        clean_url = clean_url.replace('&utm_source=Indeed', '')
        clean_url = clean_url.replace('&utm_medium=indeedorganic', '')
        clean_url = clean_url.replace('&jobboard=INDEED', '')
        clean_url = clean_url.replace('&from=indeed', '')
        clean_url = clean_url.replace('&src=indeed', '')
        clean_url = clean_url.replace('&utm_source=Indeed&utm_campaign=MSD_Indeed', '')
        clean_url = clean_url.replace('&in_site=Indeed', '')
        clean_url = clean_url.replace('indeed/', '')
        clean_url = clean_url.replace('&__jvsd=Indeed', '')
        clean_url = clean_url.replace('&jobsource=indeedOrganic', '')
        clean_url = clean_url.replace('&iisn=Indeed.com', '')
        clean_url = clean_url.replace('&Codes=D_Indeed', '')
        clean_url = clean_url.replace('&source=Indeed', '')
        clean_url = clean_url.replace('&jobPipeline=Indeed', '')
        clean_url = clean_url.replace('&utm_campaign=Singtel_Indeed', '')
        clean_url = clean_url.replace('?ref=indeed.com', '?')
        clean_url = clean_url.replace('?utm_source=indeed', '?')
        clean_url = clean_url.replace('?source=ONL_INDEED', '?')
        clean_url = clean_url.replace('?jobPipeline=Indeed', '?')
        clean_url = clean_url.replace('?source=IND', '?')
        item['original_link_clean'] = clean_url
        item['original_link'] = unclean_url
        urlhash = hashlib.md5(unclean_url)
        item['jobNumber'] = urlhash.hexdigest()

        try:
            original_html = response.xpath('//html').extract()
        except:
            original_html = None
        try:
            soup = BeautifulSoup(response.xpath('//body').extract_first())
            for script in soup.find_all('script'):
                script.extract()
            for tag in soup():
                for attribute in ["class", "id", "name", "style"]:
                    del tag[attribute]

            paragraphs = soup.find_all('p')
            try:
                header_text = soup.find('h1').get_text(
                    strip=True) + "\n"  # + soup.find('h2').get_text(strip=True) + "\n"
            except:
                header_text = ''
            all_text = ''
            for paragraph in paragraphs:
                my_text = paragraph.get_text(strip=True)
                all_text = my_text + "\n" + all_text
            original_plain_text = header_text + all_text
            original_plain_text = original_plain_text.replace('\r\n                    ', '\n')
        except:
            original_plain_text = traceback.print_exc()
            print traceback.print_exc()

        # Uncomment to stop html getting
        # original_plain_text = None
        original_html = None

        original_link_telephones = None
        original_link_emails = None
        item['original_link_telephones'] = None
        item['original_link_emails'] = None

        emails = []
        telephone_numbers = []
        try:
            re_email = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
            re1 = r'(0[1-8]{1,1} [0-9]{3,5} [0-9]{3,5})'
            re2 = r'(\([0-9]{2,2}\).[0-9]{3,5}.[0-9]{3,5})'
            re3 = r'\+61.[0-9]{1,1}.[0-9]{2,5}.[0-9]{2,5}.[0-9]{2,5}'

            e1 = re.search(re_email, original_plain_text, re.I)
            if e1:
                emails.append(e1.group())
            t1 = re.search(re1, original_plain_text, re.I)
            t2 = re.search(re2, original_plain_text, re.I)
            t3 = re.search(re3, original_plain_text, re.I)
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
                item['original_link_emails'] = return_email

                # item['original_link_emails2'] = emails[1]
                # item['original_link_emails3'] = emails[2]
            except:
                pass
            try:
                item['original_link_telephones'] = telephone_numbers[0]
                # item['original_link_telephones2'] = telephone_numbers[1]
                # item['original_link_telephones3'] = telephone_numbers[2]
            except:
                pass
        except:
            pass
        global loaded_date
        item['original_plain_text'] = original_plain_text
        item['original_html'] = loaded_date

        image_link = item['image_link']
        try:
            image_link = "http://au.indeed.com" + image_link
        except:
            image_link = None
            yield item
        if image_link != None:
            request = scrapy.Request(image_link, callback=self.parse_image_src)
            request.meta['item'] = item
            yield request

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

    def parse(self, response):
        driver = webdriver.Chrome('./chromedriver')
        start_urls = [line.rstrip("\n") for line in open('./static/indeedurls')]
        for url in start_urls:
            try:
                driver.get(url)
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
                        return job_money, range_lower, range_upper, salary_description, job_money_unchanged

                    add = add.find_element_by_xpath('..')

                    job_title = add.find_element_by_xpath('h2').text
                    job_description = add.find_element_by_css_selector('span.summary').text.replace('\n', '')
                    job_location = add.find_element_by_css_selector('span.location').text
                    job_date = add.find_element_by_css_selector('span.date').text
                    try:
                        job_company = add.find_element_by_css_selector('span.company').text
                    except NoSuchElementException:
                        pass
                    money = add.find_elements_by_css_selector('span.no-wrap')
                    job_money, range_lower, range_upper, salary_description, job_money_unchanged = get_money(money)

                    image_link = None
                    full_link = add.find_element_by_xpath('h2/a').get_attribute('href')

                    item = IndeedItem()
                    global main_counter
                    main_counter = main_counter + 1
                    with open('./static/counter', 'w') as f:
                        f.write(str(main_counter))
                    item['jobNumber'] = None
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
                    item['image_link'] = image_link
                    request = scrapy.Request(full_link, callback=self.parse_original_url)
                    request.meta['item'] = item
                    yield request
            except NoSuchElementException:
                print "#########################################"
                print "#########################################"
                print "##############SELENIUM ERROR#############"
                print "#########################################"
                print "#########################################"
                problem = traceback.format_exc()
                with open('./static/errors.txt', 'a') as f:
                    f.write(problem)
                    f.write("################################")
                time.sleep(2)
