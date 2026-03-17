from sqlalchemy.orm import Session
from thefuzz import fuzz
from crud.user import get_users
from crud.recommendation import create_recommendation
from services.whatsapp import send_whatsapp_message
import asyncio

async def process_new_jobs_for_users(db: Session, new_jobs: list):
    """
    Cruza as novas vagas coletadas com as skills dos usuários ativos.
    """
    if not new_jobs:
        return

    users = get_users(db, skip=0, limit=1000) # Busca usuários ativos (até 1000 por lote para evitar estourar a memória)
    
    for user in users:
        # Pula usuário se não tiver skills cadastradas
        if not user.skills:
            continue
            
        user_skills = user.skills.lower()
        match_threshold = user.match_threshold or 70.0
        
        for job in new_jobs:
            if not job.description and not job.title:
                continue
                
            job_text = f"{job.title} {job.description}".lower()
            
            # Usando token_set_ratio que é ideal para verificar se um conjunto
            # pequeno de palavras (skills) está contido num conjunto maior (descrição da vaga)
            match_score = fuzz.token_set_ratio(user_skills, job_text)
            
            if match_score >= match_threshold:
                create_recommendation(db, user_id=user.id, job_id=job.id, score=match_score)
                
                # Se o usuário tiver telefone, dispara o WhatsApp
                if user.phone:
                    message = (
                        f"🚀 *Nova vaga com Match!*\n\n"
                        f"*Título:* {job.title}\n"
                        f"*Empresa:* {job.company or 'Não informada'}\n"
                        f"*Score:* {match_score:.0f}%\n"
                        f"*Link:* {job.url}"
                    )
                    # Como estamos dentro de uma função async chamada pelo worker, podemos dar await
                    await send_whatsapp_message(user.phone, message)
                
                print(f"[MATCHER] Vaga '{job.title}' recomendada para '{user.name}' com score {match_score}!")
