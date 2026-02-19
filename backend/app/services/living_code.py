"""
🔄 LIVING CODE - Code Vivant Auto-Réparateur
Le code s'auto-répare, s'auto-optimise, et évolue en production
"""
from groq import Groq
from typing import Dict, List, Any, Optional
import json
import time
from dataclasses import dataclass, field
from datetime import datetime
import hashlib

@dataclass
class CodeHealth:
    """Santé du code en temps réel"""
    errors: List[Dict] = field(default_factory=list)
    warnings: List[Dict] = field(default_factory=list)
    performance_issues: List[Dict] = field(default_factory=list)
    security_issues: List[Dict] = field(default_factory=list)
    health_score: float = 100.0
    last_check: datetime = field(default_factory=datetime.now)

@dataclass
class AutoFix:
    """Correction automatique appliquée"""
    id: str
    issue_type: str
    original_code: str
    fixed_code: str
    confidence: float
    applied_at: datetime
    success: bool = False

class LivingCode:
    """
    🔄 LIVING CODE - Architecture Auto-Réparatrice
    
    Features:
    1. Auto-Repair: Détecte et corrige les bugs automatiquement
    2. Auto-Optimize: Optimise les performances en continu
    3. Self-Healing: Se répare sans intervention humaine
    4. Adaptive Learning: Apprend des erreurs passées
    """
    
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.health_history: List[CodeHealth] = []
        self.fixes_applied: List[AutoFix] = []
        self.learning_memory: Dict[str, Any] = {}
    
    async def monitor_health(self, code: Dict[str, str]) -> CodeHealth:
        """
        🏥 Monitore la santé du code en temps réel
        """
        print("\n🏥 LIVING CODE - Health Check")
        
        health = CodeHealth()
        
        # Analyse syntaxique
        syntax_issues = self._check_syntax(code)
        health.errors.extend(syntax_issues)
        
        # Analyse performance
        perf_issues = await self._check_performance(code)
        health.performance_issues.extend(perf_issues)
        
        # Analyse sécurité
        security_issues = await self._check_security(code)
        health.security_issues.extend(security_issues)
        
        # Calcul score santé
        health.health_score = self._calculate_health_score(health)
        
        self.health_history.append(health)
        
        print(f"  📊 Score santé: {health.health_score:.1f}/100")
        print(f"  ❌ Erreurs: {len(health.errors)}")
        print(f"  ⚠️  Warnings: {len(health.warnings)}")
        print(f"  ⚡ Performance: {len(health.performance_issues)}")
        print(f"  🔒 Sécurité: {len(health.security_issues)}")
        
        return health
    
    async def auto_repair(self, code: Dict[str, str], health: CodeHealth) -> Dict[str, str]:
        """
        🔧 Auto-réparation: Corrige automatiquement les problèmes
        """
        print("\n🔧 LIVING CODE - Auto-Repair")
        
        repaired_code = code.copy()
        fixes_count = 0
        
        # Réparer les erreurs critiques
        for error in health.errors[:5]:  # Top 5 erreurs
            fix = await self._generate_fix(repaired_code, error, "error")
            if fix and fix.confidence >= 0.8:
                repaired_code = self._apply_fix(repaired_code, fix)
                self.fixes_applied.append(fix)
                fixes_count += 1
                print(f"  ✅ Erreur corrigée: {error.get('type', 'unknown')}")
        
        # Optimiser les performances
        for perf_issue in health.performance_issues[:3]:  # Top 3
            fix = await self._generate_fix(repaired_code, perf_issue, "performance")
            if fix and fix.confidence >= 0.7:
                repaired_code = self._apply_fix(repaired_code, fix)
                self.fixes_applied.append(fix)
                fixes_count += 1
                print(f"  ⚡ Performance optimisée: {perf_issue.get('type', 'unknown')}")
        
        # Corriger les failles de sécurité
        for sec_issue in health.security_issues[:3]:  # Top 3
            fix = await self._generate_fix(repaired_code, sec_issue, "security")
            if fix and fix.confidence >= 0.9:  # Haute confiance pour sécurité
                repaired_code = self._apply_fix(repaired_code, fix)
                self.fixes_applied.append(fix)
                fixes_count += 1
                print(f"  🔒 Sécurité renforcée: {sec_issue.get('type', 'unknown')}")
        
        print(f"\n  🎯 Total corrections: {fixes_count}")
        
        # Apprendre des corrections
        self._learn_from_fixes()
        
        return repaired_code
    
    async def continuous_optimization(self, code: Dict[str, str], 
                                     iterations: int = 5) -> Dict[str, str]:
        """
        🔄 Optimisation continue: Améliore le code en boucle
        """
        print(f"\n🔄 LIVING CODE - Continuous Optimization ({iterations} iterations)")
        
        optimized_code = code.copy()
        
        for i in range(iterations):
            print(f"\n  Iteration {i+1}/{iterations}")
            
            # Health check
            health = await self.monitor_health(optimized_code)
            
            # Si santé parfaite, arrêter
            if health.health_score >= 98:
                print(f"  ✅ Santé parfaite atteinte!")
                break
            
            # Auto-réparation
            optimized_code = await self.auto_repair(optimized_code, health)
            
            # Pause courte
            time.sleep(0.5)
        
        # Score final
        final_health = await self.monitor_health(optimized_code)
        print(f"\n  🏆 Score final: {final_health.health_score:.1f}/100")
        
        return optimized_code
    
    def _check_syntax(self, code: Dict[str, str]) -> List[Dict]:
        """Vérifie la syntaxe basique"""
        issues = []
        
        html = code.get("html", "")
        
        # Vérifications HTML
        if html:
            if "<!DOCTYPE" not in html:
                issues.append({"type": "missing_doctype", "severity": "error", "line": 1})
            if "</html>" not in html:
                issues.append({"type": "missing_closing_tag", "severity": "error", "line": -1})
            if "<head>" not in html or "</head>" not in html:
                issues.append({"type": "missing_head", "severity": "warning", "line": -1})
        
        return issues
    
    async def _check_performance(self, code: Dict[str, str]) -> List[Dict]:
        """Analyse les problèmes de performance"""
        issues = []
        
        html = code.get("html", "")
        
        # Images non optimisées
        if "<img" in html and "loading=" not in html:
            issues.append({
                "type": "missing_lazy_loading",
                "severity": "warning",
                "description": "Images sans lazy loading",
                "fix": "Ajouter loading='lazy' aux images"
            })
        
        # Scripts bloquants
        if "<script src=" in html and "defer" not in html and "async" not in html:
            issues.append({
                "type": "blocking_scripts",
                "severity": "warning",
                "description": "Scripts bloquants",
                "fix": "Ajouter defer ou async"
            })
        
        # CSS inline trop gros
        if "<style>" in html:
            style_content = html.split("<style>")[1].split("</style>")[0] if "</style>" in html else ""
            if len(style_content) > 5000:
                issues.append({
                    "type": "large_inline_css",
                    "severity": "warning",
                    "description": "CSS inline trop volumineux",
                    "fix": "Externaliser le CSS"
                })
        
        return issues
    
    async def _check_security(self, code: Dict[str, str]) -> List[Dict]:
        """Analyse les failles de sécurité"""
        issues = []
        
        html = code.get("html", "")
        
        # Pas de CSP
        if "Content-Security-Policy" not in html:
            issues.append({
                "type": "missing_csp",
                "severity": "high",
                "description": "Pas de Content Security Policy",
                "fix": "Ajouter meta CSP"
            })
        
        # Formulaires sans CSRF
        if "<form" in html and "csrf" not in html.lower():
            issues.append({
                "type": "missing_csrf",
                "severity": "high",
                "description": "Formulaires sans protection CSRF",
                "fix": "Ajouter token CSRF"
            })
        
        # Liens externes sans rel
        if 'href="http' in html and 'rel="noopener' not in html:
            issues.append({
                "type": "unsafe_external_links",
                "severity": "medium",
                "description": "Liens externes non sécurisés",
                "fix": "Ajouter rel='noopener noreferrer'"
            })
        
        return issues
    
    async def _generate_fix(self, code: Dict[str, str], issue: Dict, 
                           issue_category: str) -> Optional[AutoFix]:
        """Génère une correction automatique"""
        
        # Vérifier si on a déjà appris cette correction
        issue_hash = hashlib.md5(json.dumps(issue).encode()).hexdigest()[:8]
        if issue_hash in self.learning_memory:
            learned_fix = self.learning_memory[issue_hash]
            print(f"    💡 Correction apprise réutilisée")
            return learned_fix
        
        # Générer nouvelle correction avec IA
        prompt = f"""Corrige ce problème de code:

Type: {issue.get('type', 'unknown')}
Catégorie: {issue_category}
Description: {issue.get('description', '')}
Fix suggéré: {issue.get('fix', '')}

Code actuel (extrait):
{code.get('html', '')[:500]}...

Retourne UNIQUEMENT le code corrigé, pas d'explications."""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "Tu corriges du code. Retourne UNIQUEMENT le code corrigé."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=2000
            )
            
            fixed_code = response.choices[0].message.content.strip()
            
            fix = AutoFix(
                id=issue_hash,
                issue_type=issue.get('type', 'unknown'),
                original_code=code.get('html', '')[:200],
                fixed_code=fixed_code,
                confidence=0.85,
                applied_at=datetime.now()
            )
            
            return fix
            
        except Exception as e:
            print(f"    ⚠️  Erreur génération fix: {str(e)[:50]}")
            return None
    
    def _apply_fix(self, code: Dict[str, str], fix: AutoFix) -> Dict[str, str]:
        """Applique une correction au code"""
        # Simplification: remplacer le HTML complet
        # TODO: Appliquer des patches ciblés
        fixed_code = code.copy()
        if fix.fixed_code and len(fix.fixed_code) > 100:
            fixed_code["html"] = fix.fixed_code
            fix.success = True
        return fixed_code
    
    def _calculate_health_score(self, health: CodeHealth) -> float:
        """Calcule le score de santé global"""
        score = 100.0
        
        # Pénalités
        score -= len(health.errors) * 10  # -10 par erreur
        score -= len(health.warnings) * 3  # -3 par warning
        score -= len(health.performance_issues) * 5  # -5 par perf issue
        score -= len(health.security_issues) * 8  # -8 par security issue
        
        return max(0, min(100, score))
    
    def _learn_from_fixes(self):
        """Apprend des corrections appliquées"""
        successful_fixes = [f for f in self.fixes_applied if f.success]
        
        for fix in successful_fixes[-10:]:  # 10 dernières
            self.learning_memory[fix.id] = fix
        
        print(f"    🧠 Mémoire: {len(self.learning_memory)} corrections apprises")
    
    def get_stats(self) -> Dict:
        """Statistiques du Living Code"""
        return {
            "health_checks": len(self.health_history),
            "fixes_applied": len(self.fixes_applied),
            "success_rate": sum(1 for f in self.fixes_applied if f.success) / len(self.fixes_applied) if self.fixes_applied else 0,
            "learned_fixes": len(self.learning_memory),
            "current_health": self.health_history[-1].health_score if self.health_history else 0,
            "avg_health": sum(h.health_score for h in self.health_history) / len(self.health_history) if self.health_history else 0
        }


