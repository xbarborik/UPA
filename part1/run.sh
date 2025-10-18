#!/usr/bin/env bash
python3 urls.py > url_test.txt
head -n 10 url_test.txt | python3 scraper.py