import logging
import time
from dataclasses import dataclass, asdict

from collections import OrderedDict
import mechanicalsoup
from bs4 import BeautifulSoup
from typing import List, Dict

import constant
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import concurrent.futures

@dataclass(frozen=True, eq=True)
class InstagramImage:
    url: str # Link to instagram photo page
    preview: str # Image preview link (small size)


def get_image(id: str) -> str:
    browser = mechanicalsoup.StatefulBrowser()
    url = f'{constant.INSTAGRAM_PHOTO_BASE_URL}/{id}/'
    logger = logging.getLogger(__name__)
    logger.info('Get image from {}'.format(url))
    browser.open(url)
    img_url = browser.get_current_page().find(property="og:image")
    logger.info('Image url is {}'.format(img_url['content']))
    return img_url['content']


def get_images(username: str) -> List[str]:
    ''' get images from instagram profile '''


    options = Options()
    options.headless = True
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(chrome_options=options)
    # browser = webdriver.PhantomJS()
    browser.get(f'https://instagram.com/{username}')
    scroll = lambda : browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var page_height=document.body.scrollHeight;return page_height;")
    page_height = scroll()
    scrolled_to_end = False
    results = []
    while not scrolled_to_end:
        current_page_height = page_height
        html = browser.page_source
        results += scrape_images_from_html(html)
        time.sleep(1)
        page_height = scroll()
        scrolled_to_end = current_page_height == page_height
    # results = list(OrderedDict.fromkeys(results))
    
    return results
    
def parse_instagram_image(div) -> Dict:
    a = div.find('a')['href'][3:-1]
    img = div.find('img', {'class': 'FFVAD'})['src']
    return InstagramImage(url=a, preview=img).__dict__

def scrape_images_from_html(html: str) -> List[str]:
    ''' Get instagram profile's pictures from html '''
    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find_all('div', {'class': 'v1Nh3'})
    with PoolExecutor() as executor:
        futures = executor.map(parse_instagram_image, divs)
        results = [result for result in futures]
        # results = []
        # for result in futures:
        #     results.append(result)
    return results
