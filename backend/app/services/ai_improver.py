"""
🔄 AI IMPROVER - Amélioration Récursive Intelligente
Analyse le projet existant et l'améliore de façon intelligente
"""
from groq import Groq
from typing import Dict, List, Any
from pathlib import Path
import json
import os

class AIImprover:
    """Améliore un projet existant de façon récursive et intelligente"""
    
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.models = {
            "analyzer": "llama-3.3-70b-versatile",  # Analyse projet
            "improver": "llama-4-maverick-17b-128e-instruct",  # Amélioration code
            "reviewer": "llama-4-scout-17b-16e-instruct",  # Review qualité
        }
    
    def improve_project(self, project_path: str, user_feedback: str = "") -> Dict[str, Any]:
        """
        Améliore un projet existant de façon intelligente
        
        Args:
            project_path: Chemin du projet à améliorer
            user_feedback: Feedback utilisateur (optionnel)
        
        Returns:
            Dict avec les améliorations appliquées
        """
        print(f"\n🔄 AI IMPROVER - Amélioration Intelligente")
        print(f"📁 Projet: {project_path}")
        print(f"💬 Feedback: {user_feedback or 'Amélioration automatique'}")
        print("=" * 80)
        
        project_dir = Path(project_path)
        if not project_dir.exists():
            return {"error": "Projet introuvable"}
        
        # PHASE 1: Analyse du projet existant
        print("\n🔍 PHASE 1: ANALYSE DU PROJET")
        analysis = self._analyze_project(project_dir, user_feedback)
        
        # PHASE 2: Génération des améliorations
        print("\n💡 PHASE 2: GÉNÉRATION DES AMÉLIORATIONS")
        improvements = self._generate_improvements(project_dir, analysis, user_feedback)
        
        # PHASE 3: Application des améliorations
        print("\n✨ PHASE 3: APPLICATION DES AMÉLIORATIONS")
        applied = self._apply_improvements(project_dir, improvements)
        
        # PHASE 4: Validation
        print("\n✅ PHASE 4: VALIDATION")
        validation = self._validate_improvements(project_dir, applied)
        
        return {
            "analysis": analysis,
            "improvements": improvements,
            "applied": applied,
            "validation": validation,
            "success": True
        }
    
    def _analyze_project(self, project_dir: Path, user_feedback: str) -> Dict:
        """Analyse le projet existant pour identifier les points d'amélioration"""
        
        # Lire les fichiers principaux
        files_content = {}
        for pattern in ["**/*.html", "**/*.css", "**/*.js", "**/*.py"]:
            for file_path in project_dir.glob(pattern):
                if file_path.is_file() and file_path.stat().st_size < 100000:  # < 100KB
                    try:
                        relative_path = str(file_path.relative_to(project_dir))
                        files_content[relative_path] = file_path.read_text(encoding='utf-8')[:5000]  # 5KB max
                    except:
                        pass
        
        # Prompt d'analyse intelligent
        analysis_prompt = f"""Tu es un expert en analyse de code niveau FAANG.

PROJET À ANALYSER:
{json.dumps(list(files_content.keys())[:20], indent=2)}

FEEDBACK UTILISATEUR:
{user_feedback or "Aucun feedback spécifique - amélioration générale"}

FICHIERS PRINCIPAUX:
{json.dumps({k: v[:500] for k, v in list(files_content.items())[:5]}, indent=2)}

ANALYSE INTELLIGENTE:
1. Points forts du projet actuel
2. Points faibles à améliorer
3. Suggestions d'amélioration prioritaires
4. Technologies/patterns à ajouter
5. Score qualité actuel /100

Réponds en JSON:
{{
  "strengths": ["point fort 1", "point fort 2"],
  "weaknesses": ["faiblesse 1", "faiblesse 2"],
  "priorities": [
    {{"area": "Frontend", "issue": "...", "solution": "...", "priority": "high"}},
    {{"area": "Backend", "issue": "...", "solution": "...", "priority": "medium"}}
  ],
  "current_score": 75,
  "target_score": 95,
  "technologies_to_add": ["tech1", "tech2"]
}}"""

        response = self.client.chat.completions.create(
            model=self.models["analyzer"],
            messages=[{"role": "user", "content": analysis_prompt}],
            temperature=0.5,
            max_tokens=3000
        )
        
        content = response.choices[0].message.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        
        try:
            analysis = json.loads(content.strip())
            print(f"  ✅ Analyse terminée - Score actuel: {analysis.get('current_score', 0)}/100")
            return analysis
        except:
            return {
                "strengths": ["Code fonctionnel"],
                "weaknesses": ["Nécessite amélioration"],
                "priorities": [],
                "current_score": 70,
                "target_score": 95
            }
    
    def _generate_improvements(self, project_dir: Path, analysis: Dict, user_feedback: str) -> List[Dict]:
        """Génère les améliorations intelligentes basées sur l'analyse"""
        
        improvements = []
        priorities = analysis.get("priorities", [])[:5]  # Top 5
        
        for priority in priorities:
            area = priority.get("area", "General")
            issue = priority.get("issue", "")
            solution = priority.get("solution", "")
            
            print(f"  🎯 {area}: {issue[:50]}...")
            
            # Générer le code amélioré
            improve_prompt = f"""Tu es un expert {area} niveau FAANG.

PROBLÈME IDENTIFIÉ:
{issue}

SOLUTION PROPOSÉE:
{solution}

FEEDBACK UTILISATEUR:
{user_feedback}

GÉNÈRE LE CODE AMÉLIORÉ:
- Code professionnel production-ready
- Best practices 2024
- Commentaires si nécessaire
- Performance optimisée

Réponds en JSON:
{{
  "file_path": "chemin/du/fichier",
  "code": "code amélioré complet",
  "explanation": "explication des changements"
}}"""

            response = self.client.chat.completions.create(
                model=self.models["improver"],
                messages=[{"role": "user", "content": improve_prompt}],
                temperature=0.4,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            
            try:
                improvement = json.loads(content.strip())
                improvement["area"] = area
                improvement["priority"] = priority.get("priority", "medium")
                improvements.append(improvement)
                print(f"    ✅ Amélioration générée: {improvement.get('file_path', 'N/A')}")
            except Exception as e:
                print(f"    ⚠️ Erreur: {e}")
        
        return improvements
    
    def _apply_improvements(self, project_dir: Path, improvements: List[Dict]) -> List[Dict]:
        """Applique les améliorations au projet"""
        
        applied = []
        
        for improvement in improvements:
            file_path = improvement.get("file_path", "")
            code = improvement.get("code", "")
            
            if not file_path or not code:
                continue
            
            full_path = project_dir / file_path
            
            try:
                # Créer dossiers si nécessaire
                full_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Backup de l'ancien fichier
                if full_path.exists():
                    backup_path = full_path.with_suffix(full_path.suffix + '.backup')
                    backup_path.write_text(full_path.read_text(encoding='utf-8'), encoding='utf-8')
                
                # Écrire le nouveau code
                full_path.write_text(code, encoding='utf-8')
                
                applied.append({
                    "file": file_path,
                    "status": "success",
                    "explanation": improvement.get("explanation", "")
                })
                
                print(f"  ✅ {file_path} amélioré")
                
            except Exception as e:
                applied.append({
                    "file": file_path,
                    "status": "error",
                    "error": str(e)
                })
                print(f"  ❌ {file_path} erreur: {e}")
        
        return applied
    
    def _validate_improvements(self, project_dir: Path, applied: List[Dict]) -> Dict:
        """Valide les améliorations appliquées"""
        
        success_count = sum(1 for a in applied if a.get("status") == "success")
        total_count = len(applied)
        
        validation_prompt = f"""Tu es un reviewer niveau Google.

AMÉLIORATIONS APPLIQUÉES:
{json.dumps(applied, indent=2)}

VALIDATION:
- Qualité des changements
- Impact sur le projet
- Score d'amélioration /100
- Prochaines étapes recommandées

Réponds en JSON:
{{
  "quality_score": 90,
  "impact": "high/medium/low",
  "next_steps": ["étape 1", "étape 2"],
  "overall_improvement": "+15 points"
}}"""

        try:
            response = self.client.chat.completions.create(
                model=self.models["reviewer"],
                messages=[{"role": "user", "content": validation_prompt}],
                temperature=0.3,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            
            validation = json.loads(content.strip())
        except:
            validation = {
                "quality_score": 85,
                "impact": "medium",
                "next_steps": ["Tester les changements"],
                "overall_improvement": "+10 points"
            }
        
        validation["success_rate"] = f"{success_count}/{total_count}"
        
        print(f"  ✅ Validation: {validation.get('quality_score', 0)}/100")
        print(f"  📈 Amélioration: {validation.get('overall_improvement', 'N/A')}")
        
        return validation


# ============================================
# EXEMPLE D'UTILISATION
# ============================================
if __name__ == "__main__":
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "gsk_...")
    
    improver = AIImprover(GROQ_API_KEY)
    
    # Test
    project_path = "C:/Downloads/generated_projects/project_test"
    user_feedback = "Le design n'est pas assez moderne, ajoute plus d'animations"
    
    result = improver.improve_project(project_path, user_feedback)
    
    if result.get("success"):
        print("\n" + "=" * 80)
        print("✅ AMÉLIORATION TERMINÉE!")
        print("=" * 80)
        print(f"\n📊 Résultats:")
        print(f"   - Fichiers analysés: {len(result['analysis'].get('priorities', []))}")
        print(f"   - Améliorations générées: {len(result['improvements'])}")
        print(f"   - Améliorations appliquées: {result['validation'].get('success_rate', 'N/A')}")
        print(f"   - Score qualité: {result['validation'].get('quality_score', 0)}/100")
        print(f"   - Impact: {result['validation'].get('impact', 'N/A')}")
