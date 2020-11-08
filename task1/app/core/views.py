import jinja2
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
        try:
            template = app.jinja_env.from_string(name).render()
        except jinja2.TemplateSyntaxError as e:
            log.error('Error: ' + str(e))
            return (render_template('core/task.html'))
        return (render_template('core/task.html', name=template))
    else:
        return (render_template('core/task.html'))