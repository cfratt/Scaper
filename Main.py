import random
from bs4 import BeautifulSoup
import requests


agentList = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


usedAgents = []
page = 0
data = []


import re
import csv
prices = []
mileages = []
years = []
Touareg = []


print('Fetching data...')


for i in range(0,10):
    used = False
    done = False
    
    while used == False:
        user_agent = random.choice(agentList)
        if user_agent not in usedAgents:
            used = True
            usedAgents.append(user_agent)
            print (str(i+1) + ':page complete')
        if len(usedAgents) == 10:
            done = True
            print('10 user agents used, exiting before error')
            break
        
    if done == False:
        page_link = "https://www.autotrader.com/cars-for-sale/Diesel/Volkswagen/Touareg/Salt+Lake+City+UT-84102?zip=84102&marketExtension=on&\\\
startYear=2002&endYear=2019&makeCodeList=VOLKS&searchRadius=0&modelCodeList=TOUAREG&fuelTypeGroup=DSL&sortBy=relevance&numRecords=100&firstRecord=" + str(page)
        page += i * 100
        
        page_response = requests.get(page_link, timeout = 6, headers = {'User-Agent' : user_agent})
        
        response = BeautifulSoup(page_response.content, 'html.parser')
        
        Touareg = response.findAll('div', attr={"class":"inventory-listing-body padding-top-3 padding-right-3 margin-bottom-2"})
        
        first_tour = Touareg[1]
        
        for first_tour in Touareg:
            
            if first_tour.find('div', class_ = "text-gray-base text-bold text-size-20") is not None:
                yeartext = first_tour.a.text
                year = re.findall("\d+", yeartext)
                years.append(year[0])
                ##print (year[0])
            else:
                year = -10
                years.append(year)
        
            if first_tour.find('div', class_ = "item-card-specifications margin-top-4 text-gray-dark margin-bottom-3") is not None:
                mileage = first_tour.find('div',attrs={"class":"item-card-specifications margin-top-4 text-gray-dark margin-bottom-3"}).text
                mileagestr = mileage.replace(',', '')
                mileagenum = re.findall("\d+", mileagestr)
                mileages.append(mileagenum[0])
                ##print(mileagenum[0])
            else:
                mileagenum = [-1]
                mileages.append(mileagenum[0])
                ##print("NA")
        
            if first_tour.find('div', class_ = "text-gray-base text-bold text-size-20") is not None:
                price = first_tour.find('div',attrs={"class":"text-gray-base text-bold text-size-20"}).text
                priceint = price.replace('$', '')
                pricesec = priceint.replace(',', '')
                pricefin = re.findall("\d+", pricesec)
                prices.append(pricefin[0])
                ##print (pricefin[0])
            else:
                price = [-2000]
                prices.append(price[0])
        
    else:
        print('done scraping')


print('Starting Extraction')
print("exporting to csv")
with open("cardata.csv", 'w', newline='') as f:
        thewriter = csv.writer(f)
        lo = 0;
        for year in years:
            thewriter.writerow([years[lo],prices[lo],mileages[lo]])
            lo += 1
        
        print(lo)
