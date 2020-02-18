from scripts.BsHelper import BsHelper
from scripts.BsParser import BsParser
from scripts.utils import Utils
import pandas as pd
import os

email = input("Enter linkedin email: ")
password = input("Enter linkedin password: ")

connectMessage = "Hi {}, I want to connect with you."

# Login to browser
bsHelper = BsHelper("chromedriver.exe")
bsHelper.loginLinkedin(email, password)
bsParser = BsParser()
utils = Utils()

# Change according to your requirements. For 1 page you get 10 results.
URL_TO_SEARCH = "https://www.linkedin.com/search/results/people/?keywords=data%20science%20job&origin=SWITCH_SEARCH_VERTICAL"
noOfPages = 100
DATA_DIR = "data"
CSV_DIR = "csv"
CSV_NAME = "accounts.csv"
# Here we have set no of pages 1. For hundered profiles set number of pages 10

def createDir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def searchAndSave(URL_TO_SEARCH, noOfPages):
    # Search profiles
    createDir(CSV_DIR)
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
        print("Saved to {}".format(os.path.join(CSV_DIR, CSV_NAME)))
        df.to_csv(os.path.join(CSV_DIR, CSV_NAME), index=None)
    except:
        print("[INFO] - Error Saving CSV file")


def processUrl(url):
    global connectMessage
    fileName = os.path.join(DATA_DIR, url.split("/")[-2] + ".json")
    soup = bsHelper.getProfilePage(url, connectMessage)
    profile = bsParser.parseProfile(soup)

    utils.saveJson(fileName, profile)
    print("Saved to: ", fileName)

def processFile():
    createDir(DATA_DIR)
    data = pd.read_csv(os.path.join(CSV_DIR, CSV_NAME))
    for row in data.iterrows():
        url = row[1]["url"]
        fileName = url.split("/")[-2]
        
        if not os.path.exists(fileName):
            print("Processing:", fileName)
            processUrl(url)


# Search for profiles
searchAndSave(URL_TO_SEARCH, noOfPages)

# Process file
processFile()