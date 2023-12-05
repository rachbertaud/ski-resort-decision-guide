
#Check out this cool site for hitting the mountain! --  https://www.onthesnow.com/ikon-pass/skireport

from datetime import date
import datetime
import requests


def websoup():
    URL = "https://www.onthesnow.com/ikon-pass/skireport"
    r = requests.get(URL)
    #print(r.text)
    return r.text


def soupfinder(resortName,textt):

    whatToFInd='"title":"'+resortName
    int2 = textt.find(whatToFInd)
    textt2 = textt[int2:int2+700]

    int3 = textt2.find('currentWeather')
    textt3 = textt2[int3:int3+100]

    int7 = textt3.find('min')
    low = textt3[int7 + 5:int7 + 11]
    if "-" in low:
        low = int(only_numerics(low)) * -1
    else:
        low = int(only_numerics(low))
    int8 = textt3.find('max')
    high = textt3[int8 + 5:int8 + 10]
    if "-" in high:
        high = int(only_numerics(high))*-1
    else:
        high = int(only_numerics(high))

    temp = (high/10+low/10)/2
    temp = temp+5
    temp = (temp*(9/6))+32

    int1 = textt2.find('openPercent')
    openPercent = textt2[int1+11:int1 + 15]

    int4 = textt2.find('"type":"')
    weatherDesc = textt2[int4+8:int4 + 29]
    int44 =weatherDesc.find('"')
    weatherDesc = weatherDesc[:int44]

    int5 = textt2.find('last24')
    last24 = textt2[int5+7:int5 + 11]

    int6 = textt2.find('base')
    base = textt2[int6+6:int6 + 9]

    print(resortName)
    #print('textt2 =',textt2)
    #print(textt3)
    #print("Temp dd=",temp)
    #print('WeatherType =',weatherDesc)
    #print('base =',int(only_numerics(base))/2)
    #print('last24 =',last24)
    #print('open percentage =',only_numerics(openPercent))
    #print("\n")
    datalist=[int(only_numerics(openPercent)),int(only_numerics(base))/2,int(only_numerics(last24)),int(temp),2]
    return datalist

def only_numerics(seq):
    seq_type= type(seq)
    num = seq_type().join(filter(seq_type.isdigit, seq))
    if num == "":
        return 0
    else:
        return num

def map_range(x, in_min, in_max, out_min, out_max):
    t=1
    if x > in_max:
        t = out_max
    if x < in_min:
         t = out_min
    if in_min < x < in_max:
        t = (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
    return t


def intro():
    print('Hello, do ya want to go skiing today!!!')
    str=input('yes or no?')
    if str == 'yes':
        return True
    else:
        print('you monster!')
        return False


def MajicOracle(textt,gnarlist,inputList,trafficlist,AdjustCoef):
    #AdjustCoef |Gnar|base depth |24 hour |temp|traffic
    score=[1,1,1,1,1]

    #inputrangeList
    i =0
    for i in range(len(inputList)):
        #print(soupfinder(inputList[i],textt),gnarlist,i)
        score[i]=Gnnarly(soupfinder(inputList[i],textt),gnarlist,i,trafficlist,AdjustCoef)
        i+1

    print(score)
    return score

def Gnnarly(datalist,gnarlist,i,trafficlist,AdjustCoef):
    print("datalist =", datalist)
    gnar=datalist[0]
    rangeList = [[1,500],[10,100],[0,120],[10,40],[60,400]]
    if not gnar:
        gnar=10
    gnar=(gnar)*gnarlist[i] #i
    gnar= map_range(gnar,rangeList[0][0],rangeList[0][1],1,100)
    gnar = gnar * AdjustCoef[0]
    print("gnar =", gnar)

    base = datalist[1]
    base= map_range(base,rangeList[1][0],rangeList[1][1],1,100)
    base = base * AdjustCoef[1]
    print("base =", base)

    dailysnow = datalist[2]
    dailysnow = map_range(dailysnow, rangeList[2][0], rangeList[2][1], 1, 100)
    dailysnow = dailysnow * AdjustCoef[2]
    print("dailysnow =", dailysnow)

    temp = datalist[3]
    temp = map_range(temp, rangeList[3][0], rangeList[3][1], 1, 100)
    temp = temp * AdjustCoef[3]

    print("temp =", temp)

    traffic = trafficlist[i]
    traffic = map_range(traffic, rangeList[4][0], rangeList[4][1], 1, 100)
    traffic = traffic * AdjustCoef[4]
    print("traffic =", traffic)

    score = gnar+base+dailysnow+temp-traffic
    print("score =", score)
    print("\n")
    return score

def WhatDayIsIt():
    today = date.today()
    # mm/dd/y
    d3 = today.strftime("%m/%d/%y")
    #print("the date is =", d3)
    weekno = datetime.datetime.today().weekday()
    if weekno < 5:
        return False
    else:
        return True

if __name__ == '__main__': #main name
    textt = websoup()
    #print (textt) #if you dare
    inputList = ['Aspen Snowmass','Arapahoe Basin Ski Area','Copper Mountain','Eldora Mountain Resort','Steamboat']
    AdjustCoef = [8,10,10,2,6] #adjustment for the 5 catagories -- | Gnar | base depth |24 hour |temp|traffic
    gnarlist =[6,8,7,2,5] # how gnar it be

    rangeList = [[1, 10], [10, 100], [0, 12], [-10, 60]] #reasonable range of 5 catagories, not extremes

    if(WhatDayIsIt):
        trafficlist = [274, 145, 154, 102, 250]  # minutes
        #print("weekday traffic :)", trafficlist)
    else:
        trafficlist = [360, 195, 194, 122, 300]  # minutes +weekend traffic
        #print("weekend traffic :(",trafficlist)

    if intro():
        score = MajicOracle(textt,gnarlist,inputList,trafficlist,AdjustCoef) # ~ call ~~ upon ~~~ the ~~~~ oracle ~~~~~
        print("Cool Resorts",inputList)
        int1=max(score)
        int2=score.index(int1)
        CoolestResort=inputList[int2]
        texttt ="Allegedly, ",CoolestResort," is cooler then a Polar Bears' toenails on this festive day"
        coolist = soupfinder(CoolestResort,textt)



        print("\n")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~****MaJic^^sno^^@racLe****~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        print(texttt)
        print('base =',coolist[1],"in of knot pow")
        print('last24 =',float(coolist[2])/10,"in of pow")
        print('open percentage =',coolist[0])

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~***Now Quest For The POW***~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    #end python

#concidered resorts
#eldora, abasisn, copper, steamboat, winterpark

#other names : add name, traffic, and gnarr, search textt for other names.

#"Mammoth Mountain"
#"Jackson Hole"

#assume, drive from ft collins, ikon pass

#https://www.onthesnow.com/ikon-pass/skireport