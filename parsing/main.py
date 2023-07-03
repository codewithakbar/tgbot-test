import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time 


def get_first_news():
    headers = {
      #   "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/114.0.0.0"

    }

    url = "https://ria.ru/world/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("div", class_="list-item")

    news_dict = {}

    for article in articles_cards:
        article_title = article.find("div", class_="list-item__content").find("a", class_="list-item__title").text.strip()
        article_date = article.find("div", class_="list-item__info").find("div", class_="list-item__date").text.strip()
        article_url = article.find("div", class_="list-item__content").find("a").get("href")
        article_img = article.find("div", class_="list-item__content").find("img").get("src")

        article_id = article_url.split("/")[-1]
        article_id = article_id[:-5]
        # print(f"{article_title} | {article_url} | {article_img}")

        news_dict[article_id] = {
            "article_date_timestamp": article_date,
            "article_title": article_title,
            "article_url": article_url,
            "article_img": article_img,
        }
    
    with open("news_dict.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_news_update():
    with open("news_dict.json", encoding="utf-8") as file:
        news_dict = json.load(file)

    headers = {
      #   "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/114.0.0.0"

    }

    url = "https://ria.ru/world/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("div", class_="list-item")

    fresh_news = {}
    for article in articles_cards:
        article_url = article.find("div", class_="list-item__content").find("a").get("href")
        article_id = article_url.split("/")[-1]
        article_id = article_id[:-5]

        if article_id in news_dict:
            continue
        else:
            article_title = article.find("div", class_="list-item__content").find("a", class_="list-item__title").text.strip()
            article_date = article.find("div", class_="list-item__info").find("div", class_="list-item__date").text.strip()
            article_img = article.find("div", class_="list-item__content").find("img").get("src")


            # print(f"{article_title} | {article_url} | {article_id}")

            news_dict[article_id] = {
                "article_date_timestamp": article_date,
                "article_title": article_title,
                "article_url": article_url,
                "article_img": article_img,
            }

            fresh_news[article_id] = {
                "article_date_timestamp": article_date,
                "article_title": article_title,
                "article_url": article_url,
                "article_img": article_img,
            }

    with open("news_dict.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news



# get_first_news()
# print(check_news_update())

def main():
    get_first_news()
    print(check_news_update())


if __name__ == '__main__':
    main()