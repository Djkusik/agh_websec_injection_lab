import jinja2, jinja2.sandbox
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, \
                  abort, jsonify
from app import gryphon_bot, EASY_TASK_PATH, MEDIUM_TASK_PATH, app


mod = Blueprint('core', __name__)

@mod.route('/', methods=['GET'])
def index():
    return (render_template('core/index.html'))


@mod.route('/gryphon', methods=['POST'])
def gryphon():
    answer = request.form.get('answer')
    return str(gryphon_bot.get_response(answer))


@mod.route(EASY_TASK_PATH, methods=['GET'])
def task():
    name = request.args.get('name')
    if name is not None:
        try:
            template = app.jinja_env.from_string(name).render()
        except jinja2.TemplateSyntaxError as e:
            app.logger.error('Error: ' + str(e))
            return (render_template('core/task.html'))
        return (render_template('core/task.html', name=template))
    else:
        return (render_template('core/task.html'))


@mod.route(MEDIUM_TASK_PATH, methods=['GET'])
def sandboxed_task():
    attack = request.args.get('attack')
    if attack is not None:
        try:
            app.logger.info(attack)
            sandboxed_env = jinja2.sandbox.SandboxedEnvironment()
            template = sandboxed_env.from_string(attack).render()
            app.logger.info(template)
        except (jinja2.TemplateSyntaxError, jinja2.sandbox.SecurityError) as e:
            app.logger.error('Sandbox error: ' + str(e))
            return (render_template('core/task2.html'))
        return render_template('core/task2.html', attack=template)
    else:
        return (render_template('core/task2.html'))