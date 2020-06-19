# import asyncio
import codecs
import os, sys
import datetime as dt

from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()

from scraping.parsers import *
from scraping.models import Vacancy, City, Language

parser = (
    (work, 'https://www.work.ua/jobs-kyiv-python/'),
    (dou, 'https://jobs.dou.ua/vacancies/?city=Киев&search=python'),
    (djinni, 'https://djinni.co/jobs/?primary_keyword=Python&location=Киев&title_only=True'),
    (rabota, 'https://rabota.ua/jobsearch/vacancy_list?keyWords=python&regionId=1')
)

city = City.objects.filter(slug='kiev').first()
language = Language.objects.filter(slug='python').first()
jobs, errors = [], []
for func, url in parser:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass

#h = codecs.open('work.txt', 'w', 'utf-8')
#h.write(str(jobs))
#h.close()
