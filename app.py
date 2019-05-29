import re
from flask import (Flask, g, flash, render_template,
                   redirect, url_for, abort)
import forms
from database import models

app = Flask(__name__)
app.secret_key = 'aoauaoisiuoai=aoisoiaoa-oauaiao!'

HOST = '127.0.0.1'
PORT = 8000
DEBUG = True

def handler_resources(text):
    links = re.compile(r"""
        ^(?P<link>[\w\s]+)[,]?
        \s?(?P<path>.+)?
    """, re.X | re.M)
    resources = []
    for match in links.finditer(text):
        path = match.group('path')
        if path and not "http" in match.group('path'):
            path = "http://" + match.group('path')
        link = (match.group('link'), path)
        resources.append(link)
    return resources


@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/entries/<int:journal_id>/delete')
def delete(journal_id):
    try:
        journal = models.Journal.get_by_id(journal_id)
    except models.DoesNotExist:
        abort(404)
    else:
        journal.delete_instance()
        flash("Your journal was deleted", "Delete")
    return redirect(url_for('index'))


@app.route('/entries/<int:journal_id>/edit', methods=('GET', 'POST'))
def edit(journal_id):
    try:
        journal = models.Journal.get_by_id(journal_id)
    except models.DoesNotExist:
        abort(404)
    else:
        form = forms.JournalForm()
        if form.validate_on_submit():
            journal.date = form.date.data
            journal.title = form.title.data
            journal.learned = form.learned.data
            journal.resources = form.resources.data
            journal.time_spent = form.time_spent.data
            journal.save()

            return redirect(url_for('index'))
    dic_journal = {
        'id': journal.id,
        'date': journal.date.strftime('%Y-%m-%d'),
        'title': journal.title,
        'learned': journal.learned,
        'resources': journal.resources,
        'time_spent': journal.time_spent
    }
    return render_template('edit.html', form=form, journal=dic_journal)


@app.route('/entries/<int:journal_id>')
def detail(journal_id):
    try:
        journal = models.Journal.get_by_id(journal_id)
        resources = handler_resources(journal.resources)
    except models.DoesNotExist:
        abort(404)
    return render_template('detail.html', journal=journal, resources=resources)


@app.route('/entries/new', methods=('GET', 'POST'))
def entrie_new():
    form = forms.JournalForm()
    if form.validate_on_submit():
        models.Journal.create_journal(
            date=form.date.data,
            title=form.title.data,
            learned=form.learned.data,
            resources=form.resources.data,
            time_spent=form.time_spent.data
        )
        flash("You added a new journal!!", "success")
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


@app.route('/')
@app.route('/entries')
def index():
    journals = models.Journal.select()
    return render_template('index.html', journals=journals)


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT, host=HOST)
