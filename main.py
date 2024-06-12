from booking.booking import Booking
import time


try:
    with Booking() as bot:
        bot.close_popup()
        bot.change_currency(
            currency=input("Enter Currency Code (ex: USD , AUD, AED):  ")
        )
        bot.search_place_to_go(place=input("Enter Destination: "))
        bot.select_dates(
            check_in_date=input("Enter Check In Date: format yyyy-mm-dd: "),
            check_out_date=input("Enter Check Out Date: "),
        )
        bot.select_details(adults=int(input("Number of adults: ")))
        bot.click_search()
        bot.apply_filtrations()
        bot.refresh()  # give time to grap data properly
        bot.report_results()
except Exception as e:
    if "in PATH" in str(e):
        print(
            "You are To run the bot from command line \n"
            "please add path to your selenium drivers \n"
            "windows: \n"
            "set PATH=%PATH;C:path-to-your-folder \n \n"
            "Linux: \n"
            "PATH=%PATH:/path/toyour/folder/ \n"
        )
    else:
        raise
