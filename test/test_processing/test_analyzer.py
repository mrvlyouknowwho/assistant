import unittest
from ..processing.nlp.analyzer import analyze_query

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
       self.data = {"user_info":{}, "context":{}}

    def test_analyze_empty_query(self):
        self.assertIsNone(analyze_query("", self.data))

    def test_analyze_exit_query(self):
        self.assertEqual(analyze_query("exit", self.data), "exit")
        self.assertEqual(analyze_query("выход", self.data), "exit")
        self.assertEqual(analyze_query("q", self.data), "exit")
        self.assertEqual(analyze_query("quit", self.data), "exit")

    def test_analyze_name_query(self):
       self.assertEqual(analyze_query("как меня называть Вася", self.data), "name_changed")
       self.assertEqual(self.data["user_info"]["как_меня_называть"], ["Вася"])

    def test_analyze_bad_name_query(self):
       self.assertEqual(analyze_query("как меня называть", self.data), "bad_name")

    def test_analyze_format_query(self):
      self.assertEqual(analyze_query("формат JSON", self.data), "format_changed")
      self.assertEqual(self.data["user_info"]["предпочтения_формат"], ["JSON"])

    def test_analyze_bad_format_query(self):
      self.assertEqual(analyze_query("формат", self.data), "bad_format")

    def test_analyze_themes_query(self):
        self.assertEqual(analyze_query("темы python", self.data), "themes_changed")
        self.assertEqual(self.data["user_info"]["предпочтения_темы"], ["python"])

    def test_analyze_bad_themes_query(self):
        self.assertEqual(analyze_query("темы", self.data), "bad_themes")

    def test_analyze_fix_query(self):
         self.assertEqual(analyze_query("ошибка", self.data), "fix")

    def test_analyze_add_function_query(self):
         self.assertEqual(analyze_query("новая функция", self.data), "add_function")

    def test_analyze_clear_query(self):
          self.assertEqual(analyze_query("очистить базу", self.data), "clear_database")

    def test_analyze_related_query(self):
          self.data["context"]["last_query"] = "test query"
          self.assertEqual(analyze_query("test", self.data),"related")
          self.assertIsNone(analyze_query("other", self.data))
if __name__ == '__main__':
    unittest.main()