from tables import SessionLocal,Student,Assignment,init_db
from flask import Flask,request,jsonify
app=Flask(__name__)
init_db()
@app.route("/",methods=['GET'])
def get_student():
    with SessionLocal() as s:
        rows=s.query(Student).all()
        data = [r.to_dict() for r in rows]
        return jsonify(data), 200
    

@app.route("/assign",methods=['GET'])
def get_assign():
    with SessionLocal() as s:
        rows=s.query(Assignment).all()
        data = [r.to_dict() for r in rows]
        return jsonify(data), 200
    


@app.route("/student/<int:id>",methods=['GET'])
def get_student_by_id(id):
    with SessionLocal() as s:
        stu= s.query(Student).filter(Student.id == id).first()
        if stu:
            return jsonify(stu.to_dict()), 200
        return jsonify({'message': 'Student not found'}), 404
    

@app.route("/assign/<int:id>",methods=['GET'])
def get_assign_by_id(id):
    with SessionLocal() as s:
        a = s.query(Assignment).filter(Assignment.id == id).first()
        if a:
            return jsonify(a.to_dict()), 200
        return jsonify({'message': 'Assignment not found'}), 404
    


@app.route("/student/post",methods=['POST'])
def post_student():
    d=request.get_json(silent=True) or {}
    x=d.get('id')
    y=d.get('name')
    z=d.get('status')
    if x is None or y is None or z is None:
        return jsonify({'message ': 'something is missing bro ,please checked it once in post methhod in student'})
    with SessionLocal() as s:
        eid = s.query(Student.id).all()
        eids = [row[0] for row in eid]
        if x not in eids:
            student=Student(id=x,name=y,status=z)
            s.add(student)
            s.commit()
            return jsonify(student.to_dict()), 201
    return jsonify({'message': 'Student ID already exists'}), 400


@app.route("/assign/post",methods=['POST'])
def post_assign():
    d=request.get_json(silent=True) or {}
    x=d.get('id')
    y=d.get('topic')
    z=d.get('status')
    w=d.get('student_id')
    if x is None or y is None or z is None or w is None:
        return jsonify({'message ': 'something is missing bro ,please checked it once in post methhod in assignment'})
    with SessionLocal() as s:
        eid = s.query(Assignment.id).all()
        eids = [row[0] for row in eid]
        sid=s.query(Student).filter(Student.id == w).first()
        if x not in eids and sid is not None:
            assignment=Assignment(id=x,topic=y,status=z,student_id=w)
            s.add(assignment)
            s.commit()
            return jsonify(assignment.to_dict()), 201
    return jsonify({'message': 'Assignment ID already exists'}), 400



@app.route("/student/delete/<int:id>",methods=['DELETE'])
def delete_student(id):
    with SessionLocal() as s:
        student = s.query(Student).filter(Student.id == id).first()
        if student:
            s.delete(student)
            s.commit()
            return jsonify({'message': 'Student deleted successfully'}), 200
        return jsonify({'message': 'Student not found'}), 404
    


@app.route("/assign/delete/<int:id>",methods=['DELETE'])
def delete_assign(id):
    with SessionLocal() as s:
        assignment = s.query(Assignment).filter(Assignment.id == id).first()
        if assignment:
            s.delete(assignment)
            s.commit()
            return jsonify({'message': 'Assignment deleted successfully'}), 200
        return jsonify({'message': 'Assignment not found'}), 404
    


@app.route("/student/update/<int:id>",methods=['PUT'])
def update_student(id):
    d=request.get_json(silent=True) or {}
    y=d.get('name')
    z=d.get('status')
    if y is None or z is None:
        return jsonify({'message ': 'something is missing bro ,please checked it once in put methhod in student'})
    with SessionLocal() as s:
        student = s.query(Student).filter(Student.id == id).first()
        if student:
            student.name = y
            student.status = z
            s.commit()
            return jsonify(student.to_dict()), 200
        return jsonify({'message': 'Student not found'}), 404




@app.route("/assign/update/<int:id>",methods=['PUT'])
def update_assign(id):
    d=request.get_json(silent=True) or {}
    y=d.get('topic')
    z=d.get('status')
    w=d.get('student_id')
    if y is None or z is None or w is None:
        return jsonify({'message ': 'something is missing bro ,please checked it once in put methhod in assignment'})
    with SessionLocal() as s:
        assignment = s.query(Assignment).filter(Assignment.id == id).first()
        sid=s.query(Student).filter(Student.id == w).first()
        if assignment and sid is not None:
            assignment.topic = y
            assignment.status = z
            assignment.student_id = w
            s.commit()
            return jsonify(assignment.to_dict()), 200
        return jsonify({'message': 'Assignment not found or Student ID invalid'}), 404




if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True, port=8000)








