"""
Test de génération SOTA - Pages web ultra-modernes
"""
import sys
sys.path.append('backend')

from app.services.code_generator import CodeGenerator
from pathlib import Path
import json

# Spec de test pour une landing page moderne
test_spec = {
    "appConfig": {
        "name": "TechStartup AI",
        "description": "Plateforme IA révolutionnaire",
        "theme": "glassmorphism"
    },
    "database": {
        "entities": [
            {
                "name": "User",
                "columns": [
                    {"name": "email", "type": "string", "required": True, "unique": True},
                    {"name": "name", "type": "string", "required": True}
                ]
            }
        ]
    },
    "api": {
        "endpoints": [
            {"method": "GET", "path": "/api/users", "description": "Get all users"},
            {"method": "POST", "path": "/api/users", "description": "Create user"}
        ]
    },
    "ui": {
        "pages": [
            {
                "route": "/",
                "title": "Welcome to the Future",
                "components": ["Hero Section", "Features Grid", "Testimonials", "CTA Form"]
            },
            {
                "route": "/dashboard",
                "title": "Analytics Dashboard",
                "components": ["Stats Cards", "Charts", "Activity Feed", "User Table"]
            },
            {
                "route": "/products",
                "title": "Our Products",
                "components": ["Product Grid", "Filters", "Shopping Cart"]
            }
        ]
    }
}

def test_sota_generation():
    print("🎨 Test Génération SOTA")
    print("=" * 60)
    
    # Créer générateur
    output_dir = "C:/Downloads/generated_projects"
    generator = CodeGenerator(output_dir)
    
    print("\n[1/3] Génération du projet...")
    try:
        zip_path = generator.generate_project(test_spec, "test_sota_app")
        print(f"✅ Projet généré: {zip_path}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    # Vérifier les fichiers générés
    print("\n[2/3] Vérification des fichiers...")
    project_path = Path(output_dir) / "test_sota_app"
    
    checks = {
        "Frontend templates": project_path / "frontend" / "templates",
        "Backend models": project_path / "backend" / "models.py",
        "Backend API": project_path / "backend" / "main.py",
        "Docker Compose": project_path / "docker-compose.yml",
        "README": project_path / "README.md",
        "Render config": project_path / "render.yaml"
    }
    
    all_ok = True
    for name, path in checks.items():
        if path.exists():
            print(f"✅ {name}: OK")
        else:
            print(f"❌ {name}: MANQUANT")
            all_ok = False
    
    # Analyser une page HTML
    print("\n[3/3] Analyse d'une page SOTA...")
    templates_dir = project_path / "frontend" / "templates"
    if templates_dir.exists():
        html_files = list(templates_dir.glob("*.html"))
        if html_files:
            sample_html = html_files[0].read_text()
            
            # Vérifier features SOTA
            sota_features = {
                "Glassmorphism": "backdrop-filter" in sample_html or "glass" in sample_html,
                "Gradients animés": "gradient" in sample_html,
                "Animations": "animate" in sample_html or "@keyframes" in sample_html,
                "Responsive": "md:" in sample_html or "lg:" in sample_html,
                "Dark mode": "dark" in sample_html.lower(),
                "JavaScript interactif": "<script>" in sample_html,
                "Meta tags SEO": "og:title" in sample_html or "description" in sample_html
            }
            
            print(f"\n📄 Analyse de {html_files[0].name}:")
            print(f"   Taille: {len(sample_html)} caractères")
            print("\n   Features SOTA détectées:")
            for feature, present in sota_features.items():
                status = "✅" if present else "❌"
                print(f"   {status} {feature}")
            
            sota_score = sum(sota_features.values()) / len(sota_features) * 100
            print(f"\n   Score SOTA: {sota_score:.0f}%")
            
            if sota_score >= 70:
                print("   🎉 Page ULTRA-MODERNE!")
            elif sota_score >= 50:
                print("   ✅ Page moderne")
            else:
                print("   ⚠️  Page basique")
    
    print("\n" + "=" * 60)
    if all_ok:
        print("✅ TOUS LES TESTS PASSENT!")
        print(f"\n📁 Projet: {project_path}")
        print(f"📦 ZIP: {zip_path}")
        print("\n🚀 Pour tester:")
        print(f"   cd {project_path}")
        print("   docker-compose up")
        return True
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        return False

if __name__ == "__main__":
    success = test_sota_generation()
    sys.exit(0 if success else 1)
