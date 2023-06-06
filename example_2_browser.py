import time
from seleniumwire import undetected_chromedriver as uc




def browser_without_proxy():
    """Браузер без прокси"""
    driver = uc.Chrome(version_main=108)
    driver.get("https://whoer.net/ru")
    time.sleep(3)
    driver.get("https://chat.openai.com/")
    time.sleep(5)


def browser_with_proxy():
    """Браузер с прокси в формате user:pass@ip:port"""
    wire_options = {
        'proxy': {
            'https': f'https://X7FiXtGT:V5xWAQSP@146.19.110.223:64304',
        }
    }
    driver = uc.Chrome(version_main=108, seleniumwire_options=wire_options)
    driver.get("https://whoer.net/ru")
    time.sleep(3)
    driver.get("https://chat.openai.com/")
    time.sleep(15)


browser_without_proxy()
browser_with_proxy()

