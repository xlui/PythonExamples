from . import api
from .. import db
from flask import jsonify, abort, make_response, request, url_for
# jsonify -- 格式化响应给客户端的数据
from app.models import Tasks
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'ok':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


def make_public_task(task):
    new_task = {'uri': url_for('api.get_task', task_id=task.id, _external=True),
                'title': task.title,
                'description': task.description,
                'done': task.done}
    return new_task


@api.route('/tasks', methods=['GET'])
@auth.login_required
def index():
    tasks = Tasks.query.all()
    return jsonify({'tasks': list(map(make_public_task, tasks))})


@api.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Tasks.query.filter_by(id=task_id).first()
    if not task:
        abort(404)
    return jsonify({'task': task.get_json()})


@api.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = Tasks(title=request.json['title'],
                 description=request.json.get('description', ''),
                 done=False)
    db.session.add(task)
    db.session.commit()
    return jsonify({'task': task.get_json()})


@api.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Tasks.query.filter_by(id=task_id).first()
    if not task:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) is not str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task.title = request.json.get('title', task.title)
    task.description = request.json.get('description', task.description)
    task.done = request.json.get('done', task.done)
    db.session.commit()
    return jsonify({'task': task.get_json()})


@api.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Tasks.query.filter_by(id=task_id).first()
    if not task:
        abort(404)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'result': True})


@api.app_errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({'error': "Not Found"}), 404)
