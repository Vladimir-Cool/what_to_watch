from flask import jsonify, request

from . import app, db
from .models import Opinion
from .views import random_opinion
from .error_handlers import InvalidAPIUsage


def get_opinion_or_raise(id):
    opinion = Opinion.query.get(id)
    if opinion is None:
        raise InvalidAPIUsage(
            f'Мнение с указанным "id={id}" не найдено',
            404
        )
    return opinion


@app.route('/api/opinions', methods=['GET'])
def get_opinions():
    opinions = Opinion.query.all()
    opinions_list = [opinion.to_dict() for opinion in opinions]
    return jsonify({'opinions': opinions_list})


@app.route('/api/opinions', methods=['POST'])
def add_opinions():
    data = request.get_json(silent=True)
    if not data or 'title' not in data or 'text' not in data:
        raise InvalidAPIUsage('В запросе отсутствует обязательные поля')

    if Opinion.query.filter_by(text=data['text']).first():
        raise InvalidAPIUsage('Такое мнение уже есть в базе данных.')

    opinion = Opinion()
    opinion.from_dict(data)
    db.session.add(opinion)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201


@app.route('/api/opinions/<int:id>', methods=['GET'])
def get_opinion(id):
    """"""
    opinion = get_opinion_or_raise()
    return jsonify({'opinion': opinion.to_dict()})


@app.route('/api/opinions/<int:id>', methods=['PATCH'])
def update_opinion(id):
    data = request.get_json()
    if (
            'text' not in data
            and Opinion.query.filter_by(text=data['text'])
    ):
        return jsonify(
            {
                'error': 'Такое мнение уже есть в базе данных.'
            }
        )
    opinion = get_opinion_or_raise()
    opinion.title = data.get('title', opinion.title)
    opinion.text = data.get('text', opinion.text)
    opinion.source = data.get('source', opinion.source)
    opinion.added_by = data.get('added_by', opinion.added_by)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()})


@app.route('/api/opinions/<int:id>', methods=['DELETE'])
def delete_opinions(id):
    opinion = get_opinion_or_raise()
    db.session.delete(opinion)
    db.session.commit()
    return '', 204


@app.route('/api/get-random-opinion/', methods=['GET'])
def ger_random_opinion():
    opinion = random_opinion()
    if opinion is None:
        raise InvalidAPIUsage(
            f'В базе данных нет мнений.',
            404
        )
    return jsonify({'opinion': opinion.to_dict()})