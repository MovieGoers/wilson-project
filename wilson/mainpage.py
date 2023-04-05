from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
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
    
    conversation = []

    conversation.append({'role': 'system', 'content': 'say Cheese!'}) #Say Cheese GPT~~
    conversation = ChatGPT_conversation(conversation)

    GPT_today = conversation[-1]['content'].strip()
    nickname = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
    
    return render_template('mainpage/mainpage.html', GPT_today = GPT_today, nickname = nickname)

@bp.route('/talktowilson', methods=['GET', 'POST'])
@login_required
def talktowilson():
    #사용자가 버튼을 클릭시 request.form으로 data가 talkingtowilson으로 전송된다.
    if request.method == 'POST':
        return redirect(url_for("talkingtowilson"))
    else:
         return render_template('mainpage/talktowilson.html')

@bp.route('/talkingtowilson', methods=['GET', 'POST'])
@login_required
def talkingtowilson():
    #talktowilson으로부터 전달받은 data 사용.
    conversation = []

    user_topic = request.form.get('input_interest')

    first_input = 'Lets do a role play that can happen in real life about '
    first_input += user_topic
    first_input += '. Your name is Wilson. what scenario are we going to play?'
    conversation.append({'role': 'system', 'content': first_input})
    conversation = ChatGPT_conversation(conversation)
    background_desc = conversation[-1]['content'].strip()

    second_input = 'what is my role? answer it in a single word.'
    conversation.append({'role': 'user', 'content': second_input})
    conversation = ChatGPT_conversation(conversation)

    user_role = conversation[-1]['content'].strip()

    final_input = 'What is Wilson role? answer it in a single word.'
    conversation.append({'role': 'user', 'content': final_input})
    conversation = ChatGPT_conversation(conversation)

    wilson_role = conversation[-1]['content'].strip()

    conversation.append({'role': 'user', 'content': 'So, You are '+wilson_role+', and I am '+user_role+'. Ok, Lets start now. Hello ' + wilson_role})
    conversation = ChatGPT_conversation(conversation)

    wilson_speaking = conversation[-1]['content'].strip()

    return render_template('mainpage/talkingtowilson.html', wilson_role = wilson_role, user_role = user_role, background_desc = background_desc, wilson_speaking = wilson_speaking)