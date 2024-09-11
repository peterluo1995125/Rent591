import os
import requests
import re
from bs4 import BeautifulSoup
import emoji
import schedule
import time

# Line Notify Token (replace with your own token)
LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN", "LZwTB697WWpPOxiu27TWBKu0oiZYndd6eJdVexekm7h")

# Line Notify API URL
LINE_NOTIFY_API = "https://notify-api.line.me/api/notify"

# 發送 LINE Notify 訊息的函數
def send_line_notify_message(message):
    headers = {
        "Authorization": f"Bearer {LINE_NOTIFY_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "message": message
    }
    response = requests.post(LINE_NOTIFY_API, headers=headers, data=data)
    if response.status_code == 200:
        print("消息已成功發送至 LINE Notify")
    else:
        print("發送失敗，狀態碼:", response.status_code)

# Function to get rental information from 591
def get_rental_info():
    url = "https://rent.591.com.tw/list?section=26,41&price=20000_30000&layout=2&other=lift,new&region=3&notice=not_cover&orderType=desc"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    }

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    houses = soup.find_all('div', class_='item-info')

    messages = []

    # Parsing each house
    for house in houses:
        # Extracting details
        title = house.find('a', class_='link').get('title')

        if "應福華" in title:
            continue

        price = house.find('strong', class_='text-26px').text.strip()

        update_info = house.find('span', class_='line', string=lambda text: '更新' in text)
        uptime = update_info.text.strip() if update_info else "N/A"

        link = house.find("a", class_="link v-middle").get("href")

        address_element = house.find("i", class_="ic-house house-place")
        address = address_element.find_next("span").text.strip() if address_element else "N/A"

        layout_element = house.find("span", string=lambda x: x and '房' in x)
        layout = layout_element.text.strip() if layout_element else "N/A"

        distance_label_element = house.find("span", string=lambda x: x and '距' in x)
        if distance_label_element:
            distance_label = distance_label_element.text.strip()
            distance_value_element = distance_label_element.find_next("strong")
            distance_value = distance_value_element.text.strip() if distance_value_element else "N/A"
            distance = f"{distance_label} {distance_value}"
        else:
            distance = "無顯示距離"

        update_time_element = house.find("span", string=lambda x: x and '小時內更新' in x)
        if update_time_element:
            update_time_text = update_time_element.text.strip()
            hours = int(''.join(filter(str.isdigit, update_time_text)))
            if hours < 4:  # Only show entries updated within 3 hours
                message = (
                    f"名稱: {title}\n"
                    f"網址: {link}\n"
                    f"價格: {price}\n"
                    f"格局: {layout}\n"
                    f"地址: {address}\n"
                    f"距離: {distance}\n"
                    f"更新: {uptime}"
                )
                messages.append(message)

    return messages

# Function to send rental updates via Line Notify
def send_rental_updates():
    rental_updates = get_rental_info()
    
    if rental_updates:
        msg = emoji.emojize('\n🤡🤡🤡 窮鬼還想租房子? \n租屋網有物件更新666! 🤔🤔🤔 \n\n')
        for update in rental_updates:
            msg += f"{update}\n\n--------------\n"
        
        send_line_notify_message(msg)
    else:
        no_update_msg = emoji.emojize('🙄 沒更新好嗎窮鬼')
        send_line_notify_message(no_update_msg)

# Function to run every 3 hours
def job():
    print("Fetching rental updates...")
    send_rental_updates()

# Schedule the job every 3 hours
#schedule.every(3).hours.do(job)

if __name__ == "__main__":
    job()  # Run it immediately on start
    #while True:
        #schedule.run_pending()
        #time.sleep(1)
