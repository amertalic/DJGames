import random
from typing import List

from fastapi import Form, Depends, HTTPException
from sqlalchemy.orm import Session

from starlette.requests import Request
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import Score, get_db
from fastapi import APIRouter

from games.utils.math_questions import generate_math_questions

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/games/math", response_class=HTMLResponse)
async def math_game(request: Request):
    player_name = request.cookies.get("player_name", request.state.t("friend"))

    # Generate 5 random math questions (addition and subtraction for kids)
    # questions = generate_math_questions(level=4, op_types=["add", "subtract", "multiply", "divide"] )
    questions = generate_math_questions(level=1, op_types=["add", "subtract"])

    return templates.TemplateResponse(
        "math_game.html",
        {
            "request": request,
            "player_name": player_name,
            "questions": questions,
            "t": request.state.t,
            "current_language": request.state.current_language,
        },
    )


@router.post("/games/math/submit")
async def submit_math_game(
    request: Request,
    answers: List[int] = Form(...),
    correct_answers: List[int] = Form(...),
    db: Session = Depends(get_db),
):
    player_id = request.cookies.get("player_id")
    if not player_id:
        raise HTTPException(status_code=400, detail="Player not found")

    # Calculate score
    correct_count = sum(
        1
        for user_ans, correct_ans in zip(answers, correct_answers)
        if user_ans == correct_ans
    )
    score_value = correct_count * 20  # 20 points per correct answer

    # Save score
    new_score = Score(player_id=player_id, game="math", score=score_value)
    db.add(new_score)
    db.commit()

    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "score": score_value,
            "correct": correct_count,
            "total": len(answers),
            "t": request.state.t,
            "current_language": request.state.current_language,
        },
    )
