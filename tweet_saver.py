from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os, re, wget


def makefolder(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            print('Created folder ' + path + ' successfully')
        else:
            print('Folder existed')
    except Exception:
        print('Creating Folder Failed')
        driver.quit()
        exit()


def videoExsit():
    flag = False
    try:
        driver.find_element_by_xpath(
            "//div[@class='css-1dbjc4n r-1p0dtai r-1d2f490 r-u8s1d r-zchlnj r-ipm5af']//div[@class='css-1dbjc4n r-1p0dtai r-1d2f490 r-u8s1d r-zchlnj r-ipm5af']")
        flag = True
    except:
        pass
    return flag


def getvideoURL(t=5):
    try:
        tryele = WebDriverWait(driver, t).until(EC.element_to_be_clickable((By.XPATH, "//td[@id='ct3']//dd[3]")))
        video_url = tryele.find_element_by_tag_name('a').get_attribute('href')
        return video_url
    except:
        try:
            tryele = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//td[@id='ct3']//dd[2]")))
            video_url = tryele.find_element_by_tag_name('a').get_attribute('href')
            return video_url
        except:
            try:
                tryele = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, "//td[@id='ct3']//dd[1]")))
                video_url = tryele.find_element_by_tag_name('a').get_attribute('href')
                return video_url
            except Exception:
                print('\nFailed to get video URL')


def saveImg(pic_list, datetime, path):
    num = 1
    try:
        for i in pic_list:
            picName = datetime + ' ' + str(num)
            picName = re.sub(r'[\\/:*?"<>|]', '', picName) + '.jpg'
            # print(picname)
            filename = wget.download(i, path + '/' + picName)
            num += 1
            print('\nSaved tweet image', filename)
    except:
        print('\nFailed to save tweet images')
        with open("FailedList.txt", "a") as f:
            f.write(FirstUrl + '\n')
        driver.quit()
        exit()


def saveVideo(datetime, path):
    try:
        driver.get('https://lab.syncer.jp/Tool/Twitter-Video-URL-Converter/')
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'ct1'))).send_keys(FirstUrl)
        driver.find_element_by_id('ct2').click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//td[@id='ct3']")))
        video_url = getvideoURL()
        print('Video URL: ' + video_url)

        videoName = re.sub(r'[\\/:*?"<>|]', '', datetime) + '.mp4'
        print(videoName)
        filename = wget.download(video_url, path + '/' + videoName)
        print('\nSaved tweet video ', filename)

    except:
        print('\nFailed to save tweet video')
        with open("FailedList.txt", "a") as f:
            f.write(FirstUrl + '\n')
        driver.quit()
        exit()


def setTime(dataText):
    if '午後' in dataText:
        timestamp = time.mktime(time.strptime(dataText, '午後%H:%M · %Y年%m月%d日')) + 43200
    else:
        timestamp = time.mktime(time.strptime(dataText, '午前%H:%M · %Y年%m月%d日'))
    datetime = time.strftime('%Y-%m-%d %H:%M', time.localtime(timestamp))
    return datetime


def setPath(username):
    namae = re.split('\n', driver.find_elements_by_xpath('//a[@href="' + username + '"]')[1].text)[0]
    path = namae + '(@' + username + ')_Twitter'
    path = re.sub(r'[\\/:*?"<>|]', '', path)
    return path


if __name__ == '__main__':
    pic_list = []
    datetime = '0000-00-00 0000'
    path = 'save'

    print('tweet_saver')
    print('Author  :  Nakateru (2021.03.08)')
    FirstUrl = input('Input tweet URL:')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("--lang=en")
    options.add_argument(r'user-data-dir=C:\Users\[username]\AppData\Local\Google\Chrome\User Data')
    driver = webdriver.Chrome(chrome_options=options)

    PicUrl = re.split('twitter.com', FirstUrl)[1]
    username = re.split('/status/', PicUrl)[0]
    # print(PicUrl)

    dateTimeXpath = '//a[@href="' + PicUrl + '"]'
    # print(xpath)
    driver.get(FirstUrl)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, dateTimeXpath)))

    print('title：', driver.title)

    dataText = driver.find_element_by_xpath(dateTimeXpath).text
    print('post time:', dataText)

    for i in range(1, 5):
        try:
            xpath = '//*[@href="' + PicUrl + '/photo/' + str(i) + '"]'
            pic = driver.find_element_by_xpath(xpath).find_element_by_tag_name("img").get_attribute('src')
            pic = re.split('\?', pic)[0] + '?format=jpg&name=large'
            # print(pic)
            pic_list.append(pic)
        except:
            pass

    if len(pic_list) > 0:
        path = setPath(username)
        makefolder(path)
        datetime = setTime(dataText)
        # print('post time:', datetime)

        saveImg(pic_list, datetime, path)
        driver.quit()
        exit()
    else:
        print('No image in this tweet')

    if videoExsit() == True:
        path = setPath(username)
        makefolder(path)
        datetime = setTime(dataText)
        print(datetime)
        print(path)
        saveVideo(datetime, path)
        driver.quit()
        exit()
    else:
        print('No video in this tweet')
