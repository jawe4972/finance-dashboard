import json
from app import create_app, db
from app.models import User

def setup_module():
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    db.drop_all(); db.create_all()
    User.create("t@t.com", "pass")

def test_register_and_login(client):
    resp = client.post("/api/login",
        data=json.dumps({"email": "t@t.com", "password": "pass"}),
        content_type="application/json")
    assert resp.status_code == 200
