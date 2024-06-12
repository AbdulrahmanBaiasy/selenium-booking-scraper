from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_filterations(self, *filters):
        popular_filteration_box = self.driver.find_element(
            By.ID, "filter_group_popular_:rj:"
        )
        popular_child_elements = popular_filteration_box.find_elements(
            By.CSS_SELECTOR, "div[data-filters-item]"
        )
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "filter_group_popular_:rj:"))
        )

        for filter_item in filters:
            for element in popular_child_elements:
                innerHTML = str(element.get_attribute("innerHTML")).strip()
                if f"{filter_item}" in innerHTML:
                    element.click()
                    
                    
    def sort_price_lowest_first(self): 
        drop_down_sorters = self.driver.find_element(
            By.CSS_SELECTOR, 
            'button[data-testid="sorters-dropdown-trigger"]'
        )
        drop_down_sorters.click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-id="price"]')))
        price_sort = self.driver.find_element(
            By.CSS_SELECTOR , 
            'button[data-id="price"]'
        )
        price_sort.click()
