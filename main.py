import time
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Імпортуємо логіку вашого планувальника з ЛР 02-04
# (Припускаємо, що у вашому модулі є відповідні функції чи класи)
try:
    import startup_planner
except ImportError:
    # Заглушка на випадок, якщо структура імпорту у вашому проєкті відрізняється
    startup_planner = None

app = FastAPI(
    title="Startup Planner API",
    description="REST API для автоматизації аналізу бізнес-ідей стартапів",
    version="1.0.0"
)

# Описуємо структуру вхідних даних за допомогою Pydantic
class ProblemPayload(BaseModel):
    text: str = Field(..., min_length=10, max_length=1000, example="Брак чистих шеринг-самокатів у спальних районах Харкова через відсутність зарядних станцій.")

# 1. ОБОВ'ЯЗКОВИЙ ENDPOINT: /health
@app.get("/health", tags=["System"])
def health_check():
    """
    Ендпоінт для моніторингу працездатності застосунку (Health Check)
    """
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "discipline": "Основи Програмної Інженерії",
        "student": "Петрук Олександр Вадимович",
        "group": "ПЗПІ-25-2",
        "environment": "production"
    }

# 2. ОСНОВНИЙ API ENDPOINT: /api/plan
@app.post("/api/plan", tags=["Core Logic"])
def generate_startup_plan(payload: ProblemPayload):
    """
    Основний ендпоінт для аналізу проблеми стартапу та генерації плану дій
    """
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Текст проблеми не може бути порожнім")
    
    # Інтеграція з вашим модулем ЛР 02-04
    # Якщо функції називаються трохи інакше, адаптуйте ці виклики під свій код
    try:
        if startup_planner and hasattr(startup_planner, 'analyze_problem'):
            risks = startup_planner.analyze_problem(payload.text)
            plan = startup_planner.generate_plan(risks) if hasattr(startup_planner, 'generate_plan') else ["Створити MVP", "Провести кастдев"]
        else:
            # Демонстраційна логіка, якщо оригінальний файл не знайдено
            risks = ["Висока конкуренція", "Технічні ризики інфраструктури"]
            plan = ["Провести аналіз ринку спальних районів", "Розробити прототип станції", "Запустити маркетинг"]
            
        return {
            "original_problem": payload.text,
            "detected_risks": risks,
            "recommended_plan": plan,
            "processed_by": "Петрук О.В."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка внутрішньої логіки: {str(e)}")

# Головна сторінка для зручності
@app.get("/", tags=["System"])
def root():
    return {"message": "Застосунок працює успішно. Документація доступна за адресою /docs"}