#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install selenium ')


# # 1. Write a python program which searches all the product under a particular product from www.amazon.in. The 
# product to be searched will be taken as input from user. For e.g. If user input is ‘guitar’. Then search for 
# guitars

# In[3]:


import selenium

import pandas as pd

import time

from bs4 import BeautifulSoup

from selenium import webdriver

from selenium.common.exceptions import StaleElementReferenceException,NoSuchElementException

import requests

from selenium.webdriver.common.by import By


# In[62]:



driver = webdriver.Chrome()

driver.get("https://www.amazon.in/")


# In[63]:


search_bar=driver.find_element(By.ID,"twotabsearchtextbox")


# In[64]:


print("Enter search word")
search_for=input()


# In[65]:


search_bar.clear()
search_bar.send_keys(search_for)


# In[66]:


search_button=driver.find_element(By.ID,"nav-search-submit-button")
search_button.click()


# # 2. In the above question, now scrape the following details of each product listed in first 3 pages of your search 
# results and save it in a data frame and csv. In case if any product has less than 3 pages in search results then 
# scrape all the products available under that product name. Details to be scraped are: "Brand 
# Name", "Name of the Product", "Price", "Return/Exchange", "Expected Delivery", "Availability" and 
# “Product URL”. In case, if any of the details are missing for any of the product then replace it by “-“.

# In[45]:


urls = []

start = 0
end = 2


for page in range(start,end+1):
    try:
        page_url=driver.find_elements(By.XPATH,'//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]')
        
        for  i in page_url:
            i = i.get_attribute('href')
            if i[0:4]=='http':                
                urls.append(i)                
        print("Product urls of page {} has been scraped.".format(page+1))
        
        nxt_button = driver.find_element(By.XPATH,'//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]')
        if nxt_button.text == 'Next':
            nxt_button.click()                                                  
            time.sleep(5)                                                        
            
        elif driver.find_element(By.XPATH,'//span[@class="s-pagination-item s-pagination-disabled"]').text == 'Next':    
            print("No new pages exist. Breaking the loop")  
            break
            
    except StaleElementReferenceException as e:             
            print("Stale Exception")
            next_page = nxt_button.get_attribute('href')       
            driver.get(next_page)  


# In[79]:


len(urls)


# In[69]:


Brand_Name = [] 
Name_of_the_Product = []
Price = []
Return_Exchange = []
Expected_Delivery = []
Availability = []
Product_URL = []

for i in urls:
    driver.get(i)
    time.sleep(5)
    
    try:
        brand = driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[5]/div[3]/div[4]/div[46]/div/table/tbody/tr[1]/td[2]')
        Brand_Name.append(brand.text)
    except NoSuchElementException as e:
        Brand_Name.append("-")
        
    
    try:
        product_name = driver.find_element(By.ID,'productTitle')
        Name_of_the_Product.append(product_name.text)
    except NoSuchElementException as e:
        Name_of_the_Product.append("-")
        
    try:
        prices = driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[5]/div[3]/div[1]/div[3]/div/div[1]/div/div/div/form/div/div/div/div/div[2]/div[1]/div/span[1]/span[2]/span[2]')
        Price.append(prices.text)
    except NoSuchElementException as e:
        Price.append("-")
        
    try:
        return_exchange = driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[5]/div[3]/div[4]/div[24]/div[2]/div/div/div/div[2]/div/ol/li[3]/div/span/div[2]')
        Return_Exchange.append(return_exchange.text)
    except NoSuchElementException as e:
        Return_Exchange.append("-")
        
    try:
        expected_delivery = driver.find_element(By.XPATH,'//span[@class="a-text-bold"]')
        Expected_Delivery.append(expected_delivery.text)
    except NoSuchElementException as e:
        Expected_Delivery.append("-")
        
    try:
        availability = driver.find_element(By.XPATH,'//span[@class="a-size-medium a-color-success"]')
        Availability.append(availability.text)
    except NoSuchElementException as e:
        Availability.append("-")


# In[70]:


print(Brand_Name)
print(Name_of_the_Product)
print(Price)
print(Return_Exchange)
print(Expected_Delivery)
print(Availability)


# In[80]:


print(len(Brand_Name),len(Name_of_the_Product),len(Price),len(Return_Exchange),len(Expected_Delivery),len(Availability),len(urls))


# In[73]:


