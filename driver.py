from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser
import time
from corpus_db import corpus_db

driver: webdriver.Chrome = None
cfg = configparser.ConfigParser()
username = ""
password = ""
driver_path = ""
proxy_url = ""
debug = False
options = webdriver.ChromeOptions()

db = None


def load_config():
    global username, password, debug, driver_path, proxy_url, db
    print("Loading config")
    cfg.read('config.ini')
    username = cfg['OU']['username']
    password = cfg['OU']['password']
    debug = cfg['Default']['debug']
    driver_path = cfg['Default']['driver_path']
    proxy_url = cfg['Default']['proxy_url']
    location = cfg['DB']['location']
    db = corpus_db.DBHandler(destination=location)
    if not debug:
        options.add_argument('headless')


def proxy_login():
    global driver
    print("Starting proxy login.")
    ts = time.time()
    driver = webdriver.Chrome(driver_path)
    driver.get(proxy_url)
    user_elt = driver.find_element_by_name('username')
    user_elt.send_keys(username)
    pass_elt = driver.find_element_by_name('password')
    pass_elt.send_keys(password)
    driver.find_element_by_name('submit').click()
    print(f"Proxy logged in: Process took {time.time() - ts} seconds.")


def next_page():
    elt = driver.find_elements_by_class_name("la-TriangleRight")[17]
    elt.click()


def end_of_pages():
    return len(driver.find_elements_by_class_name("disabled")) == 1


def fetch_text(i, page_num):
    pending = True
    while pending:
        try:
            doc_row = driver.find_element_by_id(f"doc_row_sr{page_num * 10 + i}")
            doc_row.click()
            print(f"Clicking preview for {page_num * 10 + i}")
            doc_elt = WebDriverWait(driver, 10).until(
             EC.presence_of_all_elements_located((By.CLASS_NAME, 'doc-content'))
            )
            if len(doc_elt) == 0:
                raise Exception
            body = doc_elt[0].text
            pending = False
        except Exception as e:
            print(e)
            continue
    print("Retrieved text")
    pending = True
    while pending:
        try:
            elt = driver.find_element_by_class_name("lnkClosePreviewPanel")
            elt.click()
            print(f"Closed preview panel for {page_num * 10 + i}")
            pending = False
        except:
            try:
                preview_panel = driver.find_element_by_class_name("PreviewPanelOpen")
                if preview_panel.get_attribute('style') == 'display: none':
                    break
            except:
                break
            continue
    return body


def initial_pull():
    page_num = 0
    driver.get("https://advance-lexis-com.ezproxy.lib.ou.edu/search/?pdmfid=1516831&crid=7323c5c3-43d1-4a2a-b491-6602edebfdec&pdsearchterms=last+laughs&pdstartin=hlct%3A1%3A1&pdtypeofsearch=searchboxclick&pdsearchtype=SearchBox&pdqttype=and&pdsf=MTA1MzI4NA~%5Enews~%5EThe%2520Bulletin%27s%2520Frontrunner&pdquerytemplateid=&ecomp=s7x9k&earg=pdsf&prid=e668ab9e-4f9d-4997-9d07-bc17d448dd24")
    while page_num != 513:
        for i in range(0, 10):
            body = fetch_text(i, page_num)
            db.add(body)
            print(f"Retrieved corpus for item {page_num * 10 + i}")
        next_page()
        page_num = page_num + 1


if __name__ == "__main__":
    load_config()
    proxy_login()

    initial_pull()