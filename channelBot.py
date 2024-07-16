from flask import Flask, render_template, request, redirect, url_for, jsonify
import discord
import requests
import time
import threading
from dotenv import load_dotenv, set_key
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

stop_event = threading.Event()
@app.route("/")
def home():
    token = os.getenv("DISCORD_AUTH_TOKEN", "")
    try:
        with open ('channel.txt', 'r') as file:
            channel_text = file.read()
    except FileNotFoundError:
        channel_text = ""
        
    try:
        with open('buyTemp.txt', 'r') as file:
            message_content = file.read()
    except FileNotFoundError:
        message_content = ""
    return render_template('index.html', token=token, channel_text = channel_text, message_content = message_content)

# Edit Token 
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

@app.route("/update_message_content", methods=['POST'])
def update_message_content():
    new_message_content = request.form['message_content']
    with open('buyTemp.txt', 'w') as file:
        file.write(new_message_content)
    global data
    data = {'content': new_message_content}
    print(f"Updated message content: {new_message_content}")
    return redirect(url_for('home' ))
# Editing Channel 
@app.route("/update_channel", methods=['POST'])
def update_channel():
    channel_text = request.form['channel_text']
    cleaned_channel_text = channel_text.replace('>', '')
    with open('channel.txt', 'w') as file:
        file.write(cleaned_channel_text)
    print(f"Updated channel text: {cleaned_channel_text}")
    return redirect(url_for('home'))


# Loop message Function 
def repeat_function():
    while not stop_event.is_set():
        print("repeat_function loop started")
        current_time = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime())
        for channel_id in channels:
                url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
                response = requests.post(url, headers=headers, data=data)
                print(response.text)
                print(f"Time: {current_time}, Channel: {channel_id}, Status Code: {response.status_code}\n")
        print("repeat_function sleeping for 5 sec")
        stop_event.wait(5)  # Wait for 60 seconds before sending the next message


# Start Button Functions 
@app.route("/start_repeat_function", methods=['POST'])
def start_repeat_function():
    global stop_event
    stop_event.clear()
    print("Received request to start repeat_function")
    if not any(thread.name == 'repeat_function_thread' for thread in threading.enumerate()):
        thread = threading.Thread(target=repeat_function, daemon=True, name='repeat_function_thread')
        thread.start()
        print("Started repeat_function in a separate thread.")
        print("Current threads:", threading.enumerate())
        return jsonify({"status": "started"}), 200
    else:
        print("repeat_function is already running.")
        return jsonify({"status": "already running"}), 200

# Stop Button Function 
@app.route("/stop_repeat_function", methods=['POST'])
def stop_repeat_function():
    global stop_event
    stop_event.set()
    print("Received request to stop repeat_function")
    return jsonify({"status": "stopped"}), 200
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

