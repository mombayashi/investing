# -*- coding: utf-8 -*-
from app.models import DataPoint
import csv
import datetime

SOURCE_CSV = 'softbank_10years.csv'
db_last = DataPoint.objects.all().order_by('-date').first()
last_date = db_last.date.strftime('%Y-%m-%d') if db_last and db_last.date else '1970-01-01'
last_date = datetime.datetime.strptime(last_date, '%Y-%m-%d')

header_read = False
with open(SOURCE_CSV, encoding='utf8') as f:
    reader = csv.reader(f)
    for l in reader:
        if not header_read:
            header_read = True
            continue
        #print(l)
        cur_date = l[0].replace('年','-').replace('月','-').replace('日','')
        cur_date = datetime.datetime.strptime(cur_date, '%Y-%m-%d')
        
        #print('{}/{}'.format(cur_date, last_date))
        if cur_date <= last_date:
            break
        
        end, begin, high, low, volume, ratio = l[1:]
        if volume == '-':
            continue

        dp = DataPoint(
            date=cur_date, 
            end=float(end.replace(',','')),
            begin=float(begin.replace(',','')),
            high=float(high.replace(',','')),
            low=float(low.replace(',','')),
            volume=float(volume.replace(',','').replace('M', '')),
            ratio=float(ratio.replace(',','').replace('%', ''))
        )
        dp.save()
