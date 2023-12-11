from scrappers import Manganelo
SCRAPPERS = {"Manganelo": Manganelo}


def get_scrapper(name):
    return SCRAPPERS.get(name)