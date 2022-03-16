"""
Test expendable module.
"""

from typing import List
import time

from usefull.driver import ChromeDriver, FirefoxDriver, AvailableUserAgents
from usefull.helpers import analyse_error, TimeMeasure
import css_selectors as selectors


def test_scenario(driver):
    """
    Test scenario execution, use assertions to check functionality of tested code.

    Args:
        driver (Webdriver): Webdriver instance used.
    """
    # Open website
    driver.get("http://test.celtra.com/preview/f576e12f#overrides.deviceInfo.deviceType=Phone")  # Hardcoded :(
    # Switch to phone iframe -> Not needed as we do mobile emulation
    # driver.switch_to_iframe_by_css_selector(selectors.phone_iframe)

    # Content loaded
    # Switch to expandable iFrame
    driver.switch_to_iframe_by_css_selector(selectors.expandable_iframe)
    # Get modal element
    banner_element = driver.get_element_by_css_selector(selectors.expendable_button)
    assert banner_element  # Check if not None
    assert banner_element.is_displayed()  # Check if displayed
    # Trigger modal open
    banner_element.click()
    # Switch back to previous iFrame
    driver.switch_back_to_parent_frame()
    time.sleep(1.5)  # Modal opening animation takes about 1.5s  (Should not take more)

    # Modal unit loaded
    # Switch to modal iFrame
    driver.switch_to_iframe_by_css_selector(selectors.modal_iframe)
    # Check if modal visible
    modal_div_element = driver.get_element_by_css_selector(selectors.modal_div)
    assert modal_div_element.is_displayed()

    # Logo disappearance
    celtra_logo = driver.get_element_by_css_selector(selectors.celtra_logo)
    assert celtra_logo
    assert celtra_logo.is_displayed()
    celtra_logo.click()
    # Check if logo disappeared
    assert not celtra_logo.is_displayed()

    # Close modal
    close_modal_button = driver.get_element_by_css_selector(selectors.close_modal_button)
    assert close_modal_button
    # Click close button using js, not working with Firefox otherwise
    driver.execute_script('arguments[0].click()', close_modal_button)
    # Check if modal is not visible
    assert not modal_div_element.is_displayed()


def test_expandable(driver_class) -> List[any]:
    """
    Executes above test scenario with given driver class (initialized here).
    Times execution and in case of error analyses error data.

    Args:
        driver_class (class): Class of driver to instantiate and execute test with

    Returns:
        List[any]: List containing test execution data:
            [
            bool Successful,
            str browser type,
            float execution time,
            str type of error,
            str filename,
            int line,
            str function name,
            str code that triggered error
            ]
    """
    user_agent = AvailableUserAgents[0]  # Could pick one at random
    driver = driver_class(user_agent=user_agent)
    timer = TimeMeasure()
    timer.start()
    try:
        test_scenario(driver)
    except Exception as e:  # Catch every exception
        error_data = analyse_error(output=True)
        return [0, driver.browser, timer.elapsed_seconds, type(e).__name__] + error_data
    finally:
        timer.stop()
        driver.close()
    return [1, driver.browser, timer.elapsed_seconds, "", "", "", "", ""]


if __name__ == "__main__":
    # Testing purpose
    driver = ChromeDriver
    # driver = FirefoxDriver(mobile_emulation={"deviceName": "Nexus 5"})
    result = test_expandable(driver)
    print(result)
