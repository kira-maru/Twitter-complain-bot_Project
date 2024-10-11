from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from twitter_bot import InternetSpeedTwitterBot

# Setting driver
twit_bot = InternetSpeedTwitterBot()

# Obtaining data from www.speedtest.net
twit_bot.find_and_click(EC, By.ID, "onetrust-accept-btn-handler")  # proceed with cookies' agreement
twit_bot.find_and_click(EC, By.LINK_TEXT, "GO")  # press 'GO' button

# Retrieving download speed data and sending tweet if value over provided amount
speed = twit_bot.download_speed(By.CLASS_NAME)

if speed is not None and speed < 1000:
    twit_bot.x_log_in()
    twit_bot.make_a_tweet()




