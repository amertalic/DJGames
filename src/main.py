# File structure:
# - main.py (main FastAPI application)
# - database.py (database setup and models)
# - i18n.py (internationalization support)
# - locales/
#   - bs.py (Bosnian translations)
#   - en.py (English translations)
# - static/ (CSS, JS, images)
# - templates/ (Jinja2 templates)

# app.py
from fastapi import Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import Player, Score, create_tables
from i18n import get_translation
from fastapi import FastAPI
from games.math import router as math_game_router
from database import get_db

# Create tables
create_tables()

app = FastAPI(title="Kids Learning Games")
app.include_router(math_game_router)

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")


# Middleware to add translation to request
@app.middleware("http")
async def add_translation_to_request(request: Request, call_next):
    # Get language from cookie or default to Bosnian
    language = request.cookies.get("language", "bs")

    # Get translation function
    request.state.t = get_translation(language)
    request.state.current_language = language

    response = await call_next(request)
    return response


# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    # Get top 5 scores
    top_scores = (
        db.query(Player, Score).join(Score).order_by(Score.score.desc()).limit(5).all()
    )
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "top_scores": top_scores,
            "t": request.state.t,
            "current_language": request.state.current_language,
        },
    )


@app.post("/register")
async def register_player(
    request: Request, player_name: str = Form(...), db: Session = Depends(get_db)
):
    # Check if player exists
    player = db.query(Player).filter(Player.name == player_name).first()
    if not player:
        player = Player(name=player_name)
        db.add(player)
        db.commit()
        db.refresh(player)

    response = RedirectResponse(url="/games", status_code=303)
    response.set_cookie(key="player_id", value=str(player.id))
    response.set_cookie(key="player_name", value=player_name)
    return response


@app.get("/games", response_class=HTMLResponse)
async def games_list(request: Request):
    player_name = request.cookies.get("player_name", request.state.t("friend"))
    return templates.TemplateResponse(
        "games.html",
        {
            "request": request,
            "player_name": player_name,
            "t": request.state.t,
            "current_language": request.state.current_language,
        },
    )


@app.get("/change-language/{language}")
async def change_language(language: str):
    supported_languages = ["bs", "en"]
    if language not in supported_languages:
        language = "bs"

    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="language", value=language)
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8005, reload=True)
