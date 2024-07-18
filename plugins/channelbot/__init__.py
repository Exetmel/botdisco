import subprocess
from pelican import signals

def run_channelbot_script(pelican):
    # Run the channelBot.py script
    subprocess.run(["python", "channelBot.py"], check=True)

def register():
    signals.finalized.connect(run_channelbot_script)