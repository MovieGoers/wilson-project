from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
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
    conversation = []

    conversation.append({'role': 'system', 'content': 'say cheese!'}) #Say Cheese GPT~~
    conversation = ChatGPT_conversation(conversation)

    GPT_answer = conversation[-1]['content'].strip()

    return render_template('mainpage/mainpage.html', GPT_answer = GPT_answer)