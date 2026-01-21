import unittest
from pathlib import Path
from nlp_automatos.trie import Trie

class TestTrie(unittest.TestCase):
    
    def setUp(self):
        """Cria um dicionário temporário para testes."""
        self.test_file = Path("test_dict_trie.txt")
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("casa\ncarro\ncausa\n")
            
        self.trie = Trie()
        self.trie.load_from_file(self.test_file)

    def tearDown(self):
        """Limpa o arquivo temporário após o teste."""
        if self.test_file.exists():
            self.test_file.unlink()

    def test_exact_match(self):
        """Testa busca exata (k=0)."""
        res = self.trie.search("casa", 0)
        # Deve encontrar 'casa'
        words = [w[0] for w in res]
        self.assertIn("casa", words)
        self.assertEqual(res[0][1], 0) # Distância deve ser 0

    def test_fuzzy_search(self):
        """Testa correção com erro (k=1)."""
        # 'caza' -> 'casa' (1 subst)
        res = self.trie.search("caza", 1)
        words = [w[0] for w in res]
        self.assertIn("casa", words)
        
        # 'caza' -> 'carro' (distância maior que 1, não deve vir)
        self.assertNotIn("carro", words)

if __name__ == '__main__':
    unittest.main()