df=pd.DataFrame({'Brand_Name':Brand_Name,'Name_of_the_Product':Name_of_the_Product,'Price':Price,'Return_Exchange':Return_Exchange,'Expected_Delivery':Expected_Delivery,'Availability':Availability,'Product_Url':urls})
df


# # question 3Write a python program to access the search bar and search button on images.google.com and scrape 10
# # images each for keywords ‘fruits’, ‘cars’ and ‘Machine Learning’, ‘Guitar’, ‘Cakes’

# In[185]:



driver = webdriver.Chrome()
driver.get("https://images.google.com/?gws_rd=ssl")


# In[186]:


search_bar=driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea")
search_bar.send_keys("guitar")
time.sleep(3)


# In[187]:


search_button=driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/button")
search_button.click()


# In[188]:


for i in range(0,3):
    driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")


# In[189]:


guitar_images=driver.find_elements(By.TAG_NAME,"img")


# In[192]:


import re 
import urllib.request
import os 


# In[193]:


try:
    os.mkdir("guitar_images")
except FileExistsError:
    pass
#download the image from url-->save to folder-->with image.count.jpg format
count = 0
for i in guitar_images[0:10]:
    src=i.get_attribute('src')
    count+=1
    urllib.request.urlretrieve(src,os.path.join('guitar_images','image'+str(count)+'.jpg'))
    print("number of images downloaded ="+str(count),end='\r')


# In[194]:


driver = webdriver.Chrome()
driver.get("https://images.google.com/?gws_rd=ssl")


# In[196]:


search_bar=driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea")
search_bar.send_keys("cake")
time.sleep(2)
search_button=driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/button/div")
search_button.click()


# In[197]:


for i in range(0,3):
    driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
    cake_images=driver.find_elements(By.TAG_NAME,"img")


# In[198]:


cake_images=driver.find_elements(By.TAG_NAME,"img")


# In[199]:


try:
    os.mkdir("guitar_images")
except FileExistsError:
    pass
#download the image from url-->save to folder-->with image.count.jpg format
count = 0
for i in guitar_images[0:10]:
    src=i.get_attribute('src')
    count+=1
    urllib.request.urlretrieve(src,os.path.join('guitar_images','image'+str(count)+'.jpg'))
    print("number of images downloaded ="+str(count),end='\r')


# In[200]:


try:
    os.mkdir("cake_images")
except FileExistsError:
    pass

count = 0
for i in cake_images[0:10]:
    src=i.get_attribute('src')
    count+=1
    urllib.request.urlretrieve(src,os.path.join('cake_images','image'+str(count)+'.jpg'))
    print('number of images downloaded='+str(count),end='\r')


# # 4. Write a python program to search for a smartphone(e.g.: Oneplus Nord, pixel 4A, etc.) on www.flipkart.com
# and scrape following details for all the search results displayed on 1st page. Details to be scraped: “Brand 
# Name”, “Smartphone name”, “Colour”, “RAM”, “Storage(ROM)”, “Primary Camera”, 
# “Secondary Camera”, “Display Size”, “Battery Capacity”, “Price”, “Product URL”. Incase if any of the 
# details is missing then replace it by “- “. Save your results in a dataframe and CSV

# In[159]:


driver.get('https://www.flipkart.com/')


# In[160]:


search_bar=driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div[1]/div[2]/div[2]/form/div/div/input")
search_bar.send_keys("smartphone")


# In[161]:


search_button=driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div[1]/div[2]/div[2]/form/div/button")
search_button.click()


# In[162]:


page1_url = []   #empty list
urls = driver.find_elements(By.XPATH,"//a[@class='_1fQZEK']")
for url in urls:
    page1_url.append(url.get_attribute('href'))


# In[99]:


Brand_Name = []
Phonename = []
Colour = []
RAM= []
Storage_ROM = []
PrimaryCamera= []
SecondaryCamera= []
Display_Size= []
BatteryCapacity= []
Price= []


# In[89]:


