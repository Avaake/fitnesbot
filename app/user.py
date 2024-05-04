from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="web/templates")
router = APIRouter(prefix="/users", tags=["User"])


@router.get("/calcbzy")
async def root(request: Request):
    """
        calories,proteins,fats,carbohydrates
    """
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/disease")
async def disease(request: Request):
    return templates.TemplateResponse("disease.html", {"request": request})


@router.get("/adding_food")
async def disease(request: Request):
    return templates.TemplateResponse("food.html", {"request": request})
