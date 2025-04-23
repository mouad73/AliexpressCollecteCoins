import time
import random
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
ALIEXPRESS_EMAIL = os.getenv("ALIEXPRESS_EMAIL")
ALIEXPRESS_PASSWORD = os.getenv("ALIEXPRESS_PASSWORD")

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

def login(driver):
    """Perform the login process with human-like behavior"""
    try:
        print("Starting login process...")
        
        # Wait for the email input field
        wait = WebDriverWait(driver, 15)
        email_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.cosmos-input[label='Email']"))
        )
        print("Found email input field")
        
        # Ensure email field is visible in the viewport
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", email_input)
        random_sleep(1, 2)
        
        # Try to click directly without sophisticated mouse movement
        try:
            email_input.click()
        except Exception as e:
            print(f"Direct click failed: {e}, trying JavaScript click")
            driver.execute_script("arguments[0].click();", email_input)
        
        random_sleep(0.5, 1.5)
        
        # Type email with human-like behavior
        print("Entering email address...")
        type_like_human(email_input, ALIEXPRESS_EMAIL)  # Use environment variable
        random_sleep(1, 2)
        
        # Find and click the Continue button
        continue_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, 
                "//button[contains(@class, 'cosmos-btn-primary') and .//span[text()='Continue']]"))
        )
        print("Found continue button")
        
        # Ensure button is in view and click it
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", continue_button)
        random_sleep(0.5, 1)
        
        try:
            continue_button.click()
        except Exception as e:
            print(f"Direct click failed: {e}, trying JavaScript click")
            driver.execute_script("arguments[0].click();", continue_button)
            
        print("Clicked continue button")
        random_sleep(2, 3)
        
        # Wait for password field to appear
        password_input = wait.until(
            EC.presence_of_element_located((By.ID, "fm-login-password"))
        )
        print("Found password field")
        
        # Ensure password field is in view
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", password_input)
        random_sleep(0.5, 1)
        
        # Click on password field
        try:
            password_input.click()
        except Exception as e:
            print(f"Direct click failed: {e}, trying JavaScript click")
            driver.execute_script("arguments[0].click();", password_input)
            
        random_sleep(0.5, 1)
        
        # Type password with human-like behavior
        print("Entering password...")
        type_like_human(password_input, ALIEXPRESS_PASSWORD)  # Use environment variable
        random_sleep(1, 2)
        
        # Find and click the Sign in button
        sign_in_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, 
                "//button[contains(@class, 'cosmos-btn-primary') and .//span[text()='Sign in']]"))
        )
        print("Found sign in button")
        
        # Ensure sign in button is in view and click it
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", sign_in_button)
        random_sleep(0.5, 1)
        
        try:
            sign_in_button.click()
        except Exception as e:
            print(f"Direct click failed: {e}, trying JavaScript click")
            driver.execute_script("arguments[0].click();", sign_in_button)
            
        print("Clicked sign in button")
        
        # Wait for login to complete
        # Give more time for the login process to complete
        random_sleep(5, 7)
        print("Login successful")
        
        return True
    
    except Exception as e:
        print(f"Login failed: {e}")
        return False

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
        
        # MANUAL CONFIRMATION STEP 1
        input("STEP 1: Ship-to dropdown found. The element will be highlighted in red. Press Enter to click it...")
        
        # Highlight the element to make it obvious what will be clicked
        driver.execute_script("arguments[0].style.border='3px solid red'", ship_to_dropdown)
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
            country_selector = wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//div[contains(@class, 'select--text--1b85oDo')]"))
            )
            print("Found country selector")
            
            # MANUAL CONFIRMATION STEP 2
            input("STEP 2: Country selector found. The element will be highlighted in red. Press Enter to click it...")
            
            # Highlight the element
            driver.execute_script("arguments[0].style.border='3px solid red'", country_selector)
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
            
            # Now that the country dropdown is open, search for Korea
            search_input = wait.until(
                EC.presence_of_element_located((By.XPATH, 
                    "//div[contains(@class, 'select--search--20Pss08')]/input"))
            )
            print("Found country search input")
            
            # MANUAL CONFIRMATION STEP 3
            input("STEP 3: Search input found. The element will be highlighted in red. Press Enter to click and type 'Korea'...")
            
            # Highlight the element
            driver.execute_script("arguments[0].style.border='3px solid red'", search_input)
            random_sleep(1, 1)
            
            # Click on search input and type 'Korea'
            search_input.click()
            random_sleep(0.5, 1)
            type_like_human(search_input, "Korea")
            random_sleep(1, 2)
            
            # Find and click on Korea from the filtered list
            print("Looking for Korea option in the dropdown popup...")
            
            try:
                # Try with a more specific XPath targeting the exact structure
                korea_option = wait.until(
                    EC.element_to_be_clickable((By.XPATH, 
                        "//div[@class='select--item--32FADYB' and contains(., 'Korea')]"))
                )
                print("Found Korea option with exact class match")
            except Exception as e:
                print(f"First Korea selector failed: {e}, trying alternative approach")
                try:
                    # Try with a more general approach that looks for any div containing Korea with similar structure
                    korea_option = wait.until(
                        EC.element_to_be_clickable((By.XPATH, 
                            "//div[contains(@class, 'select--item') and .//span[contains(text(), 'Korea')]]"))
                    )
                    print("Found Korea option with general class and span")
                except Exception as e2:
                    print(f"Second Korea selector failed: {e2}, trying direct JavaScript selection")
                    # Use JavaScript to find elements containing Korea text
                    korea_options = driver.execute_script("""
                        return Array.from(document.querySelectorAll('div'))
                               .filter(el => el.textContent.includes('Korea') && 
                                       (el.className.includes('item') || el.className.includes('option')));
                    """)
                    if korea_options and len(korea_options) > 0:
                        korea_option = korea_options[0]
                        print("Found Korea option using JavaScript")
                    else:
                        # Last resort - try to find by the flag class
                        korea_option = wait.until(
                            EC.element_to_be_clickable((By.XPATH, 
                                "//span[contains(@class, 'country-flag') and contains(@class, 'KR')]/following-sibling::span"))
                        ).parent
                        print("Found Korea option via country flag")
            
            print("Found Korea option")
            
            # MANUAL CONFIRMATION STEP 4
            input("STEP 4: Korea option found. The element will be highlighted in red. Press Enter to click it...")
            
            # Highlight the element
            driver.execute_script("arguments[0].style.border='3px solid red'", korea_option)
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
                    "//div[contains(@class, 'es--saveBtn--w8EuBuy')]"))
            )
            print("Found save button")
            
            # MANUAL CONFIRMATION STEP 5
            input("STEP 5: Save button found. The element will be highlighted in red. Press Enter to click it...")
            
            # Highlight the element
            driver.execute_script("arguments[0].style.border='3px solid red'", save_button)
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
            
            # MANUAL CONFIRMATION STEP 6
            input("STEP 6: Country change complete. Press Enter to continue to the coin collection page...")
            
        except Exception as e:
            print(f"Save button interaction failed: {e}")
            return False
        
        return True
    
    except Exception as e:
        print(f"Country change failed: {e}")
        return False

