import json
import os

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from flask import Flask, render_template


app = Flask(__name__)
app.config.from_object('app.config')
TASK_PATH = os.environ.get('TASK_PATH', '/just_task')

gryphon_bot = ChatBot(
    'Gryphon',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry Adventurer, but I do not understand this language.',
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': os.environ.get('SPECIFIC_INPUT', 'Hint or flag?'),
            'output_text': os.environ.get('SPECIFIC_OUTPUT', 'Who it knows?')
        }
    ],
    database_uri='sqlite:///app/bot/gryphon_bot.db'
)

trainer = ListTrainer(gryphon_bot)
trainer_corpus = ChatterBotCorpusTrainer(gryphon_bot)
trainer_corpus.train('chatterbot.corpus.english')

with open('app/bot/bot_training.json') as f:
    training_material = json.load(f)
for to_train in training_material:
    trainer.train(to_train)


@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404

@app.after_request
def apply_header(response):
	response.headers['X-Gryphon'] = os.environ.get('X_GRYPHON', 'It would be easier on prod')
	return response


from app.core.views import mod as core

app.register_blueprint(core)