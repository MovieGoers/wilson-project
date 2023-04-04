from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from wilson.auth import login_required
from wilson.db import get_db

from wilson import apiyup

'''
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
'''


bp = Blueprint('mainpage', __name__)

@bp.route('/')
@login_required
def mainpage():
    user_id = session.get('user_id')
    
    conversation = []

    #conversation.append({'role': 'system', 'content': 'say oh!'}) #Say Cheese GPT~~
    #conversation = ChatGPT_conversation(conversation)

    GPT_today = '"Can you please clarify that for me?" This expression is very useful when you are in a conversation or a meeting and someone says something that you dont fully understand or that seems vague. Instead of nodding along and pretending to understand, you can ask them to clarify what they mean. It shows that you are actively listening and engaged in the conversation, and it helps to prevent any miscommunications or misunderstandings.'
    #conversation[-1]['content'].strip()
    nickname = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
    
    return render_template('mainpage/mainpage.html', GPT_today = GPT_today, nickname = nickname)

@bp.route('/talktowilson', methods=['GET', 'POST'])
@login_required
def talktowilson():
    wilson_role = ''
    user_role = ''
    background_desc = ''
    
    #사용자가 버튼을 클릭시 request.form으로 내용이 전송된다.
    if request.method == 'POST':
        #user_text = request.form['input_text']
        wilson_role = 'Shop Owner'
        user_role = 'Customer'
        background_desc = 'You are a customer, and I am blah blah blah blah blah blah blah blahblah blah blah blahblah blah blah blahblah blah blah blahblah blah blah blah'
    return render_template('mainpage/talktowilson.html', wilson_role = wilson_role, user_role = user_role, background_desc = background_desc)