
import matplotlib.pyplot as plt
import networkx as nx
from sympy import symbols, sympify

# Function to recursively add nodes and edges to the graph
def add_nodes_edges(expr, parent=None, G=None):
    if G is None:
        G = nx.DiGraph()

    # If the expression is an atomic element (symbol or number)
    if expr.is_Atom:
        G.add_node(str(expr))  # Add node for the operand
        if parent:
            G.add_edge(parent, str(expr))  # Add edge from parent
    else:
        G.add_node(str(expr))  # Add node for the operator
        if parent:
            G.add_edge(parent, str(expr))  # Add edge from parent to the current node

        # Recursively add children (operands)
        for arg in expr.args:
            add_nodes_edges(arg, str(expr), G)

    return G

# Function to plot the expression tree
def plot_expression_tree(expr_str):
    expr = sympify(expr_str)  # Convert string to symbolic expression
    G = add_nodes_edges(expr)  # Build the binary tree

    # Position the graph in a hierarchical structure
    pos = hierarchy_pos(G, str(expr))

    # Draw the graph using matplotlib
    plt.figure(figsize=(8, 8))
    nx.draw(G, pos, with_labels=True, font_size=10, node_color='lightblue', node_size=2000, font_weight='bold', arrows=False)
    plt.title(f"Binary Tree Representation of: {expr_str}", fontsize=14)
    plt.show()

# Function to compute hierarchical positions for nodes in a tree-like layout
def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    pos = _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
    return pos

def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=None):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    
    if parsed is None:
        parsed = set()
    parsed.add(root)

    neighbors = list(G.neighbors(root))
    if not isinstance(neighbors, list):
        neighbors = [neighbors]
    
    if len(neighbors) != 0:
        dx = width / len(neighbors)
        nextx = xcenter - width/2 - dx/2
        for neighbor in neighbors:
            if neighbor not in parsed:
                nextx += dx
                pos = _hierarchy_pos(G, neighbor, width=dx, vert_gap=vert_gap, vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=root, parsed=parsed)
    
    return pos

# Example usage: Input a mathematical expression here
if __name__ == "__main__":
    expression = "(x + 5) / 3 - (3*x + 8)"
    plot_expression_tree(expression)
