import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

def extract_media_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    video_urls = []

    # Extract URLs from <video> tags
    for video in soup.find_all('video'):
        source = video.find('source')
        if source:
            video_urls.append(source['src'])
        else:
            video_urls.append(video['src'])

    # Extract URLs from <source> tags
    for source in soup.find_all('source'):
        video_urls.append(source['src'])

    # Extract URLs from <iframe> tags (for embedded videos like YouTube)
    for iframe in soup.find_all('iframe'):
        video_urls.append(iframe['src'])

    return video_urls

def extract_media_urls_dynamic(url):
    driver = webdriver.Chrome()  # Ensure you have the appropriate WebDriver for your browser
    driver.get(url)

    video_urls = []

    # Extract URLs from <video> tags
    videos = driver.find_elements(By.TAG_NAME, 'video')
    for video in videos:
        sources = video.find_elements(By.TAG_NAME, 'source')
        if sources:
            for source in sources:
                video_urls.append(source.get_attribute('src'))
        else:
            video_urls.append(video.get_attribute('src'))

    # Extract URLs from <iframe> tags
    iframes = driver.find_elements(By.TAG_NAME, 'iframe')
    for iframe in iframes:
        video_urls.append(iframe.get_attribute('src'))

    driver.quit()
    return video_urls
