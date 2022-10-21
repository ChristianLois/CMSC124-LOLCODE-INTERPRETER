from ATNode import ATNode
from collections import deque

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = 0
        self.current_token = self.tokens[self.token_idx]
    
    def nextToken(self, token_type):
        if self.current_token.type == token_type:
            self.token_idx += 1
            self.current_token = self.tokens[self.token_idx]
        else:
            raise Exception(f"Syntax Error in line number {self.current_token.line_num}: Expected {token_type} but saw {self.current_token.type}")

    # ------------------------LITERALS/EXPRESISON/VARIABLE------------------------
    def exprvar(self):
        childNodes = deque()
        if (literal := self.literal()):
            print('Enter 2')
            childNodes.append(literal)
        elif (self.current_token.type == 'Variable Identifier'):
            childNodes.append(ATNode('Variable Identifier', value = self.current_token.value))
            self.nextToken('Variable Identifier')
        # elif (expression := self.expression()):
        #     childNodes.append(expression)
        else:
            return False
        
        return ATNode('Exprvar', children_nodes = childNodes)
    
    def literal(self):
        childNodes = deque()
        nonStringLit = ['Numbar Literal', 'Numbr Literal', 'Troof Literal']
        if(self.current_token.type in nonStringLit):
            childNodes.append(ATNode(self.current_token.type, value = self.current_token.value))
            self.nextToken(self.current_token.type)
        elif(yarn_literal := self.yarn_literal()):
            childNodes.append(yarn_literal)
        else:
            return False
        
        return ATNode('Literal', children_nodes = childNodes)
    
    def yarn_literal(self):
        childNodes = deque()
        if (self.current_token.type == 'String Delimiter'):
            self.nextToken('String Delimiter')
            if(self.current_token.type == 'Yarn Literal'):
                childNodes.append(ATNode('Yarn Literal', value = self.current_token.value))
                self.nextToken('Yarn Literal')
            if (self.current_token.type == 'String Delimiter'):
                self.nextToken('String Delimiter')
        else:
            return False


        return ATNode('Yarn Literal', children_nodes = childNodes)

    # def expression(self):

    # ------------------------LITERALS/EXPRESISON/VARIABLE------------------------

    # ------------------------PRINT------------------------
    def visible(self):
        childNodes = deque()
        if(self.current_token.type == 'Output Keyword'):
            self.nextToken('Output Keyword')
            childNodes.append(ATNode('Output Keyword'))
        else:
            return False
        
        childNodes.append(self.printNodes(deque()))

        return ATNode('Output Statement', children_nodes = childNodes)

    def printNodes(self, childNodes):
        exprvar = self.exprvar()
        childNodes.append(exprvar)

        if(self.current_token.type != 'Comment Delimiter' and self.current_token.type != 'Linebreak'):
            print('Enter')
            childNodes.append(self.printNodes(childNodes))
    
        
        return ATNode('Print Statements', children_nodes = childNodes)
    # ------------------------PRINT------------------------
    def statement(self):
        childNodes = deque()

        if(visible := self.visible()):
            childNodes.append(visible)
        
        self.nextToken('Linebreak')
        childNodes.append(ATNode('Linebreak'))
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
        

