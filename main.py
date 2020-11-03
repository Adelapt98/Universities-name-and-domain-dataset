import requests
from lxml.html import fromstring
import pandas as pd


def getUnisInPage(parser):
    unis = parser.xpath("(//tr[contains(@class, 'odd')] | //tr[contains(@class, 'even')])/td")
    i = 0
    while i < len(unis):
        name = unis[i+1].xpath('.//a')[0].text

        link = unis[i+1].xpath('.//a/@href')[0]
        link = link.replace('www.', '')
        link = link.replace('https://', '')
        link = link.replace('http://', '')
        link = link.replace('/', '')

        country = unis[i+3].xpath('.//center/img/@src')[0].split('logos/')[1].split('.png')[0]

        dic = {'name': name, 'domain': link, 'country': country}

        df.loc[0] = dic
        df.to_csv('universities.csv', mode='a',header=False, index=False)

        i += 8


url = 'http://www.webometrics.info/en/world'
response = requests.get(url)
parser = fromstring(response.text)

lastPage = parser.xpath(".//li[contains(@class, 'pager-last')]/a/@href")[0].split('page=')[1]
lastPage = int(lastPage)

df = pd.DataFrame(columns=['name', 'domain', 'country'])
df.to_csv('universities.csv', encoding='utf-8', index=False)

getUnisInPage(parser)


for i in range(1,lastPage,1):
    nextUrl = url + '?page=' + str(i)
    response = requests.get(nextUrl)
    parser = fromstring(response.text)
    getUnisInPage(parser)