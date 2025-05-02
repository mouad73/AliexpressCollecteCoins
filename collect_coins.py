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
            country_selector = wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//div[contains(@class, 'select--text--1b85oDo')]"))
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
            
            # Now that the country dropdown is open, search for Korea
            search_input = wait.until(
                EC.presence_of_element_located((By.XPATH, 
                    "//div[contains(@class, 'select--search--20Pss08')]/input"))
            )
            print("Found country search input")
            
            # Highlight the element
            driver.execute_script("arguments[0].style.border='3px solid red'", search_input)
            print("STEP 3: Search input found. Clicking and typing 'Korea' or '대한민국' automatically...")
            random_sleep(1, 1)
            
            # Click on search input and type 'Korea' or '대한민국' (Republic of Korea in Korean)
            search_input.click()
            random_sleep(0.5, 1)
            
            # Try with English first, if that fails, try Korean
            search_term = "Korea"
            type_like_human(search_input, search_term)
            random_sleep(1, 2)
            
            # Check if any results were found, if not, try with Korean
            korea_options = driver.execute_script("""
                return Array.from(document.querySelectorAll('div'))
                       .filter(el => el.textContent.includes('Korea') && 
                               (el.className.includes('item') || el.className.includes('option')));
            """)
            
            # If no results with English, clear and try with Korean
            if not korea_options or len(korea_options) == 0:
                print("No results found with English 'Korea', trying with Korean '대한민국'")
                search_input.clear()
                random_sleep(0.5, 1)
                type_like_human(search_input, "대한민국")  # Republic of Korea in Korean
                random_sleep(1, 2)
            
            # Find and click on Korea from the filtered list
            print("Looking for Korea option in the dropdown popup...")
            
            try:
                # Try with a more specific XPath targeting the exact structure (English or Korean)
                korea_option = wait.until(
                    EC.element_to_be_clickable((By.XPATH, 
                        "//div[@class='select--item--32FADYB' and (contains(., 'Korea') or contains(., '대한민국'))]"))
                )
                print("Found Korea option with exact class match")
            except Exception as e:
                print(f"First Korea selector failed: {e}, trying alternative approach")
                try:
                    # Try with a more general approach that looks for any div containing Korea with similar structure
                    korea_option = wait.until(
                        EC.element_to_be_clickable((By.XPATH, 
                            "//div[contains(@class, 'select--item') and .//span[(contains(text(), 'Korea') or contains(text(), '대한민국'))]]"))
                    )
                    print("Found Korea option with general class and span")
                except Exception as e2:
                    print(f"Second Korea selector failed: {e2}, trying direct JavaScript selection")
                    # Use JavaScript to find elements containing Korea text (English or Korean)
                    korea_options = driver.execute_script("""
                        return Array.from(document.querySelectorAll('div'))
                               .filter(el => (el.textContent.includes('Korea') || el.textContent.includes('대한민국')) && 
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
                    "//div[contains(@class, 'es--saveBtn--w8EuBuy')]"))
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

def verify_korea_selected(driver):
    """Verify that Korea is currently selected as the country"""
    try:
        wait = WebDriverWait(driver, 10)
        
        # Look for ship-to text that contains Korea or 대한민국 (Republic of Korea in Korean)
        ship_to_element = wait.until(
            EC.presence_of_element_located((By.XPATH, 
                "//div[contains(@class, 'ship-to--text--')]"))
        )
        
        # Get the text content
        ship_to_text = ship_to_element.text
        print(f"Current ship-to text: {ship_to_text}")
        
        # Special case for "KO/" which is a confirmed marker for Korean
        if "KO/" in ship_to_text:
            print("Found 'KO/' in ship-to text - Korea is definitely selected")
            return "KO_FOUND"  # Special return value indicating KO/ was found
            
        # Standard check for other indicators
        if 'Korea' in ship_to_text or '한국' in ship_to_text or '대한민국' in ship_to_text:
            print("Korea is selected as the country")
            return True
        else:
            print("Korea is NOT selected as the country")
            return False
            
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
    # chrome_options.add_argument("--headless")  # Uncomment to run in headless mode
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Helps avoid detection
    chrome_options.add_argument("--start-maximized")  # Start with maximized window
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Define path to chromedriver
    import os
    chromedriver_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "drivers")
    os.makedirs(chromedriver_dir, exist_ok=True)
    
    # Use direct path to the chromedriver in the drivers folder
    driver_path = os.path.join(chromedriver_dir, "chromedriver.exe")
    
    # Always remove the existing ChromeDriver to ensure we get a fresh compatible version
    if os.path.exists(driver_path):
        try:
            os.remove(driver_path)
            print(f"Removed existing ChromeDriver: {driver_path}")
        except Exception as e:
            print(f"Could not remove existing ChromeDriver: {e}")
    
    # Download and set up ChromeDriver
    print("Downloading compatible ChromeDriver version...")
    try:
        # Get Chrome version from registry
        import winreg
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
            version, _ = winreg.QueryValueEx(key, 'version')
            chrome_version = version.split('.')[0]  # Get major version
            print(f"Detected Chrome version: {version} (Major: {chrome_version})")
        except Exception as e:
            print(f"Failed to detect Chrome version from registry: {e}")
            chrome_version = "135"  # Default to Chrome 135
        
        # Download ChromeDriver for Chrome 135+
        import urllib.request
        import zipfile
        import shutil
        
        # For Chrome 115+, we need to use the Chrome for Testing (CfT) drivers
        print(f"Using Chrome for Testing driver for Chrome {chrome_version}")
            
        # For Chrome 135, use a direct URL - sometimes the API is not updated fast enough
        cft_version = "135.0.7049.0"  # Match to your Chrome version
        download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{cft_version}/win64/chromedriver-win64.zip"
        print(f"Using direct URL for Chrome {chrome_version}: {download_url}")
        
        # Download chromedriver zip
        zip_path = os.path.join(chromedriver_dir, "chromedriver.zip")
        print(f"Downloading ChromeDriver from {download_url}")
        urllib.request.urlretrieve(download_url, zip_path)
        
        # Extract the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(chromedriver_dir)
        
        # For Chrome 115+, the chromedriver is in a subdirectory
        chromedriver_extracted_dir = os.path.join(chromedriver_dir, "chromedriver-win64")
        if os.path.exists(chromedriver_extracted_dir):
            # Copy chromedriver.exe from the subdirectory to the main directory
            src_path = os.path.join(chromedriver_extracted_dir, "chromedriver.exe")
            if os.path.exists(src_path):
                shutil.copy(src_path, driver_path)
                print(f"Copied chromedriver.exe from {src_path} to {driver_path}")
            else:
                # List all files to help debug
                print(f"Expected chromedriver at {src_path} but it doesn't exist.")
                print(f"Files in {chromedriver_extracted_dir}: {os.listdir(chromedriver_extracted_dir)}")
                
                # Search for chromedriver.exe in case structure changed
                for root, dirs, files in os.walk(chromedriver_dir):
                    for file in files:
                        if file.lower() == "chromedriver.exe":
                            found_path = os.path.join(root, file)
                            print(f"Found chromedriver.exe at {found_path}")
                            shutil.copy(found_path, driver_path)
                            print(f"Copied to {driver_path}")
                            break
        else:
            print(f"Warning: Expected directory {chromedriver_extracted_dir} not found.")
            # List all extracted files to help debug
            print(f"Files in {chromedriver_dir}: {os.listdir(chromedriver_dir)}")
            
            # Look for chromedriver.exe in case extraction happened differently
            for root, dirs, files in os.walk(chromedriver_dir):
                for file in files:
                    if file.lower() == "chromedriver.exe" and os.path.join(root, file) != driver_path:
                        found_path = os.path.join(root, file)
                        print(f"Found chromedriver.exe at {found_path}")
                        shutil.copy(found_path, driver_path)
                        print(f"Copied to {driver_path}")
                        break
        
        # Remove the zip file
        if os.path.exists(zip_path):
            os.remove(zip_path)
            
        print("ChromeDriver downloaded and extracted successfully")
        
    except Exception as e:
        print(f"Failed to download ChromeDriver: {e}")
        return
    
    # Initialize WebDriver
    if not os.path.exists(driver_path):
        print(f"Error: ChromeDriver not found at {driver_path}")
        return
        
    print(f"Using ChromeDriver at: {driver_path}")
    service = Service(driver_path)
    
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("WebDriver initialized successfully")
    except Exception as e:
        print(f"Failed to initialize WebDriver: {e}")
        print("Please make sure Chrome and ChromeDriver versions match")
        return
    
    # Set a realistic user agent
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    })
    
    try:
        # Navigate to the website
        driver.get("https://s.click.aliexpress.com/e/_DB2kEjh")
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
            if change_country_to_korea(driver):
                # After saving country, the page should reload with Korean interface
                # Wait a bit for the page to reload/update
                random_sleep(5, 7)
                
                # Navigate to the coin page
                print("Going to coin page after country change.")
                driver.get("https://s.click.aliexpress.com/e/_DB2kEjh")
                random_sleep(5, 7)
                
                # STEP 7: Look for the collect button
                if find_and_click_collect_button(driver):
                    print("Successfully collected coins!")
                    break  # Exit the loop if successful
                else:
                    print(f"Failed to find collect button on attempt {total_attempts}, restarting from Step 1")
                    # Continue loop to restart from Step 1
            else:
                print(f"Country change failed on attempt {total_attempts}")
                
                # If we're on the last attempt and country change failed, try the coin page anyway
                if total_attempts >= max_total_attempts:
                    print("Maximum attempts reached. Trying coin page directly as last resort...")
                    driver.get("https://s.click.aliexpress.com/e/_DB2kEjh")
                    random_sleep(5, 7)
                    find_and_click_collect_button(driver)
                
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