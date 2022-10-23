from ATNode import ATNode
from collections import deque

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = 0
        self.current_token = self.tokens[self.token_idx]
    
    def nextToken(self, token_type):
        if self.token_idx + 1 < len(self.tokens) and self.current_token.type == token_type:
            self.token_idx += 1
            self.current_token = self.tokens[self.token_idx]
        else:
            raise Exception(f"Syntax Error:{self.current_token.line_num}:Expected {token_type} at {self.current_token.value}")

    # ------------------------LITERALS/EXPRESISON/VARIABLE------------------------
    def exprvar(self, infAr):
        childNodes = deque()
        if (literal := self.literal()):
            childNodes.append(literal)
        elif (self.current_token.type == 'Variable Identifier'):
            childNodes.append(ATNode('Variable Identifier', value = self.current_token.value))
            self.nextToken('Variable Identifier')
        elif (expression := self.expression(infAr)):
            childNodes.append(expression)
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
            val = self.current_token.value
            self.nextToken('Yarn Literal')
            childNodes.append(ATNode('Yarn Literal', value = val))

            self.nextToken('String Delimiter')
        else:
            return False

        return ATNode('Yarn Literal', children_nodes = childNodes)

    def expression(self, infAr):
        childNodes = deque()
        if(add := self.binaryOp('Addition')):
            childNodes.append(add)
        elif(subtract := self.binaryOp('Subtraction')):
            childNodes.append(subtract)
        elif(mult := self.binaryOp('Multiplication')):
            childNodes.append(mult)
        elif(div := self.binaryOp('Division')):
            childNodes.append(div)
        elif(mod := self.binaryOp('Modulo')):
            childNodes.append(mod)
        elif(maxim := self.binaryOp('Max')):
            childNodes.append(maxim)
        elif(minim := self.binaryOp('Min')):
            childNodes.append(minim)
        elif(andOp := self.binaryOp('And')):
            childNodes.append(andOp)
        elif(orOp := self.binaryOp('Or')):
            childNodes.append(orOp)
        elif(xorOp := self.binaryOp('Xor')):
            childNodes.append(xorOp) 
        elif(notOp := self.unaryOp('Not')):
            childNodes.append(notOp)
        elif(eqCheck := self.binaryOp('Equality Check')):
            childNodes.append(eqCheck)
        elif(ineqCheck := self.binaryOp('Inequality Check')):
            childNodes.append(ineqCheck)
        elif(concat := self.infOp('Concatenate', False)):
            childNodes.append(concat)
        elif(infAr and (infAnd := self.infOp('Infinite And', True))):
            childNodes.append(infAnd)
        elif(infAr and (infOr := self.infOp('Infinite Or', True))):
            childNodes.append(infOr)
        else:
            return False
        
        return ATNode('Expression', children_nodes = childNodes)
    
    def binaryOp(self, operation):
        childNodes = deque()
        if(self.current_token.type == operation):
            childNodes.append(ATNode(operation))
            self.nextToken(operation)
        else:
            return False
        
        if(exprvar := self.exprvar(True)):
            childNodes.append(exprvar)
        else:
            self.nextToken('Expression')
        
        self.nextToken('Operation Delimiter')

        if(exprvar := self.exprvar(True)):
            childNodes.append(exprvar)
        else:
            self.nextToken('Expression')
        
        return ATNode(operation, children_nodes = childNodes)
    
    def unaryOp(self, operation):
        childNodes = deque()
        if(self.current_token.type == operation):
            childNodes.append(ATNode(operation))
            self.nextToken(operation)
        else:
            return False
        
        if(exprvar := self.exprvar(True)):
            childNodes.append(exprvar)
        else:
            self.nextToken('Expression')
        
        return ATNode(operation, children_nodes = childNodes)
    
    def infOp(self, operation, boolean):
        childNodes = deque()
        if(self.current_token.type == operation):
            childNodes.append(operation)
            self.nextToken(operation)
        else:
            return False

        if(boolean and (exprvar := self.exprvar(False))):
            childNodes.append(exprvar)
        elif(not boolean and (exprvar := self.exprvar(True))):
            childNodes.append(exprvar)
        else:
            self.nextToken('Expression')
        
        operands = self.infOperands(deque(), boolean)
        childNodes.append(operands)

        if(boolean):
            self.nextToken('Infinite Bool End')

        return ATNode(operation, children_nodes = childNodes)
        
    def infOperands(self, childNodes, boolean):
        self.nextToken('Operation Delimiter')

        if(boolean and (exprvar := self.exprvar(False))):
            childNodes.append(exprvar)
        elif(not boolean and (exprvar := self.exprvar(True))):
            childNodes.append(exprvar)
        else:
            self.nextToken('Expression')
        
        if(self.current_token.type == 'Operation Delimiter'):
            childNodes.append(self.infOperands(childNodes, boolean))
        
        return ATNode('Infinite Operands', children_nodes = childNodes)
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
        exprvar = self.exprvar(True)
        if(not exprvar):
            self.nextToken('Expression')
        childNodes.append(exprvar)

        if(self.current_token.type == 'Operation Delimiter'):
            self.nextToken('Operation Delimiter')
        if(self.current_token.type != 'Comment Delimiter' and self.current_token.type != 'Linebreak'):
            childNodes.append(self.printNodes(childNodes))
    
        return ATNode('Print Statements', children_nodes = childNodes)
    
    # ------------------------ASSIGNMENT------------------------
    def assignment(self):
        childNodes = deque()

        if(self.current_token.type == 'Variable Identifier'):
            childNodes.append(ATNode('Variable Identifier', value = self.current_token.value))
        else:
            return False
        
        self.nextToken('Assignment')
        childNodes.append(ATNode('Assignment'))

        if(exprvar := self.exprvar(True)):
            childNodes.append(exprvar)
        else:
            self.nextToken('Expression')
        
        return ATNode('Assignment Statement', children_nodes = childNodes)
    # ------------------------ASSIGNMENT------------------------
    def statement(self):
        childNodes = deque()

        if(visible := self.visible()):
            childNodes.append(visible)
        elif(assignment := self.assignment()):
            childNodes.append(assignment)
        elif(exprvar := self.exprvar(True)):
            childNodes.append(exprvar)
        
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
        while(self.current_token.type != 'Code End'):
            statement = self.statement()
            treeNode.append(statement)
        
        # KTHXBYE
        self.nextToken('Code End')
        treeNode.append(ATNode('Code End'))

        return ATNode('LOLProgram', children_nodes = treeNode)