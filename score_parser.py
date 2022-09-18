import logging


from bs4 import BeautifulSoup
import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("sp")


class ClientScore:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
            "Accept-Language": "ru"
        }

        self.score = []

    def load_page(self):
        url = "https://www.sports.ru/rfpl/calendar/"
        res = self.session.get(url=url)
        res.raise_for_status()
        return res.text

    def parse_page(self, text: str):
        soup = BeautifulSoup(text, "lxml")
        container = soup.find("div", class_="mainPart columns-layout__main js-active").find_all('a', class_="score")
        for block in container:
            self.score.append(self.parse_block(block=block))

    def parse_block(self, block):
        url_block = block.find('noindex')
        if not url_block:
            logger.error('no url_block')
            return
        score_name = url_block.get_text()
        return score_name

    def run(self):
        text = self.load_page()
        self.parse_page(text=text)
        return self.score


