from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
from src.service.jobs_pipeline import JobsPipeline

router = APIRouter(prefix="/jobs", tags=["jobs"])
DB_FILE = "f:/pe/public_html/test-migration/skill4migration-2/storage/db.sqlite3"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

class PageItem(BaseModel):
    page: str
    lot: str
    member: str
    gp: Optional[bool] = False
    q_det: Optional[float] = 0.0
    q_fab: Optional[float] = 0.0
    q_inst: Optional[float] = 0.0
    q_tr: Optional[float] = 0.0

class JobCreateRequest(BaseModel):
    job_number: int
    company: str
    address: str
    superlot: Optional[str] = ""
    lot_group: Optional[str] = ""
    site_supervisor_id: Optional[int] = 0
    invoice_number: Optional[str] = ""
    date_install: Optional[str] = None
    comment: Optional[str] = ""
    date_creation: Optional[str] = None
    pages: Optional[List[PageItem]] = []

class JobUpdateRequest(BaseModel):
    company: str
    address: str
    superlot: Optional[str] = ""
    lot_group: Optional[str] = ""
    site_supervisor_id: Optional[int] = 0
    invoice_number: Optional[str] = ""
    date_install: Optional[str] = None
    comment: Optional[str] = ""
    date_creation: str
    pages: List[PageItem]

class JobResponse(BaseModel):
    id: int
    date_creation: Optional[str]
    job_number: Optional[int]
    company: Optional[str]
    address: Optional[str]
    delivery_name: Optional[str]
    completed: Optional[str]

@router.get("/", response_model=List[JobResponse])
def get_jobs(completed: Optional[str] = None, db: sqlite3.Connection = Depends(get_db)):
    """
    모든 jobs 목록을 조회하는 API 엔드포인트.
    """
    cursor = db.cursor()
    if completed is not None:
        cursor.execute("SELECT id, date_creation, job_number, company, address, delivery_name, completed FROM tb_jobs WHERE completed = ? ORDER BY id DESC", (completed,))
    else:
        cursor.execute("SELECT id, date_creation, job_number, company, address, delivery_name, completed FROM tb_jobs ORDER BY id DESC")
    
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

@router.get("/{job_id}", response_model=JobResponse)
def get_job_detail(job_id: int, db: sqlite3.Connection = Depends(get_db)):
    """
    특정 Job 상세를 조회하는 API 엔드포인트.
    """
    cursor = db.cursor()
    cursor.execute("SELECT id, date_creation, job_number, company, address, delivery_name, completed FROM tb_jobs WHERE id = ?", (job_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Job not found")
    return dict(row)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreateRequest):
    """
    신규 작업을 생성하는 API 엔드포인트 (create_update_job.php creation 대응).
    """
    pipeline = JobsPipeline(DB_FILE)
    try:
        job_id = pipeline.create_job(payload.model_dump())
        return {"id": job_id, "message": "Job created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{job_number}", status_code=status.HTTP_200_OK)
def update_job(job_number: int, year: str, payload: JobUpdateRequest):
    """
    기존 작업을 업데이트하는 API 엔드포인트 (create_update_job.php update 대응).
    """
    pipeline = JobsPipeline(DB_FILE)
    success = pipeline.update_job(job_number, year, payload.model_dump())
    if not success:
        raise HTTPException(status_code=404, detail="Job not found or update failed")
    return {"message": "Job updated successfully"}

if __name__ == "__main__":
    print("FastAPI jobs.py module syntax check passed.")
