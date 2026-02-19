"""
🔍 DOCUMENT ANALYZER - Multi-Agents pour Analyse Parfaite
5 agents spécialisés analysent les documents en parallèle
"""
from groq import Groq
from typing import Dict, List, Any
import json
import asyncio
from dataclasses import dataclass

@dataclass
class AnalysisAgent:
    """Agent d'analyse spécialisé"""
    name: str
    model: str
    role: str
    focus: List[str]

class DocumentAnalyzer:
    """
    🔍 Analyseur Multi-Agents
    
    5 agents spécialisés:
    1. Business Analyst - Extrait besoins métier
    2. Data Architect - Conçoit base de données
    3. API Designer - Définit endpoints
    4. UX Designer - Crée pages UI
    5. Tech Lead - Synthétise et valide
    """
    
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.agents = self._initialize_agents()
    
    def _initialize_agents(self) -> Dict[str, AnalysisAgent]:
        """Initialise les 5 agents d'analyse"""
        return {
            "business_analyst": AnalysisAgent(
                name="Business Analyst",
                model="llama-3.3-70b-versatile",
                role="Senior Business Analyst (McKinsey niveau)",
                focus=["requirements", "features", "business_model", "target_audience"]
            ),
            
            "data_architect": AnalysisAgent(
                name="Data Architect",
                model="llama-3.3-70b-versatile",
                role="Senior Data Architect (Amazon niveau)",
                focus=["entities", "relationships", "indexes", "constraints"]
            ),
            
            "api_designer": AnalysisAgent(
                name="API Designer",
                model="meta-llama/llama-4-maverick-17b-128e-instruct",
                role="Senior API Designer (Stripe niveau)",
                focus=["endpoints", "authentication", "rate_limiting", "versioning"]
            ),
            
            "ux_designer": AnalysisAgent(
                name="UX Designer",
                model="llama-3.3-70b-versatile",
                role="Senior UX Designer (Apple niveau)",
                focus=["pages", "components", "user_flows", "accessibility"]
            ),
            
            "tech_lead": AnalysisAgent(
                name="Tech Lead",
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                role="Tech Lead (Google niveau)",
                focus=["architecture", "security", "performance", "scalability"]
            )
        }
    
    async def analyze_documents(self, documents_content: str) -> Dict[str, Any]:
        """
        Analyse multi-agents en parallèle
        
        Returns:
            Spécification complète fusionnée
        """
        print("\n🔍 DOCUMENT ANALYZER - Multi-Agents")
        print(f"📄 Documents: {len(documents_content)} chars")
        print(f"👥 Agents: {len(self.agents)}")
        print("=" * 80)
        
        # PHASE 1: Analyse parallèle par chaque agent
        print("\n⚡ PHASE 1: Analyse Parallèle")
        tasks = [
            self._agent_analyze(agent, documents_content)
            for agent in self.agents.values()
        ]
        
        analyses = await asyncio.gather(*tasks)
        
        # PHASE 2: Fusion par le Tech Lead
        print("\n🧬 PHASE 2: Fusion & Validation")
        final_spec = await self._fuse_analyses(analyses)
        
        return final_spec
    
    async def _agent_analyze(self, agent: AnalysisAgent, content: str) -> Dict:
        """Analyse par un agent spécifique"""
        
        if agent.name == "Business Analyst":
            prompt = f"""Tu es {agent.role}.

Analyse ces documents et extrait:

Documents:
{content[:3000]}...

Retourne en JSON:
{{
  "appConfig": {{
    "name": "Nom créatif et professionnel",
    "description": "Description détaillée et convaincante",
    "features": ["feature1", "feature2", "feature3"],
    "target_audience": "Public cible précis",
    "business_model": "Modèle économique",
    "value_proposition": "Proposition de valeur unique"
  }}
}}

Focus sur: {', '.join(agent.focus)}"""

        elif agent.name == "Data Architect":
            prompt = f"""Tu es {agent.role}.

Analyse ces documents et conçois la base de données:

Documents:
{content[:3000]}...

Retourne en JSON:
{{
  "database": {{
    "entities": [
      {{
        "name": "EntityName",
        "description": "Rôle de l'entité",
        "columns": [
          {{
            "name": "columnName",
            "type": "string|integer|boolean|datetime|text|float",
            "required": true,
            "unique": false,
            "description": "Rôle de la colonne",
            "validation": "Règles de validation"
          }}
        ],
        "relationships": [
          {{
            "type": "one-to-many|many-to-one|many-to-many",
            "target": "TargetEntity",
            "description": "Rôle de la relation"
          }}
        ],
        "indexes": ["column1", "column2"],
        "business_rules": ["rule1", "rule2"]
      }}
    ]
  }}
}}

Crée TOUTES les entités nécessaires avec relations complètes."""

        elif agent.name == "API Designer":
            prompt = f"""Tu es {agent.role}.

Analyse ces documents et conçois l'API REST:

Documents:
{content[:3000]}...

Retourne en JSON:
{{
  "api": {{
    "endpoints": [
      {{
        "method": "GET|POST|PUT|DELETE|PATCH",
        "path": "/api/v1/resource",
        "description": "Description détaillée",
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
    "versioning": "v1"
  }}
}}

Crée TOUS les endpoints CRUD + endpoints métier spécifiques."""

        elif agent.name == "UX Designer":
            prompt = f"""Tu es {agent.role}.

Analyse ces documents et conçois l'interface:

Documents:
{content[:3000]}...

Retourne en JSON:
{{
  "ui": {{
    "pages": [
      {{
        "route": "/page-route",
        "title": "Titre SEO optimisé",
        "description": "Description de la page",
        "components": ["Header", "Hero", "Features", "CTA", "Footer"],
        "layout": "default|dashboard|landing",
        "seo": {{
          "meta_title": "Titre SEO",
          "meta_description": "Description SEO",
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
    }}
  }}
}}

Crée TOUTES les pages nécessaires avec composants modernes."""

        else:  # Tech Lead
            prompt = f"""Tu es {agent.role}.

Analyse ces documents et définis l'infrastructure:

Documents:
{content[:3000]}...

Retourne en JSON:
{{
  "infrastructure": {{
    "hosting": "AWS|GCP|Azure|Render",
    "database": "PostgreSQL|MySQL|MongoDB",
    "caching": "Redis|Memcached",
    "cdn": "Cloudflare|AWS CloudFront",
    "monitoring": "Datadog|Sentry"
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

Définis infrastructure production-ready."""
        
        try:
            response = self.client.chat.completions.create(
                model=agent.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            
            result = json.loads(content)
            print(f"  ✅ {agent.name}: Analyse terminée")
            return result
            
        except Exception as e:
            print(f"  ⚠️  {agent.name}: Erreur - {str(e)[:50]}")
            return {}
    
    async def _fuse_analyses(self, analyses: List[Dict]) -> Dict:
        """Fusionne toutes les analyses en une spec complète"""
        
        final_spec = {
            "appConfig": {},
            "database": {"entities": []},
            "api": {"endpoints": []},
            "ui": {"pages": []},
            "infrastructure": {},
            "security": {},
            "performance": {}
        }
        
        # Fusionner chaque section
        for analysis in analyses:
            for key, value in analysis.items():
                if key in final_spec:
                    if isinstance(value, dict):
                        final_spec[key].update(value)
                    elif isinstance(value, list):
                        final_spec[key].extend(value)
        
        # Validation par Tech Lead
        tech_lead = self.agents["tech_lead"]
        validation_prompt = f"""Tu es {tech_lead.role}.

Valide et améliore cette spécification:

{json.dumps(final_spec, indent=2)}

Vérifie:
1. Cohérence entre entités, API et UI
2. Sécurité et performance
3. Complétude des relations
4. Qualité des endpoints

Retourne la spec AMÉLIORÉE en JSON."""

        try:
            response = self.client.chat.completions.create(
                model=tech_lead.model,
                messages=[{"role": "user", "content": validation_prompt}],
                temperature=0.5,
                max_tokens=6000
            )
            
            content = response.choices[0].message.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            
            validated_spec = json.loads(content)
            print(f"  ✅ {tech_lead.name}: Validation terminée")
            
            return validated_spec
            
        except Exception as e:
            print(f"  ⚠️  Validation erreur: {str(e)[:50]}")
            return final_spec


# ============================================
# EXEMPLE D'UTILISATION
# ============================================
if __name__ == "__main__":
    import os
    
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "gsk_...")
    
    analyzer = DocumentAnalyzer(GROQ_API_KEY)
    
    print("🔍 DOCUMENT ANALYZER - Multi-Agents")
    print("=" * 80)
    print("\n5 Agents Spécialisés:")
    for name, agent in analyzer.agents.items():
        print(f"  • {agent.name} ({agent.role})")
        print(f"    Focus: {', '.join(agent.focus)}")
    
    # Test
    # documents = "Application de gestion de tâches..."
    # spec = asyncio.run(analyzer.analyze_documents(documents))
    # print(f"\n✅ Analyse terminée!")
    # print(f"Entités: {len(spec.get('database', {}).get('entities', []))}")
    # print(f"Endpoints: {len(spec.get('api', {}).get('endpoints', []))}")
    # print(f"Pages: {len(spec.get('ui', {}).get('pages', []))}")
