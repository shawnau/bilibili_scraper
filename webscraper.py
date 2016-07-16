from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# set phantomJS's agent to Firefox
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = \
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 "
# xpath for all the elements we want
idXpath = ".//*[@id='winLogin_sfLogin_txtUserLoginID']"
pwXpath = ".//*[@id='winLogin_sfLogin_txtPassword']"
loginXpath = ".//*[@id='ext-gen5']"
redirectXpath = ".//*[@id='RegionPanel1_UpRegion_ContentPanel1_content']/table/tbody/tr/td[2]"
logoutXpath = ".//*[@id='ext-gen42']"
infoXpath = ".//*[@id='ext-gen51']"
# some system path you need to config by yourself
phantomjsPpath = "/Users/Shawn/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs"
savePath = "/Users/Shawn/Documents/webscraper/data/"


def save_cookies(driver, file_path):
    # The format could vary
    LINE = "document.cookie = '{name}={value}; path={path}; domain={domain}';\n"
    with open(file_path, 'w') as fd:
        for cookie in driver.get_cookies():
            fd.write(LINE.format(**cookie))


def load_cookies(driver, file_path):
    with open(file_path, 'r') as fd:
        driver.execute_script(fd.read())


def login(login_url, username, password):
    driver = webdriver.PhantomJS(executable_path=phantomjsPpath,
                                 desired_capabilities=dcap)
    try:
        driver.get(login_url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, idXpath)))
        wait.until(EC.presence_of_element_located((By.XPATH, pwXpath)))
        wait.until(EC.element_to_be_clickable((By.XPATH, loginXpath)))

        driver.find_element_by_xpath(idXpath).send_keys(username)
        driver.find_element_by_xpath(pwXpath).send_keys(password)
        driver.find_element_by_xpath(loginXpath).click()
        print("Login Success!")

        wait.until(EC.presence_of_element_located((By.XPATH, redirectXpath)))
        print("Current url is: " + driver.current_url)
        print("Current cookies are: " + str(driver.get_cookies()))
        save_cookies(driver, r'cookies.js')
    except Exception as ex:
        print("Login failed!")
        print(ex)
    finally:
        driver.close()


def scraper(login_url, scrape_url):
    driver = webdriver.PhantomJS(executable_path=phantomjsPpath,
                                 desired_capabilities=dcap)
    try:
        driver.get(login_url)
        driver.delete_all_cookies()
        load_cookies(driver, r'cookies.js')
        driver.get(scrape_url)

        if driver.current_url == login_url:
            raise NameError('Redirect failed!')
        print("Scraper login through cookie success!")
        print("scrapping...")
        rule(driver, login_url)
    except Exception as ex:
        print("Scraper login through cookie failed!")
        print(ex)
    finally:
        logout(driver, login_url)


def rule(driver, login_url):
    from bs4 import BeautifulSoup
    import re
    try:
        elem = driver.find_element_by_xpath(infoXpath)
        table_source = elem.get_attribute('innerHTML')

        reg = re.compile("/Base/NoticeInfo/ViewNotice\.aspx\?ID=[-a-z0-9]+")
        link_list = re.findall(reg, table_source)

        for link in link_list:
            page_link = login_url + link
            driver.get(page_link)
            current_url = driver.current_url
            if current_url != page_link:
                raise NameError('Switch page failed')

            pagesource = driver.page_source
            bsObj = BeautifulSoup(pagesource, "html.parser")
            title = bsObj.find("span", {"id": "lblNoticeName"}).get_text().encode('utf-8')
            with open(savePath + str(title)+".html", 'w') as fd:
                fd.write(bsObj.get_text().encode('utf-8') + '\n')
            print(str(title))
    except Exception as ex:
        print("Scraper finding element Error!")
        print(ex)
        driver.save_screenshot("screenshot.jpg")


def logout(driver, login_url):
    try:
        driver.get(login_url)
        driver.delete_all_cookies()
        load_cookies(driver, r'cookies.js')
        # set window size for phantomJS or it won'r find button
        driver.set_window_size(1024, 768)
        driver.get(login_url)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, logoutXpath)))
        driver.find_element_by_xpath(logoutXpath).click()
        print("Logout Success!")
    except Exception as ex:
        print("Logout Failed")
        print(ex)
    finally:
        driver.close()

login("http://mis.sse.ustc.edu.cn/", "sa16225220", "decswxaqz")
scraper("http://mis.sse.ustc.edu.cn/", "http://mis.sse.ustc.edu.cn/Base/NoticeInfo/ListView.aspx")