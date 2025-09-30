from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv,time

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--window-size=1200,900")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

url="https://owasp.org/www-project-top-ten/"
print("Opening",url)
driver.get(url)
time.sleep(3)

lis=driver.find_elements(By.CSS_SELECTOR,"#top-10-web-application-security-risks ~ ul li a")
results=[]
for a in lis:
    t=a.text.strip()
    h=a.get_attribute("href")
    if t and h:
        results.append({"Title":t,"URL":h})

driver.quit()

print("Collected:",len(results))
print(results)

with open("owasp_top_10.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=["Title","URL"])
    w.writeheader()
    for r in results:
        w.writerow(r)

print("File saved")