from typing import Dict
from .ai_service import AIService

class AIAssistant:
    def __init__(self):
        self.ai_service = AIService()
        self.client = self.ai_service.client
        self.model = self.ai_service.analysis_model
    
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
        import json
        import base64
        
        print(f"[AI-ASSISTANT] Processing request with {len(files_content)} files")
        
        # Get most relevant files
        relevant_files = {}
        for name, content in files_content.items():
            if 'index' in name.lower() or 'template' in name or name.endswith('.html'):
                relevant_files[name] = content
        
        if not relevant_files:
            relevant_files = dict(list(files_content.items())[:3])
        
        file_list = "\n".join([f"- {name}" for name in files_content.keys()])
        context = "\n\n".join([f"=== {name} ===\n{content}" for name, content in relevant_files.items()])
        
        prompt = f"""You are modifying a Flask web application.

AVAILABLE FILES:
{file_list}

CURRENT CONTENT OF RELEVANT FILES:
{context[:10000]}

User Request: {question}

IMPORTANT:
- Find the EXACT file path from the list
- Read its current content above
- Make ONLY the requested change
- Keep ALL existing structure
- Use Flask routes: href=\"/students\" NOT href=\"students.html\"

Respond with this EXACT format (use <<<CONTENT>>> and <<<END>>> as delimiters):
{{
  \"file\": \"exact/file/path.html\",
  \"content\": \"<<<CONTENT>>>\nPUT COMPLETE FILE CONTENT HERE\n<<<END>>>\",
  \"answer\": \"Modified [file] to [change]\"
}}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=8000
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Extract JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0]
            
            # Extract content between delimiters
            if "<<<CONTENT>>>" in result_text and "<<<END>>>" in result_text:
                content_start = result_text.find("<<<CONTENT>>>") + len("<<<CONTENT>>>")
                content_end = result_text.find("<<<END>>>")
                file_content = result_text[content_start:content_end].strip()
                
                # Extract file path and answer
                file_match = result_text.split('"file"')[1].split('"')[1]
                answer_match = result_text.split('"answer"')[1].split('"')[1] if '"answer"' in result_text else "Modified"
                
                result = {
                    "file": file_match,
                    "content": file_content,
                    "answer": answer_match
                }
            else:
                # Fallback: try normal JSON
                result = json.loads(result_text.strip())
            
            modified_files = []
            
            # Handle both formats
            if "file" in result and "content" in result:
                filename = result["file"]
                new_content = result["content"]
                
                # Find exact file
                actual_path = None
                if filename in files_content:
                    actual_path = project_dir / filename
                else:
                    for existing_file in files_content.keys():
                        if existing_file.endswith(filename):
                            actual_path = project_dir / existing_file
                            break
                
                if actual_path:
                    try:
                        with open(actual_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        modified_files.append(str(actual_path.relative_to(project_dir)))
                        print(f"[AI-ASSISTANT] ✓ Modified {actual_path.relative_to(project_dir)}")
                    except Exception as e:
                        print(f"[AI-ASSISTANT] ✗ Error: {e}")
                else:
                    print(f"[AI-ASSISTANT] ✗ File not found: {filename}")
            
            return {
                "answer": result.get("answer", "Modifications effectuées"),
                "modified_files": modified_files
            }
        except Exception as e:
            print(f"[AI-ASSISTANT] Error: {e}")
            import traceback
            traceback.print_exc()
            return {"answer": f"Erreur: {str(e)}", "modified_files": []}
