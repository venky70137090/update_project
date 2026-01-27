import pytest
from operations import app
from tables import SessionLocal, Student, Assignment, init_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_teardown():

    yield
    with SessionLocal() as s:
        s.query(Assignment).delete()
        s.query(Student).delete()
        s.commit()

def test_get_student(client):
    response = client.get('/')
    assert response.status_code == 200

def test_get_assign(client):
    response = client.get('/assign')
    assert response.status_code == 200

def test_get_student_by_id(client):
    client.post('/student/post', json={'id': 1, 'name': 'Vikram', 'status': 'active'})
    response = client.get('/student/1')
    assert response.json['name'] == 'Vikram'

def test_get_assign_by_id(client):
    client.post('/student/post', json={'id': 1, 'name': 'Venky', 'status': 'active'})
    client.post('/assign/post', json={'id': 1, 'topic': 'restapi', 'status': 'pending', 'student_id': 1})
    response = client.get('/assign/1')
    assert response.json['topic'] == 'restapi'

def test_post_student(client):
    response = client.post('/student/post', json={'id': 2, 'name': 'Viswant', 'status': 'active'})
    assert response.status_code == 201

def test_post_assign(client):
    client.post('/student/post', json={'id': 3, 'name': 'Abhi', 'status': 'active'})
    response = client.post('/assign/post', json={'id': 2, 'topic': 'flask', 'status': 'pending', 'student_id': 3})
    assert response.status_code == 201

def test_delete_student(client):
    client.post('/student/post', json={'id': 4, 'name': 'Charan', 'status': 'active'})
    response = client.delete('/student/delete/4')
    assert response.status_code == 200

def test_delete_assign(client):
    client.post('/student/post', json={'id': 5, 'name': 'Kittu', 'status': 'active'})
    client.post('/assign/post', json={'id': 3, 'topic': 'docker', 'status': 'pending', 'student_id': 5})
    response = client.delete('/assign/delete/3')
    assert response.status_code == 200

def test_update_student(client):
    client.post('/student/post', json={'id': 6, 'name': 'Pranath', 'status': 'active'})
    response = client.put('/student/update/6', json={'name': 'Pranath', 'status': 'inactive'})
    assert response.status_code == 200

def test_update_assign(client):
    client.post('/student/post', json={'id': 7, 'name': 'Vikram', 'status': 'active'})
    client.post('/assign/post', json={'id': 4, 'topic': 'sqlachemy', 'status': 'pending', 'student_id': 7})
    response = client.put('/assign/update/4', json={'topic': 'restapi', 'status': 'completed', 'student_id': 7})
    assert response.status_code == 200



def test_post_student_duplicate(client):
    client.post('/student/post', json={'id': 2, 'name': 'Viswant', 'status': 'active'})
    resp = client.post('/student/post', json={'id': 2, 'name': 'Another', 'status': 'inactive'})
    assert resp.status_code == 400
    assert resp.json['message'] == 'Student ID already exists'



def test_post_assignment_duplicate_id(client):
    
    client.post('/student/post', json={'id': 10, 'name': 'Venky', 'status': 'active'})
    resp1 = client.post('/assign/post', json={
        'id': 100, 'topic': 'docker', 'status': 'pending', 'student_id': 10
    })
    assert resp1.status_code == 201
    resp2 = client.post('/assign/post', json={
        'id': 100, 'topic': 'rest api', 'status': 'pending', 'student_id': 10
    })
    assert resp2.status_code == 400
    body = resp2.get_json()
    assert body is not None
    assert 'messag' in body
    assert body['message'] == 'Assignment ID already exists'

