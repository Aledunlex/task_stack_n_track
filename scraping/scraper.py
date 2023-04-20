from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

from model.element import Element, Quest


class Scraper(ABC):
    def __init__(self, element_class):
        self.element_class = element_class

    @abstractmethod
    def parse_elements_from(self) -> list[dict]:
        pass

    def get_element_instances_from(self, url) -> list[Element]:
        all_data = self.get_element_instances_from(url)

        all_elements = []
        for data in all_data:
            element = self.element_class(**data)
            all_elements.append(element)

        return all_elements


class QuestScraper(Scraper):
    def __init__(self):
        super().__init__(Quest)

    def parse_elements_from(self) -> list[dict]:
        url = 'https://www.jeuxvideo.com/wikis-soluce-astuces/1716911/quetes-annexes.htm'

        all_data = []
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for li in soup.select('ul.liste-default-jv li'):
            region_url = li.find('a')['href']
            region = li.text \
                .replace('Quêtes annexes d\'', '') \
                .replace('Quêtes annexes des ', '') \
                .replace('Quêtes annexes de ', '') \
                .replace(' ', '_').replace('-', '_') \
                .strip()

            region_response = requests.get(region_url)
            region_soup = BeautifulSoup(region_response.text, 'html.parser')

            for h2 in region_soup.find_all('h2', class_='h2-default-jv'):
                title = h2.text.strip()
                # reward is the next p tag after the h2 that starts with "Récompense", but it's not always present
                reward = ''
                for p in h2.find_next_siblings('p'):
                    if p.text.startswith('Récompense'):
                        reward = p.text
                        break
                # if there is a reward, solution is the p tag after that, otherwise it's the p tag immediately after the h2
                if reward:
                    solution = h2.find_next_sibling('p').find_next_sibling('p').text.strip()
                else:
                    solution = h2.find_next_sibling('p').text.strip()

                # Create a dictionary with the retrieved data
                data_dic = {
                    'category': region,
                    'title': title,
                    'reward': reward,
                    'solution': solution,
                }

                all_data.append(data_dic)

        return all_data
