import urllib.request
from pathlib import Path

def download_dictionary(url: str, destination: str | Path) -> Path:
    """
    Verifica se o arquivo de dicionário existe. Se não, realiza o download.
    Utiliza pathlib para gestão robusta de caminhos.
    """
    dest_path = Path(destination)

    # Verifica se o arquivo já existe
    if dest_path.exists():
        print(f"[Cache] Dicionário encontrado em: {dest_path.absolute()}")
        return dest_path

    print(f"[Download] Baixando dicionário de: {url}")
    
    try:
        # Garante que a pasta pai existe
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Realiza o download
        urllib.request.urlretrieve(url, str(dest_path))
        
        print(f"[Sucesso] Arquivo salvo em: {dest_path.name}")
        return dest_path
    
    except Exception as e:
        print(f"[Erro] Falha no download: {e}")
        # Remove arquivo parcial corrompido se tiver sido criado
        if dest_path.exists():
            dest_path.unlink()
        return None
