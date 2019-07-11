import logging
import time


from collections import OrderedDict
import mechanicalsoup
from bs4 import BeautifulSoup
from typing import List

import constant
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from selenium.webdriver.chrome.options import Options
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor as PoolExecutor


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
    # options = Options()
    # options.headless = True
    # options.add_argument('--disable-extensions')
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--no-sandbox')
    # options.add_experimental_option(
    #     'prefs', {
    #         'download.default_directory': '/tmp',
    #         'download.prompt_for_download': False,
    #         'download.directory_upgrade': True,
    #         'safebrowsing.enabled': True
    #     }
    # )
    browser = webdriver.Remote(
        command_executor='http://phantomjs:8910',
        desired_capabilities=DesiredCapabilities.PHANTOMJS
        )

    #browser = webdriver.Chrome(options=options)
    browser.get(f'http://instagram.com/{username}')
    scroll = lambda : browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var page_height=document.body.scrollHeight;return page_height;")
    page_height = scroll()
    scrolled_to_end = False
    results = []
    while not scrolled_to_end:
        current_page_height = page_height 
        time.sleep(1)
        html = browser.page_source
        results += scrape_images_from_html(html)
        page_height = scroll()
        scrolled_to_end = current_page_height == page_height
    html = browser.page_source
    results += scrape_images_from_html(html)
    results = list(OrderedDict.fromkeys(results))
    
    start = time.time()
    with PoolExecutor(max_workers=30) as executor:
        futures = executor.map(lambda x : get_image(x), results)
        results = []
        for result in futures:
            results.append(result)
    end = time.time()
    print(f'pool = {end - start}')
    return results
    

def scrape_images_from_html(html: str) -> List[str]:
    ''' Get instagram profile's pictures from html '''
    results = []
    soup = BeautifulSoup(html, "html.parser")
    for div in soup.find_all('div', {'class': 'v1Nh3'}):
        a = div.find('a')
        results.append(f"{a['href'][3:-1]}")
    return results
