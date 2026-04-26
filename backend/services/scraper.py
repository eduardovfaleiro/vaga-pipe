from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from thefuzz import fuzz
from crud.scrape_history import get_recent_scrapes, upsert_scrape_history
from worker import start_scraper_worker
from logger import get_logger

CACHE_HOURS = 6
FUZZY_MATCH_THRESHOLD = 85  # De 0 a 100, quão parecido deve ser para usar o cache

log = get_logger("sync")

def trigger_scrape_if_needed(db: Session, search_term: str, background_tasks: BackgroundTasks):
    log.debug("Verificando se scrape é necessário", extra={"search_term": search_term})
    recent_scrapes = get_recent_scrapes(db, CACHE_HOURS)
    
    # Verifica em todas as buscas recentes se existe alguma muito parecida
    for history in recent_scrapes:
        # token_sort_ratio ignora a ordem ("dev flutter" == "flutter dev")
        similarity_score = fuzz.token_sort_ratio(search_term.lower(), history.term.lower())
        
        if similarity_score >= FUZZY_MATCH_THRESHOLD:
            log.info("Utilizado termo em cache", extra={"search_term": search_term})
            return {
                "status": "cached", 
                "message": f"Termo '{search_term}' similar a '{history.term}' (Score: {similarity_score}). Usando base local."
            }
        
    start_scraper_worker(search_term, background_tasks)
    
    return {
        "status": "started", 
        "message": f"Scraping iniciado em background para: {search_term}"
    }
