from khan_token import make_token, Token
def tokenize(code):
    tokens = []
    i = 0

    while i < len(code):
        char = code[i]

        if char.isspace():
            i += 1

        elif char == '"':
            i += 1

            string = ""

            while i < len(code) and code[i] != '"':
                string += code[i]
                i +=1
            if i >= len(code):
                raise SyntaxError("Undefined string")
            tokens.append(Token('STRING', string))
            i += 1
        elif char.isalpha():
            word = ""

            while i < len(code) and code[i].isalpha():
                word += code[i]
                i += 1

            tokens.append(make_token(word))

        elif char.isdigit():
            number = ""

            while i < len(code) and code[i].isdigit():
                number += code[i]

                i += 1

            tokens.append(make_token(number))

        elif char in "=!><":
            if i + 1 < len(code) and code[i + 1] == "=":
                operator = code[i:i + 2]
                tokens.append(Token("COMPARISON", operator))
                i += 2
            elif char == "=":
                tokens.append(Token("EQUALS", "="))
                i += 1
            elif char in "><":
                tokens.append(Token("COMPARISON", char))
                i += 1
            else:
                raise SyntaxError("Expected '=' after '!'")
        elif char in "*/-+":
            tokens.append(Token("OPERATOR", char))
            i += 1

        elif char in "{}":
            tokens.append(Token("BRACE", char))
            i += 1

        elif char in "(),":
            tokens.append(Token("PUNCTUATION", char))
            i += 1

        else:
            raise ValueError(f"Unexpected character: {char}")

    return tokens
