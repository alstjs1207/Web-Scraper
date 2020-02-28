import requests
from bs4 import BeautifulSoup
URL = "https://finance.naver.com/news/mainnews.nhn"

def get_news():
    print('web news start')
    jobs = []
    news = {}
    result = requests.get(URL)
    result.raise_for_status()
    result.encoding = 'euc-kr'
    if(result.status_code==200):
        soup = BeautifulSoup(result.text, "html.parser")
        tags = soup.find('div',{"class":"mainNewsList"})
        tag = tags.find_all('li',{"class":"block1"})
        for data in tag[:-1]:
          title = data.find('dt',{"class":"articleSubject"})
          if title is not None:
            title = title.find("a").getText(strip=True)
          else:
            title = data.find('dd',{"class":"articleSubject"}).find("a").getText(strip=True)

          content = data.find('dd',{"class":"articleSummary"}).getText(strip=True)
          news = {
            'news': title,
            'content': content
          }
          jobs.append(news)
    print('web news end')
    return jobs
