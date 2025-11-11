from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage
students = {}
next_id = 1

# GET /students - List all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(list(students.values()))

# POST /students - Add a new student
@app.route('/students', methods=['POST'])
def add_student():
    global next_id
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    student = {
        'id': next_id,
        'name': data['name'],
        'email': data.get('email', ''),
        'age': data.get('age', None)
    }
    students[next_id] = student
    next_id += 1
    
    return jsonify(student), 201

# PUT /students/<id> - Update student details
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    if id not in students:
        return jsonify({'error': 'Student not found'}), 404
    
    data = request.get_json()
    student = students[id]
    
    student['name'] = data.get('name', student['name'])
    student['email'] = data.get('email', student['email'])
    student['age'] = data.get('age', student['age'])
    
    return jsonify(student), 200

# DELETE /students/<id> - Delete a student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    if id not in students:
        return jsonify({'error': 'Student not found'}), 404
    
    deleted = students.pop(id)
    return jsonify({'message': 'Student deleted', 'student': deleted}), 200

if __name__ == '__main__':
    app.run(debug=True)