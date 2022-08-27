## importing libraries
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import re as re
from datetime import datetime

## Linkedin ID and PASSWORD
email = "enter details when run"
password = "enter details when run"

## Write here the job position and local for search
position = "Data Engineer"

geoId_dict = {"Germany" : "101282230", "Japan":"101355337","Singapore":"102454443", "United Kingdom":"101165590",
"China":"102890883"} # germany 
# 101355337 japan
# 102454443 singapore 
# 101165590 united kingdom 
# 102890883 china 

## formating to linkedin model
position = position.replace(' ', "%20")
  
# instance of Options class allows
# us to configure Headless Chrome
options = Options()
  
# this parameter tells Chrome that
# it should be run without UI (Headless)
# options.add_argument("--incognito")
options.headless = True
  
## Open browser
driver_path = "/Users/andrewsmith/Downloads/chromedriver"
# initializing webdriver for Chrome with our options
driver = webdriver.Chrome(executable_path=driver_path, options=options)
#Maximizing browser window to avoid hidden elements
driver.set_window_size(1024, 600)
driver.maximize_window()

## Opening linkedin website
driver.get('https://www.linkedin.com/login')
## waiting load
time.sleep(2)

## Search for login and password inputs, send credentions 
driver.find_element_by_id('username').send_keys(email)
driver.find_element_by_id('password').send_keys(password)
driver.find_element_by_id('password').send_keys(Keys.RETURN)

    
def scrape_and_generate_csv(key, value):
    ## Opening jobs webpage
    driver.get(f"https://www.linkedin.com/jobs/search/?f_E=2&geoId={value}&keywords={position}")
    ## waiting load
    time.sleep(2)

    list_of_job_data = []
    ## linkedin show us 40 jobs pages, then the line below will repeat 40 times
    for i in range(1,41):
        try:
            ## click button to change the job list
            if (i > 1): 
                driver.get(f"https://www.linkedin.com/jobs/search/?f_E=2&geoId={value}&keywords={position}&start={(i-1) * 25}")
            # act more human! 
            time.sleep(3)
            ## each page show us some jobs, sometimes show 25, others 13 or 21 ¯\_(ツ)_/¯
            jobs_lists = driver.find_element_by_class_name('jobs-search-results__list') #here we create a list with jobs
            jobs = jobs_lists.find_elements_by_class_name('jobs-search-results__list-item')#here we select each job to count
            ## waiting load
            time.sleep(1) 
            ## the loop below is for the algorithm to click exactly on the number of jobs that is showing in list
            ## in order to avoid errors that will stop the automation
            for job in range (1, len(jobs)+1):
                ## job click
                try:
                    driver.find_element_by_xpath(f'/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li[{job}]/div/div[1]/div[1]/div[1]/a').click()                                            
                    # Be more like a human, be respectful
                    time.sleep(2)                      

                    ## select job description
                    job_desc = driver.find_element_by_class_name('jobs-search__right-rail')
                    #get text
                    soup = BeautifulSoup(job_desc.get_attribute('outerHTML'), 'html.parser')
                    ## add text to list

                    title = soup.find('h2').text
                    company_name = soup.find('span', attrs={'class' : 'jobs-unified-top-card__company-name'}).find('a').text
                    location = soup.find('span', attrs={'class' : 'jobs-unified-top-card__bullet'}).text
                    work_type = soup.find('span', attrs={'class' : 'jobs-unified-top-card__workplace-type'}).text
                    html_job_description = soup.find('div', attrs={'class' : 'jobs-description__content jobs-description-content'}).find('div').find('span')
                    job_description = re.sub('<li>|<\/li>|<ul>|<\/ul>|<p>|<\/p>|<strong>|<\/strong>|<br\/>|<!-- -->|\\n|<u>|<\/u>|<i>|<\/i>|<span>|<\/span>|(\\s\\s)+|(\\s\\s\\s)+', '', html_job_description.prettify())

                    list_of_job_data.append({'Title': title, 'Company Name' : company_name, 'Location': location, 'Work Type': work_type, 'Description': job_description})
            
                except:
                    continue
        except:
             continue

    df = pd.DataFrame(list_of_job_data, columns=['Title', 'Company Name', 'Location', 'Work Type', 'Description'])
    df.to_csv("LinkedIn_DataScience_{0}.csv".format(key))

for key, value in geoId_dict.items():
    scrape_and_generate_csv(key, value)