from bs4 import BeautifulSoup
import re
import csv
import os
from tkinter.filedialog import askdirectory



#generate ids to search by
preamble = "ContentPlaceHolder1_gvVendorList_"
labels = ["hlCompanyName", "lblPhoneNumber", "lblFaxNumber", "hlEmail"]

#initialize global variables
namePhoneFaxEmail = []

def addPageContent(pathToPage):
    #initialize local variables
    CompanyNames = []
    i = 0

    #open and parse target file
    f = open(pathToPage)
    soup = BeautifulSoup(f, 'html.parser')

    #used to find element by id in page
    def returnByID(targetID):
        return(soup.find(id=targetID))

    #get length of dataset for number of times to loop
    for a in soup.findAll(id=re.compile("^ContentPlaceHolder1_gvVendorList_hlCompanyName_\d+")):
        CompanyNames.append(a.text)

    #the magic
    for name in CompanyNames:
        currentRow = []
        for label in labels:
            a = soup.find(id=(preamble + label + f"_{i}")) #assemble id to search with, and find that element
            try:
                currentRow.append(a.text)
            except:
                currentRow.append("N/A")
        namePhoneFaxEmail.append(currentRow)
        i+=1

def writeListToCSV(writeToFile, writeFromList):
    with open(writeToFile, mode='w', newline='') as test:
        testWrite = csv.writer(test, delimiter=',')
        for entry in writeFromList:
            testWrite.writerow(entry)

#specify file directory **Have only the tables in the directory** 
directoryPath = askdirectory() #prompt user to select directory of pages, alternatively use directoryPath = os.path.join('.','Pages') to hard code it
pages = os.listdir(path=directoryPath)

for page in pages:
    addPageContent(os.path.join(directoryPath, page))

destinationPath = os.path.join('.','HUB List.csv')
writeListToCSV(destinationPath, namePhoneFaxEmail)

print("done")

