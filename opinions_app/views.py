from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import OpinionForm
from .models import Opinion


def random_opinion():
    """Возвращает случайное Мнение о фильме."""
    quantity = Opinion.query.count()
    if quantity:
        offset_value = randrange(quantity)
        return Opinion.query.offset(offset_value).first()


@app.route('/')
def index_view():
    quantity = random_opinion()
    if not quantity:
        abort(500)
    return render_template('opinion.html', opinion=opinion)


@app.route('/opinion/<int:id>')
def opinion_view(id):
    opinion = Opinion.query.get_or_404(id)
    return render_template('opinion.html', opinion=opinion)


@app.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    form = OpinionForm()

    if form.validate_on_submit():
        if Opinion.query.filter_by(text=form.text.data).first() is not None:
            flash(
                'Такое мнение уже было оставлено ранее!',
                'error-message'
            )
            return render_template(
                'add_opinion.html',
                form=form
            )
        opinion = Opinion(
            title=form.title.data,
            text=form.text.data,
            source=form.source.data,
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('add_opinion.html', form=form)

