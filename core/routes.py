from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_products():
    return [{"id": 1, "name": "Produto A"}, {"id": 2, "name": "Produto B"}]
