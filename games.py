import json
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException
from threading import Thread, Event
import subprocess
from webdriver_manager.chrome import ChromeDriverManager

# Function to install required dependencies
def install_dependencies():
    try:
        import selenium
        from webdriver_manager.chrome import ChromeDriverManager
    except ImportError:
        print("Missing dependencies detected. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium", "webdriver-manager"])

# Run the setup function to ensure dependencies are installed
install_dependencies()

# Global stop event to signal when to stop the script
stop_event = Event()

# Function to log the last processed game
def log_last_game(game_name):
    with open('last_game_log.txt', 'w') as log_file:
        log_file.write(f"Last game processed: {game_name}\n")

# Parse input from console
args = sys.argv
console_name = None
year_range = None
target_game = None

# Extract console, year range, and target game name from arguments
for i, arg in enumerate(args):
    if arg.startswith("console:"):
        console_name = arg.split(":")[1]
    elif arg.startswith("year:"):
        year_range = arg.split(":")[1]
    elif i > 2:  # Anything after console and year is assumed to be the game name
        if target_game:
            target_game += " " + arg  # Continue adding to the game name if spaces are involved
        else:
            target_game = arg  # Initialize target game

# Strip quotes from target game if present
if target_game:
    target_game = target_game.replace('"', '')

start_year, end_year = map(int, year_range.split('-'))

# Setup Selenium WebDriver
chrome_options = Options()
chrome_options.page_load_strategy = 'normal'  # Default page load strategy

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()


# Step 1: Setup region to US
def setup_region_to_us():
    driver.execute_script("window.open('https://www.ign.com', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    
    try:
        # Wait for the dropdown and select the region
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "region-dropdown")))
        region_dropdown = driver.find_element(By.ID, "region-dropdown")
        region_dropdown.click()
        us_region_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'option[data-language="US"]'))
        )
        us_region_option.click()
    except NoSuchElementException:
        print("Region dropdown not found, assuming the region is already set to US.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Continue with the rest of the logic regardless of whether the dropdown was found
    WebDriverWait(driver, 10).until(EC.url_contains("https://www.ign.com"))
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    
# Background function to scroll down every 15 seconds
def scroll_page_periodically(driver):
    try:
        while not stop_event.is_set():
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(30)
    except InvalidSessionIdException:
        print("Session ended during scrolling.")

# Step 2: Navigate to the correct page based on the console name
url = f"https://www.ign.com/games/platform/{console_name}"
driver.get(url)

# Sort by oldest release date
sort_option = Select(driver.find_element(By.ID, "sortOption"))
sort_option.select_by_value("releaseOld")

# Function to extract year from the date string
def extract_year(date_str):
    if "TBA" in date_str or any(quarter in date_str for quarter in ['Q1', 'Q2', 'Q3', 'Q4']):
        return None
    try:
        year = int(next(part for part in date_str.split() if part.isdigit() and len(part) == 4))
        return year
    except (ValueError, StopIteration):
        return None

# Helper function to convert shorthand numbers like '2.2k' to integers
def parse_shorthand_number(num_str):
    num_str = num_str.lower()
    if 'k' in num_str:
        return int(float(num_str.replace('k', '')) * 1000)
    elif 'm' in num_str:
        return int(float(num_str.replace('m', '')) * 1000000)
    else:
        return int(num_str)

# Function to calculate the final score
def calculate_final_score(amount_reviews, rating):
    return ((amount_reviews * rating) + (50 * 6)) / (amount_reviews + 50)

# Scroll and scrape function
def scroll_and_scrape():
    games_data = []
    processed_items = set()
    out_of_range_count = 0
    consecutive_valid_items = 0
    first_in_range_found = False
    target_game_found = not bool(target_game)

    while not stop_event.is_set():
        try:
            items = driver.find_elements(By.CSS_SELECTOR, "figure.figure-tile")
        except Exception as e:
            print(f"Error fetching items: {e}")
            break

        for item in items:
            if stop_event.is_set():
                return games_data

            try:
                game_link = item.find_element(By.CSS_SELECTOR, "a.tile-link").get_attribute("href")
                if game_link in processed_items:
                    continue
                processed_items.add(game_link)

                try:
                    release_date = item.find_element(By.CSS_SELECTOR, "div.tile-meta").text
                    release_year = extract_year(release_date)
                    if release_year is None or release_year < start_year or release_year > end_year:
                        driver.execute_script("arguments[0].remove();", item)
                        continue
                except NoSuchElementException:
                    driver.execute_script("arguments[0].remove();", item)
                    continue

                driver.execute_script(f"window.open('{game_link}', '_blank');")
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(2)
                driver.execute_script("window.stop();")

                game_name = driver.find_element(By.CSS_SELECTOR, "h1.display-title").text
                log_last_game(game_name)

                analytic_elements = driver.find_elements(By.CSS_SELECTOR, "a.analytic-with-text-box")
                if len(analytic_elements) >= 1:
                    first_analytic = analytic_elements[0]
                    rating_text = first_analytic.find_element(By.CSS_SELECTOR, "h3").text
                    rating = float(rating_text.strip())
                    reviews_text = first_analytic.find_element(By.CSS_SELECTOR, "div.caption").text
                    reviews_count = parse_shorthand_number(reviews_text.split()[0])
                else:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    driver.execute_script("arguments[0].remove();", item)
                    continue

                final_score = calculate_final_score(reviews_count, rating)
                games_data.append({
                    "name": game_name,
                    "rating": rating,
                    "reviews": reviews_count,
                    "final_score": final_score
                })

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                driver.execute_script("arguments[0].remove();", item)

            except Exception as e:
                print(f"Error processing item: {e}")
                try:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                except:
                    pass
                driver.execute_script("arguments[0].remove();", item)

# Function to listen for user input
def listen_for_input():
    while not stop_event.is_set():
        user_input = input("Press 'q' to quit and save progress: ").lower()
        if user_input == 'q':
            stop_event.set()

setup_region_to_us()
scroll_thread = Thread(target=scroll_page_periodically, args=(driver,))
scroll_thread.daemon = True
scroll_thread.start()

input_thread = Thread(target=listen_for_input)
input_thread.daemon = True
input_thread.start()

games_data = scroll_and_scrape()
games_data.sort(key=lambda x: x["final_score"], reverse=True)

with open('games_data.json', 'w') as json_file:
    json.dump(games_data, json_file, indent=4)

driver.quit()
print("Script ended, progress saved.")
