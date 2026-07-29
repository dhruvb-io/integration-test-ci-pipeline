import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Safari()

driver.maximize_window()

driver.get("http://127.0.0.1:5001/")

# Wait for page to load
time.sleep(2)

# Enter user name
textbox = driver.find_element(By.NAME, "name")
textbox.send_keys("Dhruv")

# Pause so you can see the entered text
time.sleep(2)

# Click Create User
button = driver.find_element(By.TAG_NAME, "button")
button.click()

print("User created successfully!")

# Keep browser open for 5 seconds after submission
time.sleep(5)

driver.quit()