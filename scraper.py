#import requests
#youtube=requests.get(youtube_trending_url)
#youtube1=youtube.text
#print(youtube.status_code)
#print(len(youtube1))
#from bs4 import BeautifulSoup
#doc = BeautifulSoup(youtube1, 'html.parser')
youtube_trending_url='https://youtube.com/trending'
#response=requests.get(youtube_trending_url)
#with open('trending.html', 'w')as f:
 # f.write(response.text)

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def get_driver():
 chrome_options = Options()
 chrome_options.add_argument('--no-sandbox')
 chrome_options.add_argument('--headless')
 chrome_options.add_argument('--disable-dev-shm-usage')
 driver = webdriver.Chrome(options=chrome_options)
 return driver

def get_videos(driver):
 driver.get(youtube_trending_url)
 videos=driver.find_elements(By.TAG_NAME,'ytd-video-renderer')
 print(f'count {len(videos)} videos')
 return videos

def parse_video(video):
 title_tag=video.find_element(By.ID,'video-title')
 title=title_tag.text
 video_url=title_tag.get_attribute('href')
 thumbnail_tag=video.find_element(By.TAG_NAME,'img')
 thumbnail_url=thumbnail_tag.get_attribute('src')
 views=video.find_element(By.XPATH,'//*[@id="metadata-line"]/span[1]')
 views=views.text
 upload=video.find_element(By.XPATH,'//*[@id="metadata-line"]/span[2]')
 upload=upload.text
 return{
    'title':title,
    'video_url':video_url,
    'thumbnail_url':thumbnail_url,
    'views':views,
    'upload time':upload,
  }


if __name__=="__main__":
 print('creating driver: ')
 driver = get_driver()

 print('getting videos list')
 videos=get_videos(driver)

 print('parsing video')
 videos_data=[parse_video(video) for video in videos[:10]]

 videos_df=pd.DataFrame(videos_data)
 print(videos_df)
 videos_df.to_csv('trending.csv')

