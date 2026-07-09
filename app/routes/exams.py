from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/exams",
    tags=["Exams"]
)

@router.get("/healt")
def get_status():
  return {
    "status": "ok"
  }