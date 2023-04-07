from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, jsonify
)
from werkzeug.exceptions import abort

from wilson.auth import login_required
from wilson.db import get_db

from wilson import apiyup

import openai

openai.api_key = apiyup.apiyupyup()
model_id = 'gpt-3.5-turbo'

def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation


bp = Blueprint('mainpage', __name__)

@bp.route('/')
@login_required
def mainpage():
    user_id = session.get('user_id')
    
    # conversation = []

    # conversation.append({'role': 'system', 'content': 'say Cheese!'}) #Say Cheese GPT~~
    # conversation = ChatGPT_conversation(conversation)

    # GPT_today = conversation[-1]['content'].strip()
    GPT_today = "Hello~"

    nickname = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
    
    return render_template('mainpage/mainpage.html', GPT_today = GPT_today, nickname = nickname)

@bp.route('/talktowilson', methods=['GET', 'POST'])
@login_required
def talktowilson():

    return render_template('mainpage/talktowilson.html')

@bp.route('/testpage', methods=['GET', 'POST'])
def testpage():
    gpt_answer = ''
    conversation = []
    initial_input = 'I will give you an English writing.'
    initial_input += ' Please change the writing to be grammatically correct in English and better in expression.'
    initial_input += ' also, do not answer except for the changed sentence.'
    conversation.append({'role': 'system', 'content': initial_input})
    conversation = ChatGPT_conversation(conversation)

    if request.method == 'POST':
        data = request.get_json()['text']
        conversation.append({'role': 'user', 'content': data})
        conversation = ChatGPT_conversation(conversation)

        gpt_answer = conversation[-1]['content'].strip()

        return jsonify({'data': gpt_answer})

    return render_template('mainpage/testpage.html', gpt_answer = gpt_answer)