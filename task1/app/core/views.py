from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, \
                  abort, jsonify
from app import gryphon_bot, TASK_PATH, app


mod = Blueprint('core', __name__)

@mod.route('/', methods=['GET'])
def index():
    return (render_template('core/index.html'))


@mod.route('/gryphon', methods=['POST'])
def gryphon():
    answer = request.form.get('answer')
    return str(gryphon_bot.get_response(answer))


@mod.route(TASK_PATH, methods=['GET'])
def task():
    name = request.args.get('name')
    if name is not None:
        template = app.jinja_env.from_string(name).render()
        return (render_template('core/task.html', name=template))
    else:
        return (render_template('core/task.html'))