def main():
    # Configure Chrome options to be more stealthy
    chrome_options = Options()
    
    # Add options that make automation less detectable
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Make the browser window visible and maximized
    chrome_options.add_argument("--start-maximized")
    
    # Initialize the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Set a realistic user agent
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    
    try:
        # Navigate to the website
        driver.get("https://www.aliexpress.com/p/coin-pc-index/index.html")
        print("Website loaded")
        
        # Add random delay to simulate page load analysis by human
        random_sleep(2, 4)
        
        # Check if we need to login and proceed with login if necessary
        if login(driver):
            print("Successfully logged in, proceeding to change country...")
            
            # Change country to Korea
            if change_country_to_korea(driver):
                print("Successfully changed country to Korea")
                
                # After changing country, we need to navigate back to the coin page
                print("Navigating back to coin collection page...")
                driver.get("https://s.click.aliexpress.com/e/_DB2kEjh")
                random_sleep(3, 5)
            else:
                print("Country change failed, continuing anyway...")
        else:
            print("Login process failed or wasn't needed, attempting to collect coins anyway...")
            
        # Add more random delay to simulate natural browsing behavior
        random_sleep(2, 3)
        
        # Scroll down gradually to simulate human reading
        total_height = driver.execute_script("return document.body.scrollHeight")
        viewport_height = driver.execute_script("return window.innerHeight")
        current_position = 0
        
        while current_position < total_height:
            # Scroll a random amount
            scroll_amount = random.randint(100, 300)
            current_position += scroll_amount
            driver.execute_script(f"window.scrollTo(0, {current_position});")
            random_sleep(0.5, 1.5)
        
        # Wait for the button to be present
        print("Looking for the Collect button...")
        wait = WebDriverWait(driver, 15)
        collect_button = wait.until(
            EC.presence_of_element_located((By.XPATH, 
                "//div[contains(@class, 'checkin-button')]"))
        )
        print("Found the Collect button")
        
        # Scroll to make button visible if needed
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", collect_button)
        random_sleep(1, 2)
        
        # Move mouse naturally to the button
        move_mouse_randomly(driver, collect_button)
        
        # Click the button
        print("Clicking the Collect button...")
        collect_button.click()
        
        # Wait after clicking to see the result
        random_sleep(5, 7)
        print("Button clicked successfully")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Don't close the browser immediately
        random_sleep(3, 5)
        driver.quit()

if __name__ == "__main__":
    main()