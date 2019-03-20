from subprocess import call
from tqdm import tqdm
import pandas as pd
import sqlite3
import os 
# Config 
email= 'YOUR_FACEBOOK_EMAIL'
password= 'YOUR_FACEBOOK_PASSWORD'
year= 2008
lang= 'it'


def crawl_pages():
    l=pd.read_csv('./update.csv')
    for name,url in tqdm(l.values):
        print('crawling %s'%name)
        print(url)
        call(['python3', '-m', 'scrapy', 'crawl', 'fb', '-a',  '-a','email=%s'%email,'-a','password=%s'%password,'-a', 'page=%s'%url, '-a', 'year=%d'%year, '-a', 'lang=%s'%lang, '-o', './result/%s.csv'%name])

def crawl_comments():
    db = pd.read_sql('select * from posts ', sqlite3.connect('./fb.db'))
    print(db.columns)
    for index,name,url_temp in tqdm(db[['index','crawl_from','url']].values):
        print('crawling %d,%s'%(index,name))
        url= 'https://mbasic.facebook.com' + url_temp
        print(url)
        call(['python3', '-m', 'scrapy', 'crawl', 'comments', '-a', 'email=%s'%email, '-a' ,'password=%s'%password, '-a', 'page=%s'%url,'-a','lang=%s'%lang,'-o', './comments/%s.csv'%index])

def crawl_batch_pages():
    url ='./pagelist'
    name ='test'
    call(['python3', '-m', 'scrapy', 'crawl', 'fb', '-a',  '-a','email=%s'%email,'-a','password=%s'%password,'-a', 'page=%s'%url, '-a', 'year=%d'year, '-a', 'lang=%s'%lang, '-o', './result/%s.csv'%name])

def crawl_batch_comments():
    post_list_dir= './comment_urls/'
    for url_filename in tqdm([i for i  in os.listdir(post_list_dir) if i.endswith('.txt')]):
        url = post_list_dir +url_filename 
        name =url_filename
        call(['python3', '-m', 'scrapy', 'crawl', 'comments', '-a', 'email=%s'%email, '-a' ,'password=%s'%password, '-a', 'page=%s'%url,'-a','lang=%s'%lang,'-o', './comments/%s.csv'%name])


if __name__ == '__main__':
    crawl_batch_comments()
