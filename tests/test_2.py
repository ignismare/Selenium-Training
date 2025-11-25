from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ActionChains as actionChains
import pytest
import time, datetime



def setup(browser,headless=False):
    # create webdriver object
    driver = ()
    match browser:
        case "Chrome":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Chrome(options=options)
        case "Firefox":
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
        case "Edge": #the literal edge case
            options = webdriver.EdgeOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Edge(options=options)
        case _:
            raise Exception("Invalid browser selected")

    wait_time = WebDriverWait(driver, 10)
    return driver, wait_time

def postconditions(driver):
    driver.quit()

def roll_dice(driver, wait_time, amount):
    # pick the amount of dice select thing
    wait_time.until(
        ec.element_to_be_clickable(
            driver.find_element(by=By.XPATH, value="//select[@name='num']"))).click()

    wait_time.until(
        ec.element_to_be_clickable(
            driver.find_element(by=By.XPATH, value="//option[@value='"+amount+"']"))).click()

    # close the list
    (actionChains(driver).move_to_element(driver.find_element(by=By.XPATH, value="//select[@name='num']")).
     move_by_offset(-50, 0).click().pause(1).perform())

    # roll them dice!
    wait_time.until(
        ec.element_to_be_clickable(
            driver.find_element(by=By.XPATH, value="//input[@value='Roll Dice']"))).click()

    # we should be moving to a different site, wait for it to load
    wait_time.until(ec.url_changes("https://www.random.org/dice/"))

testdata = (["1","Chrome"],
            ["3","Chrome"],
            ["5","Chrome"],
            ["60","Chrome"],
            ["61","Chrome"], #meant to fail, see what happens
            ["1","Firefox"],
            ["3","Firefox"],
            ["5","Firefox"],
            ["60","Firefox"],
            ["60","Edge"])# edge case scenario
@pytest.mark.parametrize("amount,browser",testdata)
def test1(amount, browser, headless):
    try:
        # go to a diceroller website
        driver, wait_time = setup(browser, headless)

        driver.get("https://www.random.org/dice/")
        wait_time.until(ec.url_changes("//data:"))

        roll_dice(driver,wait_time, amount)

        # perform a test: check if the proper amount of dice were rolled:
        dice_rolled_text = driver.find_element(by=By.ID, value="invisible").find_elements(by=By.TAG_NAME, value="p")[5].text

        if dice_rolled_text.__contains__(amount):
           print("\nTest passed: correct amount of dice were rolled")
        else:
           print("\nTest failed: incorrect amount of dice were rolled")

        assert dice_rolled_text.__contains__(amount)

    finally:
        if driver is not None:
            postconditions(driver)

test1.__doc__ = "Check if the amount of dice requested by the user is rolled"
test1.site = "https://docs.google.com/document/d/1BJoX4uaeZO09HrpHbs4_pGSLRvaqMK54M8kJeftuzR8/edit?tab=t.0"
test1.results = ()

@pytest.mark.parametrize("amount",["1","3","5","60"])
def test2(amount,record_property):
    try:
        # go to a diceroller website
        driver, wait_time = setup("Chrome")

        driver.get("https://www.random.org/dice/")
        wait_time.until(ec.url_changes("//data:"))

        roll_dice(driver,wait_time, amount)

        # perform a test: check if the proper amount of dice were rolled:
        dice_results = driver.find_element(by=By.ID, value="invisible").find_elements(by=By.TAG_NAME, value="p")[6].find_elements(by=By.TAG_NAME, value="img")

        dice_sum = 0

        for result in dice_results:
            dice_sum += int(result.get_property(name="alt"))

        if int(amount) <= dice_sum <= int(amount)*6:
           print("\nTest passed: the rolled sum of numbers is within estimates, sum: ",dice_sum)
        else:
           print("\nTest failed: the rolled sum of numbers is outside the possible range, sum: ",dice_sum)

        record_property("Dice sum",dice_sum)
        assert int(amount) <= dice_sum <= int(amount)*6

    finally:
        if driver is not None:
            postconditions(driver)

test2.__doc__ = "Check if the sum of all the rolled dice falls within the expected sum for the amount of dice specified by the user"
test2.site = "https://www.random.org/dice/"
test2.results = ()

results = []
def test3():
    try:
        # go to a diceroller website
        driver, wait_time = setup("Chrome")

        driver.get("https://www.random.org/dice/")
        wait_time.until(ec.url_changes("//data:"))

        #get the current timestamp
        ts = time.time()
        start_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        t_start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d')

        #move to the results site
        roll_dice(driver, wait_time, "1")

        # get the timestamp from the website
        website_timestamp = driver.find_element(by=By.ID, value="invisible")\
            .find_elements(by=By.TAG_NAME, value="p")[7].text[11:21]
        t_website_timestamp = datetime.datetime.strptime(website_timestamp, '%Y-%m-%d')

        # compare the two timestamps
        assert t_start_time == t_website_timestamp



        # do a second check to see if two asserts in a single test are possible
        # check if the trademark date is still valid
        trademark = driver.find_element(by=By.XPATH,value = "//div[@id='invisible']/div[4]/div").text
        results.append([t_start_time, t_website_timestamp, trademark])

        assert trademark.__contains__(t_website_timestamp.year.__str__())
    finally:
        if driver is not None:
            postconditions(driver)

test3.__doc__ = "Check if the trademark for the site is still valid"
test3.site = "https://www.random.org/dice/"
test3.results = results