"""
Test du système de heartbeat SSE pour analyses longues
"""
import requests
import time

BACKEND_URL = "http://localhost:8000"
# BACKEND_URL = "https://autodev-backend-54jo.onrender.com"

def test_sse_heartbeat():
    """Test que le heartbeat garde la connexion active"""
    print("🧪 Test SSE Heartbeat")
    print("=" * 50)
    
    # Créer un job de test
    response = requests.post(
        f"{BACKEND_URL}/api/v1/generation/job",
        json={"project_id": "test", "input_files": []},
        headers={"Authorization": "Bearer test-token"}
    )
    
    if response.status_code != 200:
        print("❌ Impossible de créer le job")
        return
    
    job_id = response.json()["id"]
    print(f"✅ Job créé: {job_id}")
    
    # Tester le streaming SSE
    print("\n📡 Connexion SSE...")
    start_time = time.time()
    last_data = start_time
    heartbeat_count = 0
    data_count = 0
    
    try:
        with requests.get(
            f"{BACKEND_URL}/api/v1/generation/analyze-stream/{job_id}",
            stream=True,
            timeout=600
        ) as r:
            for line in r.iter_lines(decode_unicode=True):
                if not line:
                    continue
                
                elapsed = time.time() - start_time
                since_last = time.time() - last_data
                
                if line.startswith(": heartbeat"):
                    heartbeat_count += 1
                    print(f"💓 Heartbeat #{heartbeat_count} (t={elapsed:.1f}s, Δ={since_last:.1f}s)")
                elif line.startswith("data:"):
                    data_count += 1
                    if data_count <= 5 or data_count % 100 == 0:
                        print(f"📦 Data #{data_count} (t={elapsed:.1f}s)")
                
                last_data = time.time()
                
                # Arrêter après 60 secondes de test
                if elapsed > 60:
                    print("\n⏱️ Test de 60s terminé")
                    break
    
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT - Le heartbeat n'a pas fonctionné!")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    total_time = time.time() - start_time
    print("\n" + "=" * 50)
    print(f"✅ Test réussi!")
    print(f"⏱️  Durée: {total_time:.1f}s")
    print(f"💓 Heartbeats: {heartbeat_count}")
    print(f"📦 Data chunks: {data_count}")
    print(f"📊 Moyenne heartbeat: {total_time/max(heartbeat_count, 1):.1f}s")
    
    if heartbeat_count == 0:
        print("⚠️  ATTENTION: Aucun heartbeat reçu!")
        return False
    
    if heartbeat_count < 3:
        print("⚠️  ATTENTION: Peu de heartbeats (< 3)")
        return False
    
    return True

def test_frontend_proxy():
    """Test le proxy frontend"""
    print("\n🧪 Test Frontend Proxy")
    print("=" * 50)
    
    FRONTEND_URL = "http://localhost:5000"
    # FRONTEND_URL = "https://autodev-frontend.onrender.com"
    
    try:
        response = requests.get(
            f"{FRONTEND_URL}/api/generation/jobs",
            timeout=10
        )
        print(f"✅ Proxy fonctionne: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Proxy erreur: {e}")
        return False

if __name__ == "__main__":
    print("🚀 AutoDev - Test Timeout & Heartbeat")
    print("=" * 50)
    print()
    
    # Test 1: SSE Heartbeat
    sse_ok = test_sse_heartbeat()
    
    # Test 2: Frontend Proxy
    proxy_ok = test_frontend_proxy()
    
    print("\n" + "=" * 50)
    print("📊 RÉSULTATS")
    print("=" * 50)
    print(f"SSE Heartbeat: {'✅ OK' if sse_ok else '❌ FAIL'}")
    print(f"Frontend Proxy: {'✅ OK' if proxy_ok else '❌ FAIL'}")
    
    if sse_ok and proxy_ok:
        print("\n🎉 Tous les tests passent!")
        print("✅ Prêt pour déploiement Render")
    else:
        print("\n⚠️  Certains tests ont échoué")
        print("Vérifiez les logs ci-dessus")
