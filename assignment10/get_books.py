from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json
import re
from time import sleep

RESULT_LI_SELECTOR = "li.cp-search-result-item"
TITLE_SELECTOR_TRY = "h2.cp-title, h3.cp-title"
TITLE_LINK_FALLBACK = "a[data-key='bib-title']"
AUTHOR_SELECTOR = "span.cp-author-link"
META_SELECTOR_TRY = "div.info, div.cp-format"

def first_line(text):
    if not text:
        return ""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    for ln in lines:
        if ln.lower().startswith("check out"):
            break
        return ln
    return ""

def pick_meta(text):
    if not text:
        return ""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    for ln in lines:
        if ln.lower().startswith("check out"):
            break
        if re.search(r",(?:\s*)(19|20)\d{2}\b", ln):
            return ln
    return first_line(text)

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--window-size=1200,900")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
print("Opening", url)
driver.get(url)

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, RESULT_LI_SELECTOR))
    )
except:
    print("Page load error")

sleep(2)
cards = driver.find_elements(By.CSS_SELECTOR, RESULT_LI_SELECTOR)
print("Found:", len(cards))

results = []
for li in cards:
    title = ""
    try:
        t_el = li.find_element(By.CSS_SELECTOR, TITLE_SELECTOR_TRY)
        title = t_el.text.strip()
        if not title:
            a = t_el.find_elements(By.CSS_SELECTOR, "a")
            if a:
                title = (a[0].text or a[0].get_attribute("textContent") or "").strip()
    except:
        try:
            a = li.find_element(By.CSS_SELECTOR, TITLE_LINK_FALLBACK)
            title = (a.text or a.get_attribute("textContent") or "").strip()
        except:
            title = ""
    title = first_line(title)

    authors = []
    for a in li.find_elements(By.CSS_SELECTOR, AUTHOR_SELECTOR):
        txt = (a.text or a.get_attribute("textContent") or "").strip()
        if txt:
            authors.append(txt)
    author_text = "; ".join(authors)

    meta_raw = ""
    try:
        m = li.find_element(By.CSS_SELECTOR, META_SELECTOR_TRY)
        meta_raw = (m.text or m.get_attribute("textContent") or "").strip()
    except:
        meta_raw = ""
    meta = pick_meta(meta_raw)

    if title:
        results.append({"Title": title, "Author": author_text, "Format-Year": meta})

driver.quit()

print("Collected:", len(results))
print(results[:3])

df = pd.DataFrame(results)
df.to_csv("get_books.csv", index=False)
with open("get_books.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Files saved")