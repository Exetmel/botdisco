from flask import Flask, render_template, request, redirect, url_for, jsonify
import discord
import requests
import time
import threading
from dotenv import load_dotenv, set_key


load_dotenv()

app = Flask (__name__)

intents = discord.Intents.default()
client = discord.Client(intents=intents)

with open ('channel.txt', 'r') as file:
    # channels = [line.strip() for line in file if line.strip()]
    channels = [item.strip().replace('>', '') for item in file.read().split(',') if item.strip()]
    

# auth_token = os.getenv("DISCORD_AUTH_TOKEN")
with open ('token.txt', 'r') as file:
    auth_token = [item.strip().replace('>', '') for item in file.read().split(',') if item.strip()]

headers = {
    'Authorization': f"{auth_token}"
}

with open('buyTemp.txt', 'r') as file:
    message_content = file.read().strip()
    
data = {'content': message_content}

logs = []

interval = 5

stop_event = threading.Event()
file_lock = threading.Lock() 



@app.route("/")
def home():
    # token = os.getenv("DISCORD_AUTH_TOKEN", "")
    token = auth_token
    try:
        with open ('token.txt', 'r') as file:
            token = file.read()
    except FileNotFoundError:
        token = ""
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
        
    try:
        with open('logs.txt', 'r') as file:
            logs = file.read()
    except FileNotFoundError:
        logs = "No logs available"
        
    return render_template('index.html', token=token, channel_text = channel_text, message_content = message_content, logs = logs, interval=interval)

# Edit Token 
@app.route("/update_all", methods=['POST'])
def update_all():
    global interval
    new_token = request.form['token'].strip()
    new_channel_text = request.form['channel_text'].strip()
    new_message_content = request.form['message_content'].strip()
    interval = int(request.form['interval'].strip())
    # os.environ["DISCORD_AUTH_TOKEN"] = new_token
    with open('token.txt', 'w') as file:
        file.write(new_token)
    # set_key('.env','DISCORD_AUTH_TOKEN', new_token)
    global headers
    headers = {
        'Authorization': f"{new_token}"
    }
    print(f"Updated TOKEN: {new_token}")
    

    cleaned_channel_text = new_channel_text.replace('>', '').replace(' ', '')
    with open('channel.txt', 'w') as file:
        file.write(cleaned_channel_text)
    print(f"Updated channel text: {cleaned_channel_text}")

    cleaned_message_content = '\n'.join(line.strip() for line in new_message_content.splitlines())
    with open('buyTemp.txt', 'w') as file:
        file.write(cleaned_message_content)
    global data
    data = {'content': new_message_content}
    print(f"Updated message content: {new_message_content}")
    
    return redirect(url_for('home'))

    


# Loop message Function 
def repeat_function():
    last_messages = {}
    while not stop_event.is_set():
        print("repeat_function loop started")
        current_time = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime())
        
         # Read channels from channel.txt within the loop
        with file_lock:
            with open('channel.txt', 'r') as file:
                channels = [item.strip().replace('>', '') for item in file.read().split(',') if item.strip()]
                
                
                
        for channel_id in channels:
                url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
                response = requests.post(url, headers=headers, data=data)
                log_entry = f"Time: {current_time}, Channel: {channel_id}, Status Code: {response.status_code}\n"
                print(log_entry)
                with open('logs.txt', 'a') as log_file:
                    log_file.write(log_entry)
                last_messages[channel_id] = message_content
        print("repeat_function sleeping for 5 sec")
        stop_event.wait(interval)  # Wait for 60 seconds before sending the next message


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
    
    with open('logs.txt', 'w') as log_file:
        log_file.write("")
    return jsonify({"status": "stopped"}), 200
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

