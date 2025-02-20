import os
import sys
import requests
import browser_cookie3
from selenium import webdriver
import ctypes
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_as_admin():
    if not is_admin():
        script = sys.argv[0]
        params = ' '.join(sys.argv[1:])
        subprocess.run(f'runas /user:Administrator "{sys.executable}" "{script}" {params}')
        sys.exit()

def main():
    cookies = browser_cookie3.chrome(domain_name='.google.com')

    session = requests.Session()
    response = session.get("https://stackoverflow.com/", cookies=cookies)
    print("StackOverflow Cookies:", session.cookies.get_dict())

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1"
    }
    response_google = requests.get('http://www.google.com', headers=headers, cookies=cookies, timeout=3)
    print("Google Response Status:", response_google.status_code)

    driver = webdriver.Chrome('./chromedriver')
    for c in cookies:
        cookie = {'domain': c.domain, 'name': c.name, 'value': c.value, 'secure': c.secure and True or False}
        driver.add_cookie(cookie)

    driver.get('http://www.google.com')

if __name__ == "__main__":
    run_as_admin()
    main()
