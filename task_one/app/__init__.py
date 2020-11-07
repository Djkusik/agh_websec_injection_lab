from flask import Flask, render_template


app = Flask(__name__)
app.config.from_object('app.config')

@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404

from app.core.views import mod as core

app.register_blueprint(core)