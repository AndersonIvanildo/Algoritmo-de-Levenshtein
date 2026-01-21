from pathlib import Path
from .trie import Trie
from .dawg import DAWG
from .downloader import download_dictionary

# Armazena as instâncias carregadas na memória RAM
_ENGINES = {
    'trie': None,
    'dawg': None
}

# Configurações Padrão
DEFAULT_URL = "https://www.ime.usp.br/~pf/dicios/br-utf8.txt"
DEFAULT_FILENAME = "dicionario_pt.txt"

def get_engine(algorithm_type: str, data_dir: str = "data"):
    """
    Factory que retorna a instância única do motor solicitado.
    Gerencia download e carregamento automático.
    
    Args:
        algorithm_type: 'trie' ou 'dawg'
        data_dir: Pasta onde salvar o dicionário
    """
    algo = algorithm_type.lower()
    
    if algo not in _ENGINES:
        raise ValueError(f"Algoritmo desconhecido: {algo}. Use 'trie' ou 'dawg'.")

    # Se já está na memória, retorna
    if _ENGINES[algo] is not None:
        return _ENGINES[algo]

    # Processo de Inicialização 
    
    # Definir caminhos com pathlib
    base_path = Path(data_dir)
    file_path = base_path / DEFAULT_FILENAME

    # Garantir que o arquivo existe
    file_path = download_dictionary(DEFAULT_URL, file_path)
    
    if not file_path:
        raise RuntimeError("Impossível inicializar engine: Falha no download do dicionário.")

    # Construir o Autômato
    print(f"[Loader] Construindo {algo.upper()} a partir do disco...")
    
    if algo == 'trie':
        engine = Trie()
    else:
        engine = DAWG()
        
    engine.load_from_file(file_path)
    
    # Salvar na memória global
    _ENGINES[algo] = engine
    print(f"[Loader] {algo.upper()} carregada e pronta para uso!")
    
    return _ENGINES[algo]
