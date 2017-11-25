from . import db


class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10))
    description = db.Column(db.String(64))
    done = db.Column(db.Boolean, default=False)

    @staticmethod
    def init():
        default_tasks = [
            {
                'id': 1,
                'title': 'Buy groceries',
                'description': 'Milk, Cheese, Pizza',
                'done': False
            },
            {
                'id': 2,
                'title': 'learn Python',
                'description': 'Need to find a good Python tutorial on the web',
                'done': False
            }
        ]
        for default_task in default_tasks:
            task = Tasks(id = default_task['id'],
                         title=default_task['title'],
                         description=default_task['description'],
                         done=default_task['done'])
            db.session.add(task)
        db.session.commit()

    def get_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'done': self.done
        }

    def __repr__(self):
        return '<Task {}>'.format(self.id)