# ============================================
# EXEMPLE D'UTILISATION
# ============================================
if __name__ == "__main__":
    import os
    import asyncio
    
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "gsk_...")
    
    living = LivingCode(GROQ_API_KEY)
    
    print("🔄 LIVING CODE - Code Vivant Auto-Réparateur")
    print("=" * 80)
    
    # Code de test avec problèmes
    test_code = {
        "html": """<html>
<head><title>Test</title></head>
<body>
    <img src="image.jpg">
    <script src="app.js"></script>
    <form action="/submit">
        <input type="text" name="data">
    </form>
    <a href="https://external.com">Link</a>
</body>
</html>""",
        "css": "",
        "js": ""
    }
    
    # Test
    # health = asyncio.run(living.monitor_health(test_code))
    # repaired = asyncio.run(living.auto_repair(test_code, health))
    # optimized = asyncio.run(living.continuous_optimization(test_code, iterations=3))
    
    # stats = living.get_stats()
    # print(f"\n📊 Statistiques:")
    # print(f"  Health checks: {stats['health_checks']}")
    # print(f"  Corrections: {stats['fixes_applied']}")
    # print(f"  Taux succès: {stats['success_rate']:.1%}")
    # print(f"  Santé actuelle: {stats['current_health']:.1f}/100")
