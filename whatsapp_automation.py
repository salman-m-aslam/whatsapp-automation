from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import socket
import pandas as pd
import winsound


# assign message to be sent to a variable
message_text = """"""


# create a list containing mobile numbers
mobile_no_list = []
df1 = pd.read_csv("content/current_list.csv")
for i in df1['Mob']:
    mobile_no_list.append(i)


# open whatsapp.com in an instance of brave browser
brave_path = "C:/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe"
option = webdriver.ChromeOptions()
option.binary_location = brave_path
driver = webdriver.Chrome(executable_path="content/chromedriver.exe", options=option)
driver.get("https://web.whatsapp.com")
sleep(30)


df1 = pd.read_csv("content/current_list.csv", index_col="Mob")
print("An element could not be located for the following numbers:")


def is_connected():

    try:
        socket.create_connection(("www.duckduckgo.com", 80))
        return True

    except:
        is_connected()


def element_presence(xpath, time):
    WebDriverWait(driver, time).until(ec.presence_of_element_located((By.XPATH, xpath)))


def send_whatsapp_msg(phone_no, text):

    driver.get("https://web.whatsapp.com/send?phone={}&source=&data=#".format(phone_no))

    try:
        element_presence('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]', 30)
        txt_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')

        # try:
        #     driver.switch_to.alert().accept()
        #
        # except:
        #     pass

        txt_box.send_keys(Keys.CONTROL, "v")
        sleep(0.5)
        # element_presence('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div[1]/span/div/div[2]/div/div[3]/div[1]/div[2]', 30)
        # txt_box_2 = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div[1]/span/div/div[2]/div/div[3]/div[1]/div[2]')
        # txt_box_2.send_keys("\n")
        #
        # for line in text.splitlines():
        #
        #     txt_box.send_keys(line, Keys.SHIFT, Keys.ENTER)

        txt_box.send_keys("\n")
        sleep(2)

    except Exception as e:
        print(str(phone_no), e, sep="\n")
        frequency = 2500
        duration = 3000
        winsound.Beep(frequency, duration)
        df2 = pd.DataFrame({'Mob': [phone_no]})
        df2.to_csv('content/error_list.csv', mode='a', index=False, header=False)
        df1.drop(phone_no, inplace=True)


def main():

    for mobile_no in mobile_no_list:

        try:
            send_whatsapp_msg(mobile_no, message_text)

        except:
            sleep(5)
            is_connected()
    # df1.to_csv('content/current_list.csv')


if __name__ == '__main__':
    main()
