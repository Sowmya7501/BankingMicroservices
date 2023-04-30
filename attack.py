'''from bs4 import BeautifulSoup
import requests

html_text = requests.get('http://localhost:9898/getUser/1').json()
soup = BeautifulSoup(html_text,'lxml')
thing = soup.find_all('pre')
print(thing)

import urllib
from urllib import request
from bs4 import BeautifulSoup
import json
import time
def fun(index):
    index = str(index)
    for i in range(10):
        url = 'http://localhost:8080/api/user/{0}'.format(index)
        index = str(int(index)+1)
        html = request.urlopen(url).read()
        soup = BeautifulSoup(html,'html.parser')
        site_json=json.loads(soup.text)
        print(site_json)

if __name__ == '__main__':
    count = 0
    while True:
        print("enter value:")
        index = input()
        fun(index)
        time_wait = 1
        count += 1 
        print(f"waiting for {time_wait} minutes")
        time.sleep(time_wait*1)
        if count == 4:
            break
'''

'''
from bs4 import BeautifulSoup
import requests
import time
def fun(index,n):
    index = str(index)
    for i in range(n):
        url = 'http://localhost:8080/api/user/{0}'.format(index)
        index = str(int(index)+1)
        html = requests.get(url)
        if html.status_code == 500:
         print("NO VALUE")
        else:
            print(html.text)
    
if __name__ == '__main__':
    count = 0
    while True:

        print("enter index value:")
        index = input()
        print("enter number of requests to be sent")
        n = int(input())
        fun(index,n)
        time_wait = 1
        count += 1 
        print(f"waiting for {time_wait} minutes")
        time.sleep(time_wait*1)
        if count == 3:
            break  '''   















# from bs4 import BeautifulSoup
# import requests
# import time
# import lxml
# def fun(index,n):
#     index = str(index)
#     start = time.time()
#     count = 0
#     for i in range(n):
#         if time.time()-start <60:
#             url = 'http://bankappmicro.eastus.cloudapp.azure.com:8089/api/user/{0}'.format(index)                   #attack happening through api gateway
#             index = str(int(index)+1)
#             html = requests.get(url)
#             if "id" in html.text:
#                 soup = BeautifulSoup(html.text,'lxml')
#                 thing = soup.find('p').text
#                 print(thing)
#                 count +=1
#             else:
#                 print("NO VALUE")
#                 count +=1
#         else:
#             return count,time.time()-start  
# if __name__ == '__main__':
#     while True:
#         print("enter intial id value:")
#         index = input()
#         print("enter number of requests to be sent")
#         n = int(input())
#         x = fun(index,n)
#         if x is None:
#             pass
#         else:
#             print(x)
#         time_wait = 1
#         print(f"waiting for {time_wait} minute")
#         time.sleep(time_wait*60)





'''

from bs4 import BeautifulSoup
import requests
import time
import lxml
from lxml.html import fromstring
from itertools import cycle

def get_proxies():
  url = 'https://free-proxy-list.net/'
  response = requests.get(url)
  parser = fromstring(response.text)
  proxies = set()
  for i in parser.xpath('//tbody/tr')[:100]:
    if i.xpath('.//td[7][contains(text(),"yes")]'):
      #Grabbing IP and corresponding PORT
      proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
      proxies.add(proxy)
  return proxies

def fun(index,n):
    index = str(index)
    start = time.time()
    count = 0
    proxies = get_proxies()
    proxy_pool = cycle(proxies)
    for i in range(n):
            proxy = next(proxy_pool)
            url = 'http://localhost:8088/api/user/{0}'.format(index)
            index = str(int(index)+1)
            try:
                html = requests.get(url,proxies={"http": proxy, "https": proxy})

                if html.text:
                    soup = BeautifulSoup(html.text,'lxml')
                    thing = soup.find('p').text
                    print(thing)
                    count +=1
                else:
                    print("NO VALUE")
                    count +=1
            except:
                print("Connnection error")
        
       
            return count,time.time()-start  
if __name__ == '__main__':
    #count = 0
    while True:

        print("enter intial id value:")
        index = input()
        print("enter number of requests to be sent")
        n = int(input())
        x = fun(index,n)
        if x is None:
            pass
        else:
            print(x)
        #time_wait = 1
        #count += 1 
        #print(f"waiting for {time_wait} minute")
        #time.sleep(time_wait*60)

'''





from bs4 import BeautifulSoup
import requests
import time
import lxml
def fun(index,n):
    index = str(index)
    for i in range(n):
            url = 'http://172.173.149.51:8089/api/user/{0}'.format(index)                   #attack happening through api gateway
            index = str(int(index)+1)
            html = requests.get(url)
            if "id" in html.text:
                soup = BeautifulSoup(html.text,'lxml')
                thing = soup.find('p').text
                print(thing)
            else:
                print("NO VALUE")
                
if __name__ == '__main__':
    while True:
        print("enter intial id value:")
        index = input()
        print("enter number of requests to be sent")
        n = int(input())
        fun(index,n)
        # x = fun(index,n)
        # if x is None:
        #     pass
        # else:
        #     print(x)
        # time_wait = 1
        # print(f"waiting for {time_wait} minute")
        # time.sleep(time_wait*60)









from bs4 import BeautifulSoup
import requests
import time
import lxml
def fun(index,n):
    index = str(index)
    url = 'http://172.173.149.51:8088/api/user/{0}'.format(index)                   #attack happening through api gateway
    index = str(int(index)+1)
    html = requests.get(url)
    if "id" in html.text:
        soup = BeautifulSoup(html.text,'lxml')
        thing = soup.find('p').text
        print(thing)
    else:
        print("NO VALUE")
                
if __name__ == '__main__':
     count = 0
     index = 1
     while count!=35:
        print(count)
        fun(index,count)
        index +=1
        count +=1
        time.sleep(60)
