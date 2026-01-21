import unittest
from pathlib import Path
from nlp_automatos.dawg import DAWG

class TestDAWG(unittest.TestCase):
    
    def setUp(self):
        """
        Cria dicionário temporário.
        Nota: DAWG exige ordem alfabética, mas nosso load_from_file trata isso.
        """
        self.test_file = Path("test_dict_dawg.txt")
        # Escrevendo fora de ordem para testar se o loader ordena
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("zebra\ncasa\namar\n")
            
        self.dawg = DAWG()
        self.dawg.load_from_file(self.test_file)

    def tearDown(self):
        if self.test_file.exists():
            self.test_file.unlink()

    def test_structure_integrity(self):
        """Verifica se palavras existem no grafo minimizado."""
        res = self.dawg.search("zebra", 0)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0][0], "zebra")

    def test_fuzzy_dawg(self):
        """Testa busca aproximada no grafo."""
        # 'zabra' -> 'zebra' (1 erro)
        res = self.dawg.search("zabra", 1)
        self.assertEqual(res[0][0], "zebra")
        self.assertEqual(res[0][1], 1)

if __name__ == '__main__':
    unittest.main()