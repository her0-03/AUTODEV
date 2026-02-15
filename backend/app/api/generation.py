from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse, FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
import json
from pathlib import Path
from ..core.database import get_db
from ..core.config import settings
from ..models.generation_job import GenerationJob, JobStatus
from ..models.user import User
from ..services.document_processor import DocumentProcessor
from ..services.ai_service import AIService
from ..services.code_generator import CodeGenerator
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/v1", tags=["generation"])

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...), current_user: User = Depends(get_current_user)):
    upload_dir = Path(settings.UPLOAD_DIR) / current_user.id
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_paths = []
    for file in files:
        file_path = upload_dir / file.filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        file_paths.append(str(file_path))
    
    return {"files": file_paths}

@router.post("/generation/job")
def create_job(job_data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from ..models.generation_job import GenerationJob
    job = GenerationJob(
        project_id=job_data.get("project_id"),
        input_files=job_data.get("input_files", [])
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return {"id": job.id}

@router.get("/generation/jobs")
def list_jobs(project_id: str = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """List all jobs, optionally filtered by project_id"""
    query = db.query(GenerationJob)
    if project_id:
        query = query.filter(GenerationJob.project_id == project_id)
    jobs = query.order_by(GenerationJob.created_at).all()
    return [{"id": j.id, "status": j.status, "created_at": str(j.created_at)} for j in jobs]

@router.get("/generation/analyze-stream/{job_id}")
async def analyze_stream(job_id: str, token: str = None, db: Session = Depends(get_db)):
    from ..core.security import decode_access_token
    if token:
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=403, detail="Invalid token")
    job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job.status = JobStatus.PROCESSING
    db.commit()
    
    processor = DocumentProcessor()
    documents_content = ""
    for file_path in job.input_files or []:
        if os.path.exists(file_path):
            documents_content += f"\n\n--- {Path(file_path).name} ---\n"
            documents_content += processor.process_file(file_path)
    
    ai_service = AIService()
    
    async def event_stream():
        async for chunk in ai_service.analyze_documents_stream(documents_content):
            yield chunk
    
    return StreamingResponse(event_stream(), media_type="text/event-stream")

@router.post("/generation/job/{job_id}/save-spec")
def save_spec(job_id: str, spec_data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job.output_path = json.dumps(spec_data)
    job.status = JobStatus.COMPLETED
    db.commit()
    return {"message": "Specification saved", "spec": spec_data}

@router.get("/generation/job/{job_id}/preview")
def preview_spec(job_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    try:
        # Utiliser spec_json si disponible, sinon output_path
        spec_data = job.spec_json if job.spec_json else job.output_path
        
        if not spec_data:
            raise HTTPException(status_code=404, detail="Specification not found")
        
        spec = json.loads(spec_data)
        
        return {
            "appName": spec.get("appConfig", {}).get("name", "Unknown"),
            "description": spec.get("appConfig", {}).get("description", ""),
            "entities": len(spec.get("database", {}).get("entities", [])),
            "endpoints": len(spec.get("api", {}).get("endpoints", [])),
            "pages": len(spec.get("ui", {}).get("pages", [])),
            "fullSpec": spec
        }
    except Exception as e:
        print(f"[API] Preview error: {e}")
        raise HTTPException(status_code=500, detail=f"Invalid specification: {str(e)}")

@router.post("/generation/job/{job_id}/generate")
def generate_code(job_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
    if not job or not job.output_path:
        raise HTTPException(status_code=404, detail="Job not found or not analyzed")
    
    try:
        print(f"[API] Using GENERATED_DIR: {settings.GENERATED_DIR}")
        spec = json.loads(job.output_path)
        
        # Sauvegarder la spec dans un attribut séparé avant de générer
        job.spec_json = job.output_path
        
        generator = CodeGenerator(settings.GENERATED_DIR)
        zip_path = generator.generate_project(spec, f"project_{job_id}")
        
        # Mettre à jour output_path avec le chemin du ZIP
        job.output_path = zip_path
        job.status = JobStatus.COMPLETED
        db.commit()
        
        # Return file directly to avoid token expiration after reload
        if os.path.exists(zip_path):
            return FileResponse(zip_path, filename=f"project_{job_id}.zip", media_type="application/zip")
        else:
            raise HTTPException(status_code=500, detail="Generated file not found")
    except Exception as e:
        job.status = JobStatus.FAILED
        job.error_log = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/generation/download/{job_id}")
def download_code(job_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
    if not job or not job.output_path or not os.path.exists(job.output_path):
        raise HTTPException(status_code=404, detail="Generated code not found")
    
    return FileResponse(job.output_path, filename=f"project_{job_id}.zip")

@router.get("/generation/job/{job_id}/files")
def get_project_files(job_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get all files from generated project"""
    project_dir = Path(settings.GENERATED_DIR) / f"project_{job_id}"
    
    if not project_dir.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    
    files = {}
    for file_path in project_dir.rglob('*'):
        if file_path.is_file() and not any(p in file_path.parts for p in ['__pycache__', '.git', 'node_modules']):
            relative_path = str(file_path.relative_to(project_dir)).replace('\\', '/')
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    files[relative_path] = f.read()
            except:
                pass  # Skip binary files
    
    return {"files": files}

@router.get("/generation/job/{job_id}/file")
def get_project_file(job_id: str, file_path: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get a specific file from generated project"""
    project_dir = Path(settings.GENERATED_DIR) / f"project_{job_id}"
    full_path = project_dir / file_path
    
    if not full_path.exists() or not str(full_path).startswith(str(project_dir)):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return {"content": f.read()}
    except:
        raise HTTPException(status_code=400, detail="Cannot read file")
