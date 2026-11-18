from typing import List, Optional
from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)

class LoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    token: str
    name: str

class CreateSessionRequest(BaseModel):
    targetRole: str = Field(..., min_length=2, max_length=100)
    techStack: str = Field(..., min_length=2)
    resumeSummary: Optional[str] = Field(default=None, max_length=12000)
    numberOfQuestions: int = Field(default=5, ge=3, le=15)

class SubmitAnswerRequest(BaseModel):
    answerText: str = Field(..., min_length=5, max_length=10000)

class RubricScore(BaseModel):
    correctness: int = Field(ge=0, le=10)
    depth: int = Field(ge=0, le=10)
    communication: int = Field(ge=0, le=10)
    relevance: int = Field(ge=0, le=10)

class QuestionResponse(BaseModel):
    id: int
    questionText: str
    category: Optional[str] = None
    difficulty: str = "Medium"
    skill: Optional[str] = None
    orderIndex: int

class FeedbackResponse(BaseModel):
    questionId: int
    answerId: Optional[int] = None
    score: int = Field(ge=0, le=10)
    feedback: str
    idealAnswerPoints: str
    rubric: RubricScore
    missingConcepts: List[str] = []
    nextQuestion: Optional[QuestionResponse] = None

class SkillGap(BaseModel):
    skill: str
    averageScore: float
    attempts: int
    priority: str
    recommendation: str

class SessionSummaryResponse(BaseModel):
    sessionId: int
    targetRole: str
    averageScore: float
    questionsAnswered: int
    totalQuestions: int
    feedbackList: List[FeedbackResponse]
    skillGaps: List[SkillGap]
    practicePlan: List[str]

class HumanReviewRequest(BaseModel):
    answerId: int
    humanScore: int = Field(ge=0, le=10)
    humanNotes: str = Field(default="", max_length=2000)

class EvaluationDashboard(BaseModel):
    reviewedAnswers: int
    meanAbsoluteError: Optional[float] = None
    averageAiScore: Optional[float] = None
    averageHumanScore: Optional[float] = None
    agreementRate: Optional[float] = None
