import time
import os
import shutil
import tempfile
from seleniumwire import undetected_chromedriver as uc

class ProxyExtension:
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {"scripts": ["background.js"]},
        "minimum_chrome_version": "76.0.0"
    }
    """

    background_js = """
    var config = {
        mode: "fixed_servers",
        rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: %d
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
        { urls: ["<all_urls>"] },
        ['blocking']
    );
    """

    def __init__(self, host, port, user, password):
        self._dir = os.path.normpath(tempfile.mkdtemp())

        manifest_file = os.path.join(self._dir, "manifest.json")
        with open(manifest_file, mode="w") as f:
            f.write(self.manifest_json)

        background_js = self.background_js % (host, port, user, password)
        background_file = os.path.join(self._dir, "background.js")
        with open(background_file, mode="w") as f:
            f.write(background_js)

    @property
    def directory(self):
        return self._dir

    def __del__(self):
        shutil.rmtree(self._dir)



def browser_with_proxy():
    """Браузер с прокси через расширение в формате ip:port:user:pass"""
    proxy = '146.19.110.223:64304:X7FiXtGT:V5xWAQSP'
    ip, port, login, password = proxy.split(":")
    proxy_extension = ProxyExtension(ip, int(port), login, password)

    options = uc.ChromeOptions()
    options.add_argument(f"--load-extension={proxy_extension.directory}")

    driver = uc.Chrome(version_main=108,options=options)
    driver.get("https://whoer.net/ru")
    time.sleep(3)
    driver.get("https://chat.openai.com/")
    time.sleep(5)


browser_with_proxy()



