from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/healt")
def get_status():
  return {
    "status": "ok"
  }