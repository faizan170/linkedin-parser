import requests, time, random
from bs4 import BeautifulSoup
from selenium import webdriver
from win32api import GetSystemMetrics


class BsHelper():
    def __init__(self, path):
        self.browser = webdriver.Chrome(path)
        self.browser.set_window_size(GetSystemMetrics(0), GetSystemMetrics(1))
        self.seeMoreView = False


    def perfromClick(self, data):
        '''
            Perform click on an element
        '''
        try:
            button = self.browser.find_element_by_xpath(data)
            button.click()
            return True
        except:
            return False

    def scrollAndLoadContent(self):
        SCROLL_PAUSE_TIME = 5
        # Get scroll height
        totalHeight = self.browser.execute_script("return document.body.scrollHeight")
        for i in range(1,int(totalHeight/600)):
            # Scroll down to bottom
            self.browser.execute_script("window.scrollTo({}, {});".format(0, 700 * i))

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            
        time.sleep(5)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        try:
            self.seeMoreView = True
            self.browser.execute_script('document.querySelectorAll(".lt-line-clamp__ellipsis:not(.lt-line-clamp__ellipsis--dummy) .lt-line-clamp__more").forEach(el => el.click())')
        except:
            pass

    def scrollAndClick(self):
        SCROLL_PAUSE_TIME = 4
        # Get scroll height
        totalHeight = self.browser.execute_script("return document.body.scrollHeight")
        
        clicks = [False, False]
        data = ["//button[@class='pv-profile-section__card-action-bar pv-skills-section__additional-skills artdeco-container-card-action-bar artdeco-button artdeco-button--tertiary artdeco-button--3 artdeco-button--fluid']",
                "//button[@class='pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle link link-without-hover-state']",
               #"//button[@class='pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle link link-without-hover-state']",
               #"//button[@aria-controls='languages-expandable-content']",
               #"//button[@aria-controls='projects-expandable-content']"
               ]
        for i in range(1,int(totalHeight/600)):
            # Scroll down to bottom
            self.browser.execute_script("window.scrollTo({}, {});".format((700*i) - 700, 700 * i))
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            for i in range(len(data)):
                if clicks[i] == False:
                    clicks[i] = self.perfromClick(data[i])
            if clicks.count(True) == len(clicks):
                break
        time.sleep(5)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        if self.seeMoreView == False:
            try:
                self.browser.execute_script('document.querySelectorAll(".lt-line-clamp__ellipsis:not(.lt-line-clamp__ellipsis--dummy) .lt-line-clamp__more").forEach(el => el.click())')
            except:
                pass



    def loginLinkedin(self, email, password):
        self.browser.get('https://www.linkedin.com/uas/login')


        elementID = self.browser.find_element_by_id('username')
        elementID.send_keys(email)

        elementID = self.browser.find_element_by_id('password')
        elementID.send_keys(password)

        elementID.submit()


    def getProfileSearch(self, link):
        '''
            Perform search on given url and return beautiful soup object
        '''
        try:
            self.browser.get(link)
        except:
            print("\t>>> Cannot get browser link")
        
        try:
            SCROLL_PAUSE_TIME = 5
            for i in range(1,5):
                # Scroll down to bottom
                self.browser.execute_script("window.scrollTo(0, {});".format(400 * i))

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)
        except:
            print("\t>>> Cannot scroll")
        try:
            src = self.browser.page_source
            soup = BeautifulSoup(src, 'lxml')
        except:
            print("\t>>> Cannot get source file")
        return soup


    def sendConnectionRequest(self, message):
        connectClick = False
        time.sleep(1)
        try:
            button = self.browser.find_element_by_xpath("//button[@class='pv-s-profile-actions pv-s-profile-actions--connect ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")
            button.click()
            connectClick = True
        except:
            pass

        FormSend = False
        if connectClick == True:
            time.sleep(3)
            try:
                button = self.browser.find_element_by_xpath("//button[@class='mr1 artdeco-button artdeco-button--muted artdeco-button--3 artdeco-button--secondary ember-view']")
                button.click()
                FormSend = True
                print("Going into form")
            except:
                button = self.browser.find_element_by_xpath("//button[@class='ml1 artdeco-button artdeco-button--3 artdeco-button--primary ember-view']")
                button.click()
                print("Going other way")
        if FormSend == True:
            time.sleep(3)
            try:
                browser.execute_script("arguments[0].value = arguments[1]", browser.find_element_by_id("custom-message"), message)
                time.sleep(3)
                button = browser.find_element_by_xpath("//button[@class='ml1 artdeco-button artdeco-button--3 artdeco-button--primary ember-view']")
                button.click()
                print("Success")
            except:
                print("Already connect")

    def getProfilePage(self, link, message):
        try:
            self.browser.get(link)
            self.scrollAndLoadContent()
            self.scrollAndClick()
            src = self.browser.page_source
            soup = BeautifulSoup(src, 'lxml')
            try:
                name_div = soup.find('div', {'class': 'flex-1 mr5'})
                name_loc = name_div.find_all('ul')
                name = name_loc[0].find('li').get_text().strip()
                message = message.format(name)
            except:
                message = "Hi, I want to connect with you."

            # Sending connection request
            try:
                self.sendConnectionRequest(message)
            except:
                pass
            return soup
        except:
            print("[INFO] - Error getting soup")
