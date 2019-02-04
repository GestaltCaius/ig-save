import mechanicalsoup
import logging

logging.basicConfig(filename='instagram_downloader.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)
import constant


def get_image(id: str) -> str:
    browser = mechanicalsoup.StatefulBrowser()
    url = '{}/{}/'.format(constant.INSTAGRAM_PHOTO_BASE_URL, id)

    logger.info('Get image from {}'.format(url))
    browser.open(url)
    img_url = browser.get_current_page().find(property="og:image")
    logger.info('Image url is {}'.format(img_url['content']))
    return img_url['content']
