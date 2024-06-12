# parsing the specific data needed from deal boxes
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


class BookingReport:
    def __init__(self, boxes_section_element: WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(
            By.CSS_SELECTOR, 'div[data-testid="property-card"]'
        )

    def pull_deal_boxes_attributes(self):
        collection = []
        for deal_box in self.deal_boxes:
            # titles
            deal_title = (
                deal_box.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]')
                .get_attribute("innerHTML")
                .strip()
            ).replace("&amp;", " ")
            # prices
            deal_prices = (
                deal_box.find_element(
                    By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]'
                )
                .get_attribute("innerHTML")
                .strip()
            ).replace("&nbsp;", " ")

            # rating
            rating = (
                deal_box.find_element(By.CLASS_NAME, "a3b8729ab1.d86cee9b25")
                .find_element(By.CLASS_NAME, "ac4a7896c7")
                .text
            )
            # Add data
            collection.append([deal_title, deal_prices, rating])
        return collection
