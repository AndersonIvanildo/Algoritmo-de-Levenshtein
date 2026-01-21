from pathlib import Path

class DawgNode:
    """
    Nó do Grafo Acíclico de Palavras (DAWG).
    Implementa hashing para permitir a verificação de equivalência
    durante a minimização.
    """
    __slots__ = ['id', 'edges', 'is_word']
    _next_id = 0

    def __init__(self):
        self.id = DawgNode._next_id
        DawgNode._next_id += 1
        self.edges = {}
        self.is_word = False

    def __repr__(self):
        # Assinatura única baseada nas arestas e se é final
        signature = f"{self.is_word}"
        for char in sorted(self.edges.keys()):
            signature += f"|{char}:{self.edges[char].id}"
        return signature

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

class DAWG:
    """
    Autômato Finito Determinístico Mínimo.
    Exige inserção em ordem alfabética.
    """
    def __init__(self):
        self.root = DawgNode()
        self.unchecked_nodes = [] # Caminho da última palavra
        self.minimized_nodes = {} # Registro de nós únicos

    def insert(self, word: str):
        # Encontrar prefixo comum com a última palavra inserida
        common_prefix = 0
        for i in range(min(len(word), len(self.unchecked_nodes))):
            if word[i] != self.unchecked_nodes[i][0]:
                break
            common_prefix += 1

        # Minimizar os sufixos divergentes
        self._minimize(common_prefix)

        # Adicionar novos nós para o novo sufixo
        if not self.unchecked_nodes:
            node = self.root
        else:
            node = self.unchecked_nodes[-1][2]

        for char in word[common_prefix:]:
            next_node = DawgNode()
            node.edges[char] = next_node
            self.unchecked_nodes.append((char, node, next_node))
            node = next_node
        
        node.is_word = True

    def _minimize(self, down_to):
        # Percorre de trás para frente, fundindo estados equivalentes
        for i in range(len(self.unchecked_nodes) - 1, down_to - 1, -1):
            char, parent, child = self.unchecked_nodes.pop()
            if child in self.minimized_nodes:
                # Reutiliza nó existente
                parent.edges[char] = self.minimized_nodes[child]
            else:
                # Registra novo nó único
                self.minimized_nodes[child] = child

    def finish(self):
        """Minimiza os nós restantes após a última palavra."""
        self._minimize(0)

    def load_from_file(self, file_path: Path):
        """
        Lê e ordena o arquivo antes de inserir.
        DAWG exige ordem alfabética estrita.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
            
        with file_path.open('r', encoding='utf-8') as f:
            # Ordenação em memória
            words = sorted([line.strip().lower() for line in f if line.strip()])
            for w in words:
                self.insert(w)
        self.finish()

    def search(self, word: str, max_k: int):
        """Mesma lógica de busca da Trie, mas navegando no grafo minimizado."""
        word = word.lower()
        current_row = range(len(word) + 1)
        results = []

        for char, node in self.root.edges.items():
            self._search_recursive(node, char, word, current_row, results, max_k, char)
        
        return sorted(results, key=lambda x: x[1])

    def _search_recursive(self, node, char, target_word, prev_row, results, max_k, current_word):
        # Lógica idêntica à Trie, apenas mudando 'children' para 'edges'
        columns = len(target_word) + 1
        current_row = [prev_row[0] + 1]

        for col in range(1, columns):
            insert_cost = current_row[col - 1] + 1
            delete_cost = prev_row[col] + 1
            replace_cost = prev_row[col - 1] + (0 if target_word[col - 1] == char else 1)
            current_row.append(min(insert_cost, delete_cost, replace_cost))

        if current_row[-1] <= max_k and node.is_word:
            results.append((current_word, current_row[-1]))

        if min(current_row) <= max_k:
            for next_char, next_node in node.edges.items():
                self._search_recursive(next_node, next_char, target_word, current_row, results, max_k, current_word + next_char)
