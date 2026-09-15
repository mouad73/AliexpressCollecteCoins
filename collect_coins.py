import time
import random
import os
import sys
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


# === FORCE UTF-8 OUTPUT ===
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
COIN_URL = "https://s.click.aliexpress.com/e/_DB2kEjh"
# Dedicated Chrome profile: keeps the cookies, so you only need to log in once
PROFILE_DIR = os.path.join(SCRIPT_DIR, "chrome_profile")
# Max time (seconds) to wait for you to solve a captcha / finish login manually in the window
MANUAL_LOGIN_TIMEOUT = 300
# Country select in the "Ship to" popup: the only one whose list has the KR flag
COUNTRY_SELECT_XPATH = ("//div[contains(@class, 'select--wrap--') and "
                        ".//span[contains(concat(' ', normalize-space(@class), ' '), ' KR ')]]")

# Load environment variables from .env file (next to the script, works from Task Scheduler too)
load_dotenv(os.path.join(SCRIPT_DIR, ".env"))

# Get credentials from environment variables
ALIEXPRESS_EMAIL = os.getenv("ALIEXPRESS_EMAIL")
ALIEXPRESS_PASSWORD = os.getenv("ALIEXPRESS_PASSWORD")

print(f"Loaded Email: {ALIEXPRESS_EMAIL}")
print(f"Loaded Password: {'*' * len(ALIEXPRESS_PASSWORD) if ALIEXPRESS_PASSWORD else 'None'}")

# Check if credentials are available
if not ALIEXPRESS_EMAIL or not ALIEXPRESS_PASSWORD:
    print("Error: Environment variables for ALIEXPRESS_EMAIL and ALIEXPRESS_PASSWORD must be set.")
    print("Please create a .env file with these variables or set them in your environment.")
    exit(1)

def random_sleep(min_seconds=1, max_seconds=3):
    """Sleep for a random amount of time to mimic human behavior"""
    time.sleep(random.uniform(min_seconds, max_seconds))

def move_mouse_randomly(driver, element):
    """Move mouse with human-like randomness before clicking - safer version"""
    try:
        # Simply move directly to the element - safest approach
        actions = ActionChains(driver)
        actions.move_to_element(element)
        actions.perform()
        random_sleep(0.3, 0.7)
    except Exception as e:
        print(f"Warning: Simple mouse movement failed: {e}. Trying direct click.")

def type_like_human(element, text):
    """Type text with human-like timing and occasional mistakes that get corrected"""
    for char in text:
        # Randomly decide if we make a typo (1% chance)
        if random.random() < 0.01:
            # Make a typo
            typo_char = random.choice('qwertyuiopasdfghjklzxcvbnm')
            element.send_keys(typo_char)
            random_sleep(0.1, 0.3)
            # Delete the typo
            element.send_keys(Keys.BACKSPACE)
            random_sleep(0.2, 0.5)
        
        # Type the correct character
        element.send_keys(char)
        
        # Random pause between keystrokes
        random_sleep(0.05, 0.15)
        
        # Occasionally pause longer as if thinking
        if random.random() < 0.05:
            random_sleep(0.5, 1.2)

def is_logged_in(driver):
    """AliExpress only puts x_lid (user id) in the xman_us_t cookie after login"""
    try:
        cookie = driver.get_cookie("xman_us_t")
        return bool(cookie and "x_lid=" in cookie.get("value", ""))
    except Exception:
        return False

def wait_for_manual_login(driver, timeout=MANUAL_LOGIN_TIMEOUT):
    """Give the user time to solve a captcha / finish login in the open window instead of hanging"""
    print(f">>> Finish the login manually in the Chrome window (solve the captcha if one appears). "
          f"Waiting up to {timeout}s...")
    end = time.time() + timeout
    while time.time() < end:
        if is_logged_in(driver):
            print("Login detected!")
            return True
        time.sleep(3)
    print("Timed out waiting for manual login.")
    return False

