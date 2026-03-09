import os
import requests
from dotenv import load_dotenv

# 1. Configuration initiale
load_dotenv()
API_KEY = os.getenv("GOOGLE_PAGESPEED_API_KEY")

class AuditService:
    """Classe pour gérer les audits techniques."""
    
    def __init__(self, key):
        self.key = key
        self.endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

    def get_performance_score(self, url):
        """Récupère le score mobile (le plus important pour le e-commerce)."""
        params = {
            "url": url,
            "key": self.key,
            "strategy": "mobile"
        }
        try:
            r = requests.get(self.endpoint, params=params, timeout=30)
            r.raise_for_status()
            data = r.json()
            # Score converti en entier (0-100)
            score = data['lighthouseResult']['categories']['performance']['score'] * 100
            return int(score)
        except Exception as e:
            print(f"[-] Erreur sur {url}: {e}")
            return None

def main():
    if not API_KEY:
        print("[-] ERREUR : La clé API manque dans le fichier .env")
        return

    audit = AuditService(API_KEY)
    
    # Liste de prospects (tu peux en ajouter 50 ici)
    prospects = ["https://www.google.fr"] 

    print("--- DEBUT DE L'AUDIT ---")
    for site in prospects:
        score = audit.get_performance_score(site)
        if score is not None:
            status = "🔴 CRITIQUE" if score < 50 else "🟡 MOYEN" if score < 90 else "🟢 OK"
            print(f"Site: {site} | Score: {score}/100 | Statut: {status}")

if __name__ == "__main__":
    main()