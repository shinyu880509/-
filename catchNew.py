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
    a = 0
    while True:
        news = driver.find_elements_by_xpath("//body[@id='gsr']/div[@id='main']/div[@id='cnt']/div[@class='mw']/div[@id='rcnt']/div[@class='col']/div[@id='center_col']/div[@id='res']/div[@id='search']/div/div[@id='rso']/div")
        for n in news:
            nDate = n.find_elements_by_tag_name("span")
            source = nDate[0].text
            rDate = nDate[2].text
            date = rDate.split(' ')
            x = datetime.datetime.now()
            if (len(date[0]) <= 3):
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
                date = nDate[2].text

            #n = n.find_element_by_class_name("JheGif nDgy9d")
            nHref = n.find_element_by_tag_name("a")
            aa = n.text.split("\n")
            print(aa[0])
            print(aa[1])
            print(aa[2])
            print(aa[3] + "\n")
            
            finalTitle.append(aa[1])
            finalSource.append(aa[0])
            finalDate.append(date)
            finalUrl.append(nHref.get_attribute('href'))
            #print(f"{n.text} --- {source,nDate[2].text} --- {nHref.get_attribute('href')}\n")
        try:
            driver.find_element_by_xpath("//a[@id='pnnext']//span[2]").click()
            a += 1
            time.sleep(1)
            if a == 3:
                break

        except Exception as e:
            break
        

    with open ('news/' + stockID[i] + '.csv', 'w', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['標題', '來源', '日期', '網址'])
        for t, s, d, u in zip(finalTitle, finalSource, finalDate, finalUrl):
            try:
                w.writerow([t, s, d, u])
            except Exception  as e:
                pass

driver.close()


