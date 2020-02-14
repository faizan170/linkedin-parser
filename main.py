from scripts.BsHelper import BsHelper
from scripts.BsParser import BsParser
from scripts.utils import Utils
import pandas as pd
import os

email = input("Enter linkedin email: ")
password = input("Enter linkedin password: ")

# Login to browser
bsHelper = BsHelper("chromedriver.exe")
bsHelper.loginLinkedin(email, password)
bsParser = BsParser()
utils = Utils()


# Here we have set no of pages 1. For hundered profiles set number of pages 10

def searchAndSave():
    # Search profiles
    URL_TO_SEARCH = "https://www.linkedin.com/search/results/people/?keywords=data%20science%20job&origin=SWITCH_SEARCH_VERTICAL"
    noOfPages = 1
    data = []
    for i in range(1,noOfPages + 1):
        print("Processing:", i)
        url = URL_TO_SEARCH
        if i > 1:
            url = url + "&page={}".format(i)
        searchSoup = bsHelper.getProfileSearch(URL_TO_SEARCH)
        results = bsParser.processSearchResults(searchSoup)
        for v in results:
            data.append(v)

    df = pd.DataFrame(data, columns=["name", "url", "connection"])
    df.to_csv("csv/accounts.csv", index=None)


def processUrl(url):
    fileName = "data/" + url.split("/")[-2] + ".json"
    soup = bsHelper.getProfilePage(url)
    profile = bsParser.parseProfile(soup)

    utils.saveJson(fileName, profile)
    print("Saved to: ", fileName)

def processFile():
    data = pd.read_csv("csv/accounts.csv")
    for row in data.iterrows():
        url = row[1]["url"]
        fileName = "data/" + url.split("/")[-2] + ".json"
        
        if not os.path.exists(fileName):
            print("Processing:", fileName)
            processUrl(url)


try:
    searchAndSave()
    processFile()
except:
    pass