import os
import json
from flask import Flask, request, render_template, jsonify
from bot.integrations.openai_chat import ask_question
from bot.integrations.openai_magic import magic_ai
from bot.forms import ChatForm
from bot.config import *
from bot.database import SessionLocal
from bot.models import User, Log, MessageLog, BotStatistics
from discord.ext import commands
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY  # Add this line to set the secret key

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    form = ChatForm()
    response = ""
    if form.validate_on_submit():
        question = form.question.data
        if form.submit.data:
            response = handle_chat_question(question)
        elif form.magic.data:
            response = handle_magic_question(question)
    return render_template('chat.html', form=form, response=response)

def handle_chat_question(question):
    print(f"WEBUI: Received question:", question)
    try:
        answer = ask_question(question)
        print(f"WEBUI: Answer:", answer)
        return answer
    except Exception as e:
        return str(e)
    
def handle_magic_question(question):
    print(f"WEBUI: Received question:", question)
    try:
        answer = magic_ai(question)
        print(f"WEBUI: Answer:", answer)
        return answer
    except Exception as e:
        return str(e)

@app.route('/config')
def config():
    config_values = {key: value for key, value in globals().items() if key.isupper()}
    return render_template('config.html', config=config_values)

@app.route('/db_stats')
def db_stats():
    session = SessionLocal()
    user_count = session.query(User).count()
    log_count = session.query(Log).count()
    message_log_count = session.query(MessageLog).count()
    bot_statistics = session.query(BotStatistics).first()
    session.close()

    if bot_statistics:
        start_time = bot_statistics.start_time
        formatted_start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        online_time = current_time - start_time
    else:
        formatted_start_time = "N/A"
        online_time = "N/A"

    stats = {
        "User Count": user_count,
        "Log Count": log_count,
        "Message Log Count": message_log_count,
        "Bot Start Time": formatted_start_time,
        "Bot Online Time": str(online_time).split('.')[0],  # Exclude microseconds
        "Last Registered Version": bot_statistics.last_registered_version if bot_statistics else "N/A"
    }
    return render_template('db_stats.html', stats=stats)

@app.route('/discord')
def discord():
    session = SessionLocal()
    bot_statistics = session.query(BotStatistics).order_by(BotStatistics.id.desc()).first()
    session.close()

    if bot_statistics:
        servers_info = json.loads(bot_statistics.servers_info)
        channels_info = json.loads(bot_statistics.channels_info)

        # Combine servers and channels information
        servers = []
        for server in servers_info:
            server_channels = [channel for channel in channels_info if channel['guild_id'] == server['id']]
            servers.append({
                'name': server['name'],
                'channels': server_channels
            })
    else:
        servers = []

    return render_template('discord.html', servers=servers)

if __name__ == '__main__':
    FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 6666))
    app.run(host=FLASK_HOST, port=FLASK_PORT)
