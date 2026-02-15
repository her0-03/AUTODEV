from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict
from ..core.database import get_db
from ..models.user import User
from ..utils.auth import get_current_user
from ..services.template_marketplace import TemplateMarketplace
from ..services.ai_assistant import AIAssistant
from ..services.analytics_service import AnalyticsService
from ..services.security_analyzer import SecurityAnalyzer
from ..services.auto_deployer import AutoDeployer

router = APIRouter(prefix="/api/v1/advanced", tags=["advanced"])

# Template Marketplace
@router.get("/templates")
def list_templates():
    """Get all available templates"""
    return TemplateMarketplace.get_templates()

@router.get("/templates/{template_id}")
def get_template(template_id: str):
    """Get template specification"""
    return TemplateMarketplace.get_template_spec(template_id)

# AI Assistant
@router.post("/assistant/modify")
def modify_code(request: Dict, current_user: User = Depends(get_current_user)):
    """Modify code using natural language"""
    assistant = AIAssistant()
    result = assistant.modify_code(
        instruction=request.get("instruction", ""),
        current_code=request.get("code", ""),
        context=request.get("context", {})
    )
    return {"modified_code": result}

@router.post("/assistant/add-oauth")
def add_oauth(request: Dict, current_user: User = Depends(get_current_user)):
    """Add OAuth authentication"""
    assistant = AIAssistant()
    result = assistant.add_oauth(
        provider=request.get("provider", "google"),
        code=request.get("code", "")
    )
    return {"code": result}

@router.post("/assistant/add-stripe")
def add_stripe(request: Dict, current_user: User = Depends(get_current_user)):
    """Add Stripe payment integration"""
    assistant = AIAssistant()
    result = assistant.add_stripe_payment(request.get("code", ""))
    return {"code": result}

@router.post("/assistant/optimize-sql")
def optimize_sql(request: Dict, current_user: User = Depends(get_current_user)):
    """Optimize SQL queries"""
    assistant = AIAssistant()
    result = assistant.optimize_sql(request.get("code", ""))
    return result

@router.post("/assistant/add-integration")
def add_integration(request: Dict, current_user: User = Depends(get_current_user)):
    """Add third-party API integration"""
    assistant = AIAssistant()
    result = assistant.add_api_integration(
        service=request.get("service", ""),
        code=request.get("code", "")
    )
    return {"code": result}

# Analytics
@router.post("/analytics/cost-estimate")
def estimate_cost(spec: Dict, current_user: User = Depends(get_current_user)):
    """Estimate hosting costs"""
    analytics = AnalyticsService()
    return analytics.estimate_hosting_cost(spec)

@router.post("/analytics/performance")
def predict_performance(spec: Dict, current_user: User = Depends(get_current_user)):
    """Predict performance metrics"""
    analytics = AnalyticsService()
    return analytics.predict_performance(spec)

@router.post("/analytics/scalability")
def analyze_scalability(spec: Dict, current_user: User = Depends(get_current_user)):
    """Analyze scalability"""
    analytics = AnalyticsService()
    return analytics.analyze_scalability(spec)

@router.post("/analytics/security-score")
def security_score(request: Dict, current_user: User = Depends(get_current_user)):
    """Calculate security score"""
    analytics = AnalyticsService()
    return analytics.calculate_security_score(
        spec=request.get("spec", {}),
        security_analysis=request.get("security_analysis", {})
    )

# Security & Code Review
@router.post("/security/analyze")
def analyze_security(request: Dict, current_user: User = Depends(get_current_user)):
    """Analyze code security"""
    analyzer = SecurityAnalyzer()
    return analyzer.analyze_security(
        code=request.get("code", ""),
        language=request.get("language", "python")
    )

@router.post("/security/optimize")
def optimize_performance(request: Dict, current_user: User = Depends(get_current_user)):
    """Get performance optimizations"""
    analyzer = SecurityAnalyzer()
    return analyzer.optimize_performance(request.get("code", ""))

@router.post("/security/generate-tests")
def generate_tests(request: Dict, current_user: User = Depends(get_current_user)):
    """Generate unit tests"""
    analyzer = SecurityAnalyzer()
    tests = analyzer.generate_tests(
        code=request.get("code", ""),
        language=request.get("language", "python")
    )
    return {"tests": tests}


@router.post("/assistant/ask")
async def ask_assistant(request: dict, current_user: User = Depends(get_current_user)):
    """Ask AI assistant - it will modify files automatically"""
    question = request.get("question")
    job_id = request.get("job_id")
    
    if not question or not job_id:
        raise HTTPException(status_code=400, detail="Question and job_id required")
    
    from pathlib import Path
    from ..core.config import settings
    project_dir = Path(settings.GENERATED_DIR) / f"project_{job_id}"
    if not project_dir.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Read ALL files with FULL content
    files_content = {}
    for file_path in project_dir.rglob('*'):
        if file_path.is_file() and file_path.suffix in ['.py', '.md', '.yml', '.txt', '.html', '.css', '.js']:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    rel_path = str(file_path.relative_to(project_dir)).replace('\\', '/')
                    files_content[rel_path] = f.read()  # FULL content
            except:
                pass
    
    print(f"[AI-ASSISTANT] Found {len(files_content)} files")
    print(f"[AI-ASSISTANT] Files: {list(files_content.keys())}")
    
    assistant = AIAssistant()
    result = assistant.process_request(question, files_content, project_dir)
    
    return result


@router.post("/deploy/auto")
async def auto_deploy(request: dict, current_user: User = Depends(get_current_user)):
    """Auto-deploy: Create GitHub repo + Deploy to Render"""
    job_id = request.get("job_id")
    app_name = request.get("app_name", f"app-{job_id[:8]}")
    
    if not job_id:
        raise HTTPException(status_code=400, detail="job_id required")
    
    from pathlib import Path
    from ..core.config import settings
    project_dir = Path(settings.GENERATED_DIR) / f"project_{job_id}"
    
    if not project_dir.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        deployer = AutoDeployer()
        result = deployer.deploy_app(project_dir, app_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
