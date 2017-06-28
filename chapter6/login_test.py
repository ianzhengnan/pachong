
from urllib.parse import urlencode
from urllib.request import Request, urlopen, build_opener, HTTPCookieProcessor

import lxml.html
from http.cookiejar import CookieJar


def main():
    LOGIN_URL = 'http://example.webscraping.com/places/default/user/login'
    LOGIN_EMAIL = 'example@webscraping.com'
    LOGIN_PASSWORD = 'example'

    cj = CookieJar()
    opener = build_opener(HTTPCookieProcessor(cj))

    html = opener.open(LOGIN_URL).read() #urlopen(LOGIN_URL).read()
    data = parse_form(html)

    data['email'] = LOGIN_EMAIL
    data['password'] = LOGIN_PASSWORD
    encoded_data = urlencode(data)
    # print(encoded_data)
    request = Request(LOGIN_URL, encoded_data.encode()) # encode('utf-8') utf-8 is default encode to bytes
    response = opener.open(request) #urlopen(request)
    print(response.geturl())


def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data

if __name__ == '__main__':
    main()