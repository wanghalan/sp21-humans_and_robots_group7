from imgurpython import ImgurClient
import configparser

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def authenticate():
  #client_id = '854786241b5ff16'
  #client_secret = '90c6a5b0068fa60c3b6b047fffec2388fe6cd6c8'

  config = configparser.ConfigParser()
  config.read('auth.ini')

  client_id = config.get('credentials', 'client_id')
  client_secret = config.get('credentials', 'client_secret')

  imgur_username = config.get('credentials', 'imgur_username')
  imgur_password = config.get('credentials', 'imgur_password')

  client = ImgurClient(client_id, client_secret)

  
  authorization_url = client.get_auth_url('pin')

  print("Go to the following URL: {0}".format(authorization_url))

  browser = webdriver.Chrome()
  browser.get(authorization_url)

  username = browser.find_element_by_xpath('//*[@id="username"]')  
  password = browser.find_element_by_xpath('//*[@id="password"]')
  username.clear()
  username.send_keys(imgur_username)
  password.send_keys(imgur_password)  

  browser.find_element_by_name("allow").click()

  timeout = 2
  try:
    element_present = EC.presence_of_element_located((By.ID, 'pin'))
    WebDriverWait(browser, timeout).until(element_present)
    pin_element = browser.find_element_by_id('pin')
    pin = pin_element.get_attribute("value")
  except TimeoutException:
    print("Timed out waiting for page to load")

  print("Your pin is : " + pin)


  # ... redirect user to `authorization_url`, obtain pin (or code or token) ...
  credentials = client.authorize(pin, 'pin')
  client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

  print("Authentication successful! Here are the details:")
  print("   Access token:  {0}".format(credentials['access_token']))
  print("   Refresh token: {0}".format(credentials['refresh_token']))

  browser.close()

  return client

# If you want to run this as a standalone script, so be it!
if __name__ == "__main__":
  authenticate()



