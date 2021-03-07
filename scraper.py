"""A script to save articles from https://www.nature.com/nature/articles
as separated files at local directories.
User inputs number of pages to look at from nature website and article type to look for.
Article would be saved in separated folders, named 'Page_N', where N is from user input.
"""
import requests
import os
from bs4 import BeautifulSoup
from string import punctuation

n_pages, article_type = [input() for i in range(2)]
saved_articles = []

for page in range(1, int(n_pages) + 1):

    os.mkdir(f'Page_{page}')

    request = requests.get(f'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={page}')

    soup = BeautifulSoup(request.content, 'html.parser')
    links = soup.find_all('article')

    for link in links:
        topic = link.find('span', {'class': 'c-meta__type'})
        href = link.a.get('href')

        if topic.text == article_type:
            title = link.a.text
            for char in title:
                if char in punctuation:
                    title = title.replace(char, '')
                if char == " ":
                    title = title.replace(char, '_')
            saved_articles.append(title)

            article_request = requests.get(f"https://www.nature.com{href}")
            article_soup = BeautifulSoup(article_request.content, 'html.parser')
            article = article_soup.find('div', {'class': 'article-item__body'})
            if not article:
                article = article_soup.find('div', {'class': 'article__body cleared'})

            if article:
                article = article.find_all('p')
                with open(f'Page_{page}/{title}.txt', 'wb') as file:
                    for string in article:
                        file.write(string.text.encode())
            else:
                article = article_soup.text.replace('\n', '')
                with open(f'Page_{page}/{title}.txt', 'wb') as file:
                    file.write(article.encode())

            """This part for testing purposes"""
            print(page, title)
            print(f"https://www.nature.com{href}")

print(f"Saved articles: ", saved_articles)
