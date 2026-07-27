import pytest
from app import app, db, User

@pytest.fixture
def client():
    # Configure app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use temporary in-memory DB for tests
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_health_check(client):
    """Test health check route"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_create_and_get_user(client):
    """Integration Test: Tests API + Database interaction"""
    # 1. POST a new user
    post_res = client.post('/users', json={"name": "Integration User"})
    assert post_res.status_code == 201
    user_id = post_res.json['user']['id']

    # 2. GET the user back from database
    get_res = client.get(f'/users/{user_id}')
    assert get_res.status_code == 200
    assert get_res.json['name'] == "Integration User"