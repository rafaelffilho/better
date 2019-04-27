from selenium import webdriver
from colorama import Fore, init
import time
import sys
import os

init()																		# start colorama


base_bet = float(input("Enter the base bet: ").replace("\n", ""))
curr_bet = float(base_bet)

side = "null"

side = input("Choose your side [ct/t] ").replace("\n", "")

bet_count = 0
curr_money = 0
loses = 0

driver = webdriver.Firefox()
driver.get("https://csgoempire.com/")

usr_name = ""
usr_pass = ""

with open("user_info.txt", "r") as usr_info:
    usr_name = str(usr_info.readline()).replace("\n", "")
    usr_pass = str(usr_info.readline()).replace("\n", "")


try:
    driver.find_element_by_class_name("c-nav-buttons__login").click()
    driver.find_element_by_name("username").send_keys(usr_name)
    driver.find_element_by_name("password").send_keys(usr_pass)
except Exception as e:
    pass
input()

curr_money = driver.find_element_by_css_selector("span.u-hl-gold").text

initial_money = float(curr_money)

while True:
    time.sleep(1)
    try:
        driver.find_element_by_css_selector(".rolling-indicator")

        driver.find_element_by_css_selector(
            "button.c-radio-group__item:nth-child(1)").click()
        driver.find_element_by_class_name(
            "bet-amount").send_keys(str(curr_bet))
        driver.find_element_by_class_name(side).click()
        print("\n--------------------------------------------------------------------------------")
        print(Fore.YELLOW + "Betting " + str(curr_bet) +
              " on " + str(side) + Fore.RESET)

        t = driver.find_element_by_css_selector(
            ".rolling-overlay__time > span:nth-child(1)").text
        t = int(t) + 10
        print("Waiting ", t, " seconds to roll")

        time.sleep(t)

        try:
            driver.find_element_by_css_selector(
                "div.popup:nth-child(9) > p:nth-child(5) > label:nth-child(1) > i:nth-child(2)").click()
            driver.find_element_by_css_selector(
                "div.popup:nth-child(9) > div:nth-child(4) > a:nth-child(1)").click()
        except Exception as identifier:
            pass

        buf = driver.find_element_by_css_selector("span.u-hl-gold").text
        if (buf >= curr_money):
            curr_bet = float(base_bet)
            loses = 0
            print(Fore.GREEN + "Won " + str(float(buf) - curr_money) + Fore.RESET)
        else:
            curr_bet = float(float(curr_bet) * 2)
            loses = loses + 1
            print(Fore.RED + "Lost" + str(float(buf) - curr_money) + Fore.RESET)
        if (loses >= 6):
            loses = 0
            curr_bet = float(base_bet)
        curr_money = buf
        bet_count += 1
        print("Refreshing in ", str(5 - bet_count), " bets")
        if(bet_count >= 5):
            driver.refresh()
            bet_count = 0
        print("Balance: " + Fore.YELLOW + str(curr_money) + Fore.RESET)
        print("Total profit for the session: ", float(curr_money) - initial_money)
        print("Finished bet")
        print("--------------------------------------------------------------------------------")
        continue

    except Exception as identifier:
        continue
