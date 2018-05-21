import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import json
import requests

quote_page = 'https://www.cs.duke.edu/people/undergraduates'
duke_page = 'https://api.colab.duke.edu/identity/v1/'

page = urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
undergradList = soup.find_all('span',attrs={'class':'name'})
writer = pd.ExcelWriter('index.xlsx',engine='xlsxwriter')

fnameList = []
lnameList = []
netidList = []
emailList = []
gradYearList = []
for people in undergradList:
    peopleList = people.text.split(',')
    fullName = (peopleList[1]+' '+peopleList[0]).strip()
    firstName = peopleList[1].strip()
    lastName = peopleList[0].strip()
    fnameList.append(firstName)
    lnameList.append(lastName)

dukeEmailList = soup.find_all('span',attrs={'class':'email'})
index = 0
for email in dukeEmailList:
    dukeEmail = email.text.split(' ')
    dukeNetID = dukeEmail[0].strip()
    r = requests.get(duke_page+dukeNetID,headers={'x-api-key':'nav-talent'})
    try:
        gradYear = r.json().get('gradYear').split(' ')[0]
        email = r.json().get('mail')
        fName = r.json().get('displayName').split(' ')[0]
        lName = r.json().get('displayName').split(' ')[1]
    except:
        gradYear = "ERROR"
        email = "ERROR"
        fName = "ERROR"
        lName = "ERROR"
    emailList.append(email)
    netidList.append(dukeNetID)
    gradYearList.append(gradYear)
    index+=1
    print(email+' '+gradYear+" "+str(index))

df = pd.DataFrame({'First Name':fnameList,'Last Name':lnameList,'NetID':netidList,'Email':emailList,'Grad Year':gradYearList})
df.to_excel(writer,sheet_name='Sheet1',index=False)
writer.save()
