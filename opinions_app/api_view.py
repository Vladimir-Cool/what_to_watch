from flask import jsonify, request

from . import app, db
from .models import Opinion
from .views import random_opinion


@app.route('/api/opinions', methods=['GET'])
def get_opinions():
    opinions = Opinion.query.all()
    opinions_list = [opinion.to_dict() for opinion in opinions]
    return jsonify({'opinions': opinions_list})


@app.route('/api/opinions', methods=['POST'])
def add_opinions():
    data = request.get_json(silent=True)
    if data or 'title' not in data or 'text' not in data:
        return
    opinion = Opinion()
    opinion.from_dict(data)
    db.session.add(opinion)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201


@app.route('/api/opinions/<int:id>', methods=['GET'])
def get_opinion(id):
    """"""
    opinion = Opinion.query.get_or_404(id)
    return jsonify({'opinion': opinion.to_dict()})


@app.route('/api/opinions/<int:id>', methods=['PATCH'])
def update_opinion(id):
    data = request.get_json()
    opinion = Opinion.query.get_or_404(id)
    opinion.title = data.get('title', opinion.title)
    opinion.text = data.get('text', opinion.text)
    opinion.source = data.get('source', opinion.source)
    opinion.added_by = data.get('added_by', opinion.added_by)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()})


@app.route('/api/opinions/<int:id>', methods=['DELETE'])
def delete_opinions(id):
    opinion = Opinion.query.get_or_404(id)
    db.session.delete(opinion)
    db.session.commit()
    return '', 204


@app.route('/api/get-random-opinion/', methods=['GET'])
def ger_random_opinion():
    opinion = random_opinion()
    return jsonify({'opinion': opinion.to_dict()})