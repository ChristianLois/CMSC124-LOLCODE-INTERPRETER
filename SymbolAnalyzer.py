# TASK: ADD THE BOOLEAN EXPRESSION

from Symbol import Symbol
import math
import re

class SymbolAnalyzer:
    def __init__(self, atnode_tree):
        self.atnode_tree = atnode_tree
        self.symbol_table = {'IT': Symbol('Noob')}
        self.line_number = 1

    def analyze(self):
        for node in self.atnode_tree.children_nodes:
            if node.type == 'Statement':
                self.analyzeStatement(node.children_nodes)
                self.line_number += 1 
            else:
                self.line_number += 1 
    
    def analyzeStatement(self, node):
        statement = node[0]
        if statement.type == 'Output Statement':
            self.visible(statement)
    
    def visible(self, statement):
        printNodes = list(statement.children_nodes)[1:]
        toPrint = ''
        for i in printNodes:
            expression = i.children_nodes[0]
            expValue = self.getValue(expression)
            if expValue.type != 'Yarn Literal':
                expValue = self.strTypecast(expValue)
            toPrint += expValue.value
        print(toPrint)

    def getValue(self, expression):
        expType = expression.children_nodes[0]
        if expType.type == 'Literal':
            litType = expType.children_nodes[0]
            if litType.type == 'Yarn Literal':
                return Symbol('Yarn Literal', litType.children_nodes[0].value)
            else:
                return Symbol(litType.type, litType.value)
        elif expType.type == 'Variable Identifier':
            variable = expType.value
            self.lookup(variable)
            return self.symbol_table[variable]
        else:
            return self.evaluateExpression(expType.children_nodes[0])
    
    def evaluateExpression(self, expression):
        if (expression.type == 'Addition' or 
        expression.type == 'Subtraction' or
        expression.type == 'Multiplication' or
        expression.type == 'Division' or
        expression.type == 'Modulo' or
        expression.type == 'Min' or
        expression.type == 'Max'):
            return self.arithmetic(expression)
    
    def arithmetic(self, expression):
        operands = expression.children_nodes
        op1Exp = self.getValue(operands[1])
        op2Exp = self.getValue(operands[2])

        if op1Exp.type == 'Numbr Literal':
            op1 = int(op1Exp.value)
        elif op1Exp.type == 'Numbar Literal':
            op1 = float(op1Exp.value)
        else:
            temp = self.numTypecast(op1Exp)
            op1 = temp.value
        
        if op2Exp.type == 'Numbr Literal':
            op2 = int(op2Exp.value)
        elif op2Exp.type == 'Numbar Literal':
            op2 = float(op2Exp.value)
        else:
            temp = self.numTypecast(op2Exp)
            op2 = temp.value

        if expression.type == 'Addition':
            ans = op1 + op2
        elif expression.type == 'Subtraction':
            ans = op1 - op2
        elif expression.type == 'Multiplication':
            ans = op1 * op2
        elif expression.type == 'Division':
            if op1Exp.type == 'Numbr Literal' and op2Exp.type == 'Numbr Literal':
                ans = op1 // op2
            else:
                ans = op1 / op2
        elif expression.type == 'Modulo':
            ans = op1 % op2
        elif expression.type == 'Max':
            ans = max(op1, op2)
        elif expression.type == 'Min':
            ans = min(op1, op2)

        if isinstance(ans, int):
            return Symbol('Numbr Literal', ans)
        else:
            return Symbol('Numbar Literal', ans)
        
    
    def numTypecast(self, expression):
        if expression.type == 'Yarn Literal':
            if re.match(r"-?[0-9]+\.[0-9]+$", expression.value):
                return Symbol('Numbar Literal', float(expression.value))
            elif re.match(r"-?[0-9]+$", expression.value):
                return Symbol('Numbr Literal', int(expression.value))
        elif expression.type == 'Troof Literal':
            if expression.value == 'WIN':
                return Symbol('Numbr Literal', 1)
            else:
                return Symbol('Numbr Literal', 0)
        elif expression.type == 'Noob':
            return Symbol('Numbr Literal', 0)
        else:
            raise Exception(f"Semantic Error:{self.line_number}: {expression.value} cannot be typecasted to numerical data type")

    def strTypecast(self, expression):
        if expression.type == 'Numbr Literal':
            return Symbol('Yarn Literal', str(expression.value))
        elif expression.type == 'Numbar Literal':
            return Symbol('Yarn Literal', str(math.floor(expression.value*100)/100))
        elif expression.type == 'Noob':
            return Symbol('Yarn Literal', '')
        else:
            raise Exception(f"Semantic Error:{self.line_number}: {expression.value} cannot be typecasted to yarn")

    def lookup(self, key):
        if key in self.symbol_table.keys():
            return
        
        raise Exception(f"Semantic Error:{self.line_number}: Variable \'{key}\' not declared")
            
