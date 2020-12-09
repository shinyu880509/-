from selenium import webdriver
import datetime
import csv
from selenium.webdriver.common.keys import Keys
import getID
import time

finalTitle = []
finalUrl = []
finalDate = []
finalSource = []

driver = webdriver.Chrome('chromedriver.exe')
a = getID.getNameData()
stockName = a[1]
stockID = a[0]
for i in range(len(stockName)):
    print(stockName[i])
    url=f"https://www.google.com/search?q={stockName[i]}+股市&tbm=nws&sxsrf=ALeKk00px9DH69ke8UmCgKCvdeoUjr8tUA:1595993782566&ei=tu4gX9SIIqiQr7wPiI-QmAw&start=0&sa=N&ved=0ahUKEwjUu-STxPHqAhUoyIsBHYgHBMM4PBDy0wMIZA&biw=1920&bih=937&dpr=1"
    driver.get(url)
    aa = 0
    while True:
        news = driver.find_elements_by_xpath("//body/div[@id='main']/div[@id='cnt']/div[9]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div")
        newsdata = news[0].text
        newsdata = newsdata.split("\n")
        hh = news[0].find_element_by_tag_name("a")
        h = hh.get_attribute('href')
        for j in range(len(news)):
            newsdata = news[j].text
            newsdata = newsdata.split("\n")
            hh = news[j].find_element_by_tag_name("a")
            finalSource.append(newsdata[0])
            finalTitle.append(newsdata[1])
            finalUrl.append(hh.get_attribute('href'))
            date = newsdata[3].split(' ')
            x = datetime.datetime.now()
            if (len(date) == 2):
                if (date[1] == '小時前'):
                    if (x.hour-int(date[0]) > 0):
                        date = str(x.year) + '年' + str(x.month) + '月' + str(x.day) + '日'
                    else:
                        date = str(x.year) + '年' + str(x.month) + '月' + str(x.day-1) + '日'
                elif (date[1] == '分鐘前'):
                    if ((x.hour*60) + (x.minute) - int(date[0]) > 0):
                        date = str(x.year) + '年' + str(x.month) + '月' + str(x.day) + '日'
                    else:
                        date = str(x.year) + '年' + str(x.month) + '月' + str(x.day-1) + '日'
                elif (date[1] == '秒鐘前'):
                    date = str(x.year) + '年' + str(x.month) + '月' + str(x.day) + '日'
                elif (date[1] == '天前'):
                    if (x.day - int(date[0]) > 0):
                        date = str(x.year) + '年' + str(x.month) + '月' + str(x.day- int(date[0])) + '日'
                    elif (x.month-1 > 0):
                        date = str(x.year) + '年' + str(x.month-1) + '月' + str(x.day- int(date[0]) + 30) + '日'
                    else:
                        date = str(x.year-1) + '年' + str(12) + '月' + str(x.day- int(date[0]) + 30) + '日'
                elif (date[1] == '週前'):
                    if (x.day - (int(date[0])*7) > 0):
                        date = str(x.year) + '年' + str(x.month) + '月' + str(x.day- (int(date[0])*7)) + '日'
                    elif (x.month-1 > 0):
                        date = str(x.year) + '年' + str(x.month-1) + '月' + str(x.day- (int(date[0])*7) + 30) + '日'
                    else:
                        date = str(x.year-1) + '年' + str(12) + '月' + str(x.day- (int(date[0])*7) + 30) + '日'
                elif (date[1] == '個月前'):
                    if (x.month - int(date[0]) > 0):
                        date = str(x.year) + '年' + str(x.month-int(date[0])) + '月' + str(x.day) + '日'
                    else:
                        date = str(x.year-1) + '年' + str(x.month-int(date[0])+12) + '月' + str(x.day) + '日'
            else:
                date = newsdata[3]
            finalDate.append(date)
        try:
            driver.find_element_by_xpath("//a[@id='pnnext']//span[2]").click()
            aa += 1
            time.sleep(100)
            if aa == 3:
                break

        except Exception as e:
            break
        
    print(stockID[i])
    with open ('news/' + stockID[i] + '.csv', 'w', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['標題', '來源', '日期', '網址'])
        
        for t, s, d, u in zip(finalTitle, finalSource, finalDate, finalUrl):
            try:
                w.writerow([t, s, d, u])
            except Exception  as e:
                pass
    finalTitle = []
    finalSource = []
    finalDate = []
    finalUrl = []

driver.close()


