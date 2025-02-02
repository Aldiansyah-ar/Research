import requests
import pandas as pd
from bs4 import BeautifulSoup
user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

def detik_page(query, start_date, end_date):
  url = f'https://www.detik.com/search/searchnews?query={query}&siteid=3&sortby=time&sorttime=1&fromdatex={start_date}&todatex={end_date}&result_type=latest'
  text = requests.get(url, user_agent).text
  sop = BeautifulSoup(text, 'lxml')
  try:
    paging = sop.find_all('div','pagination text-center mgt-16 mgb-48')[0].find_all('a')[-2]
    last_page = paging.text
  except:
    last_page = 1
  return last_page

def scrape_detik(query, start_date, end_date):
    last_page = detik_page(query, start_date, end_date)
    data = []
    id = 0
    for page in range(1,int(last_page)+1):
        url = f'https://www.detik.com/search/searchnews?query={query}&siteid=3&sortby=time&sorttime=1&fromdatex={start_date}&todatex={end_date}&result_type=latest&page={page}'
        text = requests.get(url,user_agent).text
        soup = BeautifulSoup(text, 'lxml')
        articles_container = soup.find_all('article', class_='list-content__item')
        print(f'page: {page}')
        for article in articles_container:
            headline = article.find('div', 'media__text').find('a').text
            link = article.find('div', 'media__text').find('a')['href']
            link_ = link + f'?single=1'
            try:
              news = requests.get(link_,user_agent).text
              news_soup = BeautifulSoup(news, 'lxml')
              date = news_soup.find('div', class_='detail__date').text
              content_container = news_soup.find('div', class_='detail__body-text itp_bodycontent')
              location = content_container.find('strong').text
              contents = content_container.find_all('p', class_='')
              text = []
              id += 1
              for x in contents:
                  y = x.text
                  text.append(y)
                  content = ' '.join(text).replace('ADVERTISEMENT','').replace('SCROLL TO RESUME CONTENT','')

              print(f'article: {id}')
              content = location + ' - ' + content
              data.append({'id': id,
                          'source': 'Detik',
                          'title': headline, 
                          'url': link,
                          'content': content, 
                          'date': date})
            except:
              pass

    df = pd.DataFrame(data)
    return df

scrape_detik('Kebakaran Gudang Peluru', '30/03/2024', '03/04/2024')

def detik_indeks_page(date):
  url = f'https://news.detik.com/berita/indeks?page=1&date={date}'
  text = requests.get(url).text
  sop = BeautifulSoup(text, 'lxml')
  try:
    paging = sop.find_all('div','pagination text-center mgt-16 mgb-16')[0].find_all('a')[-2]
    last_page = paging.text
  except:
    last_page = 1
  return last_page

def detik_news_indeks(date):
    last_page = detik_indeks_page(date)
    data = []
    for page in range(1,int(last_page)+1):
        url = f'https://news.detik.com/berita/indeks?page={page}&date={date}'
        text = requests.get(url,user_agent).text
        soup = BeautifulSoup(text, 'lxml')
        articles_container = soup.find_all('article', class_='list-content__item')
        for article in articles_container:
            headline = article.find('div', 'media__text').find('a').text
            link = article.find('div', 'media__text').find('a')['href']
            link_ = link + f'?single=1'
            try:
              news = requests.get(link_,user_agent).text
              news_soup = BeautifulSoup(news, 'lxml')
              date = news_soup.find('div', class_='detail__date').text
              content_container = news_soup.find('div', class_='detail__body-text itp_bodycontent')
              location = content_container.find('strong').text
              contents = content_container.find_all('p', class_='')
              text = []
              for x in contents:
                  y = x.text
                  text.append(y)
                  content = ' '.join(text).replace('ADVERTISEMENT','').replace('SCROLL TO RESUME CONTENT','').replace('SCROLL TO CONTINUE WITH CONTENT', '')

              content = location + ' - ' + content

              data.append({'source': 'Detiknews',
                          'title': headline,
                          'url': link,
                          'content': content,
                          'date': date})
            except:
              pass

    df = pd.DataFrame(data)
    return df

detik_news_indeks('01/31/2025')