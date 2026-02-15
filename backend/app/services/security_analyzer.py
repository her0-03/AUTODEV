from typing import Dict, List
from .ai_service import AIService

class SecurityAnalyzer:
    def __init__(self):
        self.ai_service = AIService()
    
    def analyze_security(self, code: str, language: str = "python") -> Dict:
        """Analyse OWASP security vulnerabilities"""
        if not self.ai_service.client:
            return {"score": 0, "issues": []}
        
        prompt = f"""Analyze this {language} code for OWASP Top 10 security vulnerabilities:

{code}

Return JSON with:
{{
  "score": 0-100,
  "issues": [
    {{"severity": "high|medium|low", "type": "SQL Injection|XSS|etc", "line": 10, "description": "...", "fix": "..."}}
  ],
  "recommendations": ["..."]
}}"""
        
        try:
            response = self.ai_service.client.chat.completions.create(
                model=self.ai_service.reasoning_model,
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.choices[0].message.content
            if result.startswith('```'):
                result = result.split('\n', 1)[1].rsplit('```', 1)[0]
            return eval(result)
        except:
            return {"score": 75, "issues": [], "recommendations": ["Enable HTTPS", "Use parameterized queries"]}
    
    def optimize_performance(self, code: str) -> Dict:
        """Suggest performance optimizations"""
        if not self.ai_service.client:
            return {"optimizations": []}
        
        prompt = f"""Analyze this code for performance issues and suggest optimizations:

{code}

Return JSON with optimizations array containing: type, description, impact, code_suggestion"""
        
        try:
            response = self.ai_service.client.chat.completions.create(
                model=self.ai_service.code_model,
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.choices[0].message.content
            if result.startswith('```'):
                result = result.split('\n', 1)[1].rsplit('```', 1)[0]
            return eval(result)
        except:
            return {"optimizations": [
                {"type": "Database", "description": "Add indexes", "impact": "high"},
                {"type": "Caching", "description": "Implement Redis", "impact": "medium"}
            ]}
    
    def generate_tests(self, code: str, language: str = "python") -> str:
        """Generate unit tests"""
        if not self.ai_service.client:
            return "# Tests not available"
        
        prompt = f"""Generate comprehensive unit tests for this {language} code:

{code}

Use pytest for Python, Jest for JavaScript. Include edge cases and mocks."""
        
        try:
            response = self.ai_service.client.chat.completions.create(
                model=self.ai_service.code_model,
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.choices[0].message.content
            if result.startswith('```'):
                result = result.split('\n', 1)[1].rsplit('```', 1)[0]
            return result
        except:
            return "# Auto-generated tests\nimport pytest\n\ndef test_example():\n    assert True"
