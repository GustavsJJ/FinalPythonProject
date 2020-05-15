# Made by: Gustavs Jānis Jākobsons
from selenium import webdriver
import os
import time
import pyautogui # avots: https://automatetheboringstuff.com/chapter18/
from bs4 import BeautifulSoup # avots: https://www.youtube.com/watch?v=4UcqECQe5Kc
import json # saglabā datus par followers un following

followerList = []
followingList = []
postLikes = []

user = []


link = input("Input Instagram profile link: ")
postLink = input("Enter Instagram post link: ")
# link = https://www.instagram.com/gustavsjj/
# postLink = https://www.instagram.com/p/BiSeKGCn0BW6SG7muEpEGZeegdw6nUbsxzt_VY0/

try:

    #  ------------------------------------------------------------ Ieiet sistēmā ------------------------------------------------------------

    driver = webdriver.Chrome() # uzsāk webdriver darbību
    driver.get(link)
    driver.maximize_window()
    driver.find_element_by_class_name('-nal3').click()

    username = open("username.txt", "r").readline()
    password = open("password.txt", "r").readline()

    driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div[2]/div/div/div[1]/div/form/div[2]/div/label/input").send_keys(username) # ieraksta username
    driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div[2]/div/div/div[1]/div/form/div[3]/div/label/input").send_keys(password) # ieraksta password
    driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div[2]/div/div/div[1]/div/form/div[4]/button").click() # nospiež login

    time.sleep(4) # pagaida, kamēr ielādējās lapa
    driver.get(link) # refresho
    time.sleep(1) # pagaida, kamēr ielādējās lapa

    soup = BeautifulSoup(driver.page_source, "html.parser") # nolasa lapas source kodu
    x = soup.find_all(class_="g47SY")[1].get_text() # follower skaits
    y = soup.find_all(class_="g47SY")[2].get_text() # following skaits

    #  ------------------------------------------------------------ Followers accounts ------------------------------------------------------------

    driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a").click() # nospiež followers
    time.sleep(1)

    x = (int(x)//12)+1 # cik reizes būs jā'scroll'o lejā
    for i in range(x):
        driver.find_element_by_css_selector("div.isgrP").click()
        pyautogui.press(" ")
        pyautogui.press(" ")
        pyautogui.press(" ")
        time.sleep(0.5)

    soup = BeautifulSoup(driver.page_source, 'html.parser') # izmanto BeautifulSoup, lai ātrāk atrastu informāciju starp <tag>
    followers = soup.find(class_='PZuss').find_all("li") # sameklē informāciju par followers string formātā

    for follower in followers: # no iegūtajiem followers string formātuu pārvērš par list no dictionaries
        xd = follower.find('div').find_all('div')[2]
        username = xd.find('a').get_text()
        try:
            info = xd.find_all('div')[1].get_text()
        except:
            info = ""
        user = [
            username,
            info,
            f"https://www.instagram.com/{username}/"
        ]
        followerList.append(user)

    driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click() # beidzās darbība ar followers

    #  ------------------------------------------------------------ Following accounts ------------------------------------------------------------

    driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a").click() # nospiež following 
    time.sleep(1)

    y = (int(y)//12)+1 # cik reizes būs jā'scroll'o lejā
    for i in range(y):
        driver.find_element_by_css_selector("div.isgrP").click()
        pyautogui.press(" ")
        pyautogui.press(" ")
        pyautogui.press(" ")
        time.sleep(0.5)

    soup = BeautifulSoup(driver.page_source, 'html.parser') # izmanto BeautifulSoup, lai ātrāk atrastu informāciju starp <tag>
    followings = soup.find(class_='PZuss').find_all("li") # sameklē informāciju par followers string formātā

    for following in followings: # no iegūtajiem followers string formātu pārvērš par list no dictionaries
        xd = following.find('div').find_all('div')[2]
        username = xd.find('a').get_text()
        try:
            info = xd.find_all('div')[1].get_text()
        except:
            info = ""
        user = [
            username,
            info,
            f"https://www.instagram.com/{username}/"
        ]
        followingList.append(user)

    driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click() # beidzās darbība ar following

    #  ------------------------------------------------------------ Iegūst post datus ------------------------------------------------------------

    try:
        driver.get(postLink)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser") # nolasa lapas source kodu
        z = soup.select("button.sqdOP span")[1].get_text()


        driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div[1]/article/div[2]/section[2]/div/div[2]/button").click() # nospiež uz "laikiem"
        time.sleep(1)

        z = (int(z)//12)+2
        for i in range(z):
            soup = BeautifulSoup(driver.page_source, 'html.parser') # izmanto BeautifulSoup, lai ātrāk atrastu informāciju starp <tag>
            likers = soup.select("div.i0EQd")[0].find_all("div")[1]
            for liker in likers:
                username = liker.find_all("div")[7].get_text()
                info = liker.find_all("div")[8].get_text()
                if(info == "Follow"):
                    info = ""
                user = [
                    username,
                    info,
                    f"https://www.instagram.com/{username}/"
                ]
                if user not in postLikes:
                    postLikes.append(user)

            driver.find_element_by_css_selector("div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd div div:nth-child(1)").click()
            pyautogui.press(" ")
            pyautogui.press(" ")
            time.sleep(0.5)

        driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click() # beidzās darbība ar post
    except:
        print("Post link is not valid")

    #  ------------------------------------------------------------ Apstrādā datus ------------------------------------------------------------

    driver.quit() # beidz webdriver darbību

    x = json.dumps(followerList)
    open("followerList.txt","w").write(x)
    x = json.dumps(followingList)
    open("followingList.txt","w").write(x)
    x = json.dumps(postLikes)
    open("postLikes.txt","w").write(x)

    print("Data scraped")


except:
    print("Error")


os.system("pause") # aptur programmu