def login(driver):
    """Perform the login process with human-like behavior"""
    if is_logged_in(driver):
        print("Already logged in (session saved in chrome_profile), skipping login.")
        return True
    try:
        print("Starting login process...")
        wait = WebDriverWait(driver, 15)
        short_wait = WebDriverWait(driver, 5)

        # The email input has no placeholder or id: "Email or phone number" is a floating label.
        email_xpath = ("//input[contains(@class, 'cosmos-input') and "
                       "(contains(@aria-label, 'mail') or contains(@aria-label, 'phone') or "
                       "contains(@aria-label, 'telefone') or @autocomplete='username webauthn')]")

        # STEP 1: Click the "Sign in" button only if the login form is not already on screen
        # (the coins link redirects straight to the login page).
        print("Looking for 'Sign in' button...")
        try:
            if driver.find_elements(By.XPATH, email_xpath):
                raise Exception("login form already visible")
            sign_in_button = short_wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Sign in') or contains(text(), 'Entrar')]"))
            )
            # Fall back to a JavaScript click if the normal click fails
            try:
                sign_in_button.click()
            except:
                driver.execute_script("arguments[0].click();", sign_in_button)
            print("Clicked 'Sign in' button.")
            random_sleep(2, 4) # Wait for the modal to open
        except Exception as e:
            print(f"Could not find or click 'Sign in' button: {e}. Assuming login form is already visible.")
            # If the button is not found, assume the form is already visible and continue.

        # STEP 2: Find the email input.
        print("Waiting for email input field...")
        email_input = wait.until(
            EC.visibility_of_element_located((By.XPATH, email_xpath))
        )
        print("Found email input field")
        
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", email_input)
        random_sleep(1, 2)
        
        try:
            email_input.click()
        except Exception as e:
            print(f"Direct click failed: {e}, trying JavaScript click")
            driver.execute_script("arguments[0].click();", email_input)
        
        random_sleep(0.5, 1.5)
        
        print("Entering email address...")
        type_like_human(email_input, ALIEXPRESS_EMAIL)
        random_sleep(1, 2)
        
        # STEP 3: Click "Continue".
        continue_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, 
                "//button[contains(@class, 'cosmos-btn-primary') and "
                "(@aria-label='Continue' or @aria-label='Continuar' or normalize-space(.)='Continue' or normalize-space(.)='Continuar')]"))
        )
        print("Found continue button")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", continue_button)
        random_sleep(0.5, 1)
        try:
            continue_button.click()
        except Exception as e:
            print(f"Direct click failed: {e}, trying JavaScript click")
            driver.execute_script("arguments[0].click();", continue_button)
        print("Clicked continue button")
        random_sleep(2, 3)
        
        # STEP 4: Enter the password.
        password_input = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='fm-login-password' or @type='password']"))
        )
        print("Found password field")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", password_input)
        random_sleep(0.5, 1)
        try:
            password_input.click()
        except Exception as e:
            print(f"Direct click failed: {e}, trying JavaScript click")
            driver.execute_script("arguments[0].click();", password_input)
        random_sleep(0.5, 1)
        
        print("Entering password...")
        type_like_human(password_input, ALIEXPRESS_PASSWORD)
        random_sleep(1, 2)
        
        # STEP 5: Click the final "Sign in" button.
        # The button text varies by language, so match several.
        print("Looking for final 'Sign in' button...")
        sign_in_button_final = wait.until(
            EC.element_to_be_clickable((By.XPATH, 
                "//button[contains(@class, 'cosmos-btn-primary') and "
                "(contains(@aria-label, 'Sign in') or contains(@aria-label, 'Entrar') or "
                "contains(normalize-space(.), 'Sign in') or contains(normalize-space(.), 'Entrar'))]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", sign_in_button_final)
        random_sleep(0.5, 1)
        try:
            sign_in_button_final.click()
        except Exception as e:
            print(f"Direct click failed: {e}, trying JavaScript click")
            driver.execute_script("arguments[0].click();", sign_in_button_final)
        print("Clicked final sign in button")

        # Confirm the login actually worked (a captcha/slider may appear after the password)
        for _ in range(10):
            if is_logged_in(driver):
                print("Login successful")
                return True
            time.sleep(1)
        print("Login not confirmed (captcha or verification probably appeared).")
        return wait_for_manual_login(driver)

    except Exception as e:
        print(f"Automatic login failed: {e}")
        return wait_for_manual_login(driver)
    
def change_country_to_korea(driver):
    """Change the country to Korea using the ship-to dropdown with manual confirmation at each step"""
    try:
        wait = WebDriverWait(driver, 15)
        
        # Look for the ship-to dropdown with the exact class structure from the HTML
        print("Looking for the ship-to dropdown...")
        try:
            # Try to find the main ship-to menu item
            ship_to_dropdown = wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//div[contains(@class, 'ship-to--menuItem--')]"))
            )
            print("Found ship-to dropdown using menuItem class")
        except Exception as e:
            print(f"menuItem selector failed: {e}, trying alternative selector")
            # Try looking for the div containing USD with dropdown icon
            try:
                ship_to_dropdown = wait.until(
                    EC.element_to_be_clickable((By.XPATH, 
                        "//div[contains(@class, 'ship-to--text--')]/b[contains(text(), 'USD')]"))
                )
                print("Found ship-to dropdown using USD text")
            except Exception as e2:
                print(f"USD text selector failed too: {e2}, trying broader selector")
                # Try the most specific element that should be unique to this dropdown
                ship_to_dropdown = wait.until(
                    EC.element_to_be_clickable((By.XPATH, 
                        "//div[contains(@class, 'es--wrap--')]/div/div[contains(@class, 'ship-to--menuItem--')]"))
                )
                print("Found ship-to dropdown using es--wrap container")
        
        # Scroll to make the dropdown visible
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", ship_to_dropdown)
        random_sleep(1, 2)
        
        # Highlight the element to make it visible in logs
        driver.execute_script("arguments[0].style.border='3px solid red'", ship_to_dropdown)
        print("STEP 1: Ship-to dropdown found. Clicking automatically...")
        random_sleep(1, 1)
        
        # Click on the ship-to dropdown
        try:
            ship_to_dropdown.click()
            print("Clicked ship-to dropdown using normal click")
        except Exception as e:
            print(f"Normal click failed: {e}, trying JavaScript click")
            driver.execute_script("arguments[0].click();", ship_to_dropdown)
            print("Clicked ship-to dropdown using JavaScript")
        
        random_sleep(2, 3)
        
        # Now look for the Korea option in the country dropdown section
        # First, find the country selector text element
        try:
            print("Looking for country selector...")
            # The popup has several selects (ZIP code, country, language, currency) with the same class.
            # The country one is the only list containing the KR flag, which works in any language.
            country_selector = wait.until(
                EC.element_to_be_clickable((By.XPATH, COUNTRY_SELECT_XPATH + "//div[contains(@class, 'select--text--')]"))
            )
            print("Found country selector")
            
            # Highlight the element
            driver.execute_script("arguments[0].style.border='3px solid red'", country_selector)
            print("STEP 2: Country selector found. Clicking automatically...")
            random_sleep(1, 1)
            
            # Click on the country selector to open the dropdown
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", country_selector)
            random_sleep(0.5, 1)
            
            try:
                country_selector.click()
                print("Clicked country selector using normal click")
            except Exception as e:
                print(f"Normal click failed: {e}, trying JavaScript click")
                driver.execute_script("arguments[0].click();", country_selector)
                print("Clicked country selector using JavaScript")
                
            random_sleep(1.5, 2.5)
            
            # Korea option: identified by the KR flag (the name changes: Korea / República da Coreia / 대한민국)
            print("STEP 3: Looking for Korea option (KR flag) in the dropdown popup...")
            korea_option = wait.until(
                EC.presence_of_element_located((By.XPATH,
                    COUNTRY_SELECT_XPATH + "//div[contains(@class, 'select--item--') and "
                    ".//span[contains(concat(' ', normalize-space(@class), ' '), ' KR ')]]"))
            )
            print("Found Korea option")
            
            # Highlight the element
            driver.execute_script("arguments[0].style.border='3px solid red'", korea_option)
            print("STEP 4: Korea option found. Clicking automatically...")
            random_sleep(1, 1)
            
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", korea_option)
            random_sleep(0.5, 1)
            
            try:
                korea_option.click()
                print("Selected Korea using normal click")
            except Exception as e:
                print(f"Normal click failed: {e}, trying JavaScript click")
                driver.execute_script("arguments[0].click();", korea_option)
                print("Selected Korea using JavaScript")
            
            random_sleep(1.5, 2.5)
            
        except Exception as e:
            print(f"Country selection process failed: {e}")
            return False
        
        # Look for Save button
        try:
            save_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//div[contains(@class, 'es--saveBtn--')]"))
            )
            print("Found save button")
            
            # Highlight the element
            driver.execute_script("arguments[0].style.border='3px solid red'", save_button)
            print("STEP 5: Save button found. Clicking automatically...")
            random_sleep(1, 1)
            
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", save_button)
            random_sleep(0.5, 1)
            
            # Click Save button
            try:
                save_button.click()
                print("Clicked save button using normal click")
            except Exception as e:
                print(f"Normal click failed: {e}, trying JavaScript click")
                driver.execute_script("arguments[0].click();", save_button)
                print("Clicked save button using JavaScript")
            
            random_sleep(3, 5)
            print("Country has been saved")
            print("STEP 6: Country change complete. Continuing to the coin collection page...")
            
        except Exception as e:
            print(f"Save button interaction failed: {e}")
            return False
        
        return True
    
    except Exception as e:
        print(f"Country change failed: {e}")
        return False

