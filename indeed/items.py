# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IndeedItem(scrapy.Item):
    #full_link = scrapy.Field()
    job_description = scrapy.Field()
    job_location = scrapy.Field()
    job_company = scrapy.Field()
    job_money = scrapy.Field()
    job_date = scrapy.Field()
    image_link = scrapy.Field()
    image_src_link = scrapy.Field()
    job_title = scrapy.Field()
    original_link = scrapy.Field()
    salary_description = scrapy.Field()
    range_lower = scrapy.Field()
    range_upper = scrapy.Field()
    
    original_link_telephones = scrapy.Field()
    original_link_emails = scrapy.Field()
    original_link2_telephones = scrapy.Field()
    original_link2_emails = scrapy.Field()
    original_link3_telephones = scrapy.Field()
    original_link4_emails = scrapy.Field()
    job_money_unchanged = scrapy.Field()
    indeed_date = scrapy.Field()


    jobNumber = scrapy.Field()
    original_plain_text = scrapy.Field()
    original_html = scrapy.Field()
    #main_url = scrapy.Field()

    #test = scrapy.Field()
