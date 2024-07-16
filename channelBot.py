from flask import Flask, render_template, jsonify
import requests
import time
import threading
# from dotenv import load_dotenv

import os


# load_dotenv()

app = Flask (__name__)

# intents = discord.Intents.default()
# client = discord.Client(intents=intents)

with open ('channel.txt', 'r') as file:
    channels = [line.strip() for line in file if line.strip()]
    

# auth_token = os.getenv("DISCORD_AUTH_TOKEN")

with open('token.txt', 'r') as file:
    auth_token = file.read().strip()

headers = {
    'Authorization': f"{auth_token}"
}

with open('buyTemp.txt', 'r') as file:
    message_content = file.read().strip()
    
data = {'content': message_content}

logs = []

@app.route("/")
def home():
    return render_template ('index.html')

@app.route("/logs")
def get_logs():
    return jsonify(logs)
async def fetch_channel_name(channel_id):
    # channel = await client.fetch_channel(channel_id)
    channel = await fetch_channel_name(channel_id)
    return channel
def repeat_function():
    while True:
        current_time = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime())
        for channel_id in channels:
            url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
            response = requests.post(url, headers=headers, data=data)
            log_entry = {
                'time': current_time,
                'channel': channel_id,
                'status_code': response.status_code,
                'response': response.text
            }
            logs.append(log_entry)
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
    if not any(thread.name == "RepeatFunctionThread" for thread in threading.enumerate()):
        thread = threading.Thread(target=repeat_function, name="RepeatFunctionThread", daemon=True)
        thread.start()
    app.run(debug=True, host='0.0.0.0', port=5000)


