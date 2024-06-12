from selenium import webdriver
import booking.constants as const
import os
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from booking.booking_filtrations import BookingFiltration
from booking.booking_report import BookingReport
from prettytable import PrettyTable


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"chromedriver.exe", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ["PATH"] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(20)
        self.maximize_window()

    # force close after code is finished
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def close_popup(self):
        self.get(const.BASE_URL)
        try:
            # check for popup window
            print("waiting for popup")
            popup_element = self.find_element(
                By.CSS_SELECTOR, "button[aria-label='Dismiss sign-in info.']"
            )
            popup_element.click()
            print("closed")
        except:
            print("no popup element")

    def change_currency(self, currency=None):
        currency_element = self.find_element(
            By.CSS_SELECTOR,
            "button.a83ed08757.c21c56c305.f38b6daa18.f671049264.deab83296e.fd3248769f",
        )
        currency_element.click()
        # choose a new currency
        currency  = currency.upper()
        new_currency_element = self.find_element(
            By.XPATH, f"//div[text()='{currency}']"
        )

        new_currency_element.click()

    def search_place_to_go(self, place):
        # destination field
        where_field = self.find_element(By.ID, ":re:")
        where_field.clear()
        where_field.send_keys(place)
        time.sleep(1)  # sleep for 1s so website can load data
        first_option = self.find_element(By.ID, "autocomplete-result-0")
        first_option.click()

    def select_dates(self, check_in_date, check_out_date):
        # select check in and check out dates
        check_in_element = self.find_element(
            By.CSS_SELECTOR, f'span[data-date="{check_in_date}"]'
        )
        check_in_element.click()
        check_out_element = self.find_element(
            By.CSS_SELECTOR, f'span[data-date="{check_out_date}"]'
        )
        check_out_element.click()

    def select_details(self, adults):
        # update number of adults, children, rooms
        selection_element = self.find_element(
            By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]'
        )
        selection_element.click()

        # adults

        while True:
            decrease_adults_button = self.find_element(
                By.CLASS_NAME,
                "a83ed08757.c21c56c305.f38b6daa18.d691166b09.ab98298258.deab83296e.bb803d8689.e91c91fa93",
            )
            decrease_adults_button.click()
            # getting the value of adults
            adults_value_element = self.find_element(By.ID, "group_adults")
            adults_value = adults_value_element.get_attribute("value")
            if int(adults_value) == 1:
                break

        increase_adults_button = self.find_element(
            By.CLASS_NAME,
            "a83ed08757.c21c56c305.f38b6daa18.d691166b09.ab98298258.deab83296e.bb803d8689.f4d78af12a",
        )

        for _ in range(adults - 1):
            increase_adults_button.click()

    def click_search(self):
        search_button = self.find_element(
            By.CLASS_NAME,
            "a83ed08757.c21c56c305.a4c1805887.f671049264.d2529514af.c082d89982.cceeb8986b",
        )
        search_button.click()

    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_filterations("Free cancellation", "Very Good: 8+")
        time.sleep(1)
        filtration.sort_price_lowest_first()

    def report_results(self):
        time.sleep(1)
        hotel_boxes = self.find_element(By.CSS_SELECTOR, 'div[class="bcbf33c5c3"]')
        report = BookingReport(hotel_boxes)
        table = PrettyTable(field_names=["Name", "Price", "Rating"])
        table.add_rows(report.pull_deal_boxes_attributes())
        print(table)
