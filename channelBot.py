from flask import Flask, render_template, request, redirect, url_for
import discord
import requests
import time
import threading
from dotenv import load_dotenv, set_key
import tkinter as tk
import os


load_dotenv()

app = Flask (__name__)

intents = discord.Intents.default()
client = discord.Client(intents=intents)

with open ('channel.txt', 'r') as file:
    # channels = [line.strip() for line in file if line.strip()]
    channels = [item.strip().replace('>', '') for item in file.read().split(',') if item.strip()]
    

auth_token = os.getenv("DISCORD_AUTH_TOKEN")

headers = {
    'Authorization': f"{auth_token}"
}

with open('buyTemp.txt', 'r') as file:
    message_content = file.read().strip()
    
data = {'content': message_content}
@app.route("/")
def home():
    token = os.getenv("DISCORD_AUTH_TOKEN", "")
    try:
        with open ('channel.txt', 'r') as file:
            channel_text = file.read()
    except FileNotFoundError:
        channel_text = ""
    return render_template('index.html', token=token, channel_text = channel_text)

@app.route("/update_token", methods=['POST'])
def update_token():
    new_token = request.form['token']
    os.environ["DISCORD_AUTH_TOKEN"] = new_token
    
    set_key('.env','DISCORD_AUTH_TOKEN', new_token)
    global headers
    headers = {
        'Authorization': f"{new_token}"
    }
    print(f"Updated DISCORD_AUTH_TOKEN: {new_token}")
    return redirect(url_for('home'))

@app.route("/update_channel", methods=['POST'])
def update_channel():
    channel_text = request.form['channel_text']
    cleaned_channel_text = channel_text.replace('>', '')
    with open('channel.txt', 'w') as file:
        file.write(cleaned_channel_text)
    print(f"Updated channel text: {cleaned_channel_text}")
    return redirect(url_for('home'))

def fetch_channel_name(channel_id):
    channel = fetch_channel_name(channel_id)
    return channel if channel else "unknown channel"



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
                last_messages[channel_id] = message_content
        time.sleep(60)  # Wait for 60 seconds before sending the next message

# root = tk.Tk()
# update_button = tk.Button(root, text="Update Channel", command=update_channel)
# update_button.pack()

# root.mainloop()

if __name__ == '__main__':
    # Start the repeat_function in a separate thread
    if not any(thread.name == 'repeat_function_thread' for thread in threading.enumerate()):
        thread = threading.Thread(target=repeat_function, daemon=True)
        thread.start()
        print("Started repeat_function in a separate thread.")
    app.run(debug=True, host='0.0.0.0', port=5000)

