import ast
import graphviz

class FunctionCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.graph = {}
        self.current_func = None

    def visit_FunctionDef(self, node):
        self.current_func = node.name
        self.graph[self.current_func] = []
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            called_func = node.func.id
            if self.current_func:
                self.graph[self.current_func].append(called_func)
        self.generic_visit(node)

def build_call_graph(source_code):
    tree = ast.parse(source_code)
    visitor = FunctionCallVisitor()
    visitor.visit(tree)
    return visitor.graph

# Example usage
py_file = '18_hierarchy_rag copy.py'
with open(py_file) as f:
    code = f.read()

graph_dict = build_call_graph(code)

dot = graphviz.Digraph()
for caller, callees in graph_dict.items():
    for callee in callees:
        dot.edge(caller, callee)

dot.render("call_graph", view=True)
