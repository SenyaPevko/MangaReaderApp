from scrappers import Manganelo
SCRAPPERS = {"Manganelo": Manganelo}


def get_scrapper(name):
    return SCRAPPERS.get(name)

def get_scrappers_names():
    return SCRAPPERS.keys()