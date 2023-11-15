import datetime
# Product by Random Alpha
#
# Twitter:
# https://twitter.com/RandomAlphaNFT

import json

import random
import time
import zipfile

import pyperclip

from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import visibility_of_element_located, element_to_be_clickable
from selenium.webdriver.support.ui import WebDriverWait as Wait
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

anticaptcha_plugin_path = r'anticaptcha-plugin_v0.62.zip'
sui_wallet_path = '22.11.9.0_0.crx'

api = ''
with open('data.txt', 'r') as file:
    for i in file:
        if i.strip('\n') == '':
            pass
        else:
            api = i.strip('\n')


def using_proxy():
    def get_proxy():
        proxy = {}

        with open("proxy.txt", "r") as file:
            proxy = file.readline()
            file.close()

        return proxy

    proxy = str(get_proxy())
    proxy_list = proxy.split(':')
    pass1 = str(proxy_list[3])

    PROXY_HOST = str(proxy_list[0])  # rotating proxy or host
    PROXY_PORT = str(proxy_list[1])
    PROXY_USER = str(proxy_list[2])
    PROXY_PASS = str(pass1.strip())

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "browsingData",
            "proxy",
            "storage",
            "tabs",
            "webRequest",
            "webRequestBlocking",
            "downloads",
            "notifications",
            "<all_urls>"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    return manifest_json, background_js, proxy


def acp_api_send_request(driver, message_type, data={}):
    message = {

        'receiver': 'antiCaptchaPlugin',

        'type': message_type,

        **data
    }

    return driver.execute_script("""
    return window.postMessage({});
    """.format(json.dumps(message)))


mails = []
with open('mails.txt', 'r') as file:
    for i in file:
        mails.append(i.strip('\n'))


