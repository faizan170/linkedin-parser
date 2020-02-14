class BsParser():
    def __init__(self):
        pass

    def getBasicUserDetails(self, name_div):
        '''
            Get user basic details such as name, location, title and connections
        '''
        userCompleteData = {}
        name_loc = name_div.find_all('ul')
        name = name_loc[0].find('li').get_text().strip()
        userCompleteData["name"] = name

        # Get location
        loc = name_loc[1].find('li').get_text().strip()
        userCompleteData["loc"] = loc

        # Profile title
        profile_title = name_div.find('h2').get_text().strip()
        userCompleteData["profileTitle"] = profile_title    

        # Connections
        connection = name_loc[1].find_all('li')
        connection = connection[1].get_text().strip()
        userCompleteData["connections"] = connection

        return userCompleteData

    def getAboutSection(self, soup):
        '''
            Get user about details
        '''
        userAbout = soup.find("p", {"class" : "pv-about__summary-text mt4 t-14 ember-view"})
        if userAbout != None:
            return userAbout.text
        else:
            return None

    def getExperienceDetails(self, exp_section):
        '''
            Get user experience section
        '''
        exp = exp_section.find("ul")
        if exp == None:
            return None
        listExp = exp.findAll("li", {"class" : "pv-entity__position-group-pager pv-profile-section__list-item ember-view"})
        if len(listExp) == 0:
            return None
        experience = []
        for exp in listExp:
            multiRole = exp.find("div", {"class" : "pv-entity__company-summary-info"})
            if multiRole != None:
                singleExp = {}
                company = multiRole.find("h3", {"class": "t-16 t-black t-bold"})
                if company != None:
                    singleExp["company"] = company.findAll("span")[1].text
                duration = multiRole.find("h4", {"class" : "t-14 t-black t-normal"})
                if duration != None:
                    singleExp["duration"] = duration.findAll("span")[1].text
            
                roles = []
                # Roles
                if exp.find("ul") != None:
                    for singleRole in exp.findAll("li", {"class" : "pv-entity__position-group-role-item"}):
                        roleDict = {}
                        #data = singleRole.find("div", {"class" : "pv-entity__summary-info-v2 pv-entity__summary-info--background-section pv-entity__summary-info-margin-top mb2"})

                        try:
                            roleDict["role"] = singleRole.find("h3", {"class" : "t-14 t-black t-bold"}).findAll("span")[1].text
                            roleDict["dateRange"] = singleRole.find("h4", {"class" : "pv-entity__date-range t-14 t-black--light t-normal"}).findAll("span")[1].text
                            roleDict["duration"] = singleRole.find("h4", {"class" : "t-14 t-black--light t-normal"}).findAll("span")[1].text
                            if singleRole.find("h4", {"class" : "pv-entity__location t-14 t-black--light t-normal block"}) != None:
                                roleDict["location"] = singleRole.find("h4", {"class" : "pv-entity__location t-14 t-black--light t-normal block"}).findAll("span")[1].text
                        
                        except:
                            continue
                        roles.append(roleDict)
                    singleExp["roles"] = roles

                experience.append(singleExp)
            else:
                singleExp = {"role" : exp.findAll("h3")[0].text}
                
                # Check company title
                company = exp.findAll("p", {"class": "pv-entity__secondary-title t-14 t-black t-normal"})
                if len(company) == 1:
                    singleExp["company"] = company[0].text
                
                typeJob = exp.findAll("p", {"class": "pv-entity__secondary-title t-14 t-black t-normal separator"})
                if len(typeJob) == 1:
                    singleExp["type"] = typeJob[0].text

                dateRange = exp.findAll("h4", {"class" : "pv-entity__date-range t-14 t-black--light t-normal"})
                singleExp["dateRange"] = dateRange[0].findAll("span")[1].text

                # Duration of work
                duration = exp.findAll("h4", {"class" : "t-14 t-black--light t-normal"})
                singleExp["duration"] = duration[0].findAll("span")[1].text

                # Location of company
                location = exp.findAll("h4", {"class" : "pv-entity__location t-14 t-black--light t-normal block"})
                if len(location) == 1:
                    singleExp["location"] = location[0].findAll("span")[1].text

                experience.append(singleExp)
        return experience

    def getEducationDetails(self, educationSection):
        '''
            Get user education details
        '''
        educationList = educationSection.findAll("ul")
        educationData = []
        if len(educationList) > 0:
            for edu in educationList[0].findAll("li"):
                data = {}
                # User institute
                data["institute"] = edu.findAll("h3", {"class" : "pv-entity__school-name t-16 t-black t-bold"})[0].text
                
                # Degree title. if exists
                title = edu.findAll("p", {"class" : "pv-entity__secondary-title pv-entity__degree-name t-14 t-black t-normal"})
                if len(title) == 1:
                    data["title"] = title[0].findAll("span")[1].text


                # Major area of study
                studyArea = edu.findAll("p", {"class" : "pv-entity__secondary-title pv-entity__fos t-14 t-black t-normal"})
                if len(studyArea) == 1:
                    data["studyArea"] = studyArea[0].findAll("span")[1].text
                # Marks
                marks = edu.findAll("p", {"class" : "pv-entity__secondary-title pv-entity__grade t-14 t-black t-normal"})
                if len(marks) == 1:
                    data["marks"] = marks[0].findAll("span")[1].text
                # Duration
                data["duration"] = edu.findAll("p", {"class" : "pv-entity__dates t-14 t-black--light t-normal"})[0].findAll("span")[1]
                data["duration"] = {"start" : data["duration"].findAll("time")[0].text, "end" : data["duration"].findAll("time")[1].text}
                educationData.append(data)
        return educationData

    def getCertifications(self, certificationsSection):
        if certificationsSection != None:
            certificationsList = certificationsSection.findAll("ul")
            if len(certificationsList) > 0:
                certificationsList = certificationsList[0].findAll("li")
            else:
                certificationsList = []
            print("Total Certifications:", len(certificationsList))
            
            certificationsData = []
            for cert in certificationsList:
                data = {}

                data["title"] = cert.findAll("h3", {"class" : "t-16 t-bold"})[0].text
                try:
                    otherData = cert.findAll("p", {"class" : "t-14"})
                    data["issuingCompany"] = otherData[0].findAll("span")[1].text
                except:
                    pass
                certificationsData.append(data)
            print("Total certifications found:", len(certificationsData))
            return certificationsData
        else:
            print("No certifications found")

    
    def getUserSkills(self, skills):
        mainSkills = skills.findAll("ol", {"class" : "pv-skill-categories-section__top-skills pv-profile-section__section-info section-info pb1"})
        mainSkills = mainSkills[0].findAll("li", {"class":"pv-skill-category-entity__top-skill pv-skill-category-entity pb3 pt4 pv-skill-endorsedSkill-entity relative ember-view"})
        
        userSkillsDetails = {}
        mainSkillsList = []
        for SingleSkill in mainSkills:
            skill = SingleSkill.find("span", {"class" : "pv-skill-category-entity__name-text t-16 t-black t-bold"})
            mainSkillsList.append(skill.text.replace("\n", "").strip())
        userSkillsDetails["mainSkills"] = mainSkillsList

        otherSkills = skills.find("div", {"class" : "pv-skill-categories-section__expanded"})
        otherSkillsMain = otherSkills.findAll("div", {"class" : "pv-skill-category-list pv-profile-section__section-info mb6 ember-view"})

        otherSkills = []
        for singleMain in otherSkillsMain:
            skillsListChild = []
            headingMain = singleMain.find("h3", {"class" : "pb2 t-16 t-black--light t-normal pv-skill-categories-section__secondary-skill-heading"}).text.replace("\n", "").strip()
            for singleSkill in singleMain.find("ol").findAll("li"):
                skillsListChild.append(singleSkill.find("span").text.strip())
                
            otherSkills.append({
                "tag" : headingMain,
                "skills" : skillsListChild
            })
            
        userSkillsDetails["otherSkills"] = otherSkills

        return userSkillsDetails

    def getAccomplishments(self, soup):
        acData = {}
        courses = soup.find("section", {"class" : "accordion-panel pv-profile-section pv-accomplishments-block courses ember-view"})
        if courses != None:
            courses = courses.find("ul")
            courses = [course.text for course in courses.findAll("li")]
        acData["courses"] = courses
        
        languages = soup.find("section", {"class" : "accordion-panel pv-profile-section pv-accomplishments-block languages ember-view"})
        if languages != None:
            languagesUl = languages.find("ul")
            languages = [language.text for language in languagesUl.findAll("li")]
        acData['languages'] = languages
        
        projects = soup.find("section", {"class" : "accordion-panel pv-profile-section pv-accomplishments-block projects ember-view"})
        if projects != None:
            projects = projects.find("ul")
            if projects !=None:
                projects = [project.text for project in projects.findAll("li")]
        acData["projects"] = projects
        return acData

    def parseProfile(self, soup):
        mainData = {}

        # Basic details
        name_div = soup.find('div', {'class': 'flex-1 mr5'})
        basicDetails = self.getBasicUserDetails(name_div)
        mainData.update(basicDetails)

        # About section
        about = self.getAboutSection(soup)
        mainData.update({"about" : about})

        # Experience
        if 1==1:
            exp_section = soup.find('section', {'id': 'experience-section'})
            if exp_section != None:
                exp = self.getExperienceDetails(exp_section)
                mainData.update({"experience" : exp})
        else:
            print("Error in Experience parse")

        # Education details
        if True:
            educationSection = soup.find('section', {'id': 'education-section'})
            if educationSection != None:
                edu = self.getEducationDetails(educationSection)
                mainData.update({"education" : edu})
        else:
            print("Error in Education Parse")

        # Certifications
        if True:
            certificationsSection = soup.find('section', {'id': 'certifications-section'})
            if certificationsSection != None:
                cert = self.getCertifications(certificationsSection)
                mainData.update({"certifications" : cert})
        else:
            print("Error in Certifications parse")

        # Skills
        print("Working with skills")
        if True:
            skills = soup.find("section", {"class" : "pv-profile-section pv-skill-categories-section artdeco-container-card ember-view"})
            if skills != None:
                skills = self.getUserSkills(skills)
                mainData.update({"skills" : skills})
        else:
            print("Error in Skills parse")

        print("Working with accomplishments")
        # Accomplishments
        if True:
            acc = self.getAccomplishments(soup)
            mainData.update({"accomplishments" : acc})
        else:
            print("Error in accomplishments parse")
        
        return mainData


    def processSearchResults(self, soup):
        searchResults = soup.findAll("ul", {"class" : "search-results__list list-style-none"})
        profilesList = searchResults[0].findAll("li", {"class" : "search-result search-result__occluded-item ember-view"})
        print("Profiles found:", len(profilesList))
        data = []
        for person in profilesList:
            name = person.find("span", {"class" : "name actor-name"}).text
            profileUrl = "https://linkedin.com" + person.find("a", {"class" : "search-result__result-link ember-view"})["href"]
            degree = person.find("span", {"class" : "distance-badge separator ember-view"}).text.replace("\n","").strip()
            data.append((name, profileUrl, degree))
        return data