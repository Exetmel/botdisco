from flask import Flask, render_template
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
}

with open('buyTemp.txt', 'r') as file:
    message_content = file.read().strip()
    
data = {'content': message_content}
@app.route("/")
def home():
    return render_template('index.html')
async def fetch_channel_name(channel_id):
    channel = await client.fetch_channel(channel_id)
    return channel.name
def repeat_function():
    last_messages = {}
    while True:
        current_time = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime())
        for channel_id in channels:
            if last_messages.get(channel_id) != message_content:
                url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
                response = requests.post(url, headers=headers, data=data)
                print(response.text)
                print(f"Time: {current_time}, Channel: {channel_id}, Status Code: {response.status_code}\n")
        time.sleep(60)  # Wait for 60 seconds before sending the next message

# @client.event
# async def on_ready():
#     print(f'Logged in as {client.user}')
#     # Start the repeat_function
#     await repeat_function()

if __name__ == '__main__':
    # Start the repeat_function in a separate thread
    thread = threading.Thread(target=repeat_function, daemon=True)
    thread.start()
    print("Started repeat_function in a separate thread.")
    app.run(debug=True, host='0.0.0.0', port=5000)


