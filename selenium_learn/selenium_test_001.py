import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# action 行动 chains 链
from selenium.webdriver.common.action_chains import ActionChains

GoogleIndex = "https://www.google.com/"
ChromeDriverPath = "/Users/fan/Develop/Library/Plugins/Chrom_Plugin/chromedriver"
SearchContent = "youtube"

# 测试用例是继承了 unittest.TestCase 类，继承这个类表明这是一个测试类
class PythonOrgSearch(unittest.TestCase):
    # setUp方法是初始化的方法，这个方法会在每个测试类中自动调用
    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverPath)

    # 每一个测试方法命名都有规范，必须以 test 开头，会自动执行
    def test_serch_in_python_ory(self):
        driver = self.driver
        driver.get(GoogleIndex)
        # self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys(SearchContent)
        elem.send_keys(Keys.ENTER)

        # 页面等待
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "rc"))
            )
            ActionChains(driver).click(element).perform()
        finally:
            driver.quit()

    # 最后的 tearDown 方法会在每一个测试方法结束之后调用（相当于析构函数）
    # close 方法相当于关闭了这个 TAB选项卡
    # quit  是退出了整个浏览器
    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
