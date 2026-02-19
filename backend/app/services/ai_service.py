import json
from typing import AsyncGenerator
from openai import OpenAI
from groq import Groq
from ..core.config import settings
from .document_analyzer import DocumentAnalyzer

class AIService:
    def __init__(self):
        self.client = None
        self.document_analyzer = None
        if settings.GROQ_API_KEY:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            self.document_analyzer = DocumentAnalyzer(settings.GROQ_API_KEY)
            # Modèles spécialisés Groq
            self.analysis_model = "llama-3.3-70b-versatile"
            self.code_model = "meta-llama/llama-4-maverick-17b-128e-instruct"
            self.fast_model = "llama-3.1-8b-instant"
            self.reasoning_model = "meta-llama/llama-4-scout-17b-16e-instruct"
        elif settings.OPENAI_API_KEY:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            self.analysis_model = "gpt-4"
            self.code_model = "gpt-4"
            self.fast_model = "gpt-3.5-turbo"
            self.reasoning_model = "gpt-4"
    
    async def analyze_documents_stream(self, documents_content: str) -> AsyncGenerator[str, None]:
        prompt = f"""You are a GENIUS software architect with 20 years experience at FAANG companies.

Analyze these documents with EXTREME PRECISION and generate a PERFECT JSON specification.

Files analyzed:
{documents_content}

Generate a COMPREHENSIVE JSON specification with this exact structure:
{{
  "appConfig": {{
    "name": "string (creative, professional name)",
    "description": "string (detailed, compelling description)",
    "theme": "modern-blue",
    "features": ["feature1", "feature2", "feature3"],
    "target_audience": "string",
    "business_model": "string"
  }},
  "database": {{
    "entities": [
      {{
        "name": "EntityName (PascalCase)",
        "description": "What this entity represents",
        "columns": [
          {{
            "name": "columnName (camelCase)",
            "type": "string|integer|boolean|datetime|text|float",
            "required": true,
            "unique": false,
            "description": "Column purpose",
            "validation": "Validation rules"
          }}
        ],
        "relationships": [
          {{
            "type": "one-to-many|many-to-one|many-to-many",
            "target": "TargetEntity",
            "description": "Relationship purpose"
          }}
        ],
        "indexes": ["column1", "column2"],
        "business_rules": ["rule1", "rule2"]
      }}
    ]
  }},
  "api": {{
    "endpoints": [
      {{
        "method": "GET|POST|PUT|DELETE|PATCH",
        "path": "/api/v1/resource",
        "description": "Detailed endpoint description",
        "authentication": "required|optional|none",
        "request_body": {{"field": "type"}},
        "response": {{"field": "type"}},
        "error_codes": [400, 401, 404, 500],
        "rate_limit": "100/hour",
        "caching": "5 minutes"
      }}
    ],
    "authentication": {{
      "type": "JWT|OAuth2|API_Key",
      "token_expiry": "24h"
    }},
    "versioning": "v1",
    "documentation": "OpenAPI 3.0"
  }},
  "ui": {{
    "pages": [
      {{
        "route": "/page-route",
        "title": "Page Title (SEO optimized)",
        "description": "Page purpose and content",
        "components": ["Header", "Hero", "Features", "CTA", "Footer"],
        "layout": "default|dashboard|landing",
        "seo": {{
          "meta_title": "SEO title",
          "meta_description": "SEO description",
          "keywords": ["keyword1", "keyword2"]
        }},
        "analytics": ["pageview", "conversion"],
        "accessibility": "WCAG AAA"
      }}
    ],
    "theme": {{
      "primary_color": "#hex",
      "secondary_color": "#hex",
      "font_family": "Inter, sans-serif",
      "design_system": "Material|Tailwind|Custom"
    }},
    "responsive": true,
    "pwa": true,
    "i18n": ["en", "fr", "es"]
  }},
  "infrastructure": {{
    "hosting": "AWS|GCP|Azure|Render",
    "database": "PostgreSQL|MySQL|MongoDB",
    "caching": "Redis|Memcached",
    "cdn": "Cloudflare|AWS CloudFront",
    "monitoring": "Datadog|New Relic|Sentry"
  }},
  "security": {{
    "https": true,
    "cors": {{"origins": ["*"]}},
    "rate_limiting": true,
    "input_validation": true,
    "sql_injection_protection": true,
    "xss_protection": true,
    "csrf_protection": true
  }},
  "performance": {{
    "lazy_loading": true,
    "code_splitting": true,
    "image_optimization": true,
    "minification": true,
    "compression": "gzip|brotli"
  }}
}}

IMPORTANT RULES:
1. Extract ALL entities, relationships, and business logic from documents
2. Create COMPREHENSIVE API endpoints (CRUD + custom operations)
3. Design BEAUTIFUL, INTUITIVE UI pages with modern components
4. Include SECURITY, PERFORMANCE, and SCALABILITY considerations
5. Add SEO, ACCESSIBILITY, and ANALYTICS features
6. Think like a SENIOR ARCHITECT at Google/Meta/Amazon
7. Be CREATIVE but PRACTICAL
8. Respond ONLY with valid JSON, no markdown formatting

Generate the PERFECT specification NOW:"""

        if not self.client:
            yield "data: Error: No AI API key configured\n\n"
            return
        
        import asyncio
        import time
        
        try:
            # Envoyer un heartbeat toutes les 10 secondes pour éviter timeout
            last_heartbeat = time.time()
            
            # 🔍 MULTI-AGENTS ANALYSIS
            if self.document_analyzer:
                yield "data: 🔍 Analyse multi-agents (5 experts)...\n\n"
                
                spec = await self.document_analyzer.analyze_documents(documents_content)
                
                spec_json = json.dumps(spec, indent=2)
                for char in spec_json:
                    if time.time() - last_heartbeat > 10:
                        yield ": heartbeat\n\n"
                        last_heartbeat = time.time()
                    yield f"data: {char}\n\n"
                    await asyncio.sleep(0.01)
                return
            
            if settings.GROQ_API_KEY:
                # Utilise le modèle d'analyse pour les documents
                response = self.client.chat.completions.create(
                    model=self.analysis_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8,  # Plus créatif
                    max_tokens=8000   # Plus de détails
                )
                content = response.choices[0].message.content
                for char in content:
                    # Heartbeat pour garder connexion active
                    if time.time() - last_heartbeat > 10:
                        yield ": heartbeat\n\n"
                        last_heartbeat = time.time()
                    yield f"data: {char}\n\n"
                    await asyncio.sleep(0.01)  # Petit délai pour streaming fluide
            else:
                stream = self.client.chat.completions.create(
                    model=self.analysis_model,
                    messages=[{"role": "user", "content": prompt}],
                    stream=True,
                    temperature=0.8,
                    max_tokens=8000
                )
                for chunk in stream:
                    # Heartbeat pour garder connexion active
                    if time.time() - last_heartbeat > 10:
                        yield ": heartbeat\n\n"
                        last_heartbeat = time.time()
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
