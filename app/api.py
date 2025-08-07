from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from .models import User, Expense, db
from .forecast import forecast_cashflow

api_bp = Blueprint("api", __name__)

# ============ AUTH ROUTES =========================================
@api_bp.post("/register")
def register():
    data = request.json
    if User.query.filter_by(email=data["email"]).first():
        return {"message": "email exists"}, 400
    user = User.create(data["email"], data["password"])
    login_user(user)
    return {"id": user.id, "email": user.email}

@api_bp.post("/login")
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return {"message": "invalid creds"}, 401
    login_user(user)
    return {"id": user.id, "email": user.email}

@api_bp.get("/logout")
@login_required
def logout():
    logout_user()
    return {"message": "logged out"}

# ============ EXPENSE CRUD ========================================
@api_bp.get("/expenses")
@login_required
def list_expenses():
    q = Expense.query.filter_by(user_id=current_user.id).all()
    return jsonify([e_to_dict(e) for e in q])

@api_bp.post("/expenses")
@login_required
def add_expense():
    data = request.json
    e = Expense(
        user_id=current_user.id,
        date=datetime.fromisoformat(data["date"]).date(),
        category=data["category"],
        description=data.get("description", ""),
        amount=float(data["amount"])
    )
    db.session.add(e)
    db.session.commit()
    return e_to_dict(e), 201

@api_bp.put("/expenses/<int:eid>")
@login_required
def edit_expense(eid):
    e = _expense_or_404(eid)
    data = request.json
    for field in ("date", "category", "description", "amount"):
        if field in data:
            setattr(e, field,
                    datetime.fromisoformat(data[field]).date()
                    if field == "date" else data[field])
    db.session.commit()
    return e_to_dict(e)

@api_bp.delete("/expenses/<int:eid>")
@login_required
def delete_expense(eid):
    e = _expense_or_404(eid)
    db.session.delete(e)
    db.session.commit()
    return {"deleted": eid}

def _expense_or_404(eid):
    e = Expense.query.filter_by(id=eid, user_id=current_user.id).first_or_404()
    return e

def e_to_dict(e):
    return {
        "id": e.id,
        "date": e.date.isoformat(),
        "category": e.category,
        "description": e.description,
        "amount": e.amount
    }

# ============ FORECAST ============================================
@api_bp.get("/forecast")
@login_required
def forecast():
    df = forecast_cashflow(current_user.id)
    return df.to_dict(orient="records")
