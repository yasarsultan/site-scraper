from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd


fields = {'Name':[], 'PAN No.': [], 'GSTIN No.':[], 'Permanent Address':[]}

chromedriver_path = '/usr/bin/chromedriver'
driver = webdriver.Chrome(service=Service(chromedriver_path))

try:
    driver.get("https://hprera.nic.in/PublicDashboard")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'form-row')]/div[contains(@class, 'col-lg-6')]"))
    )
    # time.sleep(10)
    buttons = driver.find_elements(By.XPATH, '//a[@data-qs][@title="View Application"]')
    
    for button in buttons[:5]:
        try:
            button.click()
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table_body = soup.find('tbody', {'class': 'lh-2'})
            rows = table_body.find_all('tr')
        except:
            print(f"Error in this button {button}")
            continue
        
        for row in rows:
            cells = row.find_all('td')
            key = cells[0].text.strip()
            value = cells[1].text.strip()
            parts = value.split('\n')
            cleaned_string = parts[0]

            if key in fields:
                fields[key].append(cleaned_string)

        driver.find_element(By.CLASS_NAME, 'close').click()

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()

df = pd.DataFrame(fields)
df.to_csv("output.csv")