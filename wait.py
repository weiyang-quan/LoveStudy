"""
文件名：wait
创建时间：20:53
创作人：吴昭泉
"""  # 判断元素是否可见
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


def visible_xpath(locator, driver, timeout=20):
    """
    根据xpath的等待
    :param locator: 要判断的元素
    :param driver: 加载的驱动
    :param timeout: 等待时间，默认20
    :return:
    """
    try:
        WebDriverWait(driver, timeout).until(ec.visibility_of_element_located((By.XPATH, locator)))
        return True
    except Exception as e:
        return False


def visible_id(locator, driver, timeout=20):
    """
    根据id的等待
    :param locator: 要判断的元素
    :param driver: 加载的驱动
    :param timeout: 等待时间，默认20
    :return:
    """
    try:
        WebDriverWait(driver, timeout).until(ec.visibility_of_element_located((By.ID, locator)))
        return True
    except Exception as e:
        return False


def visible_class(locator, driver, timeout=20):
    """
    根据class的等待
    :param locator: 要判断的元素
    :param driver: 加载的驱动
    :param timeout: 等待时间，默认20
    :return:
    """
    try:
        WebDriverWait(driver, timeout).until(ec.visibility_of_element_located((By.CLASS_NAME, locator)))
        return True
    except Exception as e:
        return False



