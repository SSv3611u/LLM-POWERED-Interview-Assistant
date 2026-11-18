from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    sessions = relationship("InterviewSession", back_populates="user")


class InterviewSession(Base):
    __tablename__ = "interview_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    target_role = Column(String(150), nullable=False)
    tech_stack = Column(Text, nullable=False)
    resume_summary = Column(Text)
    number_of_questions = Column(Integer, nullable=False, default=5)
    current_difficulty = Column(String(20), nullable=False, default="Medium")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    user = relationship("User", back_populates="sessions")
    questions = relationship("Question", back_populates="session", cascade="all, delete-orphan", order_by="Question.order_index", lazy="select")


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    category = Column(String(50), default="General")
    difficulty = Column(String(20), nullable=False, default="Medium")
    skill = Column(String(100), nullable=True)
    order_index = Column(Integer, nullable=False)
    session = relationship("InterviewSession", back_populates="questions")
    answer = relationship("Answer", back_populates="question", uselist=False, cascade="all, delete-orphan", lazy="select")


class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), unique=True, nullable=False)
    answer_text = Column(Text, nullable=False)
    score = Column(Integer, default=0)
    feedback = Column(Text, default="")
    ideal_answer_points = Column(Text, default="")
    rubric_json = Column(Text, default="{}")
    missing_concepts_json = Column(Text, default="[]")
    question = relationship("Question", back_populates="answer")
    evaluation = relationship("EvaluationRecord", back_populates="answer", uselist=False, cascade="all, delete-orphan")


class EvaluationRecord(Base):
    __tablename__ = "evaluation_records"
    id = Column(Integer, primary_key=True)
    answer_id = Column(Integer, ForeignKey("answers.id"), unique=True, nullable=False)
    human_score = Column(Integer, nullable=False)
    human_notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    answer = relationship("Answer", back_populates="evaluation")
