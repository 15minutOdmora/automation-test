"""
Module containing driver classes.
Each driver class should inherit from BaseDriver.
"""

from __future__ import annotations
from typing import Callable, Tuple
import os

from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement


def get_driver(directory_path: str) -> str:
    """
    Fetch driver path from given directory.
    Functionality could be expanded to return specific versions, return a random one, most recent one, ...

    Args:
        directory_path (str): Relative or absolute path to directory

    Returns:
        str: Relative or absolute (based on dir. path) path to driver
    """
    drivers = os.listdir(directory_path)
    return os.path.join(directory_path, drivers[0])


class BaseDriver:
    """
    Base class for all drivers holding methods that slightly extend and simplify the functionality of the driver object.
    """
    def __wait_executor(
        self,
        implicit_wait_time: float,
        ignored_exceptions: tuple,
        waiting_function: Callable,
        by: By,
        selector: str
    ) -> WebElement:
        """
        Method executes the WebDriverWait function on self object, waiting the specified implicit time unitl the
        waiting_function call returns True. Method fetches element at the end, if element is fetched.
        Args:
            implicit_wait_time (float): Time to implicitly wait for waiting_function to return True
            ignored_exceptions (tuple): Tuple of Selenium Exceptions to ignore
            waiting_function (Callable): Callable function, most likely defined in the By package in Selenium.
            by (By): Fetch element by type of selector
            selector (str): Selector to fetch element
        Returns:
            WebElement: Fetched WebElement (if any)
        """
        element = WebDriverWait(
            self,
            implicit_wait_time,
            ignored_exceptions=ignored_exceptions
        ).until(waiting_function((by, selector)))

        return element

    def get_element_by_css_selector(
            self,
            selector: str,
            implicit_wait_time: float = 10,
            ignored_exceptions: Tuple = (),
            waiting_function: Callable = EC.presence_of_element_located,
    ) -> WebElement:
        """
        Element tries to fetch the element given by the CSS selector by waiting on its presence.
        Args:
            selector (str): CSS selector of element
            implicit_wait_time (float, optional): Max wait time to wait for element (in seconds). Defaults to 10.
            ignored_exceptions (Tuple): tuple of Selenium exceptions to ignore
            waiting_function (Callable):
        Returns:
            WebElement: Fetched element
        """
        element = self.__wait_executor(
            implicit_wait_time=implicit_wait_time,
            ignored_exceptions=ignored_exceptions,
            waiting_function=waiting_function,
            by=By.CSS_SELECTOR,
            selector=selector
        )
        return element

    def switch_to_iframe_by_css_selector(
            self,
            selector: str,
            implicit_wait_time: int = 10
    ):
        element = self.__wait_executor(
            implicit_wait_time=implicit_wait_time,
            ignored_exceptions=(),
            waiting_function=EC.frame_to_be_available_and_switch_to_it,
            by=By.CSS_SELECTOR,
            selector=selector
        )
        return element

    def switch_back_to_parent_frame(self) -> None:
        """
        Switches back to parent frame.
        """
        self.switch_to.parent_frame()

    def switch_back_to_default_content(self) -> None:
        """
        Switches back to default content.
        """
        self.switch_to.default_content()


class ChromeDriver(BaseDriver, Chrome):
    """
    Class for creating a Chrome based driver object. This class inherits from the parent class selenium.webdriver.Chrome.
    Extends parent by setting implicit wait, mobile emulation and if it should run headless or not.
    """
    def __init__(
        self,
        *args,
        executable_path: str = get_driver("drivers/chrome"),
        headless: bool = False,
        implicit_wait: int = 10,
        user_agent: str = None,
        options: Options = None,
        **kwargs
    ) -> None:
        """
        Args:
            *args: Get passed to Chrome driver constructor.
            executable_path (str): Directory of drivers to use one from. Defaults to get_driver("drivers/chrome").
            headless (bool): If execution should be done in headless mode. Defaults to False.
            implicit_wait (int): Implicit wait time between actions (where used). Defaults to 15.
            user_agent (str): User agent to use. Defaults to None.
            options (FirefoxOptions): Options to use in execution. Defaults to None.
            **kwargs: Get passed to Chrome driver constructor.
        """
        self.browser = "chrome"
        if options:
            self.options = options
        else:
            self.options = Options()
            self.user_agent = user_agent
            self.headless = headless

        # Initialize parent class and pass arguments
        super().__init__(*args, executable_path=executable_path, options=self.options, **kwargs)
        self.implicitly_wait(implicit_wait)

    @property
    def headless(self):
        return self._headless

    @headless.setter
    def headless(self, is_headless: bool):
        if is_headless:
            self.options.add_argument("headless")
            # Set window size to full (this might lag out headless mode otherwise)
            self.options.add_argument("--window-size=1920,1080")
            print("WebDriver: Mode = Headless.")
        else:
            print("WebDriver: Mode = Normal.")

    @property
    def user_agent(self):
        return self._user_agent

    @user_agent.setter
    def user_agent(self, agent):
        if agent:
            self.options.add_argument(f"--user-agent={agent}")


class FirefoxDriver(BaseDriver, Firefox):
    """
    Class for creating a Firefox based driver object. This class inherits from the parent class selenium.webdriver.Firefox.
    Extends parent by setting implicit wait, mobile emulation and if it should run headless or not.
    """
    def __init__(
        self,
        *args,
        executable_path: str = get_driver("drivers/gecko"),
        headless: bool = False,
        implicit_wait: int = 15,
        user_agent: str = None,
        options: FirefoxOptions = None,
        **kwargs
    ) -> None:
        """
        Args:
            *args: Get passed to Firefox driver constructor.
            executable_path (str): Directory of drivers to use one from. Defaults to get_driver("drivers/gecko").
            headless (bool): If execution should be done in headless mode. Defaults to False.
            implicit_wait (int): Implicit wait time between actions (where used). Defaults to 15.
            user_agent (str): User agent to use. Defaults to None.
            options (FirefoxOptions): Options to use in execution. Defaults to None.
            **kwargs: Get passed to Firefox driver constructor.
        """
        self.browser = "firefox"
        if options:
            self.options = options
        else:
            self.options = FirefoxOptions()
            self.headless = headless
            self.user_agent = user_agent
        # Initialize parent class and pass arguments
        super().__init__(*args, executable_path=executable_path, options=self.options, **kwargs)
        self.implicitly_wait(implicit_wait)
        self.set_window_size(360, 640)

    @property
    def headless(self):
        return self._headless

    @headless.setter
    def headless(self, is_headless: bool):
        if is_headless:
            self.options.add_argument("headless")
            self.window_size = (1920, 1080)  # Set window size to full (this might lag out headless mode otherwise)
            print(f"WebDriver {self.browser}: Mode = Headless.")
        else:
            print(f"WebDriver {self.browser}: Mode = Normal.")

    @property
    def user_agent(self):
        return self._mobile_emulation

    @user_agent.setter
    def user_agent(self, agent):
        if agent:
            self.options.set_preference("general.useragent.override", agent)


# This should get imported for checking currently available driver classes and initializing them
AvailableBrowserDrivers = {
    "chrome": ChromeDriver,
    "firefox": FirefoxDriver
}

# List of different user agents
AvailableUserAgents = [
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
]
