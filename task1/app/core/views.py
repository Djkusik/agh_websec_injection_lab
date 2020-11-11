import jinja2, jinja2.sandbox
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, \
                  abort, jsonify, make_response
from app import gryphon_bot, app, EASY_TASK_PATH, MEDIUM_TASK_PATH, EASY_COOKIE, MEDIUM_COOKIE


mod = Blueprint('core', __name__)

@mod.route('/', methods=['GET'])
def index():
    is_easy_known = False
    is_medium_known = False
    if EASY_COOKIE in request.cookies:
        easy_cookie= request.cookies.get(EASY_COOKIE)
        is_easy_known = True
    if MEDIUM_COOKIE in request.cookies:
        medium_cookie= request.cookies.get(MEDIUM_COOKIE)
        is_medium_known = True
    return (render_template(
        'core/index.html', 
        is_easy_known=is_easy_known, 
        is_medium_known=is_medium_known,
        EASY_TASK_PATH=EASY_TASK_PATH,
        MEDIUM_TASK_PATH=MEDIUM_TASK_PATH
        ))


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
        if 'ULTRA_SECURITY_VARIABLE' in template:
            return(render_template('core/sneaky_bastard.html'))
        if 'REVERSEDENYLIST' in template:
            return(render_template('core/task.html', uno=template))
        return (render_template('core/task.html', name=template))
    else:
        resp = make_response(render_template('core/task.html'))
        resp.set_cookie(EASY_COOKIE, 'True')
        return resp


@mod.route(MEDIUM_TASK_PATH, methods=['GET'])
def sandboxed_task():
    attack = request.args.get('attack')
    if attack is not None:
        try:
            sandboxed_env = jinja2.sandbox.SandboxedEnvironment()
            template = sandboxed_env.from_string(attack).render()
        except (jinja2.TemplateSyntaxError, jinja2.sandbox.SecurityError) as e:
            app.logger.error('Sandbox error: ' + str(e))
            return (render_template('core/task2.html'))
        return render_template('core/task2.html', attack=template)
    else:
        resp = make_response(render_template('core/task2.html'))
        resp.set_cookie(MEDIUM_COOKIE, 'True')
        return resp