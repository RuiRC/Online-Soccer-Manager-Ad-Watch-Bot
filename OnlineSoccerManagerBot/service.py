from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from colorama import init, Fore, Style
import re
import time

class OnlineSoccerManagerService:

    # instantiante env variables and webdriver
    def __init__(self):
        self.options = Options()
        self.options.set_preference("media.volume_scale", "0.0")
        self.options.add_argument("--headless")
        self.options.add_argument("--window-size=1280,720")
        self.driver = webdriver.Firefox(options=self.options)
        self.read_credentials()

    def read_credentials(self):
        with open("details.txt", "r") as file:
            lines = file.readlines()
            self.user = lines[0].strip()  
            self.password = lines[1].strip()  

    def getTokensAmount(self):
        bosscoins = self.driver.find_element("css selector", "span.pull-left")
        bosscoinsamount = bosscoins.text
        print(Fore.RED + "You have:", bosscoinsamount, "Bosscoins" + Style.RESET_ALL)
    
    def login(self, user, password):
        while True:
            try:
                # Open 'https://en.onlinesoccermanager.com' in firefox
                print(Fore.YELLOW + 'Opening Game Page and Waiting 5 Seconds...' + Style.RESET_ALL)
                self.driver.get('https://en.onlinesoccermanager.com')
                time.sleep(5)

                # Click in accept button
                print(Fore.YELLOW + 'Pressing Accept Button and Waiting 5 Seconds...' + Style.RESET_ALL)
                self.driver.find_element('css selector', '.btn-new').click()
                time.sleep(5)

                # Click in the login button
                print(Fore.YELLOW + 'Pressing Login Button and Waiting 5 seconds...' + Style.RESET_ALL)
                self.driver.find_element('css selector', '.btn-alternative').click()
                time.sleep(5)

                # Enter the user name
                self.driver.find_element("css selector", '#manager-name').send_keys(self.user)
                print(Fore.GREEN + 'Username pasted: ' + self.user + Style.RESET_ALL)

                # Enter the password
                password_field = self.driver.find_element("css selector", '#password')
                password_field.send_keys(self.password)
                print(Fore.GREEN + 'Password pasted: ' + self.password + Style.RESET_ALL)
                time.sleep(5)

                # Press the Enter key instead of clicking the login button
                print(Fore.YELLOW + 'Pressing Enter key' + Style.RESET_ALL)
                password_field.send_keys(Keys.RETURN)
                time.sleep(10)

                # Check if the logged-in user's name matches the expected user
                logged_in_user_element = self.driver.find_element('css selector', 'html body.en-GB div#page-content div#header.theme-panna-0 div.page-spacing.clearfix div#profile-dropdown.dropdown div#profile.header-menu-button.clickable-secondary.horizontal-right.vertical-center div.header-menu-button-text.hidden-xs div.header-titles div#manager-name.header-title.vertical-center bdi span.manager-name-text.ellipsis')
                logged_in_user = logged_in_user_element.text

                if logged_in_user == user:
                    print(Fore.GREEN + 'Login Successful' + Style.RESET_ALL)
                    break
                else:
                    print(Fore.RED + 'Login failed: Incorrect Username or Password' + Style.RESET_ALL)
                    continue

            except NoSuchElementException: 
                print(Fore.RED + 'Login Failed: Element Not Found. Retrying...' + Style.RESET_ALL) # OSM has an issue where the first login may not work, so we repeat it
                time.sleep(5)

                # Click in the login button
                print(Fore.YELLOW + 'Pressing Login Button and Waiting 5 seconds...' + Style.RESET_ALL)
                self.driver.find_element('css selector', '.btn-alternative').click()
                time.sleep(5)

                # Enter the user name
                self.driver.find_element("css selector", '#manager-name').send_keys(user)
                print(Fore.GREEN + 'Username pasted: ' + self.user + Style.RESET_ALL)

                # Enter the password
                password_field = self.driver.find_element("css selector", '#password')
                password_field.send_keys(password)
                print(Fore.GREEN + 'Password pasted: ' + self.password + Style.RESET_ALL)
                time.sleep(5)

                # Press the Enter key instead of clicking the login button
                print(Fore.YELLOW + 'Pressing Enter key' + Style.RESET_ALL)
                password_field.send_keys(Keys.RETURN)
                time.sleep(10)

                # Check if the logged-in user's name matches the expected user
                logged_in_user_element = self.driver.find_element('css selector', 'html body.en-GB div#page-content div#header.theme-panna-0 div.page-spacing.clearfix div#profile-dropdown.dropdown div#profile.header-menu-button.clickable-secondary.horizontal-right.vertical-center div.header-menu-button-text.hidden-xs div.header-titles div#manager-name.header-title.vertical-center bdi span.manager-name-text.ellipsis')
                logged_in_user = logged_in_user_element.text

                if logged_in_user == user:
                    print(Fore.GREEN + 'Login Successful' + Style.RESET_ALL)
                    break
                else:
                    print(Fore.RED + 'Login failed: Incorrect Username or Password' + Style.RESET_ALL)
                    continue

    def get_business_tokens(self):
        # call the login function
        self.login(self.user, self.password)
        time.sleep(5)

        # Check if the consent button exists and click it if present
        try:
            consent_button = self.driver.find_element('css selector', '.fc-cta-consent > p:nth-child(2)')
            if consent_button:
                consent_button.click()
                print(Fore.YELLOW + "Consented, Waiting 5 seconds" + Style.RESET_ALL)
                time.sleep(5)
        except:
            print(Fore.YELLOW + "Consent button not found" + Style.RESET_ALL)

        try:
            level_result_window = self.driver.find_element('css selector', '#modal-dialog-skillratingupdate')
            if level_result_window:
                # Perform the action if the element is found
                print(Fore.YELLOW + "Skill Modal Found, clicking and waiting for 5 seconds" + Style.RESET_ALL)
                offset_x = level_result_window.location['x'] + 50
                offset_y = level_result_window.location['y'] + 50
                action = ActionChains(self.driver)
                action.move_to_element_with_offset(level_result_window, offset_x, offset_y)
                action.click()
                action.perform()
                # Optional: Wait for some time after the click
                time.sleep(5)
        except NoSuchElementException:
            print(Fore.YELLOW + "No Skill Modal Found" + Style.RESET_ALL)

        try:
            welcome_message = self.driver.find_element('css selector', 'button.btn-new > span:nth-child(1)')
            if welcome_message:
                print(Fore.YELLOW + "Found Welcome Message, clicking and waiting for 5 seconds" + Style.RESET_ALL)
                welcome_message.click()
                time.sleep(5)
        except NoSuchElementException:
            print(Fore.YELLOW + "No Welcome Message found" + Style.RESET_ALL)

        print(Fore.YELLOW + "Going to Career page" + Style.RESET_ALL)
        self.getTokensAmount()
        self.driver.get('https://en.onlinesoccermanager.com')
        time.sleep(5)
        isStoreOpen = False
        while True:
            try:
                # go to the buissnes page in game
                storepage = self.driver.find_element('css selector', 'li.dropdown:nth-child(3)')
                if(isStoreOpen):
                    #Click on the ad if the storage page is open
                    self.driver.find_element(By.CSS_SELECTOR, 'div.product-free:nth-child(1)').click()
                    print(Fore.YELLOW + 'Clicking ad and Waiting for 7 Seconds' + Style.RESET_ALL)
                    time.sleep(7)  # Wait for the ad to load and start playing
                else:
                    print(Fore.YELLOW + 'Opening Store Page and Waiting for 5 Seconds' + Style.RESET_ALL)
                    storepage.click()
                    isStoreOpen = True
                    time.sleep(5)
                    self.driver.find_element(By.CSS_SELECTOR, 'div.product-free:nth-child(1)').click()
                    print(Fore.YELLOW + 'Clicking ad and Waiting for 7 Seconds' + Style.RESET_ALL)
                    time.sleep(7)  # Wait for the ad to load and start playing

                # Handle "Can't Show Video" popup if it appears
                try:
                    cant_show_video_popup = self.driver.find_element(By.CSS_SELECTOR, 'html body.en-GB.modal-open div#page-content div#genericModalContainer.modalContainer div.modal.modal-v2.fade.modal-xs-fullscreen.modal-md-normal.modal-lg-normal.small-modal.in div#modal-dialog-alert.modal-dialog div.row.row-h-xs-24.overflow-visible.modal-content-container div.theme-panna-1.col-xs-12.col-h-xs-24.modal-content div.row.row-h-xs-24.no-padding.modal-scrollable-content-container div.modal-body div.modal-header h3.modal-title')
                    wait_time_element = self.driver.find_element(By.CSS_SELECTOR, 'html body.en-GB.modal-open div#page-content div#genericModalContainer.modalContainer div.modal.modal-v2.fade.modal-xs-fullscreen.modal-md-normal.modal-lg-normal.small-modal.in div#modal-dialog-alert.modal-dialog div.row.row-h-xs-24.overflow-visible.modal-content-container div.theme-panna-1.col-xs-12.col-h-xs-24.modal-content div.row.row-h-xs-24.no-padding.modal-scrollable-content-container div.modal-body div.modal-body div.row div.col-xs-12 p')
                    wait_time_text = wait_time_element.text
                    match = re.search(r'(\d+)\s*(hours?|minutes?|seconds?)', wait_time_text, re.IGNORECASE)
                    if match:
                        num = int(match.group(1))
                        time_unit = match.group(2).lower()
                        wait_time = num * 60 if time_unit.startswith('minute') else num if time_unit.startswith('second') else num * 3600
                    elif 'a minute' in wait_time_text:
                        wait_time = 120  # 2 minutes (1 minute + 1 minute tolerance)
                    elif 'a few seconds' in wait_time_text:
                        wait_time = 60  # 1 minute
                    elif 'an hour' in wait_time_text:
                        wait_time = 3600 # 1 hour
                    else:
                        wait_time = 0
                    if wait_time > 0:
                        print(Fore.YELLOW + f"Waiting {wait_time // 60} minutes before attempting to watch the ad again." + Style.RESET_ALL)
                        remaining_wait_time = wait_time
                        # Click the button to close the "Can't Show Video" popup
                        self.driver.find_element(By.CSS_SELECTOR, '.btn-compact > span:nth-child(1)').click()
                        # Update every minute on how much longer to wait
                        while remaining_wait_time > 0:
                            time.sleep(60)  # Wait for 1 minute before updating the remaining time
                            remaining_wait_time -= 60
                            if remaining_wait_time > 0:
                                print(Fore.YELLOW + f"Waiting {remaining_wait_time // 60} more minutes..." + Style.RESET_ALL)
                    else:
                        print(Fore.GREEN + "Wait time completed, proceeding..." + Style.RESET_ALL)
                except NoSuchElementException:
                    print(Fore.YELLOW + 'No popup, checking ad status...' + Style.RESET_ALL)
                    # Check for either the countdown or the ad duration using the same element
                    ad_status_element = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, '#duration-text-aip'))
                    )
                    ad_status_text = ad_status_element.text
                    # Checking for countdown text
                    countdown_match = re.search(r'(\d+)s to close', ad_status_text)
                    if countdown_match:
                        # Countdown scenario
                        time_left = int(countdown_match.group(1))
                        print(Fore.YELLOW + f'Countdown detected: {time_left}s to close...' + Style.RESET_ALL)
                        while time_left > 0:
                            time.sleep(1)
                            time_left -= 1
                            ad_status_element = WebDriverWait(self.driver, 10).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, '#duration-text-aip'))
                            )
                            ad_status_text = ad_status_element.text
                            countdown_match = re.search(r'(\d+)s to close', ad_status_text)
                            if countdown_match:
                                time_left = int(countdown_match.group(1))
                                print(Fore.YELLOW + f'{time_left}s to close...' + Style.RESET_ALL)
                            else:
                                print(Fore.GREEN + "Countdown finished, waiting for close button." + Style.RESET_ALL)
                                break
                    else:
                        # Duration scenario
                        duration_match = re.search(r'(\d+):(\d+) / (\d+):(\d+)', ad_status_text)
                        if duration_match:
                            total_minutes, total_seconds = map(int, duration_match.groups()[2:])
                            total_ad_duration = total_minutes * 60 + total_seconds
                            print(Fore.YELLOW + f'Ad duration is {total_ad_duration} seconds, waiting for ad to finish...' + Style.RESET_ALL)
                            time.sleep(total_ad_duration + 5)

                    # After handling countdown or duration, wait for and click the close button if necessary
                    try:
                        close_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, '#aipVideoAdUiCloseButton > div:nth-child(2)'))
                        )
                        time.sleep(2)
                        close_button.click()
                        print(Fore.YELLOW + 'Ad closed.' + Style.RESET_ALL)
                    except TimeoutException:
                        print(Fore.YELLOW + 'Close button not needed or not found.' + Style.RESET_ALL)
                        self.getTokensAmount()

            except Exception as e:
                print(Fore.RED + f"Error occurred while watching ad: {e}\nRefreshing page and retrying..." + Style.RESET_ALL)
                self.driver.refresh()  # Refresh the page to attempt to recover from the error
                isStoreOpen = False # Page Refreshed so Store closed
                time.sleep(5)  # Wait a brief moment for the page to reload
                continue  # Continue the loop to retry the ad click process
            continue  # Continue to the next iteration to click on the ad again after handling the current ad
