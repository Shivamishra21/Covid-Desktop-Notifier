def Scrap():
    #stuff that notification will contain
    def notifyme(title,message):
        plyer.notification.notify(
            title = title,
            message = message,
            app_icon = "vv.ico",
            timeout = 20
        )
    url = 'https://www.worldometers.info/coronavirus/'
    r = requests.get(url)
    #to parse data in html
    soup = BeautifulSoup(r.content, 'html.parser')
    tablebody = soup.find('tbody')
    tr = tablebody.find_all('tr')
    #to get the name of country enterred.
    notifyCountry = countryData.get()
    if(notifyCountry ==""):
        notifyCountry = 'india'
    countries,totalCases,newCases,totalDeaths,newDeaths,totalReacovered,activeCases =[],[],[],[],[],[],[]
    serious,totalCasesPerMillion,totalDeathsPerMillion,totalTests,totalTestsPerMillion = [],[],[],[],[]
    headers = ['Countries','Total Cases','New Cases','Total Deaths','New Deaths','Total Recovered','Active Cases','Serious','Total Cases Per Million','Total Deaths Per Million','Total Tests','Total Tests Per Million']

    for i in tr:
        id = i.find_all('td')
        #formatting data according to our requirement
        if(id[1].text.strip().lower() == notifyCountry):
            totalCases1 = int(id[2].text.strip().replace(",",""))
            totalDeaths1 = id[4].text.strip()
            newCases1 = id[3].text.strip()
            newDeaths1 = id[5].text.strip()
            notifyme('Corona virus Details In {}'.format(notifyCountry),
                     'Total Cases : {}\nTotal Deaths : {}\nNew Cases : {}\nNew Death : {}'.format(totalCases1,
                                                                                                 totalDeaths1,
                                                                                                 newCases1,
                                                                                                 newDeaths1))
        countries.append(id[1].text.strip())
        totalCases.append(int(id[2].text.strip().replace(',','')))
        newCases.append((id[3].text.strip()))
        totalDeaths.append((id[4].text.strip()))
        newDeaths.append((id[5].text.strip()))
        totalReacovered.append((id[6].text.strip()))
        activeCases.append((id[7].text.strip()))
        serious.append((id[8].text.strip()))
        totalCasesPerMillion.append((id[9].text.strip()))
        totalDeathsPerMillion.append((id[10].text.strip()))
        totalTests.append((id[11].text.strip()))
        totalTestsPerMillion.append((id[12].text.strip()))
        #to make data in tabular form
        df = pd.DataFrame(list(zip(countries,totalCases,newCases,totalDeaths,newDeaths,totalReacovered,activeCases,serious,
                                   totalCasesPerMillion,totalDeathsPerMillion,totalTests,totalTestsPerMillion)),columns=headers)
    #to sort value on the basis of total cases
    sor = df.sort_values('Total Cases',ascending=False)
    for i in formatlist:
        #to check which button is clicked to recieve data either in json ,csv or html
        if(i == 'html'):
            path2 = '{}/alldata.html'.format(path)
            sor.to_html(r'{}'.format(path2))
        if (i == 'json'):
            path2 = '{}/alldata.json'.format(path)
            sor.to_json(r'{}'.format(path2))
        if (i == 'csv'):
            path2 = '{}/alldata.csv'.format(path)
            sor.to_csv(r'{}'.format(path2))

    #to show where data is stored on your system
    if(len(formatlist) != 0):
        messagebox.showinfo("Notification","Corona data is stored to {}".format(path2),parent=root)


# to download the data in different formats
def download():
    global path
    if(len(formatlist)!=0):
        #Prompt user to select a directory
        path  = filedialog.askdirectory()
    else:
        pass
    Scrap()
    formatlist.clear()
    inHTML.configure(state = "normal")
    inCSV.configure(state="normal")
    JSON.configure(state="normal")
def inhtml():
    formatlist.append('html')
    inHTML.configure(state = 'disabled')

def incsv():
    formatlist.append('csv')
    inCSV.configure(state = 'disabled')

def injson():
    formatlist.append('json')
    JSON.configure(state = 'disabled')

import  plyer
#Plyer is a Python library for accessing features of your hardware / platforms.

import requests
#Thismodule allows  to send HTTP requests using Python.

from bs4 import BeautifulSoup
#This  library makes it easy to scrape information from web pages.
#It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree.

from tkinter import *
from tkinter import messagebox ,filedialog
#Tkinter for creating gui.
#messagebox -> to display message box
#filedialog ->  provides classes and factory functions for creating file/directory selection windows.

import pandas as pd
#Pandas  library  is used for data analysis.
root = Tk()
root.title("COVID Info")
root.geometry('680x400+200+80')

formatlist = []
path = ''

root.configure(bg = 'beige')
root.iconbitmap('Everaldo-Crystal-Clear-App-virus-detected.ico')

###LABELS###
introLabel = Label(root,text='COVID Info',font = ("Bell MT",30,'bold' ),bg = 'orange',width = 29).grid(row=0, column=0)


entryLabel = Label(root,text='Notify Country:',font = ("Bell MT" , 30 , 'bold' ),bg =  'beige')
entryLabel.place(x=5,y=60)

entryLabel = Label(root,text='Download In:',font = ("Bell MT" , 30 , 'bold' ),bg =  'beige')
entryLabel.place(x=5,y=120)

###ENTRY###
countryData = StringVar()
entry = Entry(root,textvariable = countryData,font =('Comic Sans MS',20,'italic'),relief=RIDGE,bd=5,width = 20)
entry.place(x=295,y=68)

###BUTTONS###
inHTML = Button(root,text = "HTML",bg = "green", font=('Bett MT',15,'bold'),relief=RIDGE ,activebackground='blue',activeforeground = 'white',bd = 5,width = 7,command= inhtml)
inHTML.place(x=260,y=130)

inCSV = Button(root,text = "CSV",bg = "green", font=('Bett MT',15,'bold'),relief=RIDGE ,activebackground='blue',activeforeground = 'white',bd = 5,width = 7,command = incsv)
inCSV.place(x=390,y=130)

JSON = Button(root,text = "JSON",bg = "green", font=('Bett MT',15,'bold'),relief=RIDGE ,activebackground='blue',activeforeground = 'white',bd = 5,width = 5,command = injson)
JSON.place(x=520,y=130)
###SUBMIT BUTTON###
submit = Button(root,text = "Submit",bg = "green", font=('Bett MT',15,'bold'),relief=RIDGE ,activebackground='red',activeforeground = 'white',bd = 5,width = 15 ,command = download)
submit.place(x=230,y=300)
root.mainloop()