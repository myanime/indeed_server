# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IndeedItem(scrapy.Item):
    jobNumber = scrapy.Field()
    job_title = scrapy.Field()
    job_location = scrapy.Field()
    job_description = scrapy.Field()
    original_link = scrapy.Field()
    original_link_clean = scrapy.Field()
    job_company = scrapy.Field()
    job_money_unchanged = scrapy.Field()
    job_money = scrapy.Field()
    salary_description = scrapy.Field()
    range_lower = scrapy.Field()
    range_upper = scrapy.Field()
    original_link_emails = scrapy.Field()
    original_link_telephones = scrapy.Field()
    logo_image_link = scrapy.Field()
    job_date = scrapy.Field()
    indeed_date = scrapy.Field()
    original_html = scrapy.Field()
    company_description_indeed = scrapy.Field()
    company_revenue_indeed = scrapy.Field()
    company_employees_indeed = scrapy.Field()
    company_industry_indeed = scrapy.Field()
    company_links_indeed = scrapy.Field()
    review_total = scrapy.Field()
    worklife = scrapy.Field()
    salary = scrapy.Field()
    job_security = scrapy.Field()
    management = scrapy.Field()
    culture = scrapy.Field()
    ceo = scrapy.Field()
    ceo_rating = scrapy.Field()
    ceo_reviews = scrapy.Field()
    ceo_image_link = scrapy.Field()
    headquarters = scrapy.Field()
    linkedin_url = scrapy.Field()
    instagram_url = scrapy.Field()
    company_website = scrapy.Field()
    banner_image = scrapy.Field()
    country_id = scrapy.Field()
    job_type = scrapy.Field()
