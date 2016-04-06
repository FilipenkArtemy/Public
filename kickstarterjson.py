from bs4 import BeautifulSoup
from urllib.request import urlopen
import json

def getjson():
    url = 'https://www.kickstarter.com/discover/advanced?category_id=16&raised=1&sort=newest&seed=2409035&page=1'
    page = urlopen(url).read()
    soup = BeautifulSoup(page)
    for tag in soup.find_all('li'):
        if tag.get('class', '') == ['project', 'col', 'col-3', 'mb4']:
            newcontent = BeautifulSoup(tag.renderContents())
            break
    dic = {'pic': newcontent.find('img')['src'], 'noteofproj': newcontent.find('h6').find('a').renderContents().decode("utf-8"), 'descript': newcontent.find('p', {'class': 'project-blurb'}).renderContents()[1:-1].decode("utf-8")}
    return(json.dumps(dic))
