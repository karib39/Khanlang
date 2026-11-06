class Token:
	def __init__(self, token_type, value):
		self.type = token_type
		self.value = value

def make_token(word):
    if word in ('ADD', 'SUB', 'MUL', 'DIV'):
        return Token('COMMAND', word)

    elif word in ('create', 'show', 'if', 'else', 'while','func','return'):
        return Token('KEYWORD', word)

    elif word.isdigit():
        num = int(word)
        return Token('NUMBER', num)

    elif word.isalpha():
        return Token('WORD', word)
