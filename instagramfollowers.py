from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from explicit import waiter, XPATH
from bs4 import BeautifulSoup
import time


driver = webdriver.Chrome()


def login(driver, user, pwd):

    driver.get("https://www.instagram.com/accounts/login/")

    # find and write in input fields to login
    waiter.find_write(driver, "//div/input[@name='username']", user, by=XPATH)
    waiter.find_write(driver, "//div/input[@name='password']", pwd, by=XPATH)
    # submit
    waiter.find_element(driver, "//div/button[@type='submit']", by=XPATH).click()

    # waits until the homepage loads before exiting function
    waiter.find_element(driver, "//a/span[@aria-label='Find People']", by=XPATH)


def getFollowers(driver):
    driver.get("https://www.instagram.com/ali.alaoui12/")

    numFollowers = int(waiter.find_element(driver, "//li[2]/a/span", by=XPATH).text) # li[2] refers to second li in structure
    print("You have " + str(numFollowers) + " followers")

    waiter.find_element(driver, "//a[@href='/ali.alaoui12/followers/']", by=XPATH).click()
    dialog = waiter.find_element(driver, "//div[@role='dialog']/div[2]/ul", by=XPATH)  # makes sure followers have loaded. select ul in div with role of dialog
    dialog.click()

    units = waiter.find_elements(driver, "//div[@role='dialog']/div[2]/ul/div/li", by=XPATH)
    numUnits = len(units)
    print("There are " + str(numUnits) + " followers per scroll.")

    scrollFinished = False
    sameCounter = 0  # makes sure we should truly stop scrolling, once this reaches 5 we stop

    while(scrollFinished is False and (numFollowers > 12)):  # no need to scroll if numfollowers is 12 or less
        followers = waiter.find_elements(driver, "//div[@role='dialog']/div[2]/ul/div/li", by=XPATH)
        lastFollower = len(followers) - 1

        dialog.click()  # ensures dialog is focused
        try:
            driver.execute_script("arguments[0].scrollIntoView();", followers[lastFollower])
        except StaleElementReferenceException:  # in case an element reloads, we're "taking a breather"
            time.sleep(3.5)
            continue

        if(lastFollower > 12 and lastFollower == oldLastFollower):  # only stop when it has loaded all followers
            sameCounter = sameCounter + 1
            if(sameCounter == 5):
                scrollFinished = True  # to avoid any bugs

        oldLastFollower = lastFollower
        time.sleep(.5)

    units = waiter.find_elements(driver, "//div[@role='dialog']/div[2]/ul/div/li", by=XPATH)
    numUnits = len(units)
    print("To confirm, you have " + str(numUnits) + " followers.")

    followers = parseHTML()
    print(len(followers))
    return followers


def getFollowing(driver):
    driver.get("https://www.instagram.com/ali.alaoui12/")
    numFollowing = int(waiter.find_element(driver, "//li[3]/a/span", by=XPATH).text)

    print("You are following " + str(numFollowing) + " people")

    waiter.find_element(driver, "//a[@href='/ali.alaoui12/following/']", by=XPATH).click()
    dialog = waiter.find_element(driver, "//div[@role='dialog']/div[2]/ul", by=XPATH)
    dialog.click()

    units = waiter.find_elements(driver, "//div[@role='dialog']/div[2]/ul/div/li", by=XPATH)
    numUnits = len(units)
    print("There are " + str(numUnits) + " followers per scroll.")

    scrollFinished = False
    sameCounter = 0

    while(scrollFinished is False and (numFollowing > 12)):  # no need to scroll if numfollowers is 12 or less
        following = waiter.find_elements(driver, "//div[@role='dialog']/div[2]/ul/div/li", by=XPATH)
        lastFollowing = len(following) - 1

        dialog.click()

        try:
            driver.execute_script("arguments[0].scrollIntoView();", following[lastFollowing])
        except StaleElementReferenceException:  # in case an element reloads, we're "taking a breather"
            time.sleep(3.5)
            continue

        if(lastFollowing > 12 and lastFollowing == oldLastFollowing):
            sameCounter = sameCounter + 1
            if(sameCounter == 5):
                scrollFinished = True  # to avoid any bugs

        oldLastFollowing = lastFollowing
        time.sleep(.5)

    following = parseHTML()
    print(len(following))
    return following

def parseHTML():  # now we parse!
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    followList = soup.findAll('li', attrs={'class': 'wo9IH'})

    followsDict = {}
    for row in followList:
        data = row.div.findAll("div")[2]
        username = data.find("a").text.strip()
        fullName = data.find('div', attrs={'class': 'wFPL8'}).text.strip()

        followsDict[username] = fullName

    return followsDict


user = input("Enter your instagram username")  # user and password
pwd = input("Enter your Instagram password")

login(driver, user, pwd)
followers = getFollowers(driver)
following = getFollowing(driver)

nonFollowers = {}  # those you follow that don't follow back


for x in following:
    followsBack = False  # tracks whether following follows back
    for y in followers:
        if(x == y):
            followsBack = True
    if(followsBack is False):
        nonFollowers[x] = following[x]

print("These people do not follow you back:")
for key in nonFollowers:
    print("Username: " + key + " Name: " + nonFollowers[key])
