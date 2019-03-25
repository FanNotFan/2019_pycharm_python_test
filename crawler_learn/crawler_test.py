import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

CrawlerWebSiteIndex = 'http://www.dancingbearsinn.com/index.html'
ChromeDriverPath = "/Users/fan/Develop/Library/Plugins/Chrom_Plugin/chromedriver"
SearchContent = "youtube"
Form_Name = 'Lennon'
Form_Email = '547878909@qq.com'


# 测试用例是继承了 unittest.TestCase 类，继承这个类表明这是一个测试类
class PythonOrgSearch(unittest.TestCase):
    # setUp方法是初始化的方法，这个方法会在每个测试类中自动调用
    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverPath)

    # 每一个测试方法命名都有规范，必须以 test 开头，会自动执行
    def test_crawler(self):
        driver = self.driver
        time.sleep(1)
        driver.get(CrawlerWebSiteIndex)
        # 页面等待
        try:
            # 通过元素的name定位
            nameElem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "Name"))
            )
            # 通过元素的name定位
            emailElem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "Email"))
            )
            print(nameElem)
            print(emailElem)
            # submitElem = driver.find_element_by_css_selector("span[value='submit'")
        finally:
            driver.quit()

        nameElem.send_keys(Form_Name)
        emailElem.send_keys(Form_Email)
        # ActionChains(driver).click(submitElem).perform()

    # 最后的 tearDown 方法会在每一个测试方法结束之后调用（相当于析构函数）
    # close 方法相当于关闭了这个 TAB选项卡
    # quit  是退出了整个浏览器
    def tearDown(self):
        self.driver.close()