for i in page1_url:
    driver.get(i)
    time.sleep(5)
    
    try:
        brand = driver.find_element(By.XPATH,'//span[@class="B_NuCI"]')
        product_name = brand.text
        brand_name = product_name.split(' ', 1)[0]
        Brand_Name.append(brand_name)
    except NoSuchElementException as e:
        Brand_Name.append("-")
        
    try:
        name = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[3]/div[1]/div[2]/div[10]/div[5]/div/div[2]/div[1]/div[1]/table/tbody/tr[3]/td[2]/ul/li')
        Phonename.append(name.text)
    except NoSuchElementException as e:
        Phonename.append("-")
        
    try:
        colourtag = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[3]/div[1]/div[2]/div[10]/div[5]/div/div[2]/div[1]/div[1]/table/tbody/tr[4]/td[2]/ul')
        Colour.append(colourtag.text)
    except NoSuchElementException as e:
        Colour.append('-')
        
    try:
        ramtag = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[3]/div[1]/div[2]/div[10]/div[5]/div/div[2]/div[1]/div[4]/table/tbody/tr[2]/td[2]')
        RAM.append(ramtag.text)
    except NoSuchElementException as e:
        RAM.append('-')
        
    try:
        romtag = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[3]/div[1]/div[2]/div[10]/div[5]/div/div[2]/div[1]/div[4]/table/tbody/tr[1]/td[2]/ul')
        Storage_ROM.append(romtag.text)
    except NoSuchElementException as e:
        Storage_ROM.append('-')
        
    try:
        cameratag = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[3]/div[1]/div[2]/div[10]/div[5]/div/div[2]/div[1]/div[5]/table/tbody/tr[2]/td[2]/ul')
        PrimaryCamera.append(cameratag.text)
    except NoSuchElementException as e:
        PrimaryCamera.append('-')
        
    try:
        sccondcamera = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[3]/div[1]/div[2]/div[10]/div[5]/div/div[2]/div[1]/div[5]/table/tbody/tr[6]/td[2]/ul')
        SecondaryCamera.append(sccondcamera.text)
    except NoSuchElementException as e:
        SecondaryCamera.append('-')
        
    try:
        displaytag = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[3]/div[1]/div[2]/div[10]/div[5]/div/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[2]/ul')
        Display_Size.append(displaytag.text)
    except NoSuchElementException as e:
        Display_Size.append('-')
        
    try:
        battrytag = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[3]/div[1]/div[2]/div[10]/div[5]/div/div[2]/div[1]/div[10]/table/tbody/tr[1]/td[2]/ul')
        BatteryCapacity.append(battrytag.text)
    except NoSuchElementException as e:
        BatteryCapacity.append('-')
        
    try:
        pricetag = driver.find_element(By.XPATH,'//div[@class="_30jeq3 _16Jk6d"]')
        Price.append(pricetag.text)
    except NoSuchElementException as e:
        Price.append('-')
        
        


# In[55]:


print(len(Brand_Name),len(Phonename),len(Colour),len(RAM),len(Storage_ROM),len(PrimaryCamera),len(SecondaryCamera),len(Display_Size),len(BatteryCapacity),len(Price))
Storage_ROM = []
PrimaryCamera= []
SecondaryCamera= []
Display_Size= []
BatteryCapacity= []
Price= []


# In[86]:


print(len(Brand_Name),len(Phonename),len(Colour),len(RAM),len(Storage_ROM),len(PrimaryCamera),len(SecondaryCamera),len(Display_Size),len(BatteryCapacity),len(Price))


# In[91]:


df=pd.DataFrame({'Brand Name':Brand_Name,
                 'Smartphone name':Phonename,
                 'Colour':Colour,
                 'RAM':RAM,
                 'Storage ROM':Storage_ROM,
                 'Primary Camera':PrimaryCamera,
                 'SecondaryCamera':SecondaryCamera,
                 'Display_Size':Display_Size,
                 'BatteryCapacity':BatteryCapacity,
                 'Price':Price})
df


# # QUESTION 5 Write a program to scrap geospatial coordinates (latitude, longitude) of a city searched on google maps

# In[ ]:


import selenium
import pandas as pd
from bs4 import BeautifulSoup
import time

#Importing requests
import requests

# importing regex
import re

# Importing selenium webdriver
from selenium import webdriver

# Importing required Exceptions
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

import warnings
warnings.filterwarnings('ignore')
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



driver = webdriver.Chrome()


# In[212]:


driver.get("https://www.google.co.in/maps")


# In[213]:


City = input('Enter City name that has to be searched : ')
search_bar = driver.find_element(By.ID,"searchboxinput")                       
search_bar.clear()                                                             
time.sleep(2)


# In[214]:


search_bar.send_keys(City) 


# In[215]:


search_btn = driver.find_element(By.ID,"searchbox-searchbutton")              
search_btn.click()                                                             
time.sleep(2)


