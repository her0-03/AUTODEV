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
import asyncio

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
    
    job.spec_json = json.dumps(spec_data)
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
    if not job or not job.spec_json:
        raise HTTPException(status_code=404, detail="Job not found or not analyzed")
    
    try:
        print(f"[API] Using GENERATED_DIR: {settings.GENERATED_DIR}")
        spec = json.loads(job.spec_json)
        
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

@router.post("/generation/job/{job_id}/preview-app")
async def preview_generated_app(job_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Launch full-stack app with AI auto-fix"""
    import subprocess
    import socket
    import sys
    
    project_dir = Path(settings.GENERATED_DIR) / f"project_{job_id}"
    if not project_dir.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    
    backend_dir = project_dir / "backend"
    frontend_dir = project_dir / "frontend"
    
    def find_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]
    
    backend_port = find_free_port()
    frontend_port = find_free_port()
    
    # Install deps
    for req_file in [(backend_dir / "requirements.txt"), (frontend_dir / "requirements.txt")]:
        if req_file.exists():
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", str(req_file)], check=False, capture_output=True)
    
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            # Fix backend
            result = subprocess.run([sys.executable, "-c", "import main"], cwd=str(backend_dir), capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                print(f"[AUTO-FIX] Backend error (attempt {attempt+1}): {result.stderr[:200]}")
                ai_service = AIService()
                fixed = await ai_service.fix_code_error(str(backend_dir / "main.py"), result.stderr)
                if fixed:
                    with open(backend_dir / "main.py", "w", encoding="utf-8") as f:
                        f.write(fixed)
                    print(f"[AUTO-FIX] Backend fixed")
                    await asyncio.sleep(1)
                    continue
            
            # Fix frontend
            result = subprocess.run([sys.executable, "-c", "import app"], cwd=str(frontend_dir), capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                print(f"[AUTO-FIX] Frontend error (attempt {attempt+1}): {result.stderr[:200]}")
                ai_service = AIService()
                fixed = await ai_service.fix_code_error(str(frontend_dir / "app.py"), result.stderr)
                if fixed:
                    with open(frontend_dir / "app.py", "w", encoding="utf-8") as f:
                        f.write(fixed)
                    print(f"[AUTO-FIX] Frontend fixed")
                    await asyncio.sleep(1)
                    continue
            
            # Start backend
            backend_process = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", str(backend_port)],
                cwd=str(backend_dir),
                env={**os.environ, "DATABASE_URL": "sqlite:///./app.db"},
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            await asyncio.sleep(2)
            
            # Check backend started
            if backend_process.poll() is not None:
                _, stderr = backend_process.communicate(timeout=1)
                print(f"[AUTO-FIX] Backend crashed: {stderr[:200]}")
                ai_service = AIService()
                fixed = await ai_service.fix_code_error(str(backend_dir / "main.py"), stderr)
                if fixed:
                    with open(backend_dir / "main.py", "w", encoding="utf-8") as f:
                        f.write(fixed)
                    continue
            
            # Start frontend
            frontend_process = subprocess.Popen(
                [sys.executable, "app.py"],
                cwd=str(frontend_dir),
                env={**os.environ, "FLASK_RUN_PORT": str(frontend_port), "BACKEND_API_URL": f"http://localhost:{backend_port}"},
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            await asyncio.sleep(2)
            
            # Check frontend started
            if frontend_process.poll() is not None:
                _, stderr = frontend_process.communicate(timeout=1)
                print(f"[AUTO-FIX] Frontend crashed: {stderr[:200]}")
                ai_service = AIService()
                fixed = await ai_service.fix_code_error(str(frontend_dir / "app.py"), stderr)
                if fixed:
                    with open(frontend_dir / "app.py", "w", encoding="utf-8") as f:
                        f.write(fixed)
                    continue
            
            # Auto-fix templates if missing
            templates_dir = frontend_dir / "templates"
            if not (templates_dir / "index.html").exists():
                print(f"[AUTO-FIX] Creating missing index.html")
                templates_dir.mkdir(exist_ok=True)
                with open(templates_dir / "index.html", "w", encoding="utf-8") as f:
                    f.write('''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Application</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen">
    <div class="container mx-auto px-4 py-12">
        <h1 class="text-5xl font-bold text-center mb-12">🚀 Application Générée</h1>
        <div class="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <a href="/students" class="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all transform hover:-translate-y-2">
                <div class="text-6xl mb-4">👨🎓</div>
                <h2 class="text-2xl font-bold">Étudiants</h2>
            </a>
            <a href="/courses" class="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all transform hover:-translate-y-2">
                <div class="text-6xl mb-4">📚</div>
                <h2 class="text-2xl font-bold">Cours</h2>
            </a>
            <a href="/transcripts" class="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all transform hover:-translate-y-2">
                <div class="text-6xl mb-4">📝</div>
                <h2 class="text-2xl font-bold">Relevés</h2>
            </a>
        </div>
    </div>
</body>
</html>''')
            
            # Auto-fix other templates
            for template_name in ["students.html", "courses.html", "transcripts.html"]:
                if not (templates_dir / template_name).exists():
                    entity = template_name.replace(".html", "")
                    print(f"[AUTO-FIX] Creating {template_name}")
                    with open(templates_dir / template_name, "w", encoding="utf-8") as f:
                        f.write(f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{entity.title()}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 p-8">
    <div class="max-w-6xl mx-auto">
        <h1 class="text-4xl font-bold mb-8">{entity.title()}</h1>
        <div class="bg-white rounded-lg shadow p-6">
            <div id="data-container"></div>
        </div>
        <a href="/" class="mt-4 inline-block text-blue-600 hover:underline">← Retour</a>
    </div>
    <script>
        fetch('http://localhost:{backend_port}/api/{entity}')
            .then(r => r.json())
            .then(data => {{
                document.getElementById('data-container').innerHTML = 
                    '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            }})
            .catch(e => {{
                document.getElementById('data-container').innerHTML = 
                    '<p class="text-red-600">Erreur: ' + e.message + '</p>';
            }});
    </script>
</body>
</html>''')
            
            return {
                "url": f"http://localhost:{frontend_port}",
                "frontend_port": frontend_port,
                "backend_port": backend_port,
                "backend_url": f"http://localhost:{backend_port}",
                "message": f"Application complète! {'(Auto-corrigée ' + str(attempt+1) + 'x)' if attempt > 0 else ''}",
                "fixed": attempt > 0,
                "deploy_instructions": {
                    "local": "Application running locally",
                    "render": "To deploy on Render, use the 'Deploy to Render' button in the downloaded project"
                }
            }
            
        except Exception as e:
            print(f"[AUTO-FIX] Attempt {attempt+1} failed: {e}")
            if attempt == max_attempts - 1:
                raise HTTPException(status_code=500, detail=f"Échec après {max_attempts} tentatives: {str(e)}")
    
    raise HTTPException(status_code=500, detail="Impossible de démarrer")
