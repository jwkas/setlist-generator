import pytest

from backend.app import create_app
from backend.models import db, Song

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client

def test_generate_setlist_hits_exceed_duration(client):
    # Add two hit songs whose total duration exceeds the request
    with client.application.app_context():
        db.session.add_all([
            Song(title='Hit 1', artist='A', duration=400, is_hit=True),
            Song(title='Hit 2', artist='B', duration=400, is_hit=True)
        ])
        db.session.commit()

    resp = client.post('/api/generate-setlist', json={'target_duration': 500})
    assert resp.status_code == 400
    data = resp.get_json()
    assert 'Hit songs exceed' in data.get('error', '')
