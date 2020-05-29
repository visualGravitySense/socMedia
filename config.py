from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver



import utils


class Config:
    # chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    chrome_path = '/Users/dmitrigornakov/Desktop/chromedriver'
    # firefox_path = 'C:\selenium_drivers\geckodriver.exe'
    # firefox_path = 'C:\Program Files (x86)\Mozilla Firefox\\firefox.exe'

    prefs = {"profile.managed_default_content_settings.images": 2}

    user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
    )

    work_user_agent = ("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

    home_user_agent = ("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0")

    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = user_agent
    service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',
                  '--load-images=no', '--log-path=logs\\']
    output_dir = 'output/'
    # os_type = 'Windows'

    def __init__(self):
        self.os_type = utils.detect_system()

        if self.os_type == "Windows":
            self.user_agent = self.work_user_agent
        else:
            self.user_agent = self.home_user_agent
