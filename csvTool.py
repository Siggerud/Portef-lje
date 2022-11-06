# tool for rebalancing a portfolio
# testStr

import os
import datetime
import csv


class csvTool:
    def __init__(self):
        self.differenceInPercentList = []
        self.sectors = ["Asia", "Europe", "Emerging markets", "Global", "Nordic", "Technology", "USA"]
        self.diffInValue = []

    # sort sectors, difference in value and percentage based on how much they have devalued
    def sortLists(self):
        # combine lists and sort based on difference in percentages
        combinedLists = zip(self.differenceInPercentList, self.sectors, self.diffInValue)
        sortedLists = sorted(combinedLists)

        # split the lists after sorting
        sectors = []
        diffInPercent = []
        diffInValue = []
        for i in range(len(sortedLists)):

            sectors.append(sortedLists[i][1])
            diffInPercent.append(sortedLists[i][0])
            diffInValue.append(sortedLists[i][2])

        sortedLists = []
        sortedLists.append(sectors)
        sortedLists.append(diffInPercent)
        sortedLists.append(diffInValue)

        sortedLists = self.addMetricsToSortedLists(sortedLists)

        return sortedLists


    # add metrics to percentages
    def addMetricsToSortedLists(self, sortedLists):
        for i in range(len(sortedLists[1])):
            sortedLists[1][i] = str(sortedLists[1][i]) + " %"

        return sortedLists

    # create portfolio data if certain requirements are met
    def createPortfolio(self, deposit):
        exportList = []

        # check if relevant CSVs downloaded today
        CSVfiles = self.findRelevantCSVs()
        if len(CSVfiles) != 2:
            print("No relevant CSVs downloaded today")
            return exportList

        if deposit == "":
            print("Please enter a deposit value")
            return exportList

        dataList = self.getDataAndCalculateFromCSVs(CSVfiles, deposit)

        exportList = self.addMetricsToDataList(dataList)
        self.diffInValue = exportList[5]

        return exportList

    # add % or NOK at end of the values
    def addMetricsToDataList(self, dataList):
        exportList = []
        for i in range(len(dataList)):
            temp = []
            for j in range(len(dataList[i])):
                value = str(dataList[i][j])
                if i < 3 or i == 6:
                    output = value + " %"
                else:
                    output = value + " NOK"
                temp.append(output)

            exportList.append(temp)

        return exportList

    def getDataAndCalculateFromCSVs(self, files, deposit):
        dataList = []

        data = self.getRelevantData(files)
        groupedDataValues = self.groupDataValues(data)

        weights = [15,15,15,15,10,15,15] # ideal weights for the sectors

        totalSum = self.getTotalSum(deposit, groupedDataValues)
        weightedValues = self.getWeightedValues(weights, totalSum)

        currentWeights = self.getCurrentWeights(groupedDataValues, totalSum)

        differenceInPercentage = self.getDifferenceInPercentage(weights, currentWeights)

        differenceInValue = self.getDifferenceInValue(groupedDataValues, weightedValues)

        dataList.append(weights)
        dataList.append(currentWeights)
        dataList.append(differenceInPercentage)
        dataList.append(weightedValues)
        dataList.append(groupedDataValues)
        dataList.append(differenceInValue)

        return dataList

    # get the difference between the ideal weighted value and current value of each sector
    def getDifferenceInValue(self, groupedDataValues, weightedValues):
        differenceInValues = []
        for i in range(len(groupedDataValues)):
            differenceInValue = groupedDataValues[i] - weightedValues[i]
            differenceInValue = round(differenceInValue, 2)
            differenceInValues.append(differenceInValue)

        return differenceInValues

    # get the absolute difference between ideal weights and the current weights
    def getDifferenceInPercentage(self, weights, currentWeigts):
        differenceInPercentagesAbs = []
        for i in range(len(weights)):
            differenceInPercentAbs = abs(currentWeigts[i] - weights[i])
            differenceInPercentAbs = round(differenceInPercentAbs, 2)

            differenceInPercent = currentWeigts[i] - weights[i]
            differenceInPercent = round(differenceInPercent, 2)

            differenceInPercentagesAbs.append(differenceInPercentAbs)
            self.differenceInPercentList.append(differenceInPercent)

        return differenceInPercentagesAbs

    # get the current weights of each sector
    def getCurrentWeights(self, groupedDataValues, totalSum):
        currentWeights = []
        for value in groupedDataValues:
            percentageOfTotal = (value / totalSum) * 100
            percentageOfTotal = round(percentageOfTotal, 2)
            currentWeights.append(percentageOfTotal)

        return currentWeights

    # get the weight of the ideal values for all sectors
    def getWeightedValues(self, weights, totalSum):

        weightedValues = []
        for i in range(len(weights)):
            fraction = weights[i] * 0.01
            weightedValue = fraction * totalSum
            weightedValue = round(weightedValue, 2)
            weightedValues.append(weightedValue)

        return weightedValues

    # get the sum of all sectors plus the deposit made
    def getTotalSum(self, deposit, groupedData):
        totalSum = sum(groupedData) + float(deposit)

        return totalSum

    # group together funds and ETFs that belong in the same category,
    # and then find the value of the sector
    def groupDataValues(self, data):
        Funds = []
        Funds.append([["Asia"], 0]) # Asia
        Funds.append([["Europ"], 0]) # Europe
        Funds.append([["Fremvoksende", "Emerging"], 0]) # Emerging market
        Funds.append([["Global"], 0]) # Global
        Funds.append([["Suomi", "Sverige", "Danmark", "Norge"], 0]) # Scandinavia
        Funds.append([["Teknologi", "Nasdaq"], 0]) # Technology
        Funds.append([["USA"], 0]) # USA

        # find the searchwords in data, and add value to the sector when found
        for fundOrEtf in data:
            for entry in fundOrEtf:
                for i in range(len(Funds)):
                    for j in range(len(Funds[i][0])):
                        if Funds[i][0][j] in entry[0]:
                            valueString = entry[1]
                            Funds[i][1] += float(valueString.replace(",", "."))

        groupedDataValues = []
        for k in range(len(Funds)):
            dataValue = round(Funds[k][1], 2)
            groupedDataValues.append(dataValue)

        return groupedDataValues

    # Get the data necessary to do calculations from downloaded csv files
    def getRelevantData(self, files):
        relevantData = []
        for file in files:
            openFile = open(file, encoding="utf-16 le")
            csv_reader = csv.reader(openFile, delimiter="\t")

            relevantSubData = []
            count=0
            for row in csv_reader:
                if count != 0: # skip title row
                    temp = []
                    temp.append(row[0]) # Name
                    temp.append(row[8]) # Todays value
                    relevantSubData.append(temp)
                count += 1

            relevantData.append(relevantSubData)

        return relevantData

    # search through download folder and get the relevant files
    def findRelevantCSVs(self):
        downloadPath = "C:\\Users\\Chris\\Downloads"
        downloadedFiles = os.listdir(downloadPath)

        relevantFileList = []
        for file in downloadedFiles:
            # check if filename found in folder
            if file[0:11] == "fondslister" or file[0:11] == "aksjelister":
                if file.endswith(".csv"):
                    # if found, check if downloaded today
                    filePath = os.path.join(downloadPath, file)
                    creationTimeRaw = os.path.getctime(filePath)
                    creationTimeFormatted = str(datetime.datetime.fromtimestamp(creationTimeRaw))

                    todayRaw = datetime.date.today()
                    todayFormatted = todayRaw.strftime("%Y-%m-%d")

                    if todayFormatted == creationTimeFormatted[0:10]:
                        relevantFileList.append(filePath)

        # sort to get aksjelister first
        relevantFileList.sort()
        return relevantFileList


