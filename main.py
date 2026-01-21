from nlp_automatos.loader import get_engine
import time

def main():
    print("=== Corretor Ortográfico (Teste de Console) ===")
    
    # Configuração Inicial
    # Escolha entre 'trie' ou 'dawg'
    tipo_algoritmo = input("Escolha o algoritmo (trie/dawg) [trie]: ").strip().lower() or "trie"
    
    print(f"\nInicializando engine '{tipo_algoritmo}'...")
    start_load = time.time()
    
    # O loader vai baixar o dicionário e carregar na memória
    try:
        engine = get_engine(tipo_algoritmo)
    except Exception as e:
        print(f"Erro ao carregar engine: {e}")
        return

    end_load = time.time()
    print(f"Engine carregada em {end_load - start_load:.4f} segundos.\n")

    # Loop de verificação
    while True:
        palavra = input("Digite uma palavra (ou 'sair' para encerrar): ").strip()
        
        if palavra.lower() in ['sair', 'exit', 'q']:
            break
            
        try:
            k = int(input(f"Distância máxima (k) para '{palavra}': "))
        except ValueError:
            print("Valor de k inválido. Usando k=1.")
            k = 1

        print(f"Buscando sugestões para '{palavra}' com k={k}...")
        
        start_search = time.time()
        sugestoes = engine.search(palavra, k)
        end_search = time.time()

        # Exibição dos Resultados
        print(f"\n--- Resultados ({len(sugestoes)} encontrados em {(end_search - start_search)*1000:.2f}ms) ---")
        
        if not sugestoes:
            print("Nenhuma palavra encontrada dentro dessa distância.")
        else:
            # Mostra as top 10 sugestões
            for i, (sugestao, dist) in enumerate(sugestoes[:10], 1):
                print(f"{i}. {sugestao} (Distância: {dist})")
        
        print("-" * 40 + "\n")

if __name__ == "__main__":
    main()
