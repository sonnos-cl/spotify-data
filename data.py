import os
import csv
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver.v2 as uc
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

SPOTYCHARTS_URL = 'https://spotifycharts.com/regional/cl/daily/%s'

chrome_driver = os.getcwd() +"/chromedriver"

year = "2021"

first_date = '10-05-2021'
last_date = '02-06-2021'

data_begins = datetime.strptime(first_date, "%d-%m-%Y")
data_ends = datetime.strptime(last_date, "%d-%m-%Y")


days = 0
current_date = data_begins



options = uc.ChromeOptions()
options.headless=True

options.add_argument('--headless')
   	
driver = uc.Chrome(options=options,executable_path=chrome_driver)

while current_date < data_ends:
      
    current_date =  data_begins + timedelta(days=days)
    string_date = current_date.strftime("%Y-%m-%d")
    print(string_date)

    url = SPOTYCHARTS_URL % string_date


    with driver:
        
        driver.get(url)

        try:
            table  = driver.find_element_by_class_name('chart-table')
            html = table.get_attribute('outerHTML')
            soup = BeautifulSoup(html, "html.parser")
            table = soup.find("table", {"class":"chart-table"})
            files =  table.find("tbody").findAll("tr")

            with open(year + '/' + string_date + '.csv', 'w',newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
                writer.writerow(['artist','song_name','song_id','streams','date'])
                for tr in files:
                    artist= tr.find("td", {"class": "chart-table-track"}).find("span").text.replace("by ","").strip()
                    song_name = tr.find("td", {"class": "chart-table-track"}).find("strong").text
                    song_id = tr.find("td", {"class": "chart-table-image"}).find("a").get("href").split("track/")[1]
                    streams = tr.find("td", {"class": "chart-table-streams"}).text
                    writer.writerow([artist,song_name,song_id,int(streams.replace(",","")),string_date])
                    #song = dict(artist=artist,song_name=song_name,song_id=song_id,streams=int(streams.replace(",","")), date=string_date)
                    #songs.append(song)
        except NoSuchElementException:
            print('No data for given date')
    days = days + 1




