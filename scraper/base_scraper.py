from abc import ABC, abstractmethod
from playwright.sync_api import sync_playwright


class BaseScraper(ABC):
    def __init__(self, headless=True):
        self.headless = headless

    def start(self):
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=self.headless
        )

        self.page = self.browser.new_page()

    def stop(self):
        self.browser.close()
        self.playwright.stop()

    @abstractmethod
    def scrape(self):
        """Return a list of ProductRecord objects."""
        pass