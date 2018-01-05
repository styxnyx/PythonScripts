# -*- coding: utf-8 -*-
__author__ = 'Kyle [Pinguin101]'

"""
If You Found this Helpful please feel free to donate: https://paypal.me/GameDev

Or Check out this awsome ebook:
[100+ 5 Star Reviews] - Sponsored
‘The Content Code: Six essential strategies to ignite your content, your marketing, and your business’
By Mark Schaefer

Only $9.99 => http://amzn.to/2F4QOnQ
"""

import binascii
import string
import re
import os
import datetime

"""
SORTED TYPES:
[0]: BID = Sorts the saved output in order of bids
[1]: COMP = Sorts the saved output in order of competition
[2]: SEARCH = Sorts the saved output in order of avg searches
[3]: KWLEN = Sorts the saved output in order of keyword length
[4]: ALL = Saves all sorted types
"""
sortByListValues = ['BID', 'COMP', 'SEARCH', 'KWLEN'] # DON'T TOUCH THIS
sortBy = 0

dataCSVPath = './Data/'
savedCSVPath = './Saved/'

# KW longer than this
bestKWLen = 25

# Anything Less than
dontBotherLen = 12

# Anything less than
bestComp = 0.05
goodComp = 0.1
okayComp = 0.15
sosoComp = 0.2

# Perfect Searches
perfectSearches = '100K - 1M'

# Best Searches
bestSearches = '10K - 100K'

# Great Searches
greatSearches = '1K - 10K'

# Good Searches
goodSearches = '100 - 1K'

# Bad Searches
badSearches = '10 - 100'

# Worst Searches
worstSearches = '0 - 10'

# Result List
keywordResults = list()

# Prefix Timeout
pfTimeout = 10
hasPFTimedOut = False

def main():
    if not os.path.exists(dataCSVPath):
        print "Creating Data Folder to dump your Google Keyword Planner CSVs... Please add some CSVs to read..."
        os.makedirs(dataCSVPath)
        exit()

    if not os.path.exists(savedCSVPath):
        print "Creating Saved Data folder for our keyword research dumps"
        os.makedirs(savedCSVPath)

    print "Please give us a prefix to save this output file... \nIf nothing is displayed only the timestamp will be used...\n"
    prefix = raw_input('> ')
    prefix = prefix.replace(' ', '_')
    print "----------------"
    if prefix is '':
        print "No value entered, using timestamp instead of a prefix..."
    else:
        prefix = "[" + prefix + "]-"
        print "Setting Prefix as: " + prefix

    print "----------------"
    print "Searching for longtail keywords!"
    print "----------------"

    for root, dirs, files in os.walk(dataCSVPath):
            print "File Count: " + str(files.__len__())
            print "----------------"
            if files.__len__() == 0:
                print "Please add some Google Keyword Planner CSVs to read..."
                exit()

            for name in files:
                if str(name) not in ".DS_Store":
                    if str(name).endswith('.csv'):
                        scanFileForKeywords(name)

    """
        The Scores:
        quality = 'PERFECT'
        quality = 'BEST'
        quality = 'GREAT'
        quality = 'GOOD'
        quality = 'ALRIGHT'
        quality = 'MEH'
    """
    perfectList = list()
    bestList = list()
    greatList = list()
    goodList = list()
    alrightList = list()
    mehList = list()

    for keyword in keywordResults:
        # keywordSearch = [quality, score, keyword, kwLen, avgSearch, comp, suggestedBid]
        if keyword[0] == 'PERFECT':
            perfectList.append(keyword)
        if keyword[0] == 'BEST':
            bestList.append(keyword)
        if keyword[0] == 'GREAT':
            greatList.append(keyword)
        if keyword[0] == 'GOOD':
            goodList.append(keyword)
        if keyword[0] == 'ALRIGHT':
            alrightList.append(keyword)
        if keyword[0] == 'MEH':
            mehList.append(keyword)

    print "Total Found: " + str(keywordResults.__len__())
    print "----------------"
    print "Total Perfects: " + str(perfectList.__len__())
    print "Total Bests: " + str(bestList.__len__())
    print "Total Greats: " + str(greatList.__len__())
    print "Total Goods: " + str(goodList.__len__())
    print "Total Alrights: " + str(alrightList.__len__())
    print "Total Mehs: " + str(mehList.__len__())
    print "----------------"

    if sortBy <= 3 and sortBy >= 0:
        saveData([perfectList, bestList, greatList, goodList, alrightList, mehList], sortByListValues[sortBy], prefix)
    elif sortBy == 4:
        saveData([perfectList, bestList, greatList, goodList, alrightList, mehList], sortByListValues[0], prefix)
        saveData([perfectList, bestList, greatList, goodList, alrightList, mehList], sortByListValues[1], prefix)
        saveData([perfectList, bestList, greatList, goodList, alrightList, mehList], sortByListValues[2], prefix)
        saveData([perfectList, bestList, greatList, goodList, alrightList, mehList], sortByListValues[3], prefix)
    else:
        print "INVALID SORT VALUE!!!"
        exit()

