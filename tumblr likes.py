# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 16:30:20 2017

@author: asus
"""

#TUMBLR SCRIPT

'''
1. Log in to tumblr
2. Redirect to favourites
3. Parse all favourites by executing infinite scroll until all data has been loaded
4. for videos, collect video links. For images, collect image links
5. Initiate queued download of data.
5a. Check for whether file already exists.
'''
import bs4
import requests
import urllib.request
import re
import os
import sys
import time
from tqdm import tqdm

#add storage file which can run straight away
x,y,z=[],[],[]
webpage='https://www.tumblr.com/likes'
session=requests.Session()
a = requests.adapters.HTTPAdapter(max_retries=3)
session.mount(webpage, a)
headers={'User-agent':'Mozilla/5.0'}
get=session.get('https://www.tumblr.com/login?redirect_to=%2Flikes', headers=headers)
soup=bs4.BeautifulSoup(get.text, 'lxml')
fk=(soup.find(attrs = {'name' : 'form_key'}))


login= {
        'determine_email':'neilasjoseph@gmail.com',
        'user[email]':'neilasjoseph@gmail.com',
        'user[password]':'kungfoo5225t',
        'tumblelog[name]':'',
        'user[age]':'',
        'context':'other',
        'version':'STANDARD',
        'follow':'',
        'http_referer':'https://www.tumblr.com/logout',
        'form_key':fk['value']
        }
    

session.post('https://www.tumblr.com/login?redirect_to=%2Flikes', data=login, headers=headers)
get1=session.get(webpage, headers=headers)
soup1=bs4.BeautifulSoup(get1.text, 'lxml')
page=(soup1.find('a', id='next_page_link'))

def next_page(page):
    page=str(page)
    regex=re.compile("/page/\d+/\d+")
    result=regex.findall(page)
    return result[0]



inp=input("type 'all' to back up all data, or enter number of pages you wish to back up.")
if inp=='all':
    start=time.time()
    print('Scraping file list. This process will not take longer than 5 minutes.')
    while True:
        print('Video file list currently '+str(len(x))+' items long')
        get1=session.get(webpage, headers=headers)
        soup1=bs4.BeautifulSoup(get1.text, 'lxml')
        x.extend(soup1.find_all('source'))
        y.extend(soup1.find_all('img', class_='post_media_photo image'))
        z.extend(soup1.find_all('a', class_='photoset_photo rapid-noclick-resp'))
        page=(soup1.find('a', id='next_page_link'))
        nextp=next_page(page)
        if nextp==None:
            print('No more pages to scrape')
            break
        elif time.time()-start>300:
            print('Scrape of code took more than 5 minutes. Stopping...')
            break
        else:
            webpage='https://www.tumblr.com/likes'+nextp
            get1=session.get(webpage, headers=headers)
                   
else:
    start=time.time()
    try:
        inpp=int(inp)
        print('Scraping file list. This process will not take longer than 5 minutes.')
    except:
        sys.exit('Incorrect sum. Cannot continue')
    for i in range(inpp):
#        if i%10==0 and i!=0:
#            print('re-logging in to avoid HTTPError')
#            login()
        print('Video file list currently '+str(len(x))+' items long')
        get1=session.get(webpage, headers=headers)
        soup1=bs4.BeautifulSoup(get1.text, 'lxml')
        x.extend(soup1.find_all('source'))
        y.extend(soup1.find_all('img', class_='post_media_photo image'))
        z.extend(soup1.find_all('a', class_='photoset_photo rapid-noclick-resp'))
        page=(soup1.find('a', id='next_page_link'))
        nextp=next_page(page)
        if nextp==None:
            print('No more pages to scrape')
            break
        elif time.time()-start>300:
            print('Scrape of code took more than 5 minutes. Stopping...')
            break
        else:
            webpage='https://www.tumblr.com/likes'+nextp
            get1=session.get(webpage, headers=headers)


print(str(len(x))+' videos, '+str(len(y))+' photos, '+str(len(z))+ 'photosets')



#get all pages stage



#download stage


def pic_list(pics):
    pics=str(pics)
    regex=re.compile("http.\\S*?.jpg|http.\\S*?.gif")
    result=regex.findall(pics)   
    return result

def photoset_list(pics):
    pics=str(pics)
    regex=re.compile("http.\\S*?.jpg|http.\\S*?.gif")
    result=regex.findall(pics)   
    result1=[]
    for i in range(len(result)):
        if i%2==0:
            result1.append(result[i])
    return result1

def vid_list(vids):
    list=[]
    regex=re.compile(r'"(.*?)"')
    vids=str(vids)
    result=regex.findall(vids)
    for i in result:
        i+='.mp4'
        if i!='video/mp4.mp4':
            list.append(i)
    return list

def name_function(name):
    x=list(name)
    for i in range(len(x)):
        if x[i] =='/':
            x[i]='.'
    result=''.join(x)
    return result
#3

#add timeout for download inactivity
#add comparison for network file size vs local file size
def vid_downloader(v_list):
    os.chdir('C:\\Users\\asus\\.spyder-py3\\my scripts\\')
    number=0
    for vid in vid_list(v_list):
        number+=1
        name=str(vid[-21:])
        name=name_function(name)
        try:
            size=urllib.request.urlopen(vid)
            size=int(size.info()['Content-Length'])
        except:
            print('error with vid '+str(number )+' '+name)
            continue
        url=str(vid)
        path = './data/'+name
        try:
            os.path.getsize(path)
        except (FileNotFoundError, NameError):
                print('downloading vid ' +str(number) +' '+ name)
                r = requests.get(url, stream=True)
                with open(path, 'wb') as f:
                    for data in tqdm(r.iter_content(1024), total=size, unit='KB', unit_scale=True, miniters=1):
                        f.write(data)
                        f.flush()
        except HTTPError:
            continue
                
        else: 
             if os.path.getsize(path)==size:
                print('vid '+str(number)+' '+name+' already exists')
             elif os.path.getsize(path)<size:
                print('Local file size incorrect, redownloading vid ' +str(number)+' '+ name)
                r = requests.get(url, stream=True)
                with open(path, 'wb') as f:
                    for data in tqdm(r.iter_content(1024), total=size, unit='KB', unit_scale=True, miniters=1):
                        f.write(data)
                        f.flush()
        

def all_photo_downloader(pics,photoset):
    pics_downloader(pics)
    photoset_downloader(photoset)
    
def pics_downloader(pics):
    os.chdir('C:\\Users\\asus\\.spyder-py3\\my scripts\\data\\pics')
    for pic in pic_list(pics):
        name=str(pic[-27:])
        name=name_function(name)
        url=str(pic)
        if os.path.isfile(name)==True:
            continue
        else:
            print('downloading pic ' + name)
            r= requests.get(url, stream=True)
            with open(name, 'wb') as f:
                    for data in tqdm(r.iter_content(32*1024), unit='B', unit_scale=True):
                        f.write(data)
                        f.flush()
                
def photoset_downloader(pics):
    os.chdir('C:\\Users\\asus\\.spyder-py3\\my scripts\\data\\pics')
    for pic in photoset_list(pics):
        name=str(pic[-27:])
        name=name_function(name)
        url=str(pic)
        if os.path.isfile(name)==True:
            continue
        else:
            print('downloading ' + name + ' photoset')
            try:
                r= requests.get(url, stream=True)
                with open(name, 'wb') as f:
                        for data in tqdm(r.iter_content(32*1024), unit='B', unit_scale=True):
                            f.write(data)
                            f.flush()
            except SSLError:
                continue
        
def all_downloads(vids,pics,photoset):
    all_photo_downloader(pics,photoset)
    vid_downloader(vids)
    print('COMPLETE!')
#

all_downloads(x,y,z)










#logdata={'login':'user','password':'pass'}
#session=requests.Session()
#session1=session.post(url)#,data=logdata )
#soup=bs4.BeautifulSoup(session1,"html5lib")
#print(soup)

