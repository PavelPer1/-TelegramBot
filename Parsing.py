import logging


from bs4 import BeautifulSoup
import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("sp")


class Client:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
            "Accept-Language": "ru"
        }
        self.date_1 = []
        self.teams_1 = []
        self.teams_date = []

    def load_page(self):
        url = "https://www.sports.ru/rfpl/calendar/"
        res = self.session.get(url=url)
        res.raise_for_status()
        return res.text

    def parse_page(self, text: str):
        soup = BeautifulSoup(text, "lxml")
        container = soup.find("div", class_="mainPart columns-layout__main js-active").find_all('tr')
        container_1 = soup.find("div", class_="mainPart columns-layout__main js-active").find_all('div', class_="rel")
        for teams in container_1:
            self.teams_1.append(self.pars_teams(teams=teams))
        for block in container:
            self.date_1.append(self.parse_block(block=block))

    def parse_block(self, block):
        url_block = block.find('a')
        if not url_block:
            logger.error('no url_block')
            return
        date = url_block.get_text()
        return date[1::]

    def pars_teams(self, teams):
        teams_name = teams.find('a', class_="player")
        if not teams_name:
            logger.error('no teams_name')
            return
        teams_nam = teams_name.get_text()
        return teams_nam

    def run(self):
        text = self.load_page()
        self.parse_page(text=text)
        for i in range(0, len(self.teams_1), 2):
            self.teams_date.append(f'{self.teams_1[i]} VS {self.teams_1[i + 1]}')
        self.date_1 = [x for x in self.date_1 if x is not None]
        for j in range(0, len(self.teams_date)):
            self.teams_date[j] = [f'{self.teams_date[j]} Дата: {self.date_1[j]}']
        return self.teams_date



