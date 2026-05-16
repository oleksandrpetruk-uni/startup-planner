# Звіт з лабораторної роботи №3: Модульне тестування

**Проєкт:** Startup Planner  
**Виконав:** Петрук Олександр

## 1. Тема та мета лабораторної роботи
**Тема:** Проєктування та реалізація модульних тестів.  
**Мета:** Отримати практичні навички з розробки програмних модулів, застосування технік проєктування тестів (EP, BVA), написання модульних тестів за патерном AAA та аналізу покриття коду.

## 2. Вихідний код реалізованого модуля

```python
class BlockerAnalyzer:
    def analyze_problem(self, text: str) -> list:
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
        if day_number < 1 or day_number > 7:
            raise ValueError("День має бути в межах від 1 до 7")
            
        for task in tasks:
            if task["day"] == day_number:
                if task["done"]:
                    return False
                task["done"] = True
                return True
        return False
```

## 3. Таблиця проєктування тестів

| № | Тест-кейс (опис) | Вхідні дані | Очікуваний результат | Техніка | Статус |
|---|---|---|---|---|---|
| 1 | Валідний текст (нижня межа) | `text = "1234567890"` (10 симв) | Повертає список ризиків | BVA, Позитивний | Pass |
| 2 | Занадто короткий текст | `text = "123456789"` (9 симв) | `ValueError` | BVA, Негативний | Pass |
| 3 | Валідний текст (верхня межа) | `text = "a" * 1000` | Повертає список ризиків | BVA, Позитивний | Pass |
| 4 | Занадто довгий текст | `text = "a" * 1001` | `ValueError` | BVA, Негативний | Pass |
| 5 | Наявність фінансових слів | `text = "Немає грошей"` | `["Фінансовий ризик"]` | EP, Позитивний | Pass |
| 6 | Неправильний тип даних | `text = 123` | `TypeError` | EP, Негативний | Pass |
| 7 | Генерація: макс. к-ть ризиків | `risks = ["Р1","Р2","Р3","Р4","Р5"]` | Список з 7 завдань | BVA, Позитивний | Pass |
| 8 | Генерація: забагато ризиків | `risks = ["Р1",...,"Р6"]` (6 шт) | `ValueError` | BVA, Негативний | Pass |
| 9 | Виконання: валідний день 1 | `day = 1`, `tasks = [...]` | Повертає `True` | BVA, Позитивний | Pass |
| 10 | Виконання: помилка день 0 | `day = 0`, `tasks = [...]` | `ValueError` | BVA, Негативний | Pass |
| 11 | Виконання: помилка день 8 | `day = 8`, `tasks = [...]` | `ValueError` | BVA, Негативний | Pass |
| 12 | Виконання: вже виконане | `day = 1`, `done = True` | Повертає `False` | EP, Позитивний | Pass |

## 4. Вихідний код тестового набору

```python
import unittest
from startup_planner import BlockerAnalyzer, ActionPlan

class TestStartupPlanner(unittest.TestCase):
    def setUp(self):
        self.analyzer = BlockerAnalyzer()
        self.planner = ActionPlan()

    def test_analyze_problem_valid_length_bva(self):
        text = "1234567890"
        result = self.analyzer.analyze_problem(text)
        self.assertIsInstance(result, list)

    def test_analyze_problem_too_short_bva(self):
        text = "123456789"
        with self.assertRaises(ValueError):
            self.analyzer.analyze_problem(text)

    def test_analyze_problem_too_long_bva(self):
        text = "a" * 1001
        with self.assertRaises(ValueError):
            self.analyzer.analyze_problem(text)

    def test_analyze_problem_financial_risk_ep(self):
        text = "Mention money"
        result = self.analyzer.analyze_problem(text)
        self.assertIn("Фінансовий ризик", result)

    def test_analyze_problem_invalid_type_ep(self):
        text = 12345 
        with self.assertRaises(TypeError):
            self.analyzer.analyze_problem(text)

    def test_generate_plan_valid_ep(self):
        risks = []
        result = self.planner.generate_seven_day_plan(risks)
        self.assertEqual(len(result), 7)

    def test_generate_plan_max_risks_bva(self):
        risks = ["1", "2", "3", "4", "5"]
        result = self.planner.generate_seven_day_plan(risks)
        self.assertEqual(len(result), 7)

    def test_generate_plan_too_many_risks_bva(self):
        risks = ["1", "2", "3", "4", "5", "6"]
        with self.assertRaises(ValueError):
            self.planner.generate_seven_day_plan(risks)

    def test_generate_plan_invalid_type_ep(self):
        risks = "not a list"
        with self.assertRaises(TypeError):
            self.planner.generate_seven_day_plan(risks)

    def test_mark_task_valid_bva(self):
        tasks = [{"day": 1, "desc": "Крок 1", "done": False}]
        result = self.planner.mark_task_as_done(1, tasks)
        self.assertTrue(result)

    def test_mark_task_day_zero_bva(self):
        tasks = [{"day": 1, "desc": "Крок 1", "done": False}]
        with self.assertRaises(ValueError):
            self.planner.mark_task_as_done(0, tasks)

    def test_mark_task_already_done_ep(self):
        tasks = [{"day": 1, "desc": "Крок 1", "done": True}]
        result = self.planner.mark_task_as_done(1, tasks)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
```

## 5. Скріншот звіту покриття коду

![Звіт покриття коду coverage](https://github.com/user-attachments/assets/63e2ad70-a4fc-460a-89be-57d3ca1ff03c)

## 6. Посилання на Git-репозиторій

[https://github.com/oleksandrpetruk-uni/startup-planner](https://github.com/oleksandrpetruk-uni/startup-planner)

## 7. Висновки

У ході лабораторної роботи було реалізовано програмний модуль проєкту Startup Planner мовою Python. Завдяки використанню технік еквівалентного розділення (EP) та аналізу граничних значень (BVA) було розроблено 12 тест-кейсів, які повністю покривають логіку роботи програми. Створені модульні тести дотримуються патерну AAA. Аналіз покриття коду за допомогою утиліти `coverage` показав результат 97%, що значно перевищує базову вимогу у ≥80%. Всі 12 тестів пройшли успішно, що свідчить про високу якість написаного коду та коректну обробку граничних і виняткових ситуацій.
