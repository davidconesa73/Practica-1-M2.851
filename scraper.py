import time
import csv
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

START_URL = "https://www.imdb.com/chart/top/"


# ---------- DRIVER ----------
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0")
    return webdriver.Chrome(options=options)


# ---------- EXTRAER JSON LD ----------
def extract_json_ld(driver):
    script = driver.find_element(
        By.XPATH, "//script[@type='application/ld+json']"
    ).get_attribute("innerHTML")
    return json.loads(script)


# ---------- DESCUBRIR LINKS TOP 250 ----------
def get_movie_links(driver):
    driver.get(START_URL)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.ipc-metadata-list"))
    )

    items = driver.find_elements(By.CSS_SELECTOR, "a.ipc-title-link-wrapper")

    links = []
    for a in items:
        href = a.get_attribute("href")
        if "/title/" in href:
            links.append(href.split("?")[0])

    print(f"Encontradas {len(links)} películas del Top 250")
    return links


# ---------- SCRAPEAR CADA PELÍCULA ----------
def scrape_movie(driver, url):
    driver.get(url)
    time.sleep(2)

    data_json = extract_json_ld(driver)
    data = {}

    data["title"] = data_json.get("name", "")
    data["year"] = data_json.get("datePublished", "")
    data["duration"] = data_json.get("duration", "")
    data["genres"] = ", ".join(data_json.get("genre", []))
    data["rating"] = data_json.get("aggregateRating", {}).get("ratingValue", "")
    data["votes"] = data_json.get("aggregateRating", {}).get("ratingCount", "")

    directors = data_json.get("director", [])
    if isinstance(directors, list):
        data["director"] = ", ".join([d["name"] for d in directors])
    else:
        data["director"] = directors.get("name", "")

    actors = data_json.get("actor", [])
    data["stars"] = ", ".join([a["name"] for a in actors])

    print(f"Scrapeado: {data['title']}")
    return data


# ---------- GUARDAR CSV ----------
def save_csv(rows):
    keys = rows[0].keys()
    with open("dataset_imdb.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


# ---------- MAIN ----------
def main():
    driver = init_driver()

    links = get_movie_links(driver)

    dataset = []
    for link in links[:250]:
        dataset.append(scrape_movie(driver, link))
        time.sleep(2)

    driver.quit()
    save_csv(dataset)
    print("Dataset guardado en dataset_imdb.csv")


if __name__ == "__main__":
    main()