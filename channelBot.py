import requests
import time
import threading

channels = [1258185894154866794,1112108028590825613,1175974812158537789,1109315576322609203,1149112378542264362]


headers = {
    'Authorization': "MTI1ODE4NTUyNDA3ODcxMDk2MA.GcA5sk.SnWnqjvMvBJ8mALYEkcpPc__ojkkCkelaHvSU"
}

with open('buyTemp.txt', 'r') as file:
    message_content = file.read().strip()
    
data = {'content': message_content}

def repeat_function():
    while True:
            current_time = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime())
            for channel in channels:
                url = f'https://discord.com/api/v9/channels/{channel}/messages'
                response = requests.post(url, headers=headers, data=data)
                print(response.text)
                print(f"Time: {current_time}, Channel: {channel}, Status Code: {response.status_code}\n")
            time.sleep(60)  # Wait for 60 seconds before sending the next message


repeat_function()





