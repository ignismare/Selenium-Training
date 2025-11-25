# Python program to demonstrate selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains as AC


# create webdriver object
driver = webdriver.Chrome()
# get google.co.in
service = driver.service
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver.quit()
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open swtest.pl
    driver.get("https://swtest.pl/")

    # click the collapsed navbar so it opens
    navbar = driver.find_element(by=By.CLASS_NAME, value="navbar-toggle")
    navbar.click()

    # find all list items on the opened navbar
    navbar_children = driver.find_element(by=By.CLASS_NAME, value="navbar-right").find_elements(by=By.TAG_NAME,
                                                                                                value="li")

    # click the "Nasza oferta" button (wait for it to be clickable first)
    waittime_button_clickable = WebDriverWait(driver, 10)

    waittime_button_clickable.until(
        EC.element_to_be_clickable(navbar_children[2].find_element(by=By.TAG_NAME, value="a"))).click()

    #we are on a new page! wait for it to load
    waittime_button_clickable.until(EC.url_changes("https://swtest.pl/"))

    # find and click the "Integration test" button
    test_type_buttons = driver.find_elements(by=By.CLASS_NAME, value="col-xs-12")
    test_type_buttons[1].find_element(by=By.TAG_NAME, value="a").click()

    # get the first section of text and print it out in the terminal
    content_column_child = driver.find_element(by=By.XPATH, value="//div[@id='editable-426']/div[1]")
    print(content_column_child.text)
    input("Press Enter to continue...")
    #-------------------------------------------------------------------------------------------------------
    # new tasks, I want to see if I can play with the map

    # go to the Kontakt page
    # click the collapsed navbar so it opens
    navbar = driver.find_element(by=By.CLASS_NAME, value="navbar-toggle")
    navbar.click()

    # find all list items on the opened navbar
    navbar_children = driver.find_element(by=By.CLASS_NAME, value="navbar-right").find_elements(by=By.TAG_NAME,
                                                                                                value="li")
    # click the "Kontakt" button (wait for it to be clickable first)
    waittime_button_clickable.until(
        EC.element_to_be_clickable(navbar_children[4].find_element(by=By.TAG_NAME, value="a"))).click()

    # we are on a new page! wait for it to load
    waittime_button_clickable.until(EC.url_changes("https://swtest.pl/page/nasza-oferta,247/"))

    # locate the map element
    map_element = driver.find_element(by=By.XPATH,value="//div[@id='map_canvas']/div[1]")

    # click and drag on the map
    #move to the center of the map
    AC(driver).move_to_element(to_element=map_element).pause(1).perform()
    #dragging needs to be done in increments, otherwise it doesn't work
    for i in range(5):
        AC(driver).click_and_hold().move_by_offset(13, 13).pause(0.01).perform()

    AC(driver).release().move_to_element(to_element=map_element).pause(1).perform()
    for i in range(15):
        AC(driver).click_and_hold().move_by_offset(10, 10).pause(0.01).perform()
    AC(driver).release().pause(1).perform()


    # try to access streetview of wherever the map was dropped
    #move over the little yellow guy and grab him
    AC(driver).move_to_element(to_element=map_element).move_by_offset(250, 150).click_and_hold().pause(1).perform()

    # move the grabbed yellow guy over a random street and drop him
    for i in range(10):
        AC(driver).move_by_offset(-10, -10).pause(0.01).perform()
    AC(driver).release().pause(1).perform()
    input("Press Enter to continue...")



finally:
    # Close the browser
    driver.quit()