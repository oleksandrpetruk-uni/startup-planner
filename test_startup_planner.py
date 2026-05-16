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
        text = "Мені не вистачає грошей на запуск"
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