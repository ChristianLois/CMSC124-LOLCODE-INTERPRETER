from Symbol import Symbol

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
            toPrint = self.getValue(expression)
    
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
            self.evaluateExpression(expType)
    
    def evaluateExpression(self, expression):
        pass
    
    def lookup(self, key):
        if key in self.symbol_table.keys():
            return
        
        raise Exception(f"Semantic Error:{self.line_number}: Variable \'{key}\' not declared")
            