def set_korea_cookie(driver):
    """Force the Korea region through the aep_usuc_f cookie (the same value the popup saves).
    Needed when the account has a saved address and the popup only changes the language."""
    driver.add_cookie({
        "name": "aep_usuc_f",
        "value": "site=kor&c_tp=KRW&region=KR&b_locale=ko_KR",
        "domain": ".aliexpress.com",
        "path": "/",
        "expiry": int(time.time()) + 365 * 24 * 3600,
    })
    print("Region cookie set to Korea (region=KR, KRW)")

def verify_korea_selected(driver):
    """Verify Korea is the ship-to country by the header flag.
    The text is not reliable: 'City/KO/BRL' contains KO (language) while the country is still Brazil."""
    try:
        flag = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'ship-to--cssFlag--')]"))
        )
        text = driver.find_element(By.XPATH, "//div[contains(@class, 'ship-to--text--')]").text.replace("\n", " ")
        is_korea = " KR" in f" {flag.get_attribute('class')} "
        print(f"Current ship-to: {text} | flag: {flag.get_attribute('class').split()[-1]} -> "
              f"{'Korea OK' if is_korea else 'NOT Korea'}")
        return is_korea
    except Exception as e:
        print(f"Error verifying Korea selection: {e}")
        return False

def find_and_click_collect_button(driver):
    """Find and click the coin collect button with multiple approaches"""
    print("STEP 7: Looking for the Collect button...")
    wait = WebDriverWait(driver, 15)
    
    # List of possible selectors for the collect button - ordered from most to least specific
    collect_button_selectors = [
        "//div[contains(@class, 'checkin-button')]",
        "//div[contains(text(), 'Collect') and contains(@class, 'button')]",
        "//div[contains(text(), '출석체크') and contains(@class, 'button')]",  # Korean for "attendance check"
        "//div[contains(text(), '적립하기') and contains(@class, 'button')]",   # Korean for "collect"
        "//div[contains(text(), '체크인') and contains(@class, 'button')]",     # Korean for "check-in"
        "//button[contains(@class, 'check-in') or contains(@class, 'checkin')]",
        "//div[contains(@class, 'coin') and contains(@class, 'collect')]",
    ]
    
    # Try each selector until one works
    for selector in collect_button_selectors:
        try:
            print(f"Trying to find collect button with selector: {selector}")
            collect_button = wait.until(
                EC.presence_of_element_located((By.XPATH, selector))
            )
            print(f"Found the Collect button using selector: {selector}")
            
            # Highlight the button to make it more visible
            driver.execute_script("arguments[0].style.border='3px solid red'", collect_button)
            random_sleep(1, 2)
            
            # Scroll to make button visible if needed
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", collect_button)
            random_sleep(1, 2)
            
            # Try to click button with several methods
            try:
                # Move mouse naturally to the button first
                move_mouse_randomly(driver, collect_button)
                
                # Try normal click
                collect_button.click()
                print("Clicked collect button using normal click")
            except Exception as e:
                print(f"Normal click failed: {e}, trying JavaScript click")
                driver.execute_script("arguments[0].click();", collect_button)
                print("Clicked collect button using JavaScript")
            
            # Wait after clicking to see the result
            random_sleep(5, 7)
            print("Collect button clicked successfully")
            return True
            
        except Exception as e:
            print(f"Couldn't find or click collect button with selector {selector}: {e}")
            continue
    
    # If no button found, try a more aggressive approach - look for any clickable element that might be the collect button
    try:
        print("Trying fallback approach - looking for any element that might be the collect button")
        
        # Use JavaScript to find elements that might be collect buttons
        potential_buttons = driver.execute_script("""
            return Array.from(document.querySelectorAll('div, button, a'))
                  .filter(el => {
                      const text = el.textContent.toLowerCase();
                      return (text.includes('collect') || 
                              text.includes('check') || 
                              text.includes('출석') || 
                              text.includes('적립') || 
                              text.includes('체크')) && 
                             (el.className.includes('button') || 
                              el.tagName === 'BUTTON' ||
                              el.style.cursor === 'pointer');
                  });
        """)
        
        if potential_buttons and len(potential_buttons) > 0:
            print(f"Found {len(potential_buttons)} potential collect buttons using JavaScript")
            
            # Try clicking the first potential button
            button = potential_buttons[0]
            driver.execute_script("arguments[0].style.border='3px solid red'", button)
            random_sleep(1, 2)
            
            # Scroll to button
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
            random_sleep(1, 2)
            
            # Click the button using JavaScript
            driver.execute_script("arguments[0].click();", button)
            
            print("Clicked potential collect button using JavaScript")
            random_sleep(5, 7)
            return True
    except Exception as e:
        print(f"Fallback approach failed: {e}")
    
    print("Could not find any collect button despite multiple attempts")
    print("*** WILL RESTART FROM STEP 1 (COUNTRY SELECTION) ***")
    return False

