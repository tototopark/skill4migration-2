from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
import sqlite3

router = APIRouter(prefix="/jobs", tags=["jobs"])
DB_FILE = "f:/pe/public_html/test-migration/skill4migration-2/storage/db.sqlite3"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

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

if __name__ == "__main__":
    print("FastAPI jobs.py module syntax check passed.")
