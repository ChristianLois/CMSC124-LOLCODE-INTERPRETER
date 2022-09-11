import re
from collections import deque
from Tokens import Token

TOKENS = [
    (r"^HAI\s", "Code Start"),
    (r"^KTHXBYE$", "Code End"),
    (r"^BTW\s", "Comment Delimiter"),
    (r"^OBTW\s", "Multiline Comment Start"),
    (r"^TLDR\s", "Multiline Comment End"),
    (r"^I HAS A\s", "Variable Declaration"),
    (r"^ITZ\s", "Variable Assignment"),
    (r"^R\s", "Assignment"),
    (r"^SUM OF\s", "Addition"),
    (r"^DIFF OF\s", "Subtraction"),
    (r"^PRODUKT OF\s", "Multiplication"),
    (r"^QUOSHUNT OF\s", "Division"),
    (r"^MOD OF\s", "Modulo"),
    (r"^BIGGR OF\s", "Max"),
    (r"^SMALLR OF\s", "Min"),
    (r"^BOTH OF\s", "And"),
    (r"^EITHER OF\s", "Or"),
    (r"^WON OF\s", "Xor"),
    (r"^NOT\s", "Not"),
    (r"^ANY OF\s", "Infinite Or"),
    (r"^ALL OF\s", "Infinite And"),
    (r"^AN\s", "Operation Delimiter"),
    (r"^MKAY\s", "Infinite Bool End"),
    (r"^BOTH SAEM\s", "Equality Check"),
    (r"^DIFFRINT\s", "Inequality Check"),
    (r"^SMOOSH\s", "Concatenate"),
    (r"^MAEK\s", "Typecast Keyword"),
    (r"^A\s", "Typecast Keyword"),
    (r"^IS NOW A\s", "Typecast Keyword"),
    (r"^VISIBLE\s", "Ouput Keyword"),
    (r"^GIMMEH\s", "Input Keyword"),
    (r"^O RLY\?\s", "If-else Start"),
    (r"^YA RLY\s", "If Keyword"),
    (r"^MEBBE\s", "Else-if Keyword"),
    (r"^NO WAI\s", "Else Keyword"),
    (r"^OIC\s", "If-else End"),
    (r"^WTF\?\s", "Switch-case Start"),
    (r"^OMG\s", "Case Keyword"),
    (r"^OMGWTF\s", "Case Default Keyword"),
    (r"^IM IN YR\s", "Loop Start"),
    (r"^UPPIN\s", "Loop Opearation"),
    (r"^NERFIN\s", "Loop Opearation"),
    (r"^YR\s", "Loop Delimiter"),
    (r"^TIL\s", "Condition Keyword"),
    (r"^WILE\s", "Condition Keyword"),
    (r"^IM OUTTA YR\s", "Loop End"),
    (r"^(WIN|FAIL)\s", "Troof Literal"),
    (r"-?[0-9]+\.[0-9]+\s", "Numbar Literal"),
    (r"-?[0-9]+\s", "Numbr Literal"),
    (r"\"[^\"]*\"\s", "Yarn Literal"),
    (r"^(NOOB|NUMBR|NUMBAR|YARN|TROOF)\s", "Data Type"),
    (r"^[a-zA-Z][a-zA-Z0-9_]*\s", "Variable Identifier")
]

class Lexer:
    def __init__(self, text):
        self.text = text

    def tokenize(self):
        tokens = deque()
        lines = self.text.split('\n')
        line_no = 1
        in_comment = False
        for line in lines:
            line = line.strip()+'\n'
            if(in_comment):
                if(line[:-1] == "TLDR"):
                    in_comment = False
                    tokens.append(Token('Multiline Comment End', line.strip(), line_no))
                else:
                    tokens.append(Token('Comment', line.strip(), line_no))
                continue
            hasToken = False
            while(line != '\n' and line !=''):
                hasToken = True
                for token in TOKENS:       
                    pattern, type = token
                    matched_token = re.match(pattern, line)
                    if(matched_token):
                        if type == 'Comment Delimiter':
                            token_value = matched_token.group(0)
                            tokens.append(Token(type, token_value.strip(), line_no))
                            line = line[matched_token.end():].lstrip()
                            tokens.append(Token('Comment', line[:-1].strip(), line_no))
                            line = line[len(line):]
                            break
                        elif type == 'Multiline Comment Start':
                            token_value = matched_token.group(0)
                            tokens.append(Token(type, token_value.strip(), line_no))
                            in_comment = True
                        elif type == 'Yarn Literal':
                            temp_token = matched_token.group(0)
                            tokens.append(Token('String Delimiter', '"', line_no))
                            tokens.append(Token(type, temp_token[1:-2], line_no))
                            tokens.append(Token('String Delimiter', '"', line_no))
                        else:
                            token_value = matched_token.group(0)
                            tokens.append(Token(type, token_value.strip(), line_no))
                        line = line[matched_token.end():].lstrip()
                        break
                if(not matched_token):
                    raise Exception(f"Error in line number {line_no}: Invalid token {line}")
            if(hasToken and not in_comment):
                tokens.append(Token('Linebreak', '\\n', line_no))
            line_no += 1
        return tokens  