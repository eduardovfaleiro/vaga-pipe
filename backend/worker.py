from fastapi import BackgroundTasks
from scrapers.adzuna import AdzunaScraper
from database import SessionLocal
from crud.job import create_job
from services.matcher import process_new_jobs_for_users

async def run_scraping_task(search_term: str):
    print(f"Iniciando scraping para: {search_term}")
    
    # Instancia os scrapers
    scrapers = [AdzunaScraper()]
    
    db = SessionLocal()
    try:
        all_jobs = []
        for scraper in scrapers:
            jobs = await scraper.scrape(search_term)
            for job_data in jobs:
                db_job = create_job(db, job_data)
                all_jobs.append(db_job)
        
        print(f"Scraping finalizado. {len(all_jobs)} vagas processadas.")
        
        # Realiza o cálculo automático de MATCH (Cruzamento)
        await process_new_jobs_for_users(db, all_jobs)
    finally:
        db.close()

def start_scraper_worker(search_term: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_scraping_task, search_term)
