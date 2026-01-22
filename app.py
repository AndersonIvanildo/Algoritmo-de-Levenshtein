import streamlit as st
import time
import re
import graphviz
from nlp_automatos.loader import get_engine
from nlp_automatos.trie import Trie
from nlp_automatos.dawg import DAWG

# Configuração da Página
st.set_page_config(
    page_title="Autômatos em NLP",
    #page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Customizado
st.markdown("""
<style>
    .correct { color: #0f5132; background-color: #d1e7dd; padding: 2px 5px; border-radius: 4px; font-weight: bold; }
    .error { color: #842029; background-color: #f8d7da; padding: 2px 5px; border-radius: 4px; font-weight: bold; text-decoration: underline; }
    .suggestion-box { border-left: 3px solid #ffc107; padding-left: 10px; margin-bottom: 10px; }
    .stGraphvizChart { border: 1px solid #ddd; border-radius: 5px; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# Função de Carregamento
@st.cache_resource(show_spinner="Carregando Motor de NLP...")
def load_nlp_engine(algorithm_type):
    return get_engine(algorithm_type, "data")

# Funções Auxiliares de Texto
def tokenize(text):
    return re.findall(r'\w+|[^\w]+', text, re.UNICODE)

def check_word_in_dict(engine, word):
    if len(word) < 2 or word.isdigit(): return True
    results = engine.search(word, 0)
    for w, dist in results:
        if dist == 0 and w.lower() == word.lower(): return True
    return False

# Função Geradora de Gráficos
def generate_dot_code(word_list, algo_type):
    """
    Cria um mini-autômato apenas com as palavras fornecidas
    e retorna o código DOT para o Graphviz desenhar.
    """
    # Instancia um motor vazio
    if algo_type == "DAWG":
        mini_engine = DAWG()
        # O DAWG precisa de ordem alfabética para ser construído corretamente
        words_sorted = sorted(word_list)
        for w in words_sorted: mini_engine.insert(w)
        mini_engine.finish()
    else:
        mini_engine = Trie()
        for w in word_list: mini_engine.insert(w)
    
    # Configuração do Gráfico
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR') # Esquerda para Direita
    dot.attr('node', shape='circle')
    
    # Travessia BFS para desenhar nós e arestas
    root = mini_engine.root
    
    # Mapeia objetos Python para IDs numéricos para o Graphviz
    def get_uid(node):
        return str(node.id) if algo_type == "DAWG" else str(id(node))
    
    queue = [root]
    visited = {get_uid(root)}
    
    # Desenha a raiz
    dot.node(get_uid(root), label="Start", shape="point")
    
    while queue:
        current_node = queue.pop(0)
        current_uid = get_uid(current_node)
        
        # Se for estado final, desenha círculo duplo
        if current_node.is_word:
            dot.node(current_uid, shape='doublecircle', label="")
        else:
            if current_uid != get_uid(root): # Raiz já desenhada
                dot.node(current_uid, label="")
        
        # Pega filhos
        children = current_node.edges if algo_type == "DAWG" else current_node.children
        
        for char, child_node in children.items():
            child_uid = get_uid(child_node)
            
            # Adiciona aresta
            dot.edge(current_uid, child_uid, label=char)
            
            # Adiciona à fila se não visitado
            if child_uid not in visited:
                visited.add(child_uid)
                queue.append(child_node)
                
    return dot

# Barra Lateral
with st.sidebar:
    st.header("Configurações")
    algo_choice = st.radio("Estrutura:", ("Trie", "DAWG"), horizontal=True)
    k_value = st.slider("Sensibilidade (k):", 0, 3, 1)
    st.divider()
    st.markdown("### Sobre o Projeto")
    st.caption("**Disciplina:** Teoria dos Autômatos e Linguagens Formais 2025.2")
    
    st.markdown("#### Equipe")
    
    # Equipe
    team_members = [
        {"name": "Anderson Ivanildo", "url": "https://github.com/AndersonIvanildo"},
        {"name": "Jonas Fontenele", "url": "https://github.com/jonas-ar"},
        {"name": "Maciel", "url": "https://github.com/macielaraujo"},
        {"name": "Isac", "url": "https://github.com/macielaraujo"},
        {"name": "Ianque", "url": "https://github.com/macielaraujo"},
        {"name": "Jefferson", "url": "https://github.com/macielaraujo"},

    ]
    
    col_team1, col_team2 = st.columns(2)

    # URL do ícone oficial
    github_icon = "https://cdn-icons-png.flaticon.com/512/25/25231.png"
    
    for i, member in enumerate(team_members):
        col = col_team1 if i % 2 == 0 else col_team2
        with col:
            # Substitui espaços no nome por %20 para a URL funcionar
            name_safe = member['name'].replace(" ", "%20")
            
            # Gera badge com logo do GitHub oficial
            st.markdown(
                f"[![GitHub](https://img.shields.io/badge/{name_safe}-181717?style=flat&logo=github&logoColor=white)]({member['url']})"
            )

# Inicialização
try:
    engine = load_nlp_engine(algo_choice.lower())
except Exception as e:
    st.error("Erro ao carregar o dicionário.")
    st.stop()

st.title("Autômato de Levenshtein")
st.write("O Autômato de Levenshtein é uma estrutura matemática que reconhece todas as palavras situadas a uma distância de edição específica de um termo original, permitindo erros de inserção, deleção ou substituição. Ele é amplamente utilizado para otimizar buscas difusas (fuzzy search) em grandes dicionários, filtrando rapidamente sugestões de correção ortográfica sem a necessidade de comparar cada palavra individualmente.")

# Novas Abas
tab1, tab2, tab3 = st.tabs(["Palavra Única", "Editor de Frase", "Visualizador do AFD"])

# ABA PALAVRA ÚNICA
with tab1:
    st.subheader("Teste Unitário")
    word_input = st.text_input("Digite uma palavra:", placeholder="Ex: escloa")
    if word_input:
        start = time.time()
        results = engine.search(word_input, k_value)
        tempo = (time.time() - start) * 1000
        st.write(f"⏱Tempo: **{tempo:.2f}ms** | {len(results)} sugestões")
        
        cols = st.columns(3)
        if not results: st.warning("Nenhuma sugestão encontrada.")
        for i, (w, d) in enumerate(results):
            with cols[i % 3]: st.info(f"**{w}** (dist: {d})")

# ABA: EDITOR DE FRASE
with tab2:
    st.subheader("Editor Inteligente")
    sentence_input = st.text_area("Digite sua frase:", height=100, placeholder="Ex: Eu gosto de comer batata frita na minha caza.")

    if sentence_input:
        tokens = tokenize(sentence_input)
        unknown_words = []
        token_status = []
        
        for token in tokens:
            if re.match(r'\w+', token):
                is_valid = check_word_in_dict(engine, token)
                token_status.append((token, is_valid))
                if not is_valid: unknown_words.append(token)
            else:
                token_status.append((token, True))

        st.markdown("### Análise do Autômato")
        annotated = "".join([t if v else f'<span class="error">{t}</span>' for t, v in token_status])
        st.markdown(f'<div style="background-color:#fff; color:#000; padding:15px; border-radius:5px; border:1px solid #ddd; font-family:monospace; font-size:1.1em;">{annotated}</div>', unsafe_allow_html=True)
        st.divider()

        if unknown_words:
            st.subheader("Correção")
            corrections = {}
            cols = st.columns(min(len(set(unknown_words)), 3))
            for idx, error_word in enumerate(set(unknown_words)):
                suggestions = engine.search(error_word, k_value)
                options = [error_word] + [s[0] for s in suggestions]
                with cols[idx % 3]:
                    corrections[error_word] = st.selectbox(f"Correção: '{error_word}'", options, key=f"fix_{idx}")
            
            st.subheader("Resultado Final")
            final_sen = "".join([corrections[t] if not v and t in corrections else t for t, v in token_status])
            st.success(final_sen)
        else:
            st.success("Texto validado!")

# ABA: LABORATÓRIO VISUAL
with tab3:
    st.subheader("Visualizador de Estrutura de Autômatos")
    st.markdown("""
    Aqui você pode ver a diferença estrutural entre uma **Trie** e um **DAWG**.
    Digite algumas palavras que compartilham prefixos ou sufixos para ver a mágica.
    
    **Sugestão de Teste:** `casa, caso, carro, carruagem, bar, mar, amar`
    """)
    
    words_to_plot = st.text_input("Palavras para desenhar (separadas por vírgula):", "casa, caso, carro, amar, mar")
    
    col_viz_opts = st.columns(2)
    with col_viz_opts[0]:
        viz_algo = st.radio("Algoritmo para desenhar:", ["Trie", "DAWG"], horizontal=True, key="viz_algo")
    
    if words_to_plot:
        try:
            # Limpa e prepara a lista
            word_list = [w.strip().lower() for w in words_to_plot.split(",") if w.strip()]
            
            if len(word_list) > 20:
                st.warning("Muitas palavras! O gráfico pode ficar ilegível. Tente usar menos de 20 palavras.")
            
            # Gera o gráfico
            dot = generate_dot_code(word_list, viz_algo)
            
            st.graphviz_chart(dot)
            
            st.info(f"Visualizando **{len(word_list)} palavras** usando estrutura **{viz_algo}**.")
            
            if viz_algo == "DAWG":
                st.markdown("**Observe:** No DAWG, palavras que terminam igual (ex: 'amar' e 'mar') fundem seus caminhos finais.")
            else:
                st.markdown("**Observe:** Na Trie, mesmo terminando igual, cada palavra tem seu próprio galho final.")
                
        except Exception as e:
            st.error(f"Erro ao gerar gráfico: {e}")
