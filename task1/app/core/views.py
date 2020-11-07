from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, \
                  abort, jsonify
from app import gryphon_bot


mod = Blueprint('core', __name__)

@mod.route('/', methods=['GET'])
def index():
    return (render_template('core/index.html'))


@mod.route('/gryphon', methods=['POST'])
def gryphon():
    answer = request.form.get('answer')
    return str(gryphon_bot.get_response(answer))


@mod.route('/task', methods=['GET', 'POST'])
def task():
    if request.method == 'GET':
        return (render_template('core/task.html'))
    if request.method == 'POST':
        answer = request.form.get('answer')
        return (answer)