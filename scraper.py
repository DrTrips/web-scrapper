import requests
import string
import os
import re

from bs4 import BeautifulSoup

num_of_pages = int(input())
article_type = input()


def content_reader(link, article_type):
    r = requests.get(link, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(r.content, 'html.parser')
    articles = soup.find_all('article')
    for article in articles:
        if article.find('span', attrs={'class': 'c-meta__type'}).text == article_type:
            article_title = article.find('h3').text
            file_title = article_title.strip().translate(str.maketrans('', '', string.punctuation)).replace(' ', '_')
            article_scrape_url = article.find('a', {"class": "c-card__link u-link-inherit"}).get('href')
            article_url = requests.get('https://www.nature.com' + article_scrape_url)
            article_soup = BeautifulSoup(article_url.content, 'html.parser')
            article_paragraphs = article_soup.find("div", {"class": "c-article-body"}, 'p')
            article_item = article_soup.find("div", {"class": "article-item__body"}, 'p')
            artic = article_soup.find("div", {"class": "article"}, 'p')
            article_file = open(f"{file_title}.txt", 'ab')
            if article_paragraphs:
                content = article_paragraphs.text.strip()
                content = re.sub('[\r\n]', '', content)
                article_file.write(content.encode())
            elif article_item:
                content = article_item.text.strip()
                content = re.sub('[\r\n]', '', content)
                article_file.write(content.encode())
            else:
                content = artic.text.strip()
                content = re.sub('[\r\n]', '', content)
                article_file.write(content.encode())
            article_file.close()


def main():
    page_num = 0
    while page_num != num_of_pages:
        page_num += 1
        url = "https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={}".format(page_num)
        os.chdir('C:\\Users\\Anton\\PycharmProjects\\Web Scraper\\Web Scraper\\task')
        os.mkdir("Page_{}".format(page_num))
        os.chdir('C:\\Users\\Anton\\PycharmProjects\\Web Scraper\\Web Scraper\\task\\Page_{}'.format(page_num))
        content_reader(url, article_type)


main()
