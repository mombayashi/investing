#! /bin/bash
scrapy crawl investing -o latest.csv -t csv
mv latest.csv ../softbank_latest.csv

