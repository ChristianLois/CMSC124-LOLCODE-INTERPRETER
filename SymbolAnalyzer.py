# TASK: ADD THE BOOLEAN EXPRESSION

from Symbol import Symbol
import math
import re

class SymbolAnalyzer:
    def __init__(self, atnode_tree):
        self.atnode_tree = atnode_tree
        self.symbol_table = {'IT': Symbol('Noob', value = None)}
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
        elif statement.type == 'Declaration Statement':
            self.declaration(statement)
        elif statement.type == 'Input Statement':
            self.gimmeh(statement)
        elif statement.type == 'Assignment Statement':
            self.assignment(statement)

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

    def declaration(self, statement):
        variable = statement.children_nodes[1].value

        if len(statement.children_nodes) > 2:
            value = self.getValue(statement.children_nodes[3])
            self.symbol_table[variable] = Symbol(value.type, value.value)
        else:
            self.symbol_table[variable] = Symbol('Noob')
    
    def gimmeh(self, statement):
        variable = statement.children_nodes[1].value
        self.lookup(variable)
        temp = input()
        self.symbol_table[variable] = Symbol('Yarn Literal', temp)

    def assignment(self, statement):
        variable = statement.children_nodes[0].value
        self.lookup(variable)
        value = self.getValue(statement.children_nodes[2])
        self.symbol_table[variable] = value
        
    # --------------------Getting Values of expresison/literal/variable-------------------
    def getValue(self, expression):
        expType = expression.children_nodes[0]
        if expType.type == 'Literal':
            litType = expType.children_nodes[0]
            if litType.type == 'Yarn Literal':
                return Symbol('Yarn Literal', litType.children_nodes[0].value)
            elif litType.type == 'Numbr Literal':
                return Symbol(litType.type, int(litType.value))
            elif litType.type == 'Numbar Literal':
                return Symbol(litType.type, float(litType.value))
            else:
                return Symbol(litType.type, litType.value)
        elif expType.type == 'Variable Identifier' or expType.type == 'Implicit Variable':
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
        elif (expression.type == 'And' or
        expression.type == 'Or' or
        expression.type == 'Xor' or
        expression.type == 'Not'):
            return self.boolean(expression)
        elif (expression.type == 'Infinite And' or
        expression.type == 'Infinite Or'):
            return self.infBoolean(expression)
        elif (expression.type == 'Equality Check' or
        expression.type == 'Inequality Check'):
            return self.comparison(expression)
        elif (expression.type == 'Concatenate'):
            return self.smoosh(expression)
    
    def arithmetic(self, expression):
        operands = expression.children_nodes
        op1Exp = self.getValue(operands[1])
        op2Exp = self.getValue(operands[2])

        if op1Exp.type != 'Numbr Literal' and op1Exp.type != 'Numbar Literal':
            temp = self.numTypecast(op1Exp)
            op1 = temp.value
        else:
            op1 = op1Exp.value
        
        if op2Exp.type != 'Numbr Literal' and op2Exp.type != 'Numbar Literal':
            temp = self.numTypecast(op2Exp)
            op2 = temp.value
        else:
            op2 = op2Exp.value

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

    def boolean(self, expression):
        operands = expression.children_nodes
        op1Exp = self.getValue(operands[1])

        if op1Exp.type == 'Troof Literal':
            if op1Exp.value == 'WIN':
                op1 = True
            else:
                op1 = False
        else:
            temp = self.boolTypecast(op1Exp)
            if temp.value == 'WIN':
                op1 = True
            else:
                op1 = False
        
        if expression.type != 'Not':
            op2Exp = self.getValue(operands[2])
            if op2Exp.type == 'Troof Literal':
                if op2Exp.value == 'WIN':
                    op2 = True
                else:
                    op2 = False
            else:
                temp = self.boolTypecast(op2Exp)
                if temp.value == 'WIN':
                    op2 = True
                else:
                    op2 = False
        
        if expression.type == 'And':
            ans = op1 and op2
        elif expression.type == 'Or':
            ans = op1 or op2
        elif expression.type == 'Not':
            ans = not op1
        elif expression.type == 'Xor':
            ans = op1 ^ op2
        
        if ans == True:
            return Symbol('Troof Literal', 'WIN')
        else:
            return Symbol('Troof Literal', 'FAIL')

    def infBoolean(self, expression):
        operations = list(expression.children_nodes)[2:]

        res = self.getValue(expression.children_nodes[1])
        if res.type != 'Troof Literal':
            res = self.boolTypecast(res)
        if res.value == 'WIN':
            ans = True
        else:
            ans = False
        for op in operations:
            res = self.getValue(op)
            if res.type != 'Troof Literal':
                res = self.boolTypecast(res)
            if res.value == 'WIN':
                temp = True
            else:
                temp = False
            if expression.type == 'Infinite And':
                ans = ans and temp
            else:
                ans = ans or temp
        
        if ans == True:
            return Symbol('Troof Literal', 'WIN')
        else:
            return Symbol('Troof Literal', 'FAIL')

    def smoosh(self, expression):
        operations = list(expression.children_nodes)[1:]

        toConcat = ''
        for op in operations:
            temp = self.getValue(op)
            if temp.type != 'Yarn Literal':
                temp = self.strTypecast(temp)
            toConcat += temp.value
        
        return Symbol('Yarn Literal', value = toConcat)

    def comparison(self, expression):
        operands = expression.children_nodes
        op1Exp = self.getValue(operands[1])
        op2Exp = self.getValue(operands[2])

        if op1Exp.type == 'Troof Literal':
            op1 = True
        else:
            op1 = op1Exp.value
        
        if op2Exp.type == 'Troof Literal':
            op2 = True
        else:
            op2 = op2Exp.value

        if expression.type == 'Equality Check':
            ans = op1 == op2
        elif expression.type == 'Inequality Check':
            ans = op1 != op2

        if ans == True:
            return Symbol('Troof Literal', 'WIN')
        else:
            return Symbol('Troof Literal', 'FAIL')
    # --------------------Getting Values of expresison/literal/variable-------------------

    # --------------------Implicit typecasting-------------------
    def boolTypecast(self, expression):
        if expression.type == 'Yarn Literal':
            if expression.value == '':
                return Symbol('Troof Literal', 'FAIL')
            else:
                return Symbol('Troof Literal', 'WIN')
        elif expression.type == 'Numbr Literal' or expression.type == 'Numbar Literal':
            if float(expression.value) == 0:
                return Symbol('Troof Literal', 'FAIL')
            else:
                return Symbol('Troof Literal', 'WIN')
        elif expression.type == 'Noob':
            return Symbol('Troof Literal', 'FAIL')
        else:
            raise Exception(f"Semantic Error:{self.line_number}: {expression.value} cannot be typecasted to troof")
    
    def numTypecast(self, expression):
        print(expression.value)
        if expression.type == 'Yarn Literal':
            if re.match(r"-?[0-9]+\.[0-9]+$", expression.value):
                return Symbol('Numbar Literal', float(expression.value))
            elif re.match(r"-?[0-9]+$", expression.value):
                return Symbol('Numbr Literal', int(expression.value))
            else:
                raise Exception(f"Semantic Error:{self.line_number}: {expression.value} cannot be typecasted to numerical data type")
        elif expression.type == 'Troof Literal':
            if expression.value == 'WIN':
                return Symbol('Numbr Literal', 1)
            else:
                return Symbol('Numbr Literal', 0)
        else:
            raise Exception(f"Semantic Error:{self.line_number}: {expression.value} cannot be typecasted to numerical data type")

    def strTypecast(self, expression):
        if expression.type == 'Numbr Literal':
            return Symbol('Yarn Literal', str(expression.value))
        elif expression.type == 'Numbar Literal':
            return Symbol('Yarn Literal', str(math.floor(expression.value*100)/100))
        elif expression.type == 'Troof Literal':
            return Symbol('Yarn Literal', expression.value)
        else:
            raise Exception(f"Semantic Error:{self.line_number}: {expression.value} cannot be typecasted to yarn")
    # --------------------Implicit typecasting-------------------

    # --------------------Utils-------------------
    def lookup(self, key):
        if key in self.symbol_table.keys():
            return
        
        raise Exception(f"Semantic Error:{self.line_number}: Variable \'{key}\' not declared")
    # --------------------Utils-------------------
            
