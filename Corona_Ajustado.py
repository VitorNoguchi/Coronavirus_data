#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests as req
import re
from csv import DictWriter
from os import path
from datetime import datetime

class Corona:
    def __init__(self):
        self.country = ''
        self.date = ''
        self.cases = ''
        self.deaths = ''
        self.recovered = ''

    def site(self, user):
        if len(user) == 2:
            self.country = user[1].lower()
            if self.country == 'usa':
                self.country = 'us'
            elif self.country == 'brasil':
                self.country = 'brazil'
            elif self.country == 'itália':
                self.country == 'italy'
            elif self.country == 'espanha':
                self.country = 'spain'
            else:
                pass
            url = 'https://www.worldometers.info/coronavirus/country/{}'.format(self.country)
        else:
            self.country = 'world'
            url = 'https://www.worldometers.info/coronavirus/'
        return url

    def connection(self):
        try:
            r = req.get(url)
            r = r.text
            return r
        except:
            return "URL Inválida"

    def update(self, data_text):
        cases_regex = re.compile(r'<h1>Coronavirus[\S\s]+\">([\d, ]+)<\Wspan>\s<\Wdiv>')
        cases_search = cases_regex.search(data_text)
        self.cases = cases_search.group(1)
        deaths_regex = re.compile(r'<h1>Deaths:<\Wh1>\s<[\s\S]+\Smaincounter-number\S>\s<span>([\d, ]+)<\Sspan>')
        deaths_search = deaths_regex.search(data_text)
        self.deaths = deaths_search.group(1)
        recovered_regex = re.compile(r'<h1>Recovered:<\Wh1>\s<[\s\S]+\W{2}maincounter-number\W\sstyle\W{2}color:\W8ACA2B\s\W>\s<span>([\d, ]+)<\Sspan>')
        recovered_search = recovered_regex.search(data_text)
        self.recovered = recovered_search.group(1)
        self.cases = self.cases.replace(',', '')
        self.cases = self.cases.replace(' ', '')
        self.deaths = self.deaths.replace(',', '')
        self.recovered = self.recovered.replace(',', '')

    def CSV(self):
        field_names = ['Country', 'Total Cases', 'Total Deaths', 'Total Recovered', 'TimeStamp']
        self.date = datetime.now().strftime("%d/%m/%Y %H:%M")
        dictionary = {field_names[0]: self.country,
                field_names[1]: self.cases,
                field_names[2]: self.deaths,
                field_names[3]: self.recovered,
                field_names[4]: self.date}

        if path.exists('/home/semantix/PycharmProjects/Desafio4/{}.csv'.format(self.country)):
            with open('/home/semantix/PycharmProjects/Desafio4/{}.csv'.format(self.country), 'a+', newline='') as f:
                dict_writer = DictWriter(f, fieldnames=field_names)
                dict_writer.writerow(dictionary)
        else:
            with open('/home/semantix/PycharmProjects/Desafio4/{}.csv'.format(self.country), 'w') as f:
                dict_writer = DictWriter(f, fieldnames=field_names)
                dict_writer.writeheader()
                dict_writer.writerow(dictionary)

if __name__ == '__main__':
    user = sys.argv
    classe = Corona()
    url = classe.site(user)
    data_text = classe.connection()
    if data_text != "URL Inválida":
        classe.update(data_text)
        classe.CSV()

