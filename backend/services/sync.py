from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from services.scraper import trigger_scrape_if_needed

# Termos genéricos que cobrem as vagas de interesse dos nossos usuários
GLOBAL_JOB_TERMS = [
    "desenvolvedor",
    "software developer",
    "programador",
    "backend",
    "frontend",
    "fullstack",
    "engenheiro de software",
    "dados",
    "estágio ti"
]

def sync_all_global_terms(db: Session, background_tasks: BackgroundTasks):
    results = []
    
    for term in GLOBAL_JOB_TERMS:
        # A própria função trigger_scrape_if_needed cuidará do cache (6 horas)
        # e da similaridade (ex: "software developer" e "desenvolvedor de software")
        result = trigger_scrape_if_needed(db, term, background_tasks)
        results.append({
            "term": term,
            "status": result["status"],
            "message": result["message"]
        })
        
    return {
        "message": "Sincronização global concluída",
        "details": results
    }
