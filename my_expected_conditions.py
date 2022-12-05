from typing import Any
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

class element_located_is_steady:

    def __init__(self, locator: Any) -> None:
        self.locator = locator
        self.element = None
        self.location = None
    
    def __call__(self, driver: Any) -> Any:
        if self.element is None:
            try:
                self.element = driver.find_element(*self.locator)
            except NoSuchElementException:
                return False
        
        try:
            if self.element.is_displayed():
                location = self.element.location
                if location == self.location:
                    return self.element
                self.location = location
        except StaleElementReferenceException:
            self.element = None
        
        return False
