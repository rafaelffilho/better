from selenium import webdriver
import time
import sys
import os
from colorama import Fore, init

# Bet buttons class are
# ct & t

init()																		# start colorama


base_bet = float(input("Enter the base bet: "))
curr_bet = float(base_bet)

side = "null"

while(side != "ct" or side != "t"):
	side = input("Choose your side [ct/t] ")

bet_count = 0
curr_money = 0
loses = 0

driver = webdriver.Firefox()
driver.get("https://csgoempire.com/")

usr_info = open("user_info.txt", "r")
usr_name = usr_info.readline()
usr_pass = usr_info.readline()
usr_info.close()

try:
	driver.find_element_by_class_name("c-nav-buttons__login").click()
	driver.find_element_by_name("username").send_keys(usr_name)
	driver.find_element_by_name("password").send_keys(usr_pass)
except Exception as e:
	pass
input()

curr_money = driver.find_element_by_css_selector("span.u-hl-gold").text

while True:
	time.sleep(1)
	try:
		driver.find_element_by_css_selector(".rolling-indicator")

		driver.find_element_by_css_selector("button.c-radio-group__item:nth-child(1)").click()
		driver.find_element_by_class_name("bet-amount").send_keys(str(curr_bet))
		driver.find_element_by_class_name(side).click()
		print("\n--------------------------------------------------------------------------------")
		print(Fore.YELLOW + "Betted " +  str(curr_bet) + " on " + str(side) + Fore.RESET)

		t = driver.find_element_by_css_selector(".rolling-overlay__time > span:nth-child(1)").text
		t = int(t) + 10
		print("Waiting to roll - ", t)

		time.sleep(t)

		try:
			driver.find_element_by_css_selector("div.popup:nth-child(9) > p:nth-child(5) > label:nth-child(1) > i:nth-child(2)").click()
			driver.find_element_by_css_selector("div.popup:nth-child(9) > div:nth-child(4) > a:nth-child(1)").click()
		except Exception as identifier:
			pass

		buf = driver.find_element_by_css_selector("span.u-hl-gold").text
		if (buf >= curr_money):
			curr_bet = float(base_bet)
			loses = 0
			print(Fore.GREEN + "Win" + Fore.RESET)
		else:
			curr_bet = float(float(curr_bet) * 2)
			loses = loses + 1
			print(Fore.RED + "Lose" + Fore.RESET)
		if (loses >= 6):
			loses = 0
			curr_bet = float(base_bet)
		curr_money = buf
		print("Finished")
		bet_count += 1
		print("Betted times ", str(bet_count))
		if(bet_count >= 5):
			driver.refresh()
			bet_count = 0
		print("Current balance: " + Fore.YELLOW + str(curr_money) + Fore.RESET)
		print("--------------------------------------------------------------------------------")
		continue

	except Exception as identifier:
		continue

# Wait time for next roll is 19 sec

#time.sleep(10)

