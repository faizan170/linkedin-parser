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

# Change according to your requirements. For 1 page you get 10 results.
URL_TO_SEARCH = "https://www.linkedin.com/search/results/people/?keywords=data%20science%20job&origin=SWITCH_SEARCH_VERTICAL"
noOfPages = 3
    
# Here we have set no of pages 1. For hundered profiles set number of pages 10

def searchAndSave(URL_TO_SEARCH, noOfPages):
    # Search profiles
    data = []
    for i in range(1,noOfPages + 1):
        try:
            print("Processing Page:", i)
            url = URL_TO_SEARCH
            if i > 1:
                url = url + "&page={}".format(i)
            searchSoup = bsHelper.getProfileSearch(url)
            results = bsParser.processSearchResults(searchSoup)
            for v in results:
                data.append(v)
        except:
            print("Error fetching data")
    
    df = pd.DataFrame(data, columns=["name", "url", "connection"])
    print("[INFO] - Current data shape", df.shape)
    try:
        print("Saved to csv/accounts.csv")
        df.to_csv("csv/accounts.csv", index=None)
    except:
        print("[INFO] - Error Saving CSV file")


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
            print("Processing:", fileName.split("/")[1])
            processUrl(url)


# Search for profiles
searchAndSave(URL_TO_SEARCH, noOfPages)

# Process file
processFile()


