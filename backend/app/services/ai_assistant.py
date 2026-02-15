from typing import Dict
from .ai_service import AIService

class AIAssistant:
    def __init__(self):
        self.ai_service = AIService()
    
    def modify_code(self, instruction: str, current_code: str, context: Dict) -> str:
        """Modify generated code based on natural language instructions"""
        if not self.ai_service.client:
            return current_code
        
        prompt = f"""You are a senior developer. Modify this code based on the instruction.

Instruction: {instruction}

Current code:
{current_code}

Context: {context}

Return ONLY the modified code, no explanations."""
        
        try:
            response = self.ai_service.client.chat.completions.create(
                model=self.ai_service.code_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            result = response.choices[0].message.content
            if result.startswith('```'):
                result = result.split('\n', 1)[1].rsplit('```', 1)[0]
            return result
        except:
            return current_code
    
    def add_oauth(self, provider: str, code: str) -> str:
        """Add OAuth authentication"""
        prompt = f"""Add {provider} OAuth authentication to this FastAPI code:

{code}

Include:
- OAuth routes
- Token handling
- User session management
- Redirect URLs

Return complete code."""
        
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
            return code
    
    def add_stripe_payment(self, code: str) -> str:
        """Add Stripe payment integration"""
        prompt = f"""Add Stripe payment processing to this code:

{code}

Include:
- Payment intent creation
- Webhook handling
- Subscription management
- Error handling

Return complete code."""
        
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
            return code
    
    def optimize_sql(self, code: str) -> Dict:
        """Optimize SQL queries"""
        prompt = f"""Analyze and optimize SQL queries in this code:

{code}

Return JSON with:
{{
  "optimized_code": "...",
  "changes": ["Added index on user_id", "Used JOIN instead of subquery"],
  "performance_gain": "30%"
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
            return {"optimized_code": code, "changes": [], "performance_gain": "0%"}
    
    def add_api_integration(self, service: str, code: str) -> str:
        """Add third-party API integration (Twilio, SendGrid, etc.)"""
        integrations = {
            "twilio": "SMS sending with Twilio",
            "sendgrid": "Email sending with SendGrid",
            "stripe": "Payment processing with Stripe",
            "aws-s3": "File storage with AWS S3",
            "redis": "Caching with Redis"
        }
        
        description = integrations.get(service, f"{service} integration")
        
        prompt = f"""Add {description} to this code:

{code}

Include:
- API client setup
- Error handling
- Environment variables
- Usage examples

Return complete code."""
        
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
            return code

    
    def ask_question(self, question: str, context: str) -> str:
        """Ask AI a question about the project"""
        prompt = f"""You are an AI assistant helping with a software project.

Project Context:
{context[:8000]}

User Question: {question}

Provide a helpful, detailed answer based on the project files."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except:
            return "Unable to answer the question at this time."
    
    def process_request(self, question: str, files_content: dict, project_dir) -> dict:
        """Process user request and modify files if needed"""
        from pathlib import Path
        
        # Build context
        context = "\n".join([f"--- {name} ---\n{content}" for name, content in list(files_content.items())[:10]])
        
        prompt = f"""You are an AI assistant that modifies project files based on user requests.

Project Files:
{context[:6000]}

User Request: {question}

Analyze the request and respond in JSON format:
{{
  "action": "modify" or "answer",
  "files_to_modify": ["file1.md", "file2.py"],
  "modifications": {{
    "file1.md": "new content here",
    "file2.py": "new code here"
  }},
  "answer": "explanation of what was done"
}}

If the request requires modifying files, provide the complete new content for each file."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=4000
            )
            
            import json
            result_text = response.choices[0].message.content
            
            # Extract JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0]
            
            result = json.loads(result_text.strip())
            
            # Modify files if needed
            modified_files = []
            if result.get("action") == "modify" and result.get("modifications"):
                for filename, new_content in result["modifications"].items():
                    file_path = project_dir / filename
                    try:
                        file_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        modified_files.append(filename)
                    except Exception as e:
                        print(f"Error modifying {filename}: {e}")
            
            return {
                "answer": result.get("answer", "Modifications effectuées"),
                "modified_files": modified_files
            }
        except Exception as e:
            print(f"AI processing error: {e}")
            return {"answer": "Unable to process request", "modified_files": []}