# In[216]:


try:
    url_str = driver.current_url
    print("URL Extracted: ", url_str)
    latitude_longitude = re.findall(r'@(.*)data',url_str)
    if len(latitude_longitude):
        lat_lng_list = latitude_longitude[0].split(",")
        if len(lat_lng_list)>=2:
            latitude = lat_lng_list[0]
            longitude = lat_lng_list[1]
        print("Latitude = {}, Longitude = {}".format(latitude, longitude))

except Exception as e:
        print("Error: ", str(e))


# # question 6 . Write a program to scrap all the available details of best gaming laptops from digit.in.

# In[234]:


driver = webdriver.Chrome()
url = "https://www.digit.in/"
driver.get(url)
time.sleep(2)


# In[235]:


best_gam_laptops = driver.find_element(By.XPATH,"//div[@class='listing_container']//ul//li[9]").click()
time.sleep(4)


# In[236]:



Laptop_Name = []
Operating_sys = []
Display = []
Processor = []
Memory = []
Weight = []
Dimensions = []
Graph_proc = []
Price = []


# In[237]:


laptop_name= driver.find_elements(By.XPATH,'//span[@class="datahreflink"]')
for name in laptop_name:
    Laptop_Name.append(name.text)


# In[238]:


try:
    op_sys = driver.find_elements(By.XPATH,"//div[@class='Spcs-details'][1]/table/tbody/tr[5]/td[3]")
    for os in op_sys:
        Operating_sys.append(os.text)
except NoSuchElementException:
    pass


try:
    display= driver.find_elements(By.XPATH,"//div[@class='product-detail']/div/ul/li[2]/div/div")
    for disp in display:
        Display.append(disp.text)
except NoSuchElementException:
    
    pass

try:
    processor = driver.find_elements(By.XPATH,"//div[@class='Spcs-details'][1]/table/tbody/tr[5]/td[3]")
    for pro in processor:
        Processor.append(pro.text)
except NoSuchElementException:
    pass

try:
    memory = driver.find_elements(By.XPATH,"//div[@class='Spcs-details'][1]/table/tbody/tr[6]/td[3]")
    for memo in memory:
        Memory.append(memo.text)
except NoSuchElementException:
    pass

try:
    weight = driver.find_elements(By.XPATH,"//div[@class='Spcs-details'][1]/table/tbody/tr[7]/td[3]")
    for wgt in weight:
        Weight.append(wgt.text)
except NoSuchElementException:
    pass

try:
    dimension = driver.find_elements(By.XPATH,"//div[@class='Spcs-details'][1]/table/tbody/tr[8]/td[3]")
    for dim in dimension:
        Dimensions.append(dim.text)
except NoSuchElementException:
    pass

try:
    graph = driver.find_elements(By.XPATH,"//div[@class='Spcs-details'][1]/table/tbody/tr[9]/td[3]")
    for gra in graph:
        Graph_proc.append(gra.text)
except NoSuchElementException:
    pass

try:
    price = driver.find_elements(By.XPATH,"//td[@class='smprice']")
    for pri in price:
        Price.append(pri.text.replace('₹','Rs '))
except NoSuchElementException:
    pass


# In[239]:


Laptop_Names=Laptop_Name[0:7]
print(Laptop_Names)


# In[240]:


print(len(Laptop_Names),len(Operating_sys),len(Display),len(Processor),len(Memory),len(Weight),len(Dimensions),len(Price))


# In[241]:


df=pd.DataFrame({"Laptop_Name":Laptop_Names,"Operating_System":Operating_sys,"'Display":Display,"Processor":Processor,'Memory':Memory,'Weight':Weight,'Price':Price})
df


# # 7. Write a python program to scrape the details for all billionaires from www.forbes.com. Details to be scrapped: 
# “Rank”, “Name”, “Net worth”, “Age”, “Citizenship”, “Source”, “Industry”. 

# In[ ]:


driver = webdriver.Chrome()


# In[164]:


driver.get('https://www.forbes.com/')


# In[165]:


bnt = driver.find_element(By.XPATH,'//div[@class="_69hVhdY4"]')
bnt.click()


# In[167]:


bill = driver.find_element(By.XPATH,'/html/body/div[1]/header/nav/div[1]/div[1]/div/div[2]/ul/li[2]/div[1]')
bill.click()


# In[168]:


