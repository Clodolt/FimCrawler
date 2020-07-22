"""Das ist der Webcrawler. Je nach Website muss hier angegeben werden, wo die gewünschten Informationen zu finden sind (XPath)."""

import smtplib
import ssl
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import scrapy
import mysql.connector
import configparser
from datetime import datetime

from ..items import Quelle
import mysqlCmd
import sendMail


class CombinedSpider(scrapy.Spider):
    name = "combined"

    def start_requests(self):
        sources = mysqlCmd.get_sources()

        for row in sources:
            yield self.make_requests_from_url(row[1])

    # Parse wird überschrieben um bestimmte Elemente der Website auszugeben, Parameter bei fast jede Website anders
    def parse(self, response):
        try:
            if mysqlCmd.is_crawlable(response.request.url):
                if response.request.url.startswith('https://dl.acm.org/'):      # Link hier einfügen (Datenbank auch updaten)
                    link = response.request.url
                    volume = response.css('.toc-badge__label').re(r'Volume \d+')    # mit .css oder .xpath auf Ort zuweisen
                    issue = response.css('.toc-badge__label').re(r'Issue \d+')
                    date = response.css('.toc-badge__value::text').re(r'\w+ \d{4}')

                elif response.request.url.startswith('https://link.springer.com/'):
                    link = response.request.url
                    volume = response.xpath('//*[@id="main-content"]/div/div/div[1]/ul/li[1]/h2/span[1]/text()').re(
                        r'Volume \d+')
                    issue = response.xpath('//*[@id="main-content"]/div/div/div[1]/ul/li[1]/ul/li[1]/a/text()').re(
                        r'issue \d+')
                    date = response.xpath('//*[@id="main-content"]/div/div/div[1]/ul/li[1]/ul/li[1]/a/text()').re(
                        r'\w+ \d{4}')

                elif response.request.url.startswith('https://aisel.aisnet.org/misqe/'):
                    link = response.request.url
                    volume = response.xpath('/html/body/div/div/div/div[3]/div[1]/div[1]/ul[2]/div[1]/h1').re(r'Volume \d+')
                    issue = response.xpath('/html/body/div/div/div/div[3]/div[1]/div[1]/ul[2]/div[1]/h1').re(r'Issue \d+') or 'n'
                    date = response.xpath('/html/body/div/div/div/div[3]/div[1]/div[1]/ul[2]/div[1]/h1').re(r'\d{4}')

                elif response.request.url.startswith('https://onlinelibrary.wiley.com/loi/'):
                    link = response.request.url
                    volume = response.xpath(
                        '//*[@id="e34763ef-ba0c-4ac7-95f4-b1bb491dd263"]/div/div[2]/ul/li[1]/div[2]/h4/a/text()').re(
                        r'Volume \d+')
                    issue = response.xpath(
                        '//*[@id="e34763ef-ba0c-4ac7-95f4-b1bb491dd263"]/div/div[2]/ul/li[1]/div[2]/h4/a/text()').re(
                        r'Issue \d+')
                    date = response.xpath(
                        '//*[@id="e34763ef-ba0c-4ac7-95f4-b1bb491dd263"]/div/div[2]/ul/li[1]/div[2]/div[2]/label/span/text()').re(
                        r'\w+ \d{4}')

                elif response.request.url.startswith('https://aisel.aisnet.org/'):
                    link = response.request.url
                    volume = response.xpath('/html/body/div/div/div/div[3]/div[1]/div[1]/div[3]/div[1]').re(r'Volume \d+')
                    issue = response.xpath('/html/body/div/div/div/div[3]/div[1]/div[1]/div[3]/div[1]').re(r'Issue \d+') or 'n'
                    date = response.css('.vol').re(r'\d{4}') or response.css('.issue').re(r'\d{4}')

                elif response.request.url.startswith('https://www.computerwoche.de/pdf-archiv/'):
                    link = response.request.url
                    volume = response.xpath('//*[@id="year2020"]/ul/li[1]/div/div[2]/h3/a/text()').re(r'\d{2}-\d{2}')
                    issue = response.xpath('//*[@id="main-content"]/div/div/div[1]/ul/li[1]/ul/li[1]/a').re(
                        r'issue \d+') or 'n'
                    date = response.xpath('//*[@id="year2020"]/ul/li[1]/div/div[2]/h3/a/text()').re(r'\d{4}')

                elif response.request.url.startswith('https://www.cio.de/pdf-archiv/'):
                    link = response.request.url
                    volume = response.xpath('/html/body/div[1]/div/div[3]/div[6]/div/div[2]/div/div/div[1]/ul/li[1]/div/div[2]/h2').re(r'\d{2}-\d{2}')
                    issue = response.xpath('//*[@id="main-content"]/div/div/div[1]/ul/li[1]/ul/li[1]/a').re(
                        r'issue \d+') or 'n'
                    date = response.xpath('/html/body/div[1]/div/div[3]/div[6]/div/div[1]/div/ul').re(r'\d{4}')

                elif response.request.url.startswith('https://pubsonline.informs.org/'):
                    link = response.request.url
                    volume = response.xpath('/html/body/div[1]/div/main/div[3]/div/div/div[2]/div[1]/div/div/div/div/h2').re(r'Volume \d+')
                    issue = response.xpath('/html/body/div[1]/div/main/div[3]/div/div/div[2]/div[1]/div/div/div/div/h2').re(r'Issue \d+') or 'n'
                    date = response.xpath('/html/body/div[1]/div/main/div[3]/div/div/div[2]/div[1]/div/div/div/div/div[1]').re(r'\w+ \d{4}')


                elif response.request.url.startswith('http://gibybyte.com/'):
                    link = response.request.url
                    volume = response.xpath('/html/body/h3').re(r'Volume \d+')
                    issue = response.xpath('/html/body/h3').re(r'Issue \d+')
                    date = response.xpath('/html/body/h3[2]').re(r'\w+ \d{4}')


                quelle = Quelle()
                if response.request.url.startswith('https://aisel.aisnet.org/misqe/'):
                    quelle['link'] = link
                    quelle['volume'] = ''.join(filter(lambda i: i.isdigit(), volume[0]))
                    quelle['issue'] = ''.join(filter(lambda i: i.isdigit(), volume[0])) + " " + ''.join(filter(lambda i: i.isdigit(), issue[0]))
                    quelle['date'] = date[0]  # datetime.today().strftime('%Y-%m-%d') for current date
                    quelle['checkDate'] = datetime.today().strftime('%Y-%m-%d')
                elif response.request.url.startswith('https://aisel.aisnet.org/'):
                    quelle['link'] = link
                    quelle['volume'] = ''.join(filter(lambda i: i.isdigit(), volume[0]))
                    quelle['issue'] = ''.join(filter(lambda i: i.isdigit(), volume[0])) + " " + ''.join(filter(lambda i: i.isdigit(), issue[-1]))
                    quelle['date'] = date[0]  # datetime.today().strftime('%Y-%m-%d') for current date
                    quelle['checkDate'] = datetime.today().strftime('%Y-%m-%d')
                else:
                    quelle['link'] = link
                    quelle['volume'] = ''.join(filter(lambda i: i.isdigit(), volume[0]))
                    quelle['issue'] = ''.join(filter(lambda i: i.isdigit(), volume[0])) + " " + ''.join(filter(lambda i: i.isdigit(), issue[0]))
                    quelle['date'] = date[0]  # datetime.today().strftime('%Y-%m-%d') for current date
                    quelle['checkDate'] = datetime.today().strftime('%Y-%m-%d')
                yield quelle
        except: #da diese Funktion einmal pro Quelle aufgerufen wird, läuft der Webcrawler auch bei einer Exception komplett durch
            sendMail.send_errormail_crawler(response.request.url)