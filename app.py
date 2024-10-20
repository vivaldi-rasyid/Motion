from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__, template_folder='Template')

# Konfigurasi PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://motionval:motionval@20.33.103.134/motion'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model untuk Tabel 'todos'
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)

# Route untuk Halaman Utama
@app.route('/')
def index():
    return render_template('home.html')

# API untuk Mengambil Semua Tugas
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    todos_list = [{"id": todo.id, "task": todo.task} for todo in todos]
    return jsonify(todos_list)

# API untuk Menambah Tugas
@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    new_task = data.get('task')

    if not new_task:
        return jsonify({"error": "Task is required"}), 400

    try:
        todo = Todo(task=new_task)
        db.session.add(todo)
        db.session.commit()
        return jsonify({"id": todo.id, "task": todo.task}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# API untuk Menghapus Tugas
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)

    if not todo:
        return jsonify({"error": "Todo not found"}), 404

    try:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({"message": "Todo deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
