import geckodriver_autoinstaller
import selenium
import bs4
import requests
import os, time
from selenium import webdriver
import re

geckodriver_autoinstaller.install()

def make_folder():
    nums = []
    cr_folder_name = 'downloaded'
    for fname in os.listdir():
        if cr_folder_name in fname:
            nums.append(re.search('[0-9]+$', fname).group())

    if len(nums) > 0:
        fnames_nums = max([int(fname) for fname in nums]) + 1
        cr_folder_name = 'downloaded' + str(fnames_nums)
    else:
        cr_folder_name += '1'

    return cr_folder_name

def run(cntr_end=10000, sleep_time=3):
    url_nature = 'https://www.skypixel.com/tags/nature'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
    downfolder = make_folder()
    browser = webdriver.Firefox()
    browser.get(url_nature)
    time.sleep(1)
    try:
        browser.find_element_by_css_selector('.sky-ui-button-theme-primary').click() # Accept all cookies
    except Exception as E:
        print(E)
        browser.quit()
        browser = webdriver.Firefox()
        browser.get(url_nature)
        time.sleep(1)
        browser.find_element_by_css_selector('.sky-ui-button-theme-primary').click() # Accept all cookies
        
    time.sleep(2)
    
    try:
        browser.find_element_by_css_selector("#work_detail_event_tag_detail-0 .\_26az").click() # Click the first photo
    except Exception as E:
        print(E)
        browser.find_element_by_css_selector("#work_detail_event_tag_detail-0 .\_26az").click() # Click the first photo
    
    os.mkdir(downfolder)
    
    for cntr in range(cntr_end):
        time.sleep(sleep_time)
        html = browser.page_source
        soup = bs4.BeautifulSoup(html, features="lxml")
        try:
            img_str = soup.find_all('img', attrs={'class': '_18wC'})[0]
            img_url = img_str.attrs['src']
            img = requests.get(img_url, stream=True, headers=headers)
            File = open(os.path.join(downfolder, str(cntr)+'.jpg'), "wb")
            File.write(img.raw.read())
            File.close()
            browser.find_element_by_css_selector('.\_29Z5 path:nth-child(1)').click()
            time.sleep(2)
        except IndexError:
            time.sleep(2)
            browser.find_element_by_css_selector('.\_29Z5 path:nth-child(1)').click()
    
    browser.quit()

if __name__ == '__main__':
    run()