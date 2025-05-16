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
import numpy as  np 
# ============================================================================================================================
def get_date (isrent,minsurf,maxsurf,minbed,maxbed):
    # def feature structure:
# =================================================
    links = [] 
    prices = []
    places = []   
# ============================================================================================================================
    myOptions = Options()
    myOptions.add_argument('--start-maximized')
    myOptions.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=myOptions)
    driver.get('https://www.immotop.lu/en/vente-maisons-appartements/luxembourg-pays/?criterio=rilevanza')
# =================================================
#finding Rent items :
# =================================================
# '//div[contains(@class,"nd-select")]//div[contains(@class,"nd-select__control")]'
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div.nd-select__value'))).click()
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div[class*="nd-stackItem"]')))
    items_isrent = driver.find_elements(By.CSS_SELECTOR,'div[class*="nd-stackItem"]')

    for item in items_isrent :

        if item.text == isrent :
            item.click()
        else:
            continue    
# =================================================        
# sleep For Loading:   
    time.sleep(3)
# define starter page:
    page = 1
# ============================================================================================================================
    while True:

        last_height =  0
        while True :

    # find all ads in each page and enter each ad for get information :
    # =================================================
            
            new_height = driver.execute_script("return document.body.scrollHeight;") 
            if new_height == last_height:
                break 
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)   
            last_height = new_height
        time.sleep(3)
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//div[contains(@class,"nd-mediaObject__content")]//a[contains(@class,"in-listingCardTitle")]')))
        time.sleep(3)
        link_items = driver.find_elements(By.XPATH,'//a[contains(@class,"in-listingCardTitle")]')
        for link in link_items:
            links.append(link.get_attribute('href'))
            

    # find the page segment to change the page and proceed the procedure in other pages:
    # =================================================                
#<div class="nd-mediaObject__content in-listingCardPropertyContent"><div class="in-listingCardAgencyLogo"><figure class="nd-figure nd-ratio in-listingCardAgencyLogo__figure"><img class="nd-figure__content nd-ratio__img in-listingCardAgencyLogo__image" alt="LA immo Sàrl" width="135" height="35" src="https://pic.immotop.lu/imagenoresize/145700161.jpg"></figure></div><div class="in-listingCardPrice"><span><span class="in-formattedPrice__text">from </span>€ 342,875</span></div><a href="https://www.immotop.lu/en/annonces/1348041/" title="New build Studios and Apartments in Erpeldange-sur-Sûre" class="in-listingCardTitle is-spaced">New build Studios and Apartments in Erpeldange-sur-Sûre</a><div class="in-listingCardFeatureList"><div class="in-listingCardFeatureList__item"><svg viewBox="0 0 24 24" class="nd-icon in-listingCardFeatureList__icon"><use class="nd-icon__use" href="#planimetry"></use></svg><span>1 - 3 rooms</span></div><div class="in-listingCardFeatureList__item"><svg viewBox="0 0 24 24" class="nd-icon in-listingCardFeatureList__icon"><use class="nd-icon__use" href="#size"></use></svg><span>from 35 m²</span></div><div class="in-listingCardFeatureList__item"><svg viewBox="0 0 24 24" class="nd-icon in-listingCardFeatureList__icon"><use class="nd-icon__use" href="#home"></use></svg><span>18 types</span></div></div><div class="in-listingCardDescription is-high is-highOnXLCard">The LA Immo real estate agency welcomes you to the Résidence «&nbsp;HEIRENSBIERG&nbsp;» located in Erpeldange-sur-Sûre in the new housing estate «&nbsp;In der mittelsten Gewan&nbsp;» 6-8 rue Dr Louise Welter on a 28.58 plot.

# The Résidence «&nbsp;HEIRENSBIERG" offers you 20 apartments and 9 studios, carefully designed to meet a variety of needs:

