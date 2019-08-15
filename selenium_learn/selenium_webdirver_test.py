
import time
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
ua = UserAgent()
target_website_url = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
# target_website_url = 'https://www.hyatt.com/shop/seagh?rooms=1&adults=1&location=seattle%2C%20washington%2C%20united%20states&checkinDate=2019-08-01&checkoutDate=2019-08-02&kids=0&rate=Standard'
# target_website_url = "https://www.agoda.com/los-angeles-adventurer-all-suite-hotel/hotel/los-angeles-ca-us.html?checkin=2019-07-06&los=1&adults=2&rooms=1&cid=-1&searchrequestid=78330461-996d-4189-ae6e-6a9cff85cf2c&travellerType=1&tspTypes=8,9&tabbed=true"
# target_website_url = "https://www.trip.com/hotels/los-angeles-hotel-detail-2024722/hotel-figueroa-downtown-los-angeles/"

chromedriver_path = "/Users/hiCore/Software/WebDrivers/chromedriver_75"
extension_path = '/Users/hiCore/Develop/Workspace_Own/Workspace_Pycharm/2019_pycharm_python_test/selenium_learn/BaiduExporter/BaiduExporter.crx'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'referer': 'http://google.com'
}

injected_javascript = (
   """
      delete navigator.__proto__.webdriver;
      Object.defineProperty(navigator, 'webdriver', {
        get: () => false,
      });
      window.navigator.chrome = {
        runtime: {},
      };
      Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5],
      });
      Object.defineProperty(navigator, 'languages', {
        get: () => ['en-US', 'en'],
      });
      originalQuery = window.navigator.permissions.query;
      return window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' ?
          Promise.resolve({ state: Notification.permission }) :
          originalQuery(parameters)
      );
   """
)

def chrome_webdriver():
    options = webdriver.ChromeOptions()
    # 添加实验性质的设置参数 SSL errors
    options.add_experimental_option('excludeSwitches', ['enable-automation', "ignore-certificate-errors"])
    # 添加启动参数 (add_argument)
    # required when running as root user. otherwise you would get no sandbox
    options.add_extension(extension_path)
    # dubug need open this
    # options.add_argument('--no-sandbox')
    options.add_argument('--profile-directory=Default')
    options.add_argument("--incognito")
    # 开
    options.add_argument('--disable-extensions')
    # options.add_argument("--disable-plugins-discovery")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    # options.add_argument('--headless')
    options.add_argument("--window-size=1920x1080")
    options.add_argument(f'user-agent={ua.random}')
    browser = webdriver.Chrome(chromedriver_path, options=options, service_args=['--verbose', '--log-path=./chromedriver.log'])
    browser.get(target_website_url)
    browser.execute_script("""
              delete navigator.__proto__.webdriver;
              window.navigator.chrome = {
                runtime: {},
              };
              Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
              });
              Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
              });
           """)
    time.sleep(5)
    print(browser.page_source)
    browser.close()


# hyatt
def chrome_driver2():
    def init_browser():
        options = webdriver.ChromeOptions()
        # 'enable-automation' 让webdriver undetected
        options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        options.add_experimental_option('excludeSwitches', ['enable-automation', "ignore-certificate-errors"])
        browser = webdriver.Chrome(executable_path=chromedriver_path, options=options, service_args=['--verbose', '--log-path=./chromedriver.log'])
        return browser
    browser = init_browser()
    browser.get(target_website_url)
    time.sleep(7)
    print(browser.page_source)
    browser.close()


def chrome_driver3():
    def init_browser():
        options = webdriver.ChromeOptions()
        # options.add_extension(extension_path)
        options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        options.add_argument('--disable-extensions')
        # options.add_argument('--headless')
        # 添加UserAgent
        # options.add_argument(f'user-agent={ua.random}')
        webdriver.Remote('http://http://10.184.144.12:48080', desired_capabilities=webdriver.DesiredCapabilities.CHROME)
        browser = webdriver.Chrome(executable_path=chromedriver_path, options=options, service_args=['--verbose', '--log-path=./chromedriver.log'])
        return browser

    browser = init_browser()
    browser.execute_script(injected_javascript)
    browser.get(target_website_url)
    time.sleep(10)
    print(browser.page_source)
    browser.close()


def phantom_webdriver():
    def init_browser():
        PhantomJS_Path = "/Users/hiCore/Software/WebDrivers/phantomjs"

        service_args = []
        service_args.append('--load-images=no')  ##关闭图片加载
        service_args.append('--disk-cache=yes')  ##开启缓存
        service_args.append('--ignore-ssl-errors=true')  ##忽略https错误

        cap = DesiredCapabilities.PHANTOMJS.copy()

        for key, value in HEADERS.items():
            cap['phantomjs.page.customHeaders.{}'.format(key)] = value

        browser = webdriver.PhantomJS(executable_path=PhantomJS_Path, desired_capabilities=cap, service_args=service_args)
        # browser.set_window_size(1400, 900)
        # 设置phantomjs浏览器全屏显示
        browser.maximize_window()
        browser.set_page_load_timeout(40)
        browser.set_script_timeout(40)
        return browser

    browser = init_browser()
    browser.delete_all_cookies()
    browser.set_window_size(800, 800)
    browser.set_window_position(0, 0)
    browser.get(target_website_url)
    browser.execute_script("""
           delete navigator.__proto__.webdriver;
        """)
    # delete
    # navigator.__proto__.webdriver;
    # Object.defineProperty(navigator, 'plugins', {
    #     get: () = > [1, 2, 3, 4, 5],
    # });
    # Object.defineProperty(navigator, 'languages', {
    #     get: () = > ['en-US', 'en'],
    # });
    time.sleep(5)
    print(browser.page_source)
    browser.close()


if __name__ == '__main__':
    # phantom_webdriver()
    chrome_webdriver()
    # chrome_driver2()
    # chrome_driver3()