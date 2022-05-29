import os
import json
import datetime
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# we use this to get api key from env files
load_dotenv()
Dev_Token = os.getenv('Dev_Token')

'''
💡Use this version if you deploying it on repl.it
# Getiing bot token from env file
Dev_Token = os.environ['Dev_Token']

'''


# Getting TLDR articales
def currentDate():
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d")
    return date

# Scrapping data from tldr page


def get_tldr():
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d")
    url = 'https://tldr.tech/newsletter/' + date
    print(url+"\nSending Data...")
    response = requests.get(url)
    # check response status
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
    # find all div tag with class mt-3
        divs = soup.find_all('div', class_='mt-3')
        for content in divs:
            rawData = content.text.strip()
            # clear new line from data
            data = rawData.replace('\n\n', '')
            # dropFile = rawData.replace('\n\n', '\n')
            # firsthalf
            firsthalf = data.split('\n')[2:9]
            # secondhalf
            secondhalf = data.split('\n')[9:16]
            # thirdHalf
            thirdHalf = data.split('\n')[16:24]
            # fourthHalf
            fourthHalf = data.split('\n')[24:32]

            # Addinf data and then replacinf ir with new line
            firsthalf = '\n'.join(firsthalf).replace('\n', '\n\n')
            secondhalf = '\n'.join(secondhalf).replace('\n', '\n\n')
            thirdHalf = '\n'.join(thirdHalf).replace('\n', '\n\n')
            fourthHalf = '\n'.join(fourthHalf).replace('\n', '\n\n')
            print("TLDR Sent Succesfully 🚀")

            return (firsthalf, secondhalf, thirdHalf, fourthHalf)

    else:
        print("No articles today")
        noArt = "Sorry, on "+date+" there is no new article on tldr.tech ☹️"
        a, b, c, d = (noArt, noArt, noArt, noArt)
        return (a, b, c, d)


# Getting Devtop Top articles:


def devtoTop():
    url = "https://dev.to/api/articles/"
    res = requests.get(url, headers={"Api-Key": Dev_Token})
    data = res.json()
    # only take the title from the data
    titles = [i.get("title") for i in data]
    urls = [i.get("url") for i in data]
    # combining the both arrays as a dictionary
    devto = dict(zip(titles, urls))
    dev = list(devto.items())
    all_articles = []
    # looping over every title and url and then return ''<a href='+'"' + url+'"'+'>'+title+'</a>'+'\n\n'\'
    # two methods to obtain same thing
    # method 1
    for title, url in dev:
        # getting index number
        num = f"{dev.index((title, url))+1}"
        # adding the index number to the title
        articles = num+". "+'<a href='+'"' + url+'"'+'>'+title+'</a>'+'\n'
        # adding the articles to the list
        all_articles.append(articles)

    articles = '\n'.join(all_articles)
    print("Devto Top Sent Succesfully 🚀")
    return ("Devto Top Articles 💻\n\n"+articles)


# Getting latest articles from devto


def devtoLatest():
    latest = "https://dev.to/api/articles/latest"
    latestRes = requests.get(latest, headers={"Api-Key": Dev_Token})
    data = latestRes.json()
    # only take the title from the data
    titles = [i.get("title") for i in data]
    urls = [i.get("url") for i in data]
    # combining the both arrays as a dictionary
    devto = dict(zip(titles, urls))
    dev = list(devto.items())
    all_articles = []
    # looping over every title and url and then return ''<a href='+'"' + url+'"'+'>'+title+'</a>'+'\n\n'\'
    # two methods to obtain same thing
    # method 1
    for title, url in dev:
        # getting index number
        num = f"{dev.index((title, url))+1}"
        # adding the index number to the title
        articles = num+". "+'<a href='+'"' + url+'"'+'>'+title+'</a>'+'\n'
        # adding the articles to the list
        all_articles.append(articles)

    articles = '\n'.join(all_articles)
    print("Devto Latest Sent Succesfully 🚀")
    return ("Devto Latest Articles 💻\n\n"+articles)


