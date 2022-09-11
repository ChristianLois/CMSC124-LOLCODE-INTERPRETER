from ATNode import ATNode
from collections import deque

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = 0
        self.current_token = self.tokens[self.token_idx]
    
    def nextToken(self, token_type):
        if self.current_token.type == token_type:
            self.token_idx +=1
            self.current_token = self.tokens[self.token_idx]
        else:
            raise Exception(f"Syntax Error in line number {self.current_token.line_num}: Expected {token_type} but saw {self.current_token.type}")
            # return False
    
    def visible(self):
        childNodes = deque()
        if(self.current_token.type == 'Output Keyword'):
            self.nextToken('Output Keyword')
            childNodes.append(ATNode('Output Keyword'))
        else:
            return False
        
        self.nextToken('String Delimiter')
        childNodes.append(ATNode('String Delimiter'))
        
        self.nextToken('Yarn Literal')
        childNodes.append(ATNode('Yarn Literal'))

        self.nextToken('String Delimiter')
        childNodes.append(ATNode('String Delimiter'))

        self.nextToken ('Linebreak')
        childNodes.append(ATNode('Linebreak'))

        return ATNode('Output Statement', children_nodes = childNodes)


    def statement(self):
        childNodes = deque()

        if(visible := self.visible()):
            childNodes.append(visible)
        
        return ATNode('Statement', children_nodes = childNodes)
        
    def lolProgram(self):
        treeNode = deque()

        # HAI
        self.nextToken('Code Start')
        treeNode.append(ATNode('Code Start'))

        # checks if the version exists
        if (self.current_token.type == 'Numbar Literal' or self.current_token.type == 'Numbr Literal'):
            self.nextToken(self.current_token.type)
        
        self.nextToken('Linebreak')
        treeNode.append(ATNode('Linebreak'))

        # Code Body
        if(self.current_token.type != 'Code End'):
            statement = self.statement()
            treeNode.append(statement)
        
        # KTHXBYE
        self.nextToken('Code End')
        treeNode.append(ATNode('Code End'))

        return ATNode('LOLProgram', children_nodes = treeNode)
        

