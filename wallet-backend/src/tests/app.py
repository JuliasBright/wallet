import json
import pytest
from app import app, db, User, Transactions

# Define test configurations
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://juliusbright:juliusbright@localhost/wallet'

@pytest.fixture
def client():
    client = app.test_client()
    with app.app_context():
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()

def test_list_endpoints(client):
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)
    assert 'routes' in data

def test_create_account(client):
    data = {
        'username': 'testuser',
        'password': 'testpassword',
        'initial_balance': 100.0
    }
    response = client.post('/create_account', json=data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Account created successfully'

def test_login(client):
    # Create a test user
    user = User(username='testuser', password='testpassword', balance=100.0)
    db.session.add(user)
    db.session.commit()

    data = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    response = client.post('/login', json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data


if __name__ == '__main__':
    pytest.main()