# Getting latest archived articles from medium {technology}
# adding type of string for parameter
def get_medium(params: str):
    url = 'https://medium.com/tag/' + params
    res = requests.get(url, headers={
                       "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'})
    # print(res.status_code)
    soup = BeautifulSoup(res.text, 'html.parser')
    all_articles = []
    for article in soup.select('.meteredContent'):
        # print(article.text)
        title = article.find_all('h2')[0].getText()
        # The index 3 shows the 4th "a" tag
        url = article.find_all('a')[3].get('href')
        # appending medium.com before url
        link = "https://medium.com" + url
        # Appending data into array
        all_articles.append(title)
        all_articles.append(link)

    # splitting the array into two
    titles = all_articles[::2]
    urls = all_articles[1::2]
    # combining the both arrays as a dictionary
    medium = dict(zip(titles, urls))
    # converting the dictionary into a list
    medArray = list(medium.items())
    # looping over every title and url and then return ''<a href='+'"' + url+'"'+'>'+title+'</a>'+'\n\n'\'
    articlesArray = []
    for title, url in medArray:
        # getting index number
        num = f"{medArray.index((title, url))+1}"
        # adding the index number to the title
        article = num+". "+'<a href='+'"' + url+'"'+'>'+title+'</a>'+'\n'
        # adding the articles to the list
        articlesArray.append(article)

    articles = '\n'.join(articlesArray)
    print("Medium Sent Succesfully 🚀")
    return ("Medium "+params+" Articles 💻\n\n"+articles)


# All the articles from TechCrunch
def get_techcrunch():
    url = "https://techcrunch.com/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    article_titles, article_contents, article_hrefs = [], [], []

    for tag in soup.findAll("div", {"class": "post-block post-block--image post-block--unread"}):
        tag_header = tag.find("a", {"class": "post-block__title__link"})
        tag_content = tag.find("div", {"class": "post-block__content"})

        article_title = tag_header.get_text().strip()
        article_href = tag_header["href"]
        # article_content = tag_content.get_text().strip()

        article_titles.append(article_title)
        article_hrefs.append(article_href)
        # article_contents.append(article_content)

    all_articles = []
    article_count = int(len(article_titles))

    for i in range(article_count):
        all_articles.append([])

    for i in range(article_count):
        all_articles[i].append(article_titles[i])
        all_articles[i].append(article_hrefs[i])
        # all_articles[i].append(article_contents[i])

    articlesArray = []
    for i in range(article_count):
        articlesArray.append(
            f"{i+1}. <a href='{all_articles[i][1]}'>{all_articles[i][0]}</a>\n")

    techCrunchArticles = '\n'.join(articlesArray)

    print("Tech Crunch Articles sent successfully🚀")
    return ("Tech Crunch Articles 💻\n\n"+techCrunchArticles)


# HackerNews
def get_hackerNews():
    response = requests.get("https://news.ycombinator.com/news")
    soup = BeautifulSoup(response.content, 'html.parser')
    all_articles = []
    for item in soup.find_all('tr'):
        data = item.select('.titlelink')
        if data:
            all_articles.append(item.select('.titlelink')[0].get_text())
            all_articles.append(item.select('.titlelink')[0].get('href'))

    articlesArray = []
    for i in range(1, 30):
        articlesArray.append(
            f"{i+1}. <a href='{all_articles[i*2+1]}'>{all_articles[i*2]}</a>\n")

    hackerNewsArticles = '\n'.join(articlesArray)
    print('Hackernews Articles sent successfully🚀')
    return("Hacker News Articles 💻\n\n"+hackerNewsArticles)


# The Verge Articles
def get_theVerge():
    url = "https://www.theverge.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_articles = []
    for article in soup.select('.c-entry-box--compact__body'):
        title = article.select_one('.c-entry-box--compact__title').getText()
        # print(title)
        all_articles.append(title)
        link = article.select_one('a').get('href')
        # print(link)
        all_articles.append(link)

    articlesArray = []
    for i in range(len(all_articles)//2):
        articlesArray.append(
            f"{i+1}. <a href='{all_articles[i*2+1]}'>{all_articles[i*2]}</a>\n")

    theVergeArticles = '\n'.join(articlesArray)
    return("The Verge Articles 💻\n\n"+theVergeArticles)

# Product Hunt Articles


def get_productHunt():
    url = "https://www.producthunt.com/posts"
    user_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
    page = requests.get(url, headers={'User-Agent': user_Agent})
    soup = BeautifulSoup(page.content, 'html.parser')
    all_articles = []
    # finding all href tag and title tag via passing class
    links = soup.find_all('a', class_='styles_title__jWi91')
    for link in links:
        all_articles.append(link.text)
        post = link.get('href')
        url = "https://www.producthunt.com"+post
        all_articles.append(url)

    articlesArray = []
    for i in range(len(all_articles)//2):
        articlesArray.append(
            f"{i+1}. <a href='{all_articles[i*2+1]}'>{all_articles[i*2]}</a>")

    # Getting Description
    desc = soup.find_all('a', class_='styles_tagline__j29pO')
    descArray = []
    for desc in desc:
        descArray.append(desc.text)

    mergeArray = []
    for i in range(len(articlesArray)):
        mergeArray.append(articlesArray[i])
        mergeArray.append(descArray[i])
        mergeArray.append("\n")

    productHuntArticles = '\n'.join(mergeArray)
    return("Producthunt Articles 💻\n\n"+productHuntArticles)

# Wired Articles


def get_wired():
    url = "https://www.wired.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_articles = []
    for article in soup.find_all('a', class_='SummaryItemHedLink-cgPsOZ cnoEIb summary-item-tracking__hed-link summary-item__hed-link'):
        title = article.text
        href = article.get('href')
        url = "https://www.wired.com"+href
        all_articles.append(title)
        all_articles.append(url)

    articlesArray = []
    for i in range(len(all_articles)//2):
        articlesArray.append(
            f"{i+1}. <a href='{all_articles[i*2+1]}'>{all_articles[i*2]}</a>\n")

    wiredArticles = '\n'.join(articlesArray)
    return("Wired Articles 💻\n\n"+wiredArticles)


# Sidebar Articles
def get_sidebar():
    url = "https://sidebar.io/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_articles = []
    for article in soup.find_all('a', class_='post-link'):
        title = article.text
        url = article.get('href')
        all_articles.append(title)
        all_articles.append(url)

    articlesArray = []
    for i in range(len(all_articles)//2):
        articlesArray.append(
            f"{i+1}. <a href='{all_articles[i*2+1]}'>{all_articles[i*2]}</a>\n")

    sidebarArticles = '\n'.join(articlesArray)
    print("sidebar Articles sent successfully🚀")
    return("Sidebar Articles 💻\n\n"+sidebarArticles)


#  CssTricks Articles
def get_cssTricks():
    url = "https://css-tricks.com/archives/"
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
    page = requests.get(url, headers={'User-Agent': userAgent})
    soup = BeautifulSoup(page.content, 'html.parser')
    all_articles = []
    content = soup.find_all('h2')
    for articles in content:
        # Using strip to remove white space from the beginning and end
        title = articles.select_one('a').getText().strip()
        url = articles.select_one('a').get('href')
        all_articles.append(title)
        all_articles.append(url)

    articlesArray = []
    for i in range(len(all_articles)//2):
        articlesArray.append(
            f"{i+1}. <a href='{all_articles[i*2+1]}'>{all_articles[i*2]}</a>\n")

    cssTricksArticles = '\n'.join(articlesArray)
    print("cssTricks Articles sent successfully🚀")
    return("CssTricks Articles 💻\n\n"+cssTricksArticles)


# The Next Web Articles
def get_theNextWeb():
    url = "https://thenextweb.com/"
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
    page = requests.get(url, headers={'User-Agent': userAgent})
    soup = BeautifulSoup(page.content, 'html.parser')
    all_articles = []
    content = soup.find_all(
        'li', class_='o-grid__col md:o-grid__col--1/2 lg:o-grid__col--1/4')
    for articles in content:
        title = articles.find(
            'h4', class_='text-s leading-snug sm:text-m sm:leading-normal').getText().strip()
        # access the a tag using parent
        href = articles.find(
            'h4', class_='text-s leading-snug sm:text-m sm:leading-normal').parent.get('href')
        url = "https://thenextweb.com"+href
        all_articles.append(title)
        all_articles.append(url)

    articleArray = []
    for i in range(len(all_articles)//2):
        articleArray.append(
            f"{i+1}. <a href='{all_articles[i*2+1]}'>{all_articles[i*2]}</a>\n")

    theNextWebArticles = '\n'.join(articleArray)
    print("The Next Web Articles sent successfully🚀")
    return("The Next Web Articles 💻\n\n"+theNextWebArticles)


#  Echo js
def get_echojs():
    url = 'https://www.echojs.com/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_articles = []
    content = soup.select('section', class_='newslist')
    for articles in content:
        title = articles.find_all('h2')
        for article in title:
            title = article.find('a').getText().strip()
            url = article.find('a').get('href')
            all_articles.append(title)
            all_articles.append(url)

    # print(all_articles)
    articlesArray = []
    for i in range(len(all_articles)//2):
        articlesArray.append(
            f"{i+1}. <a href='{all_articles[i*2+1]}'>{all_articles[i*2]}</a>\n")

    echojsArticles = '\n'.join(articlesArray)
    print("Echojs Articles sent successfully🚀")
    return("Echojs Articles 💻\n\n"+echojsArticles)