# - 7 one-bedroom apartments, perfect for singles or couples looking for peace and quiet.
# - 11 two-bedroom apartments, offering generous space for families or those looking for extra room.
# - 2 three-bedroom apartments, ideal for larger families or those looking for even more sp</div><div class="in-listingCardActions"><div class="in-listingCardActions__contacts"><button class="nd-button" data-cy="contact-button"><svg viewBox="0 0 24 24" class="nd-icon nd-button__icon"><use class="nd-icon__use" href="#chat"></use></svg>message</button><button class="nd-button" type="button"><svg viewBox="0 0 24 24" class="nd-icon nd-button__icon"><use class="nd-icon__use" href="#calendar"></use></svg>Visit</button></div><div class="in-listingCardActions__userPref" data-cy="listing-card-actions"><button class="nd-button nd-button--iconOnly cy-hideButton in-listingCardActions__userButton" aria-label="hide listing"><svg viewBox="0 0 24 24" class="nd-icon nd-button__icon"><use class="nd-icon__use" href="#bin"></use></svg></button><button class="nd-button nd-button--iconOnly in-listingCardSaveButton in-listingCardActions__userButton" aria-label="Save as favorite" data-cy="save-button"><svg viewBox="0 0 24 24" class="nd-icon nd-button__icon"><use class="nd-icon__use" href="#heart"></use><use class="nd-icon__use nd-icon__use--alternate" href="#heart--active"></use></svg></button></div></div></div>
        
        if last_height==new_height :
            page+=1
            time.sleep(2)
            driver.execute_script('document.querySelector(".in-pagination__list").scrollIntoView({ behavior: "smooth", block: "center" });')
            time.sleep(3)
            next_page = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//a[text()="{page}"]'))
            )
            next_page.click()
    # we limit this project to get information untill page 5 :
    # =================================================               
        if page > 10:
            break
        last_height = new_height 


    # ==================================================================================================================
    KEY_FEATURE = ['Type','Contract','Floor' , 'Lift' ,'Surface' , 'Rooms', 'Bed', 'Bath', 'Furnished', 'Terrace', 'Garage' ]
    # Type = [np.zeros((len(links),1))]
    # Contract = [np.zeros((len(links),1))]
    # Floor = [np.zeros((len(links),1))]
    # Lift = [np.zeros((len(links),1))]
    # Surface = [np.zeros((len(links),1))] 
    # Rooms = [np.zeros((len(links),1))]
    # Bed = [np.zeros((len(links),1))]
    # Bath = [np.zeros((len(links),1))]
    # Furnished = [np.zeros((len(links),1)) ]
    # Terrace = [np.zeros((len(links),1))]
    # Parking = [np.zeros((len(links),1))]
    all_features = []
    # all_links = []
    # feature =  {
    # 'Type': Type,
    # 'Contract': Contract,
    # 'Floor': Floor,
    # 'Lift': Lift,
    # 'Surface': Surface,
    # 'Rooms': Rooms,
    # 'Bed': Bed,
    # 'Bath': Bath,
    # 'Furnished': Furnished,
    # 'Terrace': Terrace,
    # 'Parking': Parking
    # }
    # get all linkd in order to enter in :
    # =================================================    
    for l in links:
        driver.get(l)
        time.sleep(3)
    # get price and title :
    # =================================================    

        price_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//div[@data-tracking-key="box-overview"]//div[contains(@class,"ld-overview__price")]'))
            )
        prices.append(price_element.text)
        places.append(driver.find_element(By.XPATH,'//h1[contains(@class, "ld-title__title")]').text)
    # finding the fetuares :
    # =================================================    

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")     
        driver.execute_script('document.querySelector(".ld-featuresGrid__list.ld-featuresGrid__list--twoColumnsOnMobile").scrollIntoView({ behavior: "smooth", block: "center" });')
        features = driver.find_elements(By.XPATH,'//dl[contains(@class,"ld-featuresGrid__list--twoColumnsOnMobile")]/div[@class="ld-featuresItem"]')
    # add all features in a specific column:
    # =================================================
        feature = {k : 0 for k in KEY_FEATURE}            
        for f in features[:10]:
            for k in KEY_FEATURE :
                if k in f.text:
                    feature[k] = f.text.split('\n')[-1]
                    break
        all_features.append(feature)        
    driver.quit()        

# store datsa in sata frame structure :
# =================================================
    feature_df = pd.DataFrame(all_features)
    df = pd.DataFrame(zip(prices,places,links))         
    result = pd.concat((df,feature_df),axis=1)
    return result     

get_date('Rent',50,80,0,2).to_csv('rent.csv')

