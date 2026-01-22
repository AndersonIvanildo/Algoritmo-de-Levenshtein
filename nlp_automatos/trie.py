from pathlib import Path

class TrieNode:
    """
    Nó da Trie.
    Usa __slots__ para reduzir consumo de memória.
    """
    __slots__ = ['children', 'is_word']

    def __init__(self):
        self.children = {}
        self.is_word = False

class Trie:
    """
    Implementação de DFA de Prefixo otimizado para busca de Levenshtein.
    """
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_word = True 

    def load_from_file(self, file_path: Path):
        """Lê o arquivo linha por linha e popula o autômato."""
        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        count = 0
        with file_path.open('r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                word = line.strip().lower()
                if word:
                    self.insert(word)
                    count += 1
        print(f"[Trie] Total de palavras indexadas: {count}")

    def search(self, word: str, max_k: int):
        word = word.lower()
        # Primeira linha da matriz de Levenshtein: 0, 1, 2...
        current_row = range(len(word) + 1)
        results = []

        # Percorre o autômato recursivamente
        for char, node in self.root.children.items():
            self._search_recursive(node, char, word, current_row, results, max_k, char)
        
        return sorted(results, key=lambda x: x[1])

    def _search_recursive(self, node, char, target_word, prev_row, results, max_k, current_word):
        columns = len(target_word) + 1
        current_row = [prev_row[0] + 1]

        # Lógica de Programação Dinâmica para Levenshtein
        for col in range(1, columns):
            insert_cost = current_row[col - 1] + 1
            delete_cost = prev_row[col] + 1
            replace_cost = prev_row[col - 1] + (0 if target_word[col - 1] == char else 1)
            
            current_row.append(min(insert_cost, delete_cost, replace_cost))

        # Verifica se é estado final e se a distância é aceitável
        if current_row[-1] <= max_k and node.is_word:
            results.append((current_word, current_row[-1]))

        # Poda (Pruning)
        if min(current_row) <= max_k:
            for next_char, next_node in node.children.items():
                self._search_recursive(next_node, next_char, target_word, current_row, results, max_k, current_word + next_char)
