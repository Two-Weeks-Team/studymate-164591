from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from datetime import date
import uuid

from models import StudyPlan, RevisionCard, get_db
from ai_service import generate_study_plan, generate_revision_cards

router = APIRouter()

# ---------------------------------------------------------------------------
# Pydantic request / response schemas – keep them simple and explicit
# ---------------------------------------------------------------------------
class StudyPlanRequest(BaseModel):
    user_id: str = Field(..., description="Identifier of the requesting user")
    syllabus: str = Field(..., description="Full syllabus or exam topics text")
    start_date: date = Field(..., description="Desired start date for the 7‑day plan")

class TopicModel(BaseModel):
    topic_id: str
    name: str
    study_days: list[date]
    completion_status: bool = False

class StudyPlanResponse(BaseModel):
    plan_id: str
    user_id: str
    topics: list[TopicModel]
    start_date: date
    end_date: date

class RevisionCardsRequest(BaseModel):
    user_id: str = Field(..., description="Identifier of the requesting user")
    material: str = Field(..., description="Raw study material to turn into flashcards")

class RevisionCardResponse(BaseModel):
    card_id: str
    user_id: str
    front: str
    back: str
    last_reviewed: date | None = None

# ---------------------------------------------------------------------------
# AI‑powered endpoints
# ---------------------------------------------------------------------------
@router.post("/study-plans", response_model=StudyPlanResponse)
async def create_study_plan(
    payload: StudyPlanRequest,
    db: Depends = Depends(get_db),
):
    # Call AI service
    ai_result = await generate_study_plan(
        syllabus=payload.syllabus,
        start_date=payload.start_date.isoformat(),
    )
    if "note" in ai_result:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=ai_result["note"],
        )

    plan_id = str(uuid.uuid4())
    # Expected AI payload shape – ensure required fields exist
    topics = ai_result.get("topics", [])
    end_date_str = ai_result.get("end_date")
    end_date = date.fromisoformat(end_date_str) if end_date_str else payload.start_date

    # Persist plan (store the whole payload for future reference)
    db_plan = StudyPlan(
        id=plan_id,
        user_id=payload.user_id,
        start_date=payload.start_date,
        end_date=end_date,
        plan_data=ai_result,
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)

    # Build response matching StudyPlanResponse schema
    response_topics = []
    for t in topics:
        response_topics.append(
            TopicModel(
                topic_id=t.get("topic_id", str(uuid.uuid4())),
                name=t.get("name", ""),
                study_days=[date.fromisoformat(d) for d in t.get("study_days", [])],
                completion_status=t.get("completion_status", False),
            )
        )

    return StudyPlanResponse(
        plan_id=plan_id,
        user_id=payload.user_id,
        topics=response_topics,
        start_date=payload.start_date,
        end_date=end_date,
    )

@router.post("/revision-cards", response_model=list[RevisionCardResponse])
async def create_revision_cards(
    payload: RevisionCardsRequest,
    db: Depends = Depends(get_db),
):
    ai_result = await generate_revision_cards(material=payload.material)
    if "note" in ai_result:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=ai_result["note"],
        )
    cards = []
    for item in ai_result:
        card_id = str(uuid.uuid4())
        front = item.get("front", "")
        back = item.get("back", "")
        rc = RevisionCard(
            id=card_id,
            user_id=payload.user_id,
            front=front,
            back=back,
            last_reviewed=None,
        )
        db.add(rc)
        cards.append(
            RevisionCardResponse(
                card_id=card_id,
                user_id=payload.user_id,
                front=front,
                back=back,
                last_reviewed=None,
            )
        )
    db.commit()
    return cards

# ---------------------------------------------------------------------------
# Simple read‑only endpoints (optional but useful for demo)
# ---------------------------------------------------------------------------
@router.get("/study-plans/{plan_id}", response_model=StudyPlanResponse)
def get_study_plan(plan_id: str, db: Depends = Depends(get_db)):
    plan = db.query(StudyPlan).filter(StudyPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Study plan not found")
    topics = plan.plan_data.get("topics", [])
    response_topics = []
    for t in topics:
        response_topics.append(
            TopicModel(
                topic_id=t.get("topic_id", ""),
                name=t.get("name", ""),
                study_days=[date.fromisoformat(d) for d in t.get("study_days", [])],
                completion_status=t.get("completion_status", False),
            )
        )
    return StudyPlanResponse(
        plan_id=plan.id,
        user_id=plan.user_id,
        topics=response_topics,
        start_date=plan.start_date,
        end_date=plan.end_date,
    )

@router.get("/revision-cards", response_model=list[RevisionCardResponse])
def list_revision_cards(user_id: str, db: Depends = Depends(get_db)):
    cards = db.query(RevisionCard).filter(RevisionCard.user_id == user_id).all()
    return [
        RevisionCardResponse(
            card_id=c.id,
            user_id=c.user_id,
            front=c.front,
            back=c.back,
            last_reviewed=c.last_reviewed,
        )
        for c in cards
    ]
