from dotenv import load_dotenv
load_dotenv()

import io
import os
from typing import List

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pypdf import PdfReader
from sqlalchemy.orm import Session as DBSession

import interview_service
import models
import schemas
from auth import create_token, current_user, hash_password, verify_password
from database import Base, engine, get_db, apply_sqlite_compatibility_migrations
from grok_service import GroqServiceError

Base.metadata.create_all(bind=engine)
apply_sqlite_compatibility_migrations()
app = FastAPI(title="Interview Prep Assistant API", version="3.0.0")
allow_origins = ["http://localhost:5173", "http://127.0.0.1:5173"] + [x.strip() for x in os.getenv("ALLOWED_ORIGINS", "").split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=allow_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.exception_handler(GroqServiceError)
async def ai_error(_, exc): return JSONResponse(status_code=502, content={"success": False, "error": str(exc)})
@app.exception_handler(LookupError)
async def lookup_error(_, exc): return JSONResponse(status_code=404, content={"success": False, "error": str(exc)})
@app.exception_handler(ValueError)
async def value_error(_, exc): return JSONResponse(status_code=400, content={"success": False, "error": str(exc)})
@app.exception_handler(Exception)
async def unexpected_error(_, exc):
    return JSONResponse(status_code=500, content={"success": False, "error": "The interview service could not process that response. Please try again."})

@app.get("/")
def home(): return {"message": "Interview Prep Assistant API", "status": "running", "version": "3.0.0"}
@app.get("/health")
def health(): return {"status": "healthy"}

@app.post("/api/auth/register", response_model=schemas.AuthResponse)
def register(request: schemas.RegisterRequest, db: DBSession = Depends(get_db)):
    email = request.email.strip().lower()
    if db.query(models.User).filter_by(email=email).first(): raise ValueError("An account already exists for this email.")
    user = models.User(name=request.name.strip(), email=email, password_hash=hash_password(request.password))
    db.add(user); db.commit(); db.refresh(user)
    return schemas.AuthResponse(token=create_token(user.id), name=user.name)

@app.post("/api/auth/login", response_model=schemas.AuthResponse)
def login(request: schemas.LoginRequest, db: DBSession = Depends(get_db)):
    user = db.query(models.User).filter_by(email=request.email.strip().lower()).first()
    if not user or not verify_password(request.password, user.password_hash): raise HTTPException(status_code=401, detail="Invalid email or password.")
    return schemas.AuthResponse(token=create_token(user.id), name=user.name)

@app.post("/api/resume/extract")
async def extract_resume(file: UploadFile = File(...), user: models.User = Depends(current_user)):
    if file.content_type not in {"application/pdf", "application/x-pdf"}: raise HTTPException(status_code=400, detail="Upload a PDF resume.")
    content = await file.read()
    if len(content) > 5 * 1024 * 1024: raise HTTPException(status_code=400, detail="Resume must be 5 MB or smaller.")
    try:
        text = "\n".join((page.extract_text() or "") for page in PdfReader(io.BytesIO(content)).pages).strip()
    except Exception as exc: raise HTTPException(status_code=400, detail="The PDF could not be read.") from exc
    if not text: raise HTTPException(status_code=400, detail="No selectable text was found in this PDF.")
    return {"text": text[:12000]}

@app.post("/api/sessions")
def create_session(request: schemas.CreateSessionRequest, db: DBSession = Depends(get_db), user: models.User = Depends(current_user)):
    session = interview_service.create_session(db, request, user.id)
    return {"success": True, "sessionId": session.id}

@app.get("/api/sessions", response_model=List[dict])
def session_history(db: DBSession = Depends(get_db), user: models.User = Depends(current_user)):
    return interview_service.history(db, user.id)

@app.get("/api/sessions/{session_id}/questions", response_model=List[schemas.QuestionResponse])
def get_questions(session_id: int, db: DBSession = Depends(get_db), user: models.User = Depends(current_user)):
    return [interview_service._question_response(q) for q in interview_service.get_questions(db, session_id, user.id)]

@app.post("/api/sessions/{session_id}/questions/{question_id}/answers", response_model=schemas.FeedbackResponse)
def submit_answer(session_id: int, question_id: int, request: schemas.SubmitAnswerRequest, db: DBSession = Depends(get_db), user: models.User = Depends(current_user)):
    return interview_service.submit_answer(db, session_id, question_id, request, user.id)

@app.get("/api/sessions/{session_id}/summary", response_model=schemas.SessionSummaryResponse)
def get_summary(session_id: int, db: DBSession = Depends(get_db), user: models.User = Depends(current_user)):
    return interview_service.get_summary(db, session_id, user.id)

@app.post("/api/evaluations")
def human_review(request: schemas.HumanReviewRequest, db: DBSession = Depends(get_db), user: models.User = Depends(current_user)):
    interview_service.save_human_review(db, user.id, request)
    return {"success": True}

@app.get("/api/evaluations/dashboard", response_model=schemas.EvaluationDashboard)
def evaluation_dashboard(db: DBSession = Depends(get_db), user: models.User = Depends(current_user)):
    return interview_service.evaluation_dashboard(db, user.id)
