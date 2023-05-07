from flask import Flask, render_template, url_for, request, redirect
from bs4 import BeautifulSoup
import requests
import random
import os

##fun temperature game, scrapes weather data from timeanddate.com such as text and images

def countryList():
    website = "https://www.timeanddate.com/weather/?sort=1"

    html_text = requests.get(website).text
    soup = BeautifulSoup(html_text, 'html.parser')
    thestr = soup.find_all('td')
    newlist = list(str(thestr))
    countrylist = []
    for i in range(len(newlist)-10):
        if newlist[i]+newlist[i+1]+newlist[i+2]+newlist[i+3]+newlist[i+4]=='href=':
            while newlist[i]!='>':
                i+=1
            i+=1
            countrystring = ''
            while newlist[i]!='<':
                countrystring += newlist[i]
                i+=1
            countrylist.append(countrystring)
    return countrylist

def pickCountry(allcountries):
    return allcountries[random.randint(0,len(allcountries))]


def tempfind(region):
    website = "https://www.timeanddate.com/weather/?sort=1"
    html_text = requests.get(website).text
    soup = BeautifulSoup(html_text, 'html.parser')
    thestr = soup.find_all('td')
    newlist = list(str(thestr))
    thereg = list(region)
    for i in range(len(newlist)-10):
        j=0
        while newlist[i+j] == thereg[j]:
            j+=1
            if j == len(thereg):
                while newlist[i] != "°":
                    i+=1
                i-=2
                tempstring = ''
                while newlist[i] != ">":
                    tempstring = newlist[i]+tempstring
                    i-=1
                return tempstring

def imageget1(theurl):

    url = theurl

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    images = soup.find_all('img')
    j=0
    for image in images:
        try:
            name = image['alt']
        except:
            name = str(j)
            j+=1
        link = image['src']
        if j == 2:
            with open(name+'.png', 'wb') as f:
                im = requests.get('https:'+link)
                f.write(im.content)
                print('something written')
                break

def imageget2(theurl):

    url = theurl

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    images = soup.find_all('img')
    j=1
    for image in images:
        try:
            name = image['alt']
        except:
            name = str(j)
            j+=1
        link = image['src']
        if j == 3:
            with open(name+'.png', 'wb') as f:
                im = requests.get('https:'+link)
                f.write(im.content)
                print('something written')
                break

def urlget(thecountry):
    fstring = ''
    newstring = str(thecountry)
    newlist = list(newstring)
    for i in range(len(newlist)):
        if newlist[i] == ',':
            j = -1
            while i+j >= 0:
                fstring = newlist[i+j] + fstring
                j-=1
            break
    fstring = 'https://www.timeanddate.com/weather/'+fstring
    return fstring



##countries = countryList()
##randomcountry = pickCountry(countries)
##regtemp = tempfind(randomcountry)
##print(regtemp)

app = Flask(__name__)

global score
score = 0

def resetscore():
    global score
    score = 0

def addscore():
    global score
    score+=1

@app.route('/')
def homepg():
    return render_template('homepage.html')

@app.route('/play/')
def index():

    countries = countryList()

    country1= pickCountry(countries)
    temp1 = tempfind(country1)

    country2 = pickCountry(countries)
    temp2 = tempfind(country2)

    resetscore()

    global tempOne
    tempOne = temp1
    global tempTwo
    tempTwo = temp2
    global countryOne
    countryOne = country1
    global countryTwo
    countryTwo = country2

    if os.path.exists('1.png'):
        os.remove('1.png')
    if os.path.exists('2.png'):
        os.remove('2.png')

    url1 = urlget(countryOne)
    url2 = urlget(countryTwo)

    imageget1(url1)
    imageget2(url2)

    if os.path.exists('static/images/1.png'):
        os.remove('static/images/1.png')
    if os.path.exists('static/images/2.png'):
        os.remove('static/images/2.png')
    
    if os.path.exists('1.png'):
            os.rename('1.png','static/images/1.png')
    if os.path.exists('2.png'):
        os.rename('2.png','static/images/2.png')



    return render_template('index.html',country1=str(country1),temp1 = str(temp1),country2=str(country2),score=str(score))

@app.route('/play/lost/')
def templates():
    return render_template('lostpage.html')

@app.route('/play/higher/')
def delete():
    

    global tempOne
    global tempTwo
    global countryOne
    global countryTwo

    print(countryOne)
    print(tempOne)
    print(countryTwo)
    print(tempTwo)

    if int(tempTwo) >= int(tempOne):
        addscore()

        countries = countryList()

        country1= countryTwo
        temp1 = tempTwo

        country2 = pickCountry(countries)
        temp2 = tempfind(country2)

        tempOne = temp1
        tempTwo = temp2


        countryOne = country1
        countryTwo = country2

        if os.path.exists('1.png'):
            os.remove('1.png')
        if os.path.exists('2.png'):
            os.remove('2.png')

        url1 = urlget(countryOne)
        url2 = urlget(countryTwo)

        imageget1(url1)
        imageget2(url2)
        if os.path.exists('static/images/1.png'):
            os.remove('static/images/1.png')
        if os.path.exists('static/images/2.png'):
            os.remove('static/images/2.png')
        
        if os.path.exists('1.png'):
            os.rename('1.png','static/images/1.png')
        if os.path.exists('2.png'):
            os.rename('2.png','static/images/2.png')

        return render_template('index.html',country1=str(country1),temp1 = str(temp1),country2=str(country2),score=str(score))
    else:
        return render_template('lostpage.html', score = str(score), region1 = str(countryTwo), tempTwo = str(tempTwo))

@app.route('/play/lower/')
def update():

    global tempOne
    global tempTwo
    global countryOne
    global countryTwo

    print(countryOne)
    print(tempOne)
    print(countryTwo)
    print(tempTwo)

    if int(tempTwo) <= int(tempOne):
        addscore()

        countries = countryList()

        country1= countryTwo
        temp1 = tempTwo

        country2 = pickCountry(countries)
        temp2 = tempfind(country2)

        tempOne = temp1
        tempTwo = temp2

        countryOne
        countryTwo


        countryOne = country1
        countryTwo = country2

        if os.path.exists('1.png'):
            os.remove('1.png')
        if os.path.exists('2.png'):
            os.remove('2.png')

        url1 = urlget(countryOne)
        url2 = urlget(countryTwo)

        imageget1(url1)
        imageget2(url2)

        if os.path.exists('static/images/1.png'):
            os.remove('static/images/1.png')
        if os.path.exists('static/images/2.png'):
            os.remove('static/images/2.png')

        if os.path.exists('1.png'):
            os.rename('1.png','static/images/1.png')
        if os.path.exists('2.png'):
            os.rename('2.png','static/images/2.png')

        return render_template('index.html',country1=str(country1),temp1 = str(temp1),country2=str(country2),score=str(score))
    else:
        return render_template('lostpage.html', score = str(score), region1 = str(countryTwo), tempTwo = str(tempTwo))

try:
    os.mkdir(os.path.join(os.getcwd(), 'static\images'))
except:
    pass
os.chdir(os.path.join(os.getcwd(), ''))
print(os.getcwd())

if __name__ == "__main__":
    app.run(debug=True)