import os
import requests
import zipfile
from pathlib import Path

class RenderDeployer:
    """Deploy generated apps to Render automatically"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('RENDER_API_KEY')
        self.base_url = "https://api.render.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def deploy_generated_app(self, project_dir: Path, app_name: str) -> dict:
        """Deploy a generated application to Render"""
        
        # 1. Create GitHub repo (or use Render's direct deploy)
        # 2. Push code to repo
        # 3. Create Render services via API
        
        backend_dir = project_dir / "backend"
        frontend_dir = project_dir / "frontend"
        
        # Create backend service
        backend_service = self._create_web_service(
            name=f"{app_name}-backend",
            repo_url=f"https://github.com/her0-03/{app_name}",
            root_dir="backend",
            build_command="pip install -r requirements.txt",
            start_command="uvicorn main:app --host 0.0.0.0 --port $PORT",
            env_vars={
                "DATABASE_URL": "sqlite:///./app.db"
            }
        )
        
        # Create frontend service
        frontend_service = self._create_web_service(
            name=f"{app_name}-frontend",
            repo_url=f"https://github.com/her0-03/{app_name}",
            root_dir="frontend",
            build_command="pip install -r requirements.txt",
            start_command="gunicorn app:app",
            env_vars={
                "BACKEND_API_URL": backend_service['url']
            }
        )
        
        return {
            "backend_url": backend_service['url'],
            "frontend_url": frontend_service['url'],
            "status": "deployed"
        }
    
    def _create_web_service(self, name, repo_url, root_dir, build_command, start_command, env_vars):
        """Create a web service on Render"""
        
        payload = {
            "type": "web_service",
            "name": name,
            "repo": repo_url,
            "rootDir": root_dir,
            "buildCommand": build_command,
            "startCommand": start_command,
            "envVars": [
                {"key": k, "value": v} for k, v in env_vars.items()
            ],
            "plan": "free"
        }
        
        response = requests.post(
            f"{self.base_url}/services",
            headers=self.headers,
            json=payload
        )
        
        if response.ok:
            service = response.json()
            return {
                "id": service['id'],
                "url": f"https://{service['name']}.onrender.com"
            }
        else:
            raise Exception(f"Failed to create service: {response.text}")
    
    def create_one_click_deploy(self, project_dir: Path, app_name: str) -> str:
        """Create a one-click deploy button for the generated app"""
        
        # Create render.yaml for the generated app
        render_yaml = f"""services:
  - type: web
    name: {app_name}-backend
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    rootDir: backend
    envVars:
      - key: DATABASE_URL
        value: sqlite:///./app.db
    
  - type: web
    name: {app_name}-frontend
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    rootDir: frontend
    envVars:
      - key: BACKEND_API_URL
        fromService:
          name: {app_name}-backend
          type: web
          property: url
"""
        
        # Save render.yaml in project
        with open(project_dir / "render.yaml", "w") as f:
            f.write(render_yaml)
        
        # Return deploy button markdown
        return f"[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/her0-03/{app_name})"
