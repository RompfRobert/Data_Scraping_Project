# Import packages
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep

# Broker site
broker_url = 'https://www.flatex.de/produkte-handel/produkte/cfd/cfd-demo-konto/login/'

# Credentials for login
login_credentials = {
    'username': 'bc_data_hw',
    'password': 'sirm.clab7EENG4spog'
}

# Instrument list to scrape
instrument_list = ["EURUSD",
                   "GBPUSD",
                   "AUDUSD",
                   "EURCHF",
                   "EURGBP",
                   "US 500 INDEX",
                   "EURO 50 INDEX",
                   "APPLE INC",
                   "VODAFONE GROUP PLC"]


# Helper functions

# Waits for an element to appear
def get_element(driver, by, selector):
    return WebDriverWait(driver, 10).until(lambda d: driver.find_element(by, selector))


# Waits for elements to appear, returns an array
def get_elements(driver, by, selector):
    return WebDriverWait(driver, 10).until(lambda d: driver.find_elements(by, selector))


# Scraper function which should output a dictionary with the instrument names as keys and the spread values
def scrape_spreads():
    with Chrome() as driver:
        # Open broker site
        driver.get(broker_url)
        driver.implicitly_wait(120)

        # Try to close the cookie popup window
        try:
            cookie_accept_button = get_element(driver, By.CSS_SELECTOR, '.sg-cookie-optin-box-button-accept-all')
            cookie_accept_button.click()
        except:
            pass

        # Fill login credentials
        username_field = login_credentials.get('username')
        get_element(driver, By.ID, "user").send_keys(username_field)
        password_field = login_credentials.get('password')
        get_element(driver, By.ID, "pass").send_keys(password_field)

        # Press login button and wait
        login_button = get_element(driver, By.CSS_SELECTOR, "input[type=\"submit\" i]")
        login_button.click()
        sleep(3)

        # Start a demo account by clicking the demo button and wait
        demo_button = get_element(driver, By.XPATH, "//*[@id=\"c10410\"]/div/p/a")
        demo_button.click()
        sleep(3)

        # Open the search window and wait
        search_button = get_element(driver, By.ID, "applicationbariconbutton-1052")
        search_button.click()
        sleep(3)

        # Search for every instrument and scrape the spreads
        spreads = {}
        search_field = driver.find_element(By.ID, "textfield-1302-inputEl")
        for instrument in instrument_list:
            try:
                values_list = []
                # Write into search field the instrument name
                search_field.send_keys(instrument)
                sleep(1)
                # Get the bid ask values, if that fails the spread should be 0.
                bid_price = get_element(driver, By.XPATH,
                                        "/html/body/div[6]/div[2]/div/div/div[1]/div[2]/div/table/tbody/tr/td[3]/div/a")
                bid_price_new = bid_price.text.replace(".", "")
                # Parse text into float values
                values_list.append(float(bid_price_new.replace(",", ".")))
                ask_price = get_element(driver, By.XPATH,
                                        "/html/body/div[6]/div[2]/div/div/div[1]/div[2]/div/table/tbody/tr/td[4]/div/a")
                ask_price_new = ask_price.text.replace(".", "")
                # Parse text into float values
                values_list.append(float(ask_price_new.replace(",", ".")))
            except ValueError:
                values_list.append(0)
                values_list.append(0)
            # Add spread to the dictionary
            spreads[instrument] = values_list
            search_field.clear()

        return spreads


print(scrape_spreads())
