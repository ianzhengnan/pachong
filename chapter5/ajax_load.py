
import json
import string
import csv
from chapter3.downloader import Downloader

temp_str = 'http://example.webscraping.com/places/ajax/search.json?&search_term={}&page_size=10&page={}'

FIELDS = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_code', 'currency_name', 'phone', 'postal_code_format', 'postal_code_regex', 'languages', 'neighbours')

countries = set()
download = Downloader()

def download_by_page():
    for letter in string.ascii_lowercase:
        page = 0
        while True:
            html = download(temp_str.format(letter, page))
            try:
                ajax = json.loads(html)
            except ValueError as e:
                print(e)
                ajax = None
            else:
                for record in ajax['records']:
                    countries.add(record['country'])
            page += 1

            if ajax is None or page >= ajax['num_pages']:
                break

def download_all():
    temp_url = 'http://example.webscraping.com/places/ajax/search.json?&search_term=.&page_size=1000&page=0'
    writer = csv.writer(open('countries.csv', 'w'))
    writer.writerow(FIELDS)
    html = download(temp_url)
    try:
        ajax = json.loads(html)
    except ValueError as e:
        print(e)
        ajax = None
    else:
        for record in ajax['records']:
            row = record['country']
            # row = [record[field] for field in FIELDS]
            writer.writerow(row)

if __name__ == '__main__':
    # open('countries.txt', 'w').write('\n'.join(sorted(countries)))
    download_all()