def main(t):

    global driver

    chrome_options = Options()

    manifest_json, background_js, proxy = using_proxy()
    pluginfile = 'Proxy_ext.zip'

    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    chrome_options.add_extension(pluginfile)

    chrome_options.add_argument('--user-agent=%s' % UserAgent)

    # chrome_options.add_experimental_option("debuggerAddress", response["data"]["ws"]["selenium"])
    chrome_options.add_extension(sui_wallet_path)
    chrome_options.add_extension(anticaptcha_plugin_path)
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    wait = Wait(driver, 120)

    driver.get('https://antcpt.com/blank.html')
    acp_api_send_request(
        driver,
        'setOptions',
        {'options': {'antiCaptchaApiKey': api}}
    )

    time.sleep(4)
    driver.maximize_window()
    time.sleep(1)

    for i in driver.window_handles:
        driver.switch_to.window(i)
        if 'Sui' in driver.title:
            break

    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#/initialize/select"]')))
    time.sleep(3)
    ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()

    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#/initialize/create"]')))
    ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()

    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))
    driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys('19191919ArtArtawd')
    driver.find_element(By.CSS_SELECTOR, 'input[name="confirmPassword"]').send_keys('19191919ArtArtawd')

    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'input[name="terms"]')).click().perform()
    # time.sleep(111111)
    ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.SPACE).perform()

    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'i[title="Copy to clipboard"]')))
    driver.find_element(By.CSS_SELECTOR, 'i[title="Copy to clipboard"]').click()

    time.sleep(1)

    seed = pyperclip.paste()

    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button[type="button"]')).click().perform()
    #
    # wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#/tokens?menu=%2F"]')))
    # ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR ,'a[href="#/tokens?menu=%2F"]')).click().perform()
    #
    # wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#/tokens?menu=%2Fnetwork"]')))
    # ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR ,'a[href="#/tokens?menu=%2Fnetwork"]')).click().perform()

    # wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button[data-network="testNet"]')))
    # ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR ,'button[data-network="testNet"]')).click().perform()
    #
    # time.sleep(1)
    #
    # ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR ,'a[href="#/tokens"]')).click().perform()
    # time.sleep(1)
    #
    # wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button[type="button"]')))
    # ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR ,'button[type="button"]')).click().perform()
    # import pyautogui as PAG
    # PAG.moveTo(button_coords)
    # PAG.click()

    time.sleep(4)

    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button[type="button"]')))
    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button[type="button"]')).click().perform()


    # PAG.click()

    while True:
        try:
            # print(driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')[0].text)
            if float(driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')[0].text.split('\n')[0]) > 0:
                break
        except:
            pass

    # print('success')
    # time.sleep(11111)

    # input()

    # driver.get('chrome-extension://dlpmlfdkanckdipggbbadihbnpgdpiif/popup.html')
    # Wait(driver, 10).until(element_to_be_clickable((By.CSS_SELECTOR, 'input[id="account_key"]')))
    # driver.find_element(By.CSS_SELECTOR, 'input[id="account_key"]').send_keys(API)
    # time.sleep(1)
    # ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')).click().perform()



    driver.get('chrome-extension://opcgpfmipidbgpenhmajoajpbobppdil/ui.html#/apps')
    wait.until(element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/main/div/div/section/div/div[1]/button')))
    ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/main/div/div/section/div/div[1]/button')).click().perform()

    time.sleep(2)

    driver.switch_to.new_window()
    driver.get('https://ethoswallet.github.io/2048-demo/')

    # for i in driver.window_handles:
    #     driver.switch_to.window(i)
    #     if '2048' in driver.title:
    #         break

    pages = driver.window_handles
    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button.start-button')))
    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button.start-button')).click().perform()

    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'svg[id="SuiSvg"]')))
    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'svg[id="SuiSvg"]')).click().perform()

    while len(driver.window_handles) == len(pages):
        pass

    driver.switch_to.window(driver.window_handles[-1])

    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button[data-allow="true"]')))
    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button[data-allow="true"]')).click().perform()

    while len(driver.window_handles) != len(pages):
        pass

    for i in driver.window_handles:
        driver.switch_to.window(i)
        if '2048' in driver.title:
            break

    while True:

        try:
            ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'a.retry-button')).click().perform()
            break
        except:
            pass

        ActionChains(driver).send_keys(random.choice([Keys.ARROW_DOWN,Keys.ARROW_RIGHT,Keys.ARROW_UP,Keys.ARROW_LEFT])).perform()

    wait.until(visibility_of_element_located((By.CSS_SELECTOR, 'button[id="claim-button"]')))
    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button[id="claim-button"]')).click().perform()

    while len(driver.window_handles) == len(pages):
        pass

    driver.switch_to.window(driver.window_handles[-1])

    try:
        Wait(driver, 2).until(element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))
        driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys('19191919ArtArtawd')
        ActionChains(driver).send_keys(Keys.ENTER).perform()
    except:
        pass

    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button[data-allow="true"]')))
    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button[data-allow="true"]')).click().perform()

    while len(driver.window_handles) != len(pages):
        pass

    for i in driver.window_handles:
        driver.switch_to.window(i)
        if '2048' in driver.title:
            break

    driver.close()

    for i in driver.window_handles:
        driver.switch_to.window(i)
        if 'Sui' in driver.title:
            break

    pages = driver.window_handles

    driver.switch_to.new_window()
    driver.get('https://sui-wallet-demo.sui.io/')
    pages = driver.window_handles

    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button[type="button"]')))
    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button[type="button"]')).click().perform()

    while len(driver.window_handles) == len(pages):
        pass

    driver.switch_to.window(driver.window_handles[-1])

    try:
        Wait(driver, 2).until(element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))
        driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys('19191919ArtArtawd')
        ActionChains(driver).send_keys(Keys.ENTER).perform()
    except:
        pass

    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button[data-allow="true"]')))
    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button[data-allow="true"]')).click().perform()

    while len(driver.window_handles) != len(pages):
        pass

    for i in driver.window_handles:
        driver.switch_to.window(i)
        if 'Demo' in driver.title:
            break

    abc = 'qwertyuiopasdfghjklzxcvbnm'

    name = ''
    for i in range(random.randint(4, 8)):
        name+=abc[random.randint(0, len(abc)-1)]


    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Example NFT"]').send_keys(name)

    name = ''
    for i in range(random.randint(10, 16)):
        name+=abc[random.randint(0, len(abc)-1)]

    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="An example NFT created by demo Dapp"]').send_keys(name)

    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button[type="button"]')).click().perform()

    while len(driver.window_handles) == len(pages):
        pass

    driver.switch_to.window(driver.window_handles[-1])

    try:
        Wait(driver, 2).until(element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))
        driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys('19191919ArtArtawd')
        ActionChains(driver).send_keys(Keys.ENTER).perform()
    except:
        pass

    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button[data-allow="true"]')))
    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button[data-allow="true"]')).click().perform()

    while len(driver.window_handles) != len(pages):
        pass

    for i in driver.window_handles:
        driver.switch_to.window(i)
        if 'Demo' in driver.title:
            break


    driver.close()

    for i in driver.window_handles:
        driver.switch_to.window(i)
        if 'Sui' in driver.title:
            break

    driver.switch_to.new_window()
    driver.get('https://test-wizardland.vercel.app/')

    pages = driver.window_handles

    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button.wkit-button')))
    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button.wkit-button')).click().perform()

    wait.until(visibility_of_element_located((By.CSS_SELECTOR, 'div.wkit-select-item')))
    ActionChains(driver).move_to_element(driver.find_elements(By.CSS_SELECTOR, 'div.wkit-select-item')[1]).click().perform()

    while len(driver.window_handles) == len(pages):
        pass

    driver.switch_to.window(driver.window_handles[-1])

    try:
        Wait(driver, 2).until(element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))
        driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys('19191919ArtArtawd')
        ActionChains(driver).send_keys(Keys.ENTER).perform()
    except:
        pass

    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button[data-allow="true"]')))
    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button[data-allow="true"]')).click().perform()

    while len(driver.window_handles) != len(pages):
        pass

    for i in driver.window_handles:
        driver.switch_to.window(i)
        if 'Wizard' in driver.title:
            break


    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'div.btn-group button')))
    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'div.btn-group button')).click().perform()

    while len(driver.window_handles) == len(pages):
        pass

    driver.switch_to.window(driver.window_handles[-1])

    try:
        Wait(driver, 2).until(element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))
        driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys('19191919ArtArtawd')
        ActionChains(driver).send_keys(Keys.ENTER).perform()
    except:
        pass

    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button[data-allow="true"]')))
    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button[data-allow="true"]')).click().perform()

    while len(driver.window_handles) != len(pages):
        pass

    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])

    wait.until(expected_conditions.alert_is_present())
    alert = driver.switch_to.alert

    # Store the alert text in a variable
    text = alert.text

    # Press the Cancel button
    alert.dismiss()
    time.sleep(1)

    # driver.get('https://sui.bluemove.net/account')
    #
    #
    #
    # wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/connect-wallet"]')))
    # ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'a[href="/connect-wallet"]')).click().perform()
    #
    # wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'div[typeof="button"]')))
    # ActionChains(driver).move_to_element(driver.find_elements(By.CSS_SELECTOR, 'div[typeof="button"]')[1]).click().perform()
    #
    # while len(driver.window_handles) == len(pages):
    #     pass
    #
    # driver.switch_to.window(driver.window_handles[-1])
    #
    # try:
    #     Wait(driver, 2).until(element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))
    #     driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys('19191919ArtArtawd')
    #     ActionChains(driver).send_keys(Keys.ENTER).perform()
    # except:
    #     pass
    #
    # wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button[data-allow="true"]')))
    # ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button[data-allow="true"]')).click().perform()
    #
    # while len(driver.window_handles) != len(pages):
    #     pass
    #
    # for i in driver.window_handles:
    #     driver.switch_to.window(i)
    #     if 'Account' in driver.title:
    #         break
    #
    # # time.sleep(1111)
    #
    # time.sleep(2)
    #
    # ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button.nc-Button')).click().perform()
    #
    # time.sleep(4)

    # driver.get('https://talofagames.us5.list-manage.com/subscribe?u=514b137ee3cfc15e5c6c38aa9&id=54a65f4aad')
    #
    # wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'input[id="simple-search"]')))
    #
    # name = ''
    # for i in range(random.randint(4, 8)):
    #     name+=abc[random.randint(0, len(abc)-1)]
    #
    # driver.find_element(By.CSS_SELECTOR, 'input[id="simple-search"]').send_keys(name)
    # ActionChains(driver).send_keys(Keys.ENTER).perform()
    #
    # wait.until(element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div/div/div[2]/div/div/button/span')))
    # ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div/div[2]/div/div/button/span')).click().perform()
    #
    # while len(driver.window_handles) == len(pages):
    #     pass
    #
    # driver.switch_to.window(driver.window_handles[-1])
    #
    # try:
    #     Wait(driver, 2).until(element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))
    #     driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys('19191919ArtArtawd')
    #     ActionChains(driver).send_keys(Keys.ENTER).perform()
    # except:
    #     pass
    #
    # wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button[data-allow="true"]')))
    # ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button[data-allow="true"]')).click().perform()
    #
    # while len(driver.window_handles) != len(pages):
    #     pass
    #
    # for i in driver.window_handles:
    #     driver.switch_to.window(i)
    #     if 'Sui Name' in driver.title:
    #         break
    #
    # wait.until(element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div/div/div[2]/div/div/button/span')))
    # ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div/div[2]/div/div/button/span')).click().perform()

    driver.get('https://talofagames.us5.list-manage.com/subscribe?u=514b137ee3cfc15e5c6c38aa9&id=54a65f4aad')

    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'input[name="MERGE0"]')))
    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR, 'input[name="MERGE0"]').send_keys(mails[t].split(':')[0])

    name = ''
    for i in range(random.randint(4, 8)):
        name+=abc[random.randint(0, len(abc)-1)]

    driver.find_element(By.CSS_SELECTOR, 'input[name="MERGE1"]').send_keys(name)
    time.sleep(1)

    name = ''
    for i in range(random.randint(4, 8)):
        name+=abc[random.randint(0, len(abc)-1)]

    driver.find_element(By.CSS_SELECTOR, 'input[name="MERGE2"]').send_keys(name)
    time.sleep(1)

    for i in range(0, random.randint(1, 3)):
        ActionChains(driver).send_keys(Keys.TAB).perform()

    ActionChains(driver).send_keys(Keys.SPACE).perform()
    time.sleep(1)

    for i in range(0, random.randint(2, 10)):
        ActionChains(driver).send_keys(Keys.TAB).perform()

    ActionChains(driver).send_keys(Keys.SPACE).perform()

    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'input[name="submit"]')).click().perform()

    Wait(driver, 180).until(visibility_of_element_located((By.CSS_SELECTOR, '.antigate_solver.solved')))

    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'input.formEmailButton[value="Subscribe"]')).click().perform()
    time.sleep(3)

    # driver.get('https://app.shinami.com/signup')
    # Wait(driver, 180).until(visibility_of_element_located((By.CSS_SELECTOR, '.antigate_solver.solved')))
    #
    #
    # wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="Email"]')))
    # driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Email"]').send_keys(mails[it].split(':')[0])
    #
    # ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')).click().perform()
    #
    # time.sleep(4)


    driver.get('https://gzr9hedzug3.typeform.com/to/yVT5CA3h')

    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'input[type="email"]')))
    driver.find_element(By.CSS_SELECTOR, 'input[type="email"]').send_keys(mails[t].split(':')[0])

    ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.SPACE).perform()
    time.sleep(2)

    ActionChains(driver).move_to_element(driver.find_elements(By.CSS_SELECTOR, 'div[aria-disabled="false"][class*="Root"]')[random.randint(0, 5)]).click().perform()
    time.sleep(3)

    ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
    time.sleep(3)

    ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.SPACE).perform()
    time.sleep(3)
    # ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.SPACE).perform()

    ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '//span[text()="Submit"]')).click().perform()

    time.sleep(2)
    # ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button[data-qa="submit-button deep-purple-submit-button"]')).click().perform()

    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="thank-you-button"]')))

    time.sleep(3)

    print(f'{datetime.datetime.now()} - {t} Complete')

    driver.quit()

    with open('result.txt', 'a+') as file:
        file.write(f'{seed}:::{mails[0]}:::{proxy[:-1]}\n')

    with open('proxy.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open('proxy.txt', 'w', encoding='utf-8') as file:
        lines = file.writelines(lines[1:])

    with open('mails.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open('mails.txt', 'w', encoding='utf-8') as file:
        lines = file.writelines(lines[1:])

    time.sleep(3)







if __name__ == '__main__':


    t = 0
    while True:
        try:
            main(t)
            t+=1
        except:

            with open('proxy.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()

            with open('proxy.txt', 'w', encoding='utf-8') as file:
                lines = file.writelines(lines[1:])