def main():
    """Main function to run the coin collection process"""
        # Set up Chrome options
    chrome_options = Options()
    
    # Force Chrome to start in English so Google Translate does not kick in
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    
    # Disable the translator and password saving in Chrome's internal preferences
    chrome_options.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False,
        'translate': {'enabled': False},
        'intl.accept_languages': 'en-US,en'
    })
    
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument(f"--user-data-dir={PROFILE_DIR}")

    driver = None
    try:
        # Selenium 4.10+ downloads the matching chromedriver automatically (Selenium Manager)
        print("Starting Chrome...")
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Selenium Manager failed ({e}), trying drivers/chromedriver.exe")
        local_driver = os.path.join(SCRIPT_DIR, "drivers", "chromedriver.exe")
        try:
            driver = webdriver.Chrome(service=Service(local_driver), options=chrome_options)
        except Exception as e2:
            print(f"Failed to start Chrome: {e2}")
            print("Close any Chrome window still using the chrome_profile folder and try again.")
            return
    print("WebDriver initialized successfully")

    # Prevent driver.get from hanging forever
    driver.set_page_load_timeout(60)
    # Hide navigator.webdriver (no user agent override: a UA from another Chrome version gives the bot away)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    try:
        # Navigate to the website
        try:
            driver.get(COIN_URL)
        except Exception as e:
            print(f"Page load timed out ({e}), continuing with what loaded")
        print("Website loaded")
        
        # Add random delay to simulate page load analysis by human
        random_sleep(2, 4)
        
        # Check if we need to login and proceed with login if necessary
        login_successful = login(driver)
        if not login_successful:
            print("Login process failed, attempting to continue anyway...")
        else:
            print("Successfully logged in")

        # Main collection loop - allows restarting from Step 1 when needed
        max_total_attempts = 3  # Maximum number of complete cycles to try
        total_attempts = 0
        
        while total_attempts < max_total_attempts:
            total_attempts += 1
            print(f"Starting collection attempt {total_attempts}/{max_total_attempts}")
            
            # STEP 1-5: Change country to Korea (Step 6 is inside the function)
            print("RESTARTING FROM STEP 1: Changing country to Korea")
            if verify_korea_selected(driver):
                print("Korea already active, skipping popup")
            else:
                if not change_country_to_korea(driver):
                    print(f"Country popup failed on attempt {total_attempts}")
                random_sleep(5, 7)

                # With a saved account address, the popup sometimes only changes the language (KO) and keeps the old country.
                if not verify_korea_selected(driver):
                    print("Popup did not switch the country, forcing it via cookie...")
                    set_korea_cookie(driver)
                    driver.refresh()
                    random_sleep(4, 6)

            # Navigate to the coin page
            print("Going to coin page after country change.")
            try:
                driver.get(COIN_URL)
            except Exception as e:
                print(f"Page load timed out ({e}), continuing with what loaded")
            random_sleep(5, 7)

            if not verify_korea_selected(driver):
                print(f"Country is still NOT Korea on attempt {total_attempts} "
                      "(the account address may be overriding it). Retrying...")
                continue

            # STEP 7: Look for the collect button
            if find_and_click_collect_button(driver):
                print("Successfully collected coins!")
                break  # Exit the loop if successful
            print(f"Failed to find collect button on attempt {total_attempts}, restarting from Step 1")
                
        if total_attempts >= max_total_attempts:
            print("Maximum attempts reached without successful coin collection.")
            
        print("Coin collection process completed.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Don't close the browser immediately
        print("Script execution complete. Closing browser in 5 seconds...")
        random_sleep(3, 5)
        driver.quit()

if __name__ == "__main__":
    main()