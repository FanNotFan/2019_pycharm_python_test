from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 配置驱动位置
driver = webdriver.Chrome("/Users/fan/Develop/Library/Plugins/Chrom_Plugin/chromedriver")
# 打开如下页面
driver.get("http://www.python.org")
assert "Python" in driver.title

# WebDriver 提供了许多寻找网页元素的方法，譬如 find_element_by_* 的方法
elem = driver.find_element_by_id("id-search-field")
# elem = driver.find_element_by_name("q")

elem.send_keys("python")

# Keys class imported from selenium.webdriver.common.keys
# 模拟点击了回车
elem.send_keys(Keys.RETURN)

# 获取网页渲染后的源代码 page_source
print(driver.page_source)