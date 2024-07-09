from flask import Flask
import discord
import requests
import time
import threading
from dotenv import load_dotenv

import os


load_dotenv()

app = Flask (__name__)

intents = discord.Intents.default()
client = discord.Client(intents=intents)

with open ('channel.txt', 'r') as file:
    channels = [line.strip() for line in file if line.strip()]
    

auth_token = os.getenv("DISCORD_AUTH_TOKEN")

headers = {
    'Authorization': f"{auth_token}"
    # 'Authorization': "MTI1ODE4NTUyNDA3ODcxMDk2MA.GcA5sk.SnWnqjvMvBJ8mALYEkcpPc__ojkkCkelaHvSnU"
}

with open('buyTemp.txt', 'r') as file:
    message_content = file.read().strip()
    
data = {'content': message_content}
@app.route("/")
def home():
    return "Ads is Running!"
async def fetch_channel_name(channel_id):
    channel = await client.fetch_channel(channel_id)
    return channel.name
def repeat_function():
    while True:
        current_time = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime())
        for channel_id in channels:
            url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
            response = requests.post(url, headers=headers, data=data)
            print(response.text)
            print(f"Time: {current_time}, Channel: {channel_id}, Status Code: {response.status_code}\n")
        time.sleep(60)  # Wait for 60 seconds before sending the next message

if __name__ == '__main__':
    # Start the repeat_function in a separate thread
    threading.Thread(target=repeat_function, daemon=True).start()
    app.run(debug=True, host='0.0.0.0', port=5000)







