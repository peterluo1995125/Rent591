import requests, re
from bs4 import BeautifulSoup
#要抓取頁面的Url
url = "https://rent.591.com.tw/list?section=26,41&price=20000_30000&layout=2&other=lift,new&region=3&notice=not_cover&orderType=desc"

#自訂 Request Headers
headers = {
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding" : "gzip, deflate, br",
    "Accept-Language" : "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection" : "keep-alive",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Upgrade-Insecure-Requests" : "1",
    "Cache-Control" : "max-age=0",
    "Host" : "rent.591.com.tw",   
    "Cookie" : "urlJumpIp=8; urlJumpIpByTxt=%E5%8F%B0%E4%B8%AD%E5%B8%82; is_new_index=1; is_new_index_redirect=1; T591_TOKEN=0mgp6gnmca0m1aes0a653qpk76; _ga=GA1.3.1853129893.1614755590; tw591__privacy_agree=0; _ga=GA1.4.1853129893.1614755590; _fbp=fb.2.1614755592267.503379817; new_rent_list_kind_test=0; _gid=GA1.3.990458239.1615170698; _gid=GA1.4.990458239.1615170698; webp=1; PHPSESSID=ugspv0rqvnetihun53ane0jlc4; XSRF-TOKEN=eyJpdiI6ImloZzR5Qm9SRk1XNVd4bmJ2VG8zNUE9PSIsInZhbHVlIjoiSExCSnRITEZjSE8rWktjVEptSnlEd1AxNEs1cHRcL1dEYktOR0dvUUNwdU9vNVVPUHlaK3UyXC9pOWpCVElxV0JJdzZGWFF0bytcL3MrSGNGSlpyQk96OGc9PSIsIm1hYyI6IjQ5NDgzZjc1YWExYTkyZDQ2YWRjZWQwZDI5YTIwODZhMTJkYzNlMmZiYzUwNmZmMzY2YjNhZjQ4NGI4OGY2NjMifQ%3D%3D; 591_new_session=eyJpdiI6ImpYUE9QWDJWYVwvaVlJc3dUK0ZiY3h3PT0iLCJ2YWx1ZSI6ImVMYnpSQ2ZhNG9VZHNSdWZNMjZTSG5nUTZOaWZlZ05kQkRXVkNLZDAxQlBqWWJneXVZbXZEWmd6SVRrMU5ZbGtrOU9tVG9RZm1CM2ZKUnNYQVlJaTNRPT0iLCJtYWMiOiIwN2UzODgzYWE0OGM2YTlkMDI1YTVjYjkzNmUyYWJiMzA5M2JmN2M0M2Q4NDQ1ODhlYTZkM2E3NzFkMjVjMWZlIn0%3D"
}

response = requests.get(url=url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

houses = soup.find_all('div', class_='item-info')

# 解析每個房屋的名稱、價格和更新時間
for house in houses:

    # 提取名稱
    title = house.find('a', class_='link').get('title')
    
    # 提取價格
    price = house.find('strong', class_='text-26px').text.strip()
    
    # 提取更新時間
    # 查找所有包含 '更新' 字樣的 span 標籤
    update_info = house.find('span', class_='line', string=lambda text: '更新' in text)
    for info in update_info:
        if '更新' in info.get_text():
            uptime = info.getText()
    
    # 網址
    link = house.find("a", class_="link v-middle").get("href")

    address_element = house.find("i", class_="ic-house house-place")
    if address_element:
        address = address_element.find_next("span").text.strip()
    else:
        address = "N/A"

    # 格局
    layout_element = house.find("span", string=lambda x: x and '房' in x)
    layout = layout_element.text.strip() if layout_element else "N/A"

    # 距離
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
        # Extract the number of hours
        hours = int(''.join(filter(str.isdigit, update_time_text)))
        if hours < 4:  # Only include if updated within 3 hours
            print(
                '名稱: ' + title + ", " + 
                '網址:' + link + ", " + 
                '價格: ' + price + ", " + 
                '格局:' + layout + ", " + 
                '更新:' + uptime + ", " + 
                '距離:' + distance
            )
            print("--------------")
    