def saveData(dataToSave, sortedBy, prefix = ''):

    outputFile = prefix + str(datetime.datetime.now()).replace(':', '_').replace(' ', '_').split('.')[0] + "_SORTBY_" + sortedBy
    with open(savedCSVPath + outputFile + '.txt','w') as f:
        f.close()

    #print "[" + str(quality) + " (Score: " + str(score) + ")]> " + keyword + " (" + str(kwLen) +  ") | Search: " + avgSearch + " | Comp: " + str(comp) + " | BID: " + suggestedBid

    for dataList in dataToSave:
        keyIndex = 0
        if sortedBy == "BID":
            keyIndex = 6
        elif sortedBy == "COMP":
            keyIndex = 5
        elif sortedBy == "SEARCH":
            keyIndex = 4
        elif sortedBy == "KWLEN":
            keyIndex = 3

        if keyIndex != 3:
            dataList.sort(key=lambda k: (k[keyIndex]))
        else:
            dataList.sort(key=lambda k: (k[keyIndex]), reverse=True)

        for data in dataList:
            with open(savedCSVPath + outputFile + '.txt','a') as f:
                if data[6] == 9999999999999999:
                    suggestedBid = 'UNKNOWN'
                else:
                    suggestedBid = "$" + str(float(data[6]))

                searchResults = ""
                if data[4] == 0:
                    searchResults = perfectSearches
                elif data[4] == 1:
                    searchResults = bestSearches
                elif data[4] == 2:
                    searchResults = greatSearches
                elif data[4] == 3:
                    searchResults = goodSearches
                elif data[4] == 4:
                    searchResults = badSearches
                elif data[4] == 5:
                    searchResults = worstSearches


                dataToWrite = "[" + str(data[0]) + " (Score: " + str(data[1]) + ")]> " + data[2] + " (" + str(data[3]) +  ") | Search: " + searchResults + " | Comp: " + str(data[5]) + " | BID: " + str(suggestedBid)
                f.write(str(dataToWrite) + '\r')
            f.close()

    print "Saved to: " + str(outputFile) + '.txt'

def scanFileForKeywords(fileToScan):
    print "Scanning: " + fileToScan

    with open(dataCSVPath + fileToScan,'r') as f:
        csv_file = f.readlines()
    f.close()

    rCount = 0
    foundCount = 0
    perfects = 0
    bests = 0
    greats = 0
    goods = 0
    alrights = 0
    mehs = 0

    for row in csv_file:
        rCount += 1
        if rCount > 1:
            data = row.replace('\n', '').replace('\r', '').split('	')
            if str(data) != '' and data.__len__() != 1:
                score = 0
                keyword = returnStr(data[1])
                kwLen = keyword.__len__()
                avgSearch = returnStr(data[3]).replace('   ', ' - ')
                comp = re.findall(r'^[0-9\.]*$', returnStr(data[4]))
                suggestedBid = re.findall(r'^[0-9\.]*$', returnStr(data[5]))
                if comp.__len__() == 0:
                    comp = 0
                    score -= 1
                else:
                    if comp[0] != '':
                        comp = float(comp[0])
                    else:
                        comp = 0
                        score -= 1

                if suggestedBid.__len__() == 0:
                    suggestedBid = 9999999999999999
                else:
                    if suggestedBid[0] != '':
                        suggestedBid = float(suggestedBid[0])
                    else:
                        suggestedBid = 9999999999999999

                if kwLen >= bestKWLen:
                    score += 3
                elif kwLen >= dontBotherLen:
                   score += 1
                elif kwLen < dontBotherLen:
                    score -= 2

                if avgSearch == perfectSearches:
                    score += 3
                    avgSearchKey = 0
                elif avgSearch == bestSearches:
                    score += 3
                    avgSearchKey = 1
                elif avgSearch == greatSearches:
                    score += 2
                    avgSearchKey = 2
                elif avgSearch == goodSearches:
                    score += 1
                    avgSearchKey = 3
                elif avgSearch == badSearches:
                    score -= 3
                    avgSearchKey = 4
                elif avgSearch == worstSearches:
                    score -= 3
                    avgSearchKey = 5

                if comp <= bestComp and comp != 0:
                    score += 4
                elif comp <= goodComp:
                    score += 3
                elif comp <= okayComp:
                    score += 2
                elif comp <= sosoComp:
                    score += 1

                quality = returnQuality(score)

                if quality != "BAD":
                    keywordSearch = [quality, score, keyword, kwLen, avgSearchKey, comp, suggestedBid]

                    if keywordSearch not in keywordResults:
                        keywordResults.append(keywordSearch)
                        foundCount += 1

                        if quality == 'PERFECT':
                            perfects += 1
                        elif quality == 'BEST':
                            bests += 1
                        elif quality == 'GREAT':
                            greats += 1
                        elif quality == 'GOOD':
                            goods += 1
                        elif quality == 'ALRIGHT':
                            alrights += 1
                        elif quality == 'MEH':
                            mehs += 1

    print "Found: " + str(foundCount) + " results that might be good! Added to results list!"
    print "[Perfects: " + str(perfects) + "][Bests: " + str(bests) + "][Greats: " + str(greats) + "][Goods: " + str(goods) + "][Alrights: " + str(alrights) + "][Mehs: " + str(mehs) + "]"
    print "Current list size: " + str(keywordResults.__len__())
    print "----------------"


def returnStr(stringToDecode):
    daStr = binascii.b2a_hex(stringToDecode)
    daStr = binascii.unhexlify(daStr)
    filtered_string = filter(lambda x: x in string.printable, daStr)
    return filtered_string

def returnQuality(score):
    quality = 'BAD'
    if score >= 9:
        quality = 'PERFECT'
    if score == 8:
        quality = 'BEST'
    if score == 7:
        quality = 'GREAT'
    if score == 6:
        quality = 'GOOD'
    if score == 5:
        quality = 'ALRIGHT'
    if score == 4:
        quality = 'MEH'

    return quality

if __name__ == "__main__":
    main()
