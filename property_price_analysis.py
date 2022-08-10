if __name__ == ('__main__'):

    #AVERAGE PROPERTY PRICE AGAINST COMMUTE TIME
    import csv
    import matplotlib.pyplot as plt
    import numpy as np
    with open(r'Rightmove_South-Eastern_Station_Properties_2022-08-01_13-34-18.csv','r',encoding = 'unicode_escape') as file:
        data = file.readlines()
    strippedData = [element.strip() for element in data]
    header = strippedData[0].split(',')
    formattedData = [element.split(',') for element in strippedData[1:]]

    #CLEANING PRICE COLUMN OF £ SIGN
    for element in formattedData:
        x = element[1].split('£')
        element[1] = x[-1]

    #STRUCTURING A CONDENSED FORMAT OF THE TABLE
    shortList = []
    for element in formattedData:
        tempList = [element[0],element[1],element[4],element[9]]
        if tempList[1] != 'POA':
            shortList.append(tempList)

    #FINDING DISTINCT STATION NAMES
    stationList = []
    for element in shortList:
        if element[0] not in stationList:
            stationList.append(element[0])

    #FINDING COMMUTES
    commutes = []
    for station in stationList:
        tempList = []
        for element in shortList:
            if station == element[0]:
                tempList.append(element[3])
        commutes.append([station,tempList[0]])

    #FINDING AVERAGE PROPERTY PRICE FOR EACH STATION
    stationAverages = []
    for station in stationList:
        propertyPriceList = []
        for record in shortList:
            if record[0] == station:
                propertyPriceList.append(float(record[1]))
        average = sum(propertyPriceList) / len(propertyPriceList)
        stationAverages.append([station,average])

    #FINDING NUMBER OF PROPERTIES FOR EACH STATION
    stationOccurances = []
    for element in shortList:
        stationOccurances.append(element[0])

    propertyCounts = []
    for station in stationList:
        propertyCounts.append([station,stationOccurances.count(station)])

    #JOINING PROPERTY COUNTS AND AVERAGE PRICES TOGETHER
    joinedList = []
    for i in stationAverages:
        for j in propertyCounts:
            for k in commutes:
                if i[0] == j[0] == k[0]:
                    joinedList.append([i[0],j[1],i[1],k[1]])   
                    
    #SORT THE STATIONS BY AVERAGE PRICE
    joinedList.sort(key=lambda price: price[2])
    joinedList = joinedList[::-1]

    #SPLITTING THE DATA INTO LISTS OF EACH ATTRIBUTE
    stations = []
    num_of_properties = []
    average_prices = []
    commutes = []   
    for element in joinedList:
        stations.append(element[0])
        num_of_properties.append(int(element[1]))
        average_prices.append(float(element[2]))
        commutes.append(int(element[3]))

    stations = stations[::-1]
    average_prices = average_prices[::-1]
    num_of_properties = num_of_properties[::-1]
    commutes = commutes[::-1]

    xaxis = stations
    y = average_prices
    y2 = commutes
    average_of_average_price = sum(y) / len(y)
    average_commute = sum(y2) / len(y2)

    # PLOT ONE AVERAGE PRICE LINE
    fig, ax1 = plt.subplots(figsize=(40, 15))
    ax1.plot(xaxis, y, color = 'green')
    ax1.set_xlabel('STATION NAME')
    ax1.set_ylabel('AVERAGE PROPERTY PRICE (£)',color='green' )

    #PLOT TWO COMMUTE TIMES
    ax2 = ax1.twinx()
    ax2.scatter(xaxis, y2, color = 'blue')  
    ax2.set_ylabel('COMMUTE TIME (MINUTES)',color='blue')

    # AVERAGE PRICE POINTT FOR COMMUTE LINE
    middle = len(xaxis) / 2
    plt.axvline(x=middle, color = 'purple')
    plt.text(middle+1,min(y2),'Low Commute Time',color='red',fontsize=15)
    plt.text(middle+1,max(y2),'High Commute Time',color='red',fontsize=15)

    #AVERAGE COMMUTE POINT FOR PRICE LINE
    plt.axhline(y=average_commute, color = 'purple')
    plt.text(xaxis[0],average_commute-3,'Low Property Price',rotation=0,color='red',fontsize=15)
    plt.text(xaxis[-7],average_commute-3,'High Property Price',rotation=0,color='red',fontsize=15)

    # ANNOTATING EACH STATION TO EACH COMMUTE POINT
    for element in xaxis:
        index = xaxis.index(element)
        plt.text(element,y2[index],' '.join(element.split(' station')),rotation=0)

    plt.xticks([])
    plt.savefig('Property_Analysis.png')

     
     