world = driver.find_element(By.XPATH,'/html/body/div[1]/header/nav/div[1]/div[1]/div/div[2]/ul/li[2]/div[2]/div[3]/ul/li[1]')
world.click()


# In[169]:


Rank = []
Name = []
total_net_worth = []
Age = []
citizenship = []
Source = []
industry = []


# In[180]:


while(True):

#Scraping the data of rank of the billionaires
    rank_tags= driver.find_elements(By.XPATH,'//div[@class="Table_rank___YBhk Table_dataCell__2QCve"]')
    for rank in rank_tags:
        Rank.append(rank.text)
    time.sleep(1)
    
    
    #Scraping the data of names of the billionaires
    name_tags= driver.find_elements(By.XPATH,'//div[@class="Table_dataCell__2QCve"]')
    for name in name_tags[1::5]:
        Name.append(name.text)
    time.sleep(1)
    
    
    #Scraping data of age of the billionaires
    age_tags= driver.find_elements(By.XPATH,"//div[@class='age']/div")
    for age in age_tags:
        Age.append(age.text)   
    time.sleep(1)
    
    
    #Scraping data of citizenship of the billionaires
    cit_tags= driver.find_elements(By.XPATH,"//div[@class='countryOfCitizenship']")
    for cit in cit_tags:
        citizenship.append(cit.text)
    time.sleep(1)
    
    
    #Scraping data of source of income of the billionaires
    sour_tags= driver.find_elements(By.XPATH,"//div[@class='source']")
    for sour in sour_tags:
        Source.append(sour.text)    
    time.sleep(1)
    
     #Scraping data of Industry of the billionaires
    ind_tags= driver.find_elements(By.XPATH,"//div[@class='category']//div")
    for ind in ind_tags:
        industry.append(ind.text)
        
        
    #scraping data of net_worth of billionaires
    net_tags= driver.find_elements(By.XPATH,'//div[@class="Table_netWorth___L4R5 Table_dataCell__2QCve"]')
    for net in net_tags:
        total_net_worth.append(net.text)
    time.sleep(1)
    
    
    #Clicking on next button
    try:
        next_button = driver.find_element(By.XPATH,"//button[@class='pagination-btn pagination-btn--next ']")
        next_button.click()
    except:
        break
        
#Scraping data of net worth
Net_Worth = []
for i in range(0,len(total_net_worth),2):
    Net_Worth.append(total_net_worth[i])


# In[181]:


print(Name)


# In[138]:


print(total_net_worth)


# In[184]:


Name


# In[ ]:





# In[ ]:





# In[ ]:





# # que 8 Write a program to extract at least 500 Comments, Comment upvote and time when comment was posted from any YouTube Video.

# In[4]:


driver = webdriver.Chrome()
url = "https://www.youtube.com/"
driver.get(url)
time.sleep(2)


# In[7]:


url="https://www.youtube.com/watch?v=f_vbAtFSEc0"
driver.get(url)


# In[6]:


#scroll the webpage

i=0
while(i<100):
    driver.execute_script("window.scrollBy(0,5000)") # scroll down to get more comments
    i+=1
while(i<402):
    driver.execute_script("window.scrollBy(0,10000)") # scroll down to get more comments
    i+=1


# In[9]:


#fetch comments tag

com_tags=driver.find_elements(By.XPATH,'//yt-formatted-string[@id="content-text"]')

comments=[]

for i in com_tags:
    comments.append(i.text)
len(comments)


# In[11]:


comments_yt=comments[0:500]
comments_yt


# In[12]:


upvote_tags=driver.find_elements(By.XPATH,'//span[@id="vote-count-middle"]')

upvotes=[]

for i in upvote_tags:
    try:
        upvotes.append(i.text)
    except:
        upvotes.append('---')
len(upvotes)


# In[13]:


upvotes_yt=upvotes[0:500]
len(upvotes_yt)


# In[14]:


print(upvotes_yt)


# In[15]:


ago_tags=driver.find_elements(By.XPATH,'//a[@class="yt-simple-endpoint style-scope yt-formatted-string"]')

ago=[]

for i in ago_tags:
    try:
        ago.append(i.text)
    except:
        ago.append('---')
len(ago)


# In[17]:


time_ago=ago[7:507]
time_ago


# In[18]:


df=pd.DataFrame({"comments":comments_yt,"comments_like":upvotes_yt,"time_ago":time_ago,})
df


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




