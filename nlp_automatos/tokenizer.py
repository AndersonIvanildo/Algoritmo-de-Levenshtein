class TokenizerDFA:
    """
    Implementação manual do autômato de tokenização baseado 
    nos estados: Inicial, Lendo Palavra, Lendo Número e Símbolo.
    """
    def __init__(self):
        # Estados possíveis
        self.INITIAL = 0
        self.READING_WORD = 1
        self.READING_NUMBER = 2
        
    def tokenize(self, text: str):
        tokens = []
        current_token = ""
        state = self.INITIAL

        for char in text:
            if state == self.INITIAL:
                if char.isalpha():
                    state = self.READING_WORD
                    current_token += char
                elif char.isdigit():
                    state = self.READING_NUMBER
                    current_token += char
                else:
                    # Símbolos/Espaços são tratados como tokens individuais 
                    if not char.isspace():
                        tokens.append(char)
            
            elif state == self.READING_WORD:
                if char.isalpha():
                    current_token += char
                else:
                    # Transição para qf (token reconhecido) e volta para q0
                    tokens.append(current_token)
                    current_token = ""
                    if char.isspace():
                        state = self.INITIAL
                    elif char.isdigit():
                        state = self.READING_NUMBER
                        current_token += char
                    else:
                        tokens.append(char)
                        state = self.INITIAL

            elif state == self.READING_NUMBER:
                if char.isdigit():
                    current_token += char
                else:
                    tokens.append(current_token)
                    current_token = ""
                    if char.isspace():
                        state = self.INITIAL
                    elif char.isalpha():
                        state = self.READING_WORD
                        current_token += char
                    else:
                        tokens.append(char)
                        state = self.INITIAL

        # Adiciona o último token se houver
        if current_token:
            tokens.append(current_token)
            
        return tokens


tokenizer_dfa = TokenizerDFA()
