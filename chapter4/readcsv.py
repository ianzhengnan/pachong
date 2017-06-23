
import io
# import sys
# sys.path.insert(0, '/home/vagrant/python/pachong')
from chapter3.downloader import Downloader

import csv
from zipfile import ZipFile
from io import StringIO, BytesIO

# read from a zip file, there is still some issues with python3 version
def alexa1():
    downloader = Downloader()
    zipped_data = downloader('http://localhost/top-1m.csv.zip')
    urls = []
    with ZipFile(BytesIO(zipped_data)) as zf:
        csv_filename = zf.namelist()[0]
        for website in zf.read(csv_filename).decode('utf-8'):
            urls.append('http://' + website[0] if website else '')

    return urls

# read from local csv file
def alexa():
    urls = []
    with open('/home/vagrant/Downloads/top-1m.csv', 'r') as csvfile:
        for _, website in csv.reader(csvfile):
            urls.append('http://' + website)

    # with ZipFile('/home/vagrant/Downloads/top-1m.csv.zip') as myzip:
    #     with myzip.open('top-1m.csv', 'rU') as csvfile:
    #         # print(csvfile.read())
    #         for website in csvfile.readlines():
    #             # urls.append('http://' + website)
    #             print(str(website, 'utf-8'))
    return urls

if __name__ == '__main__':
    # print(alexa())
    # alexa()
    print(alexa1())