from ATNode import ATNode

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = 0
        self.current_token = self.tokens[self.token_idx]
    
    def nextToken(self, token_type):
        self.token_idx +=1
        if self.tokens[self.token_idx] == token_type:
            self.current_token = self.tokens[self.token_idx]
        else:
            raise Exception(f"Syntax Error in line number {self.current_token.line_number}: Expect {token_type} but saw {self.current_token.type}")
        
    def lolProgram(self):
        treeNode = []

        self.nextToken('Code Start')
        treeNode.append('Code Start')

        self.nextTok
