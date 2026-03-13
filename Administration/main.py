from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, get_db

app = FastAPI(title="Admin System Backend")

# Database tables create karna
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Admin System is live!"}

# Naya Admin User banane ke liye
@app.post("/admin/create")
def create_user(username: str, email: str, db: Session = Depends(get_db)):
    user = models.AdminUser(username=username, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Admin Created", "user": user}

# Sab admins ki list dekhne ke liye
@app.get("/admin/list")
def list_admins(db: Session = Depends(get_db)):
    return db.query(models.AdminUser).all()