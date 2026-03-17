from abc import ABC, abstractmethod
from typing import List, Dict
import httpx
from bs4 import BeautifulSoup

class BaseScraper(ABC):
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    @abstractmethod
    async def scrape(self, search_term: str) -> List[Dict]:
        """
        Executa o scraping e retorna uma lista de dicionários com as vagas.
        """
        pass

    async def fetch_page(self, url: str) -> str:
        async with httpx.AsyncClient(headers=self.headers) as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            return response.text
