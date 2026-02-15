import json
from typing import AsyncGenerator
from openai import OpenAI
from groq import Groq
from ..core.config import settings

class AIService:
    def __init__(self):
        self.client = None
        if settings.GROQ_API_KEY:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            # Modèles spécialisés Groq
            self.analysis_model = "llama-3.3-70b-versatile"           # Analyse documents
            self.code_model = "meta-llama/llama-4-maverick-17b-128e-instruct"  # Génération code
            self.fast_model = "llama-3.1-8b-instant"                  # Validation rapide
            self.reasoning_model = "meta-llama/llama-4-scout-17b-16e-instruct"  # Raisonnement
        elif settings.OPENAI_API_KEY:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            self.analysis_model = "gpt-4"
            self.code_model = "gpt-4"
            self.fast_model = "gpt-3.5-turbo"
            self.reasoning_model = "gpt-4"
    
    async def analyze_documents_stream(self, documents_content: str) -> AsyncGenerator[str, None]:
        prompt = f"""You are a senior software architect. Analyze these documents and generate a JSON specification for a web application.

Files analyzed:
{documents_content}

Generate a JSON specification with this exact structure:
{{
  "appConfig": {{
    "name": "string",
    "description": "string",
    "theme": "modern-blue"
  }},
  "database": {{
    "entities": [
      {{
        "name": "EntityName",
        "columns": [
          {{
            "name": "columnName",
            "type": "string",
            "required": true,
            "unique": false
          }}
        ],
        "relationships": []
      }}
    ]
  }},
  "api": {{
    "endpoints": [
      {{
        "method": "GET",
        "path": "/api/resource",
        "description": "Endpoint description"
      }}
    ]
  }},
  "ui": {{
    "pages": [
      {{
        "route": "/page-route",
        "title": "Page Title",
        "components": ["ComponentName"]
      }}
    ]
  }}
}}

Respond ONLY with valid JSON, no markdown formatting."""

        if not self.client:
            yield "data: Error: No AI API key configured\n\n"
            return
        
        try:
            if settings.GROQ_API_KEY:
                # Utilise le modèle d'analyse pour les documents
                response = self.client.chat.completions.create(
                    model=self.analysis_model,
                    messages=[{"role": "user", "content": prompt}],
                )
                content = response.choices[0].message.content
                for char in content:
                    yield f"data: {char}\n\n"
            else:
                stream = self.client.chat.completions.create(
                    model=self.analysis_model,
                    messages=[{"role": "user", "content": prompt}],
                    stream=True
                )
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield f"data: {chunk.choices[0].delta.content}\n\n"
        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"
    
    def generate_code_snippet(self, spec: dict, entity: str) -> str:
        """Utilise le modèle de code pour générer du code spécifique"""
        if not self.client:
            return ""
        
        prompt = f"Generate Python code for entity: {entity}\nSpec: {json.dumps(spec)}"
        response = self.client.chat.completions.create(
            model=self.code_model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def quick_validation(self, data: str) -> bool:
        """Utilise le modèle rapide pour validation"""
        if not self.client:
            return True
        
        prompt = f"Is this valid JSON? Answer only yes or no: {data[:500]}"
        response = self.client.chat.completions.create(
            model=self.fast_model,
            messages=[{"role": "user", "content": prompt}]
        )
        return "yes" in response.choices[0].message.content.lower()
    
    def analyze_architecture(self, spec: dict) -> str:
        """Utilise le modèle de raisonnement pour analyser l'architecture"""
        if not self.client:
            return ""
        
        prompt = f"Analyze this application architecture and suggest improvements:\n{json.dumps(spec, indent=2)}"
        response = self.client.chat.completions.create(
            model=self.reasoning_model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    async def fix_code_error(self, file_path: str, error_message: str) -> str:
        """Auto-fix code errors using AI"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            is_flask = 'flask' in code.lower() or 'app.py' in file_path
            
            if is_flask:
                prompt = f"""Fix this Flask application code:

ERROR:
{error_message}

CODE:
{code}

Return ONLY the fixed code. Requirements:
1. Import Flask, render_template, requests
2. Add @app.route('/') for homepage
3. Use <int:id> not {{id}} in routes
4. Connect to BACKEND_API_URL environment variable
5. Add try/except for API calls
6. Use port from FLASK_RUN_PORT environment variable
7. Make sure all routes return valid responses
"""
            else:
                prompt = f"""Fix this Python FastAPI code:

ERROR:
{error_message}

CODE:
{code}

Return ONLY the fixed code. Requirements:
1. Import APIRouter, List, BaseModel
2. Define router = APIRouter()
3. Include all response models with from_attributes = True
4. Include app.include_router(router)
5. Add @app.get("/") root endpoint
6. Fix all syntax errors
"""
            
            response = self.client.chat.completions.create(
                model=self.analysis_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=4000
            )
            
            fixed_code = response.choices[0].message.content.strip()
            if fixed_code.startswith("```"):
                lines = fixed_code.split("\n")
                fixed_code = "\n".join(lines[1:-1]) if len(lines) > 2 else fixed_code
            
            return fixed_code
        except Exception as e:
            print(f"[AI-FIX] Error: {e}")
            return None
