from django.shortcuts import render
from django.template.loader import render_to_string

import time 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as BSoup

# Create your views here.

class Winning:
    path = "http://winningstrategy.co.uk/table/free_matchodds.php"
    timeout = 10
    def __init__(self):
        chrome_options = Options()
#        chrome_options.add_argument("--headless") 
        prefs = {'profile.managed_default_content_settings.images':2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_path = r"chromedriver.exe"
        self.driver = webdriver.Chrome(chrome_path,chrome_options=chrome_options)
        self.value_list = {'888sport':41,'bet365':56,'betclic':4,'betafairsportbook':8,'betstars':54,'betway':34,'netbet':36,'unibet':40,'williamhill':29}
        self.data_list = []

    def get_data(self):
        self.driver.get(self.path)
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME,"layAvail"))
            WebDriverWait(self.driver, self.timeout).until(element_present)
            time.sleep(3)
            country_input = self.driver.find_element_by_id("bookienameselect")
            options = country_input.find_elements_by_tag_name("option")
            sel = Select(self.driver.find_element_by_id("bookienameselect"))
            sel.select_by_value("56")
            time.sleep(2)

            bs_obj = BSoup(self.driver.page_source, 'html.parser')
            table = bs_obj.find_all('table',{'id':'tableBase'})[0]
            tbody = table.find_all('tbody')[0]
            trs = tbody.find_all('tr')
            count = 1
            for tr in trs:
                event_time = tr.find_all('td',{'class','eventTime'})[0].text

                event_name = tr.find_all('td',{'class','eventName'})[0].text
                bet = tr.find_all('td',{'class','outcome'})[0].text
                market_type = tr.find_all('td',{'class','oddsName'})[0].text
                rating = tr.find_all('td',{'class','rating'})[0].text
                book = tr.find_all('td',{'class','bookString'})[0]
                bookmaker = book.find_all('img')[0]['alt']
                backOdds = tr.find_all('td',{'class','backOdds'})[0].text

                exString = tr.find_all('td',{'class','exString'})[0].text
                layOdds = tr.find_all('td',{'class','layOdds'})[0].text
                layAvail = tr.find_all('td',{'class','layAvail'})[0].text

                temp = {}
                
                temp['count'] = count
                temp['event_time'] = event_time
                temp['event_name']= event_name
                temp['bet'] = bet
                temp['market_type'] = market_type
                temp['rating'] = rating
                temp['bookmaker'] = bookmaker
                temp['backOdds'] = backOdds
#                temp.append(exString)
                temp['layOdds'] = layOdds
                temp['layAvail'] = layAvail
                self.data_list.append(temp)
                count +=1
                print(temp)
        except TimeoutException:
            print("timeout!")
        return self.data_list


def index(request):
    scraper = Winning()
    scrape_data = scraper.get_data()

    return render(request, 'index.html',{'odds_list'scrape_data})
