# Гілка для проведення Code Review
class BlockerAnalyzer:
    def analyze_problem(self, text: str) -> list:
        """Аналізує текст проблеми та повертає список ризиків."""
        if not isinstance(text, str):
            raise TypeError("Текст проблеми має бути рядком (string)")
        
        if len(text) < 10:
            raise ValueError("Опишіть проблему детальніше (мінімум 10 символів)")
        if len(text) > 1000:
            raise ValueError("Текст занадто довгий (максимум 1000 символів)")

        risks = []
        text_lower = text.lower()
        
        if "грош" in text_lower or "фінанс" in text_lower:
            risks.append("Фінансовий ризик")
        if "час" in text_lower or "встиг" in text_lower:
            risks.append("Ризик зриву термінів")
            
        if not risks:
            risks.append("Загальний ризик невизначеності")
            
        return risks

class ActionPlan:
    def generate_seven_day_plan(self, risks: list) -> list:
        """Генерує план з 7 завдань на основі ризиків."""
        if not isinstance(risks, list):
            raise TypeError("Ризики мають бути передані як список")
        if len(risks) > 5:
            raise ValueError("Занадто багато ризиків для одного плану (максимум 5)")

        tasks = []
        for i in range(1, 8):
            if i == 1 and risks:
                tasks.append({"day": i, "desc": f"Опрацювати: {risks[0]}", "done": False})
            else:
                tasks.append({"day": i, "desc": f"Стандартний крок {i}", "done": False})
        return tasks

    def mark_task_as_done(self, day_number: int, tasks: list) -> bool:
        """Позначає завдання певного дня як виконане."""
        if day_number < 1 or day_number > 7:
            raise ValueError("День має бути в межах від 1 до 7")
            
        for task in tasks:
            if task["day"] == day_number:
                if task["done"]:
                    return False
                task["done"] = True
                return True
        return False
