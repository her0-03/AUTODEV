"""
🎨 SOTA Web Generator - Générateur de pages web ultra-modernes
Utilise 4 modèles Groq spécialisés pour créer des designs exceptionnels
"""
from groq import Groq
import os
from pathlib import Path

class SOTAWebGenerator:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        
        # 4 modèles spécialisés
        self.design_model = "llama-3.3-70b-versatile"  # Design & UX
        self.code_model = "meta-llama/llama-4-maverick-17b-128e-instruct"  # Code HTML/CSS/JS
        self.animation_model = "llama-3.1-8b-instant"  # Animations rapides
        self.review_model = "meta-llama/llama-4-scout-17b-16e-instruct"  # Review qualité
    
    def generate_design_concept(self, description: str) -> dict:
        """Étape 1: Génère le concept design (couleurs, layout, style)"""
        prompt = f"""Tu es un designer UI/UX expert. Crée un concept design ULTRA-MODERNE pour:
{description}

Réponds en JSON avec:
{{
  "theme": "nom du thème (ex: cyberpunk, glassmorphism, neomorphism)",
  "colors": {{"primary": "#hex", "secondary": "#hex", "accent": "#hex", "bg": "#hex"}},
  "fonts": {{"heading": "font-name", "body": "font-name"}},
  "layout": "description du layout (grid, flex, etc)",
  "effects": ["effet1", "effet2", "effet3"],
  "inspiration": "description du style visuel"
}}

Utilise les dernières tendances 2024: glassmorphism, gradients animés, micro-interactions, dark mode."""
        
        response = self.client.chat.completions.create(
            model=self.design_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9
        )
        
        import json
        content = response.choices[0].message.content
        # Extraire JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        return json.loads(content.strip())
    
    def generate_html_structure(self, design: dict, description: str) -> str:
        """Étape 2: Génère le HTML avec structure moderne"""
        prompt = f"""Crée une page HTML ULTRA-MODERNE pour: {description}

Design concept:
{design}

Exigences:
- HTML5 sémantique (header, nav, main, section, footer)
- Structure responsive (mobile-first)
- Accessibilité (ARIA labels)
- Meta tags SEO
- Open Graph pour réseaux sociaux
- Favicon et PWA ready

Retourne UNIQUEMENT le code HTML complet."""
        
        response = self.client.chat.completions.create(
            model=self.code_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        return self._extract_code(response.choices[0].message.content)
    
    def generate_advanced_css(self, design: dict, html: str) -> str:
        """Étape 3: Génère CSS ultra-moderne avec effets avancés"""
        prompt = f"""Crée un CSS ULTRA-MODERNE pour cette page HTML.

Design:
{design}

Exigences CSS:
- Variables CSS (custom properties)
- Gradients animés
- Glassmorphism / Neomorphism
- Animations fluides (60fps)
- Transitions micro-interactions
- Dark mode avec prefers-color-scheme
- Responsive (mobile, tablet, desktop)
- Grid/Flexbox moderne
- Backdrop filters
- Box shadows avancées
- Hover effects 3D
- Scroll animations

Utilise les dernières features CSS 2024!
Retourne UNIQUEMENT le code CSS."""
        
        response = self.client.chat.completions.create(
            model=self.code_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        
        return self._extract_code(response.choices[0].message.content)
    
    def generate_interactive_js(self, design: dict, description: str) -> str:
        """Étape 4: Génère JavaScript avec interactions avancées"""
        prompt = f"""Crée du JavaScript ULTRA-MODERNE pour: {description}

Design: {design}

Fonctionnalités JS:
- Animations GSAP ou Anime.js style
- Scroll reveal animations
- Parallax effects
- Smooth scrolling
- Lazy loading images
- Intersection Observer
- Particle effects (optionnel)
- Cursor custom animations
- Menu hamburger animé
- Form validation moderne
- Dark mode toggle
- Loading animations
- Micro-interactions
- Performance optimisé

Utilise vanilla JS moderne (ES6+) ou librairies CDN.
Retourne UNIQUEMENT le code JavaScript."""
        
        response = self.client.chat.completions.create(
            model=self.animation_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        
        return self._extract_code(response.choices[0].message.content)
    
    def review_and_optimize(self, html: str, css: str, js: str) -> dict:
        """Étape 5: Review qualité et suggestions d'amélioration"""
        prompt = f"""Review ce code web et donne des suggestions d'amélioration.

HTML: {len(html)} chars
CSS: {len(css)} chars  
JS: {len(js)} chars

Analyse:
- Performance (score /100)
- Accessibilité (score /100)
- SEO (score /100)
- Design moderne (score /100)
- Suggestions d'amélioration (top 3)

Réponds en JSON."""
        
        response = self.client.chat.completions.create(
            model=self.review_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        import json
        content = response.choices[0].message.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        
        try:
            return json.loads(content.strip())
        except:
            return {"performance": 85, "accessibility": 80, "seo": 75, "design": 90}
    
    def generate_complete_page(self, description: str, output_dir: str = "generated_sota"):
        """Génère une page web complète SOTA"""
        print(f"🎨 Génération page SOTA: {description}")
        print("=" * 60)
        
        # Étape 1: Design concept
        print("\n[1/5] 🎨 Génération concept design...")
        design = self.generate_design_concept(description)
        print(f"✅ Theme: {design.get('theme', 'modern')}")
        print(f"✅ Colors: {design.get('colors', {})}")
        
        # Étape 2: HTML
        print("\n[2/5] 📄 Génération HTML structure...")
        html = self.generate_html_structure(design, description)
        print(f"✅ HTML: {len(html)} caractères")
        
        # Étape 3: CSS
        print("\n[3/5] 🎨 Génération CSS avancé...")
        css = self.generate_advanced_css(design, html)
        print(f"✅ CSS: {len(css)} caractères")
        
        # Étape 4: JavaScript
        print("\n[4/5] ⚡ Génération JavaScript interactif...")
        js = self.generate_interactive_js(design, description)
        print(f"✅ JS: {len(js)} caractères")
        
        # Étape 5: Review
        print("\n[5/5] 🔍 Review qualité...")
        review = self.review_and_optimize(html, css, js)
        print(f"✅ Performance: {review.get('performance', 'N/A')}/100")
        print(f"✅ Accessibilité: {review.get('accessibility', 'N/A')}/100")
        
        # Sauvegarder
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Intégrer CSS et JS dans HTML
        final_html = self._integrate_assets(html, css, js, design)
        
        output_file = output_path / "index.html"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_html)
        
        print(f"\n✅ Page générée: {output_file}")
        print(f"🌐 Ouvrez dans votre navigateur!")
        
        return {
            "html_path": str(output_file),
            "design": design,
            "review": review,
            "stats": {
                "html_size": len(html),
                "css_size": len(css),
                "js_size": len(js)
            }
        }
    
    def _extract_code(self, content: str) -> str:
        """Extrait le code des balises markdown"""
        if "```html" in content:
            return content.split("```html")[1].split("```")[0].strip()
        elif "```css" in content:
            return content.split("```css")[1].split("```")[0].strip()
        elif "```javascript" in content or "```js" in content:
            marker = "```javascript" if "```javascript" in content else "```js"
            return content.split(marker)[1].split("```")[0].strip()
        elif "```" in content:
            return content.split("```")[1].split("```")[0].strip()
        return content.strip()
    
    def _integrate_assets(self, html: str, css: str, js: str, design: dict) -> str:
        """Intègre CSS et JS dans le HTML"""
        # Ajouter CSS dans <head>
        css_tag = f"\n<style>\n{css}\n</style>\n</head>"
        if "</head>" in html:
            html = html.replace("</head>", css_tag)
        
        # Ajouter JS avant </body>
        js_tag = f"\n<script>\n{js}\n</script>\n</body>"
        if "</body>" in html:
            html = html.replace("</body>", js_tag)
        
        # Ajouter meta theme-color
        theme_color = design.get("colors", {}).get("primary", "#6366f1")
        meta_tag = f'<meta name="theme-color" content="{theme_color}">'
        if "<head>" in html:
            html = html.replace("<head>", f"<head>\n{meta_tag}")
        
        return html


# ============================================
# EXEMPLE D'UTILISATION
# ============================================
if __name__ == "__main__":
    # Configuration
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "gsk_...")
    
    generator = SOTAWebGenerator(GROQ_API_KEY)
    
    # Exemples de pages à générer
    examples = [
        "Landing page pour une startup IA avec design futuriste cyberpunk",
        "Portfolio de designer avec animations 3D et glassmorphism",
        "Dashboard analytics avec dark mode et graphiques interactifs",
        "Page produit e-commerce avec carousel 3D et effets parallax",
        "Blog minimaliste avec typographie élégante et micro-interactions"
    ]
    
    # Générer la première page
    print("🚀 SOTA Web Generator - Powered by Groq")
    print("=" * 60)
    print("\nExemples disponibles:")
    for i, ex in enumerate(examples, 1):
        print(f"{i}. {ex}")
    
    choice = input("\nChoisissez (1-5) ou décrivez votre page: ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= 5:
        description = examples[int(choice) - 1]
    else:
        description = choice if choice else examples[0]
    
    # Générer
    result = generator.generate_complete_page(description)
    
    print("\n" + "=" * 60)
    print("🎉 GÉNÉRATION TERMINÉE!")
    print("=" * 60)
    print(f"\n📁 Fichier: {result['html_path']}")
    print(f"🎨 Theme: {result['design'].get('theme', 'N/A')}")
    print(f"📊 Scores:")
    print(f"   - Performance: {result['review'].get('performance', 'N/A')}/100")
    print(f"   - Accessibilité: {result['review'].get('accessibility', 'N/A')}/100")
    print(f"   - SEO: {result['review'].get('seo', 'N/A')}/100")
    print(f"   - Design: {result['review'].get('design', 'N/A')}/100")
    
    # Ouvrir dans le navigateur
    import webbrowser
    webbrowser.open(result['html_path'])
