if __name__ == ('__main__'):

    ############################################


    #IMPORTS


    ############################################


    import os
    import random
    import time
    import requests
    import bs4
    import csv
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from datetime import datetime
    from tqdm import tqdm
    from IPython.display import clear_output
    import concurrent.futures



    ############################################

    #GATHERING ALL SOUTH-EASTERN RAILWAY STATIONS

    ############################################


    # IF THE STATION DATA DOESN'T EXIST IT WILL FETCH THE DATA
    if os.path.exists('Station_Data.txt') == False:
        base_url = 'https://en.wikipedia.org/wiki/Category:Railway_stations_served_by_Southeastern'
        res = requests.get(base_url)
        soup = bs4.BeautifulSoup(res.text, 'html5lib' )
        textData = []
        for element in soup.find('div', class_='mw-category mw-category-columns'):
            textData.append(element.text)
        stationLists = []
        for i in textData:
            letterList = i.split('\n')
            stationLists.append(letterList[1:])
        stations = []
        for i in stationLists:
            for j in i:
                stations.append(j)
        # Removing railway for the rightmove search
        cleanedStations = []
        for element in stations:
            x = element.split(' railway')
            y = ''.join(x)
            cleanedStations.append(y)
        noKents = []
        for element in cleanedStations:
            index = cleanedStations.index(element)
            if element != 'Wye station':
                if element != 'Rainham station (Kent)':
                    x = element.split(' (Kent)')
                    cleanedStations[index] = x[0]
                if element == 'Rainham station (Kent)':
                    cleanedStations[index] = 'Rainham (Kent) Station'
                if element == 'London Victoria station':
                    cleanedStations[index] = 'Victoria Station'

        # SELENIUM FUNCTION TO CONVERT STATION NAMES INTO THE FORMAT REQUIRED TO FETCH PROPERTIES ON RIGHTMOVE
        import time
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager
        def get_driver():
            #set options for easier browsing
            options = webdriver.ChromeOptions()
            options.add_argument('disable-infobars')
            options.add_argument('start-maximized')
            options.add_argument('disable-dev-shm-usage')
            options.add_argument('no-sandbox')
            options.add_experimental_option('excludeSwitches',['enable-automation'])
            options.add_argument('disable-blink-features=AutomationControlled')
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.get('https://www.rightmove.co.uk/property-for-sale.html')
            return driver
        def stationFinder(station):
            driver = get_driver()
            search_engine = driver.find_element(by='xpath',value='/html/body/div/div[1]/div[1]/div/div/form/fieldset/div/input[1]')
            search_engine.send_keys(station)
            main_page_button = driver.find_element(by='xpath',value='/html/body/div/div[1]/div[1]/div/div/form/fieldset/div/input[5]')
            main_page_button.click()
            time.sleep(1)
            try:
                search_results_button = driver.find_element(by='xpath',value='/html/body/div[1]/div[2]/div/div[1]/div/form/fieldset[2]/div[4]/button')
                search_results_button.click()
            except:
                search_engine = driver.find_element(by='xpath',value='/html/body/div[1]/div[2]/div[1]/div/div/form/fieldset/div/input[1]')
                search_engine.send_keys(station)
                autofill = driver.find_element(by='xpath',value='/html/body/div[6]/ul/li/span')
                autofill.click()
                search_engine_button = driver.find_element(by='xpath',value='/html/body/div[1]/div[2]/div[1]/div/div/form/fieldset/div/input[4]')
                search_engine_button.click()
                main_page_button = driver.find_element(by='xpath',value='/html/body/div[1]/div[2]/div/div[1]/div/form/fieldset[2]/div[4]/button')
                main_page_button.click()
            time.sleep(1)
            url = driver.current_url
            location = url.split('&')[1]
            station_id = location.split('%')[1]
            return station_id

        # CALLING THE FUNCTIONS WITH THE CLEANED STATIONS
        station_ids = []
        from tqdm import tqdm
        from IPython.display import clear_output
        for element in tqdm(cleanedStations):
            print(element)
            station_ids.append(stationFinder(element))
            for i in range(10):
                clear_output(wait=True)

        # JOINING THE STATION NAMES AND IDS AND WRITING TO A TEXT FILE
        stationData = []
        for num in range(0,len(cleanedStations)-1):
            stationData.append(cleanedStations[num]+'_'+station_ids[num]+'\n')
        with open('Station_Data.txt','w') as file:
            file.writelines(stationData)

    ############################################


    #SCRAPING COMMUTE TIMES FROM GOOGLE MAPS


    ############################################

    # SCRAPING COMMUTE TIMES FROM GOOGLE MAPS

    # IF USER DOESN'T HAVE THE COMMUTE TIMES IT WILL FETCH THE DATA
    if os.path.exists('Commute_Times.txt') == False:
        def get_driver():
            #set options for easier browsing
            options = webdriver.ChromeOptions()
            options.add_argument('disable-infobars')
            options.add_argument('start-maximized')
            options.add_argument('disable-dev-shm-usage')
            options.add_argument('no-sandbox')
            options.add_experimental_option('excludeSwitches',['enable-automation'])
            options.add_argument('disable-blink-features=AutomationControlled')
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.get('https://www.google.com/maps/dir/')
            return driver
        def commuteTime(station,destination):
            driver = get_driver()
            accept_cookies = driver.find_element(by='xpath',value='/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button')
            time.sleep(1)
            accept_cookies.click()
            time.sleep(2)
            public_transport = driver.find_element(by='xpath',value='/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[2]/div/div/div/div[3]/button')
            public_transport.click()
            time.sleep(1)
            search_engine1 = driver.find_element(by='xpath',value='/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/input')
            search_engine1.send_keys(station)
            autofill1 = driver.find_element(by='xpath',value='/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/button[1]')
            autofill1.click()
            time.sleep(1)
            search_engine2 = driver.find_element(by='xpath',value='/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[2]/div[1]/div/input')
            search_engine2.send_keys(destination)
            autofill2 = driver.find_element(by='xpath',value='/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[2]/button[1]')
            autofill2.click()
            leaveSelect = driver.find_element(by='xpath',value='/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/span/div/div/div/div[1]')
            leaveSelect.click()
            time.sleep(3)
            departAt = driver.find_element(by='xpath',value='/html/body/div[6]/div[2]/div')
            departAt.click()
            time.sleep(3)
            timeSelect = driver.find_element(by='xpath',value='/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/span[1]/input')
            time.sleep(1)
            timeSelect.clear()
            time.sleep(1)
            timeSelect.send_keys('06:30')
            time.sleep(1)
            dateButton = driver.find_element(by='xpath',value='/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/span[2]/span[1]')
            #Friday Scrapes skip to Monday
            if dateButton.text.split(' ')[0] == 'Fri,':
                dateCycle = driver.find_element(by='xpath',value='/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/span[2]/span[2]/button[2]')
                dateCycle.click()
                time.sleep(1)
                dateCycle.click()
                time.sleep(1)
                dateCycle.click()
                time.sleep(1)    
            #Saturday scrcapes skip to Monday
            elif dateButton.text.split(' ')[0] == 'Sat,':
                dateCycle = driver.find_element(by='xpath',value='/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/span[2]/span[2]/button[2]')
                dateCycle.click()
                time.sleep(1)
                dateCycle.click()
                time.sleep(1)
            #Sunday-Thursday Scrapes cycle to next day
            else:
                dateCycle = driver.find_element(by='xpath',value='/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/span[2]/span[2]/button[2]')
                dateCycle.click()
                time.sleep(1)
            time.sleep(5)
            duration = driver.find_element(by='xpath',value='/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/div[1]/div[2]/div[1]/div')
            return duration.text
        with open('Station_Data.txt','r') as file:
            rawData = file.readlines()
        strippedData = [element.strip() for element in rawData]
        stationNames = [element.split('_')[0] for element in strippedData]
        stationIds = [element.split('_')[1] for element in strippedData]
        commutes = []

        # Starting the scrap
        for element in tqdm(stationNames):
            print(element)
            if element != 'Cannon Street station':
                if element != 'London Bridge station':
                    commutes.append(commuteTime(element,'London Bridge'))
            if element == 'Cannon Street station':
                commutes.append('0 min')
            if element == 'London Bridge station':
                commutes.append('0 min')
            for i in range(10):
                clear_output(wait=True)
        names_and_times = []
        for element in range(0,len(stationNames)):
            names_and_times.append(stationNames[element]+'_'+commutes[element])

        # Convert string times to minutes
        names1 = [element.split('_')[0] for element in names_and_times]
        times1 = [element.split('_')[1] for element in names_and_times]
        newTimes = []
        for element in times1:
            split = element.split(' ')
            if split[1] == 'min':
                newTimes.append(int(split[0]))
            if len(split) == 2 and split[1] == 'hr':
                newTimes.append((int(split[0]) * 60))
            if len(split) == 4 and split[1] == 'hr':
                newTimes.append((int(split[0]) * 60) + int(split[2]))

        #Save to file
        cleanedCommutes = []
        for element in range(0,len(stationNames)):
            cleanedCommutes.append(stationNames[element]+'_'+str(newTimes[element])+'\n')
        with open('Commute_Times.txt','w') as file:
            file.writelines(cleanedCommutes)

    ############################################


    #SCRAPING PROPERTIES

    ############################################

    def propertyScraper(data):
        #print(stationName)
        stationName = data.split('_')[0]
        print(stationName)
        areaId = data.split('_')[1]

        def pageScraper(number):
            propertiesForSale = []
            errors = []
            junkData = ['Offers Over','Premium Listing','Offers in Excess of','Guide Price','Shared ownership','Viewing Advised','Coastal Location','Offers in Region of','Retirement','Just Launched','No Chain','Fixed Price','Flooring Package','*','Off-Street Parking','Sea View','Buy to Let','Close to Shops','New Listing','Balcony','Garage','Plot for sale','24 Hours Security','Riverside views','Move In Now','Shared Ownership','Attention Investors','Show Home Now Open','From','Star Buy','Auction','Garden','Town centre location','Ground floor','Last 1 Remaining','Part buy, part rent']    
            #STARTING THE SEARCH ON OTHER PAGEs
            page = number
            base_url = 'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=STATION%{}&maxPrice=350000&minPrice=100000&radius=3.0&sortType=1&index={}&propertyTypes=bungalow%2Cdetached%2Cflat%2Csemi-detached%2Cterraced&includeSSTC=false&mustHave=&dontShow=retirement%2CsharedOwnership&furnishTypes=&keywords='.format(areaId,page)
            res = requests.get(base_url)
            soup = bs4.BeautifulSoup(res.text, 'html5lib' )
            # RESPONSE CHECK
            textData = []
            for element in soup.find_all('div', class_='propertyCard-wrapper'):
                textData.append([element.text])
            noNewLines = []
            for element in textData:
                tempList = []
                tempList2 = []
                for i in element:
                    x = i.split('\n')
                    for j in x:
                        if len(j) > 0:
                            if j.isspace() == False:
                                tempList.append(j)
                noNewLines.append(tempList)
            # TRIMING WHITESPACE AND FILTERING THE DATA TO REMOVE PROPERTY SPECIFIC TRAITS AND INFORMATION
            trimed_list = []   
            for element in noNewLines:
                tempList = []
                tempList2 = []
                for i in element:
                    tempList.append(i.strip())
                for j in tempList:
                    if j not in junkData:
                        if 'SHARED' not in j:
                                tempList2.append(j)
                trimed_list.append(tempList2[1:])
            # REMOVING THE RANDOM PREMIUM LISTING FROM THE LIST
            propertyList = trimed_list[1:]
            # IF THE PROPERTY DESCRIPTION IS SEPERATED THEN JOIN THE SPLIT STRINGS
            index = 0
            for element in propertyList:
                if len(element) == 15:
                    tempList = []
                    start = element[0:4]
                    join = ' '.join(element[4:7])
                    end = element[7:]
                    for i in start:
                        tempList.append(i)
                    tempList.append(join)
                    for i in end:
                        tempList.append(i)
                    propertyList[index] = tempList
                index += 1
            for element in propertyList:
                if len(element) != 13:
                     errors.append(element)
            for element in propertyList:
                if element != ['Commercial', 'Development Microsite', 'Local call rate', 'Email agent']:
                    propertiesForSale.append(element)
            # DATA VERFICATION
            verifiedPropertyList = []
            for element in propertiesForSale:
                if len(element) != 13:
                    errors.append(element)
                if len(element) == 13:
                    verifiedPropertyList.append(element)
            #print('Errors prior to final length check: ',len(errors))
            #print(errors)
            for element in errors:
                if len(element) == 13:
                    verifiedPropertyList.append(element)
            for element in verifiedPropertyList:
                if len(element) != 13:
                    print('Length Error',element)

            # REMOVING IRRELEVANT FIELDS FOR THE CSV FILE
            cleanedList = []
            for element in verifiedPropertyList:
                tempList = []
                tempList.append(stationName)
                usefulData1 = element[0:5]
                for i in usefulData1:
                    tempList.append(i)
                dateAdded_byWhom = element[7:9]
                for i in dateAdded_byWhom:
                    tempList.append(i)
                phoneNumber = element[10]
                tempList.append(phoneNumber)
                cleanedList.append(tempList)
            shortList = []
            for element in cleanedList:
                if element not in shortList:
                    shortList.append(element)
        #print('Properties: ',len(shortList))
            return shortList

        # Creating the list of indexes that the URL needs to cycle through the pages
        rangeList = []
        for num in range(0,43):
            rangeList.append(num*24)

        #Using concurrent futures to scrape through the pages as efficiently as possible
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            complete_scans = executor.map(pageScraper, rangeList)
            for i in complete_scans:
                results.append(i)
            print('Station complete')
        return results


    with open('Station_Data.txt','r') as file:
        rawData = file.readlines()
    strippedData = [element.strip() for element in rawData]

    # Running the function
    finalResults = []
    for element in tqdm(strippedData):
        finalResults.append(propertyScraper(element))
        for i in range(10):
            clear_output(wait=True)

    # Removing empty lists and restructuring the list 
    cleanedList = []
    for element in finalResults:
        for i in element:
            for j in i:
                if len(j) > 0:
                    cleanedList.append(j)

    # WRITING TO A CSV
    with open('Commute_Times.txt','r') as file:
        commuteData = [element.strip() for element in file.readlines()]
    commuteDataStations = [element.split('_')[0] for element in commuteData]
    commuteDataTimes = [element.split('_')[1] for element in commuteData]

    # CLEANING THE DISTANCE FROM STATION DATE AND ADDING COMMUTE TIMES TO EACH RECORD
    for element in cleanedList:
        index = cleanedList.index(element)
        stationCSV = element[0]
        commuteTimeIndex = commuteDataStations.index(stationCSV)
        element.append(commuteDataTimes[commuteTimeIndex])
        # CLEANING DISTANCE FROM STATION FIELD
        x = element[4].split(' ')
        cleanedList[index][4] = x[0]


    #REMOVING UNNECESSARY COMMAS
    for element in cleanedList:
        for i in element:
            index = element.index(i)
            commaJoin = str(''.join(i.split(',')))
            element[index] = commaJoin

    # FOR A VERY SMALL PERCENTAGE OF RESULTS WE NEED TO ALIGN THE RECORD CORRECTLY AGAIN
    for element in cleanedList:
        # CHECK DISTANCE FROM STATION CAN BE 'FLOATED'
        try:
            float(element[4])
        # IF NOT WE HAVE A MISALIGNMENT OF THE RECORD
        except ValueError:
            splitDescription = element[5].split(' ')
            element[3] = str(element[3]) + ' ' +str(splitDescription[0])
            # SPLITING DESCRIPTION AND FINDING THE DISTANCE FROM STATION WITH FLOAT CHECK
            for i in splitDescription:
                try:
                    if float(i):
                        element[4] = i
                except:
                    pass
            # FIXING THE DESCRIPTION
            element[5] = element[5].split('station')[1]
            element[5] = element[5].lstrip()
            for i in element:
                index = element.index(i)

    header = ['Station','Price','Property_Size','Address','Distance from Station (miles)','Description','Date Added','Added By Whom',' Telephone Number','Commute Time']
    # FETCHING DATETIME AND CLEANING IT INTO A SAVEABLE FILE FORMAT
    dateTime = '-'.join(str(str('_'.join(str(datetime.now()).split(' '))).split('.')[0]).split(':'))
    #WRITING TO CSV
    with open('Rightmove_South-Eastern_Station_Properties_'+ dateTime +'.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(header)
            # write multiple rows
            writer.writerows(cleanedList)