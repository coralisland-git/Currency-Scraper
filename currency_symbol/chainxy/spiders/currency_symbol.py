# from __future__ import unicode_literals
import scrapy

import json

import os

import scrapy

from scrapy.spiders import Spider

from scrapy.http import FormRequest

from scrapy.http import Request

from chainxy.items import ChainItem

from scrapy import signals

from scrapy.xlib.pydispatch import dispatcher

from selenium import webdriver

from lxml import etree

from lxml import html

import time

import pdb


class Currency_symbol(scrapy.Spider):

	name = 'currency_symbol'

	domain = 'https://www.xe.com/symbols.php'

	history = []

	output = []

	def __init__(self):

		pass

	
	def start_requests(self):

		url = 'https://www.xe.com/symbols.php'

		yield scrapy.Request(url=self.domain, callback=self.parse) 


	def parse(self, response):

		currency_list = response.xpath('//table[@class="currencySymblTable"]//tr')[1:]

		for currency in currency_list:

			item = ChainItem()

			data = currency.xpath('./td')

			item['country'] = data[0].xpath('./a[2]/text()').extract_first()

			item['title'] = data[0].xpath('./a[1]/@title').extract_first()

			item['usd_rate'] = data[1].xpath('./text()').extract_first()

			item['eur_rate'] = data[2].xpath('./text()').extract_first()

			yield item


	def validate(self, item):

		try:

			return item.replace('\n', '').replace('\t','').replace('\r', '').strip()

		except:

			pass


	def eliminate_space(self, items):

	    tmp = []

	    for item in items:

	        if self.validate(item) != '':

	            tmp.append(self.validate(item))

	    return tmp