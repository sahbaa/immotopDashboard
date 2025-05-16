from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
# ,minsurf,maxsurf,minbde,maxbed
def get_date (isrent,minsurf,maxsurf,minbed,maxbed):

    myOptions = Options()
    myOptions.add_argument('--start-maximized')
    myOptions.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=myOptions)
    driver.get('https://www.immotop.lu/en/vente-maisons-appartements/luxembourg-pays/?criterio=rilevanza')
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div.nd-select__value'))).click()
    # driver.find_element(By.CSS_SELECTOR,'div[class*="nd-stackItem"]').click()
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div[class*="nd-stackItem"]')))
    items_isrent = driver.find_elements(By.CSS_SELECTOR,'div[class*="nd-stackItem"]')
    for item in items_isrent :

        if item.text == isrent :
            print(item.text)
            item.click()
        else:
            continue    
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Surface")]'))
    ).click()    
    time.sleep(3)
    
    from_input = driver.find_element(By.XPATH, '//input[@placeholder="From"]')
    to_input = driver.find_element(By.XPATH, '//input[@placeholder="To"]')
    from_input.clear()
    from_input.send_keys(minsurf)
    to_input.clear()
    to_input.send_keys(maxsurf)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button.nd-button.nd-button--accent.nd-button--block'))).click()
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//div[contains(text(),"Bedrooms")]'))).click()
    bed_from_input = driver.find_element(By.XPATH,
                                         '//div[contains(text(), "Bedrooms")]/ancestor::div[contains(@class, "nd-select")]//input[@placeholder="From"]')
    bed_to_input = driver.find_element(By.XPATH,'//div[contains(text(), "Bedrooms")]/ancestor::div[contains(@class, "nd-select")]//input[@placeholder="To"]')

    bed_from_input.clear()
    bed_from_input.send_keys(minbed)
    bed_to_input.clear()
    bed_to_input.send_keys(maxbed)

    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button.nd-button.nd-button--accent.nd-button--block'))).click()
    time.sleep(5)
    prices = []
    places = []
    
    page = 1
    while True : 
        last_height =  driver.execute_script("return document.body.scrollHeight;") 
        price_items = driver.find_elements(By.CSS_SELECTOR,"div.in-listingCardPrice")
        place_items = driver.find_elements(By.XPATH,'//a[contains(@class , "in-listingCardTitle")]')
        for price,place in zip(price_items,place_items) :
            try:
                place = place.text.split(',')[-1]
                prices.append(price.text)
                places.append(place)
            except : 
                print('could not find any home for you! Try later')
          
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        new_height = driver.execute_script("return document.body.scrollHeight;")
        if last_height==new_height :
            page+=1
            time.sleep(2)
            driver.execute_script('document.querySelector(".in-pagination__list").scrollIntoView({ behavior: "smooth", block: "center" });')
            time.sleep(3)
            next_page = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//a[text()="{page}"]'))
            )
            next_page.click()
            
        if page >5:
            driver.quit()
            break
        last_height = new_height 
    df = pd.DataFrame(zip(prices,places),columns=['price','place'])         

    return df     

get_date('Rent',50,80,0,2).to_csv('rent.csv')

