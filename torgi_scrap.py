import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from itertools import zip_longest

driver = webdriver.Chrome(executable_path='/Users/Mishanya/Documents/python/ufa_scraping/chromedriver')
lots = []
download_links = []

file_with_requests = 'elkibaevo'  # enter txt-filename with parsing data


def links_scraping():
    time.sleep(10)

    all_links = driver.find_elements_by_xpath("//img[contains(@src, 'img/s.gif')]/parent::a")

    for i in all_links:
        if i.get_attribute('href').find('notificationView') != -1:
            lots.append(i.get_attribute('href'))


def write_csv(req_name):
    with open(f'{file_with_requests}.csv', 'a') as file:
        w = csv.writer(file)
        for lot, doc in zip_longest(lots, download_links):
            w.writerow([lot, doc, req_name])


def get_links_from_pages():
    for lot in lots:
        driver.get(lot)
        download_links.append(driver.find_element_by_link_text('Скачать').get_attribute('href'))


def main():
    # open txt with requests
    with open(f'{file_with_requests}.txt', 'r') as txt_requests:
        requests = txt_requests.readlines()

    # add new csv
    with open(f'{file_with_requests}.csv', 'w') as file:
        w = csv.writer(file)
        w.writerow(['Ссылка  на страницу', 'Ссылка на результат', 'Запрос'])

    # go to site and enter our requests
    for request in requests:
        driver.get('https://torgi.gov.ru/allLotsSearch.html')
        lot_description = driver.find_element_by_name('lotOptions:fts')
        lot_description.send_keys(request)

        find_btn = driver.find_element_by_id('lot_search')
        find_btn.click()

        time.sleep(20)

        category = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div[2]/div[2]/div[1]/div/div/div/div/div/div/div/div/span/div/div[4]/a')
        category.click()

        # start scraping main-links from search pages
        links_scraping()
        try:
            while True:
                next_page = driver.find_element_by_link_text('Вперед')
                next_page.click()
                links_scraping()
        except NoSuchElementException:
            pass

        # get download-links from lots pages
        get_links_from_pages()

        write_csv(request)
        lots.clear()
        download_links.clear()
        driver.close()


if __name__ == '__main__':
    main()
