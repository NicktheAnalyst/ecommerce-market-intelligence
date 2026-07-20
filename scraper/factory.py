from scraper.registry import SCRAPERS


class ScraperFactory:

    @staticmethod
    def get_scrapers():
        return [scraper() for scraper in SCRAPERS]