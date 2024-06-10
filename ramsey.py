
import itertools

def main():
    colors = ["red", "blue"]
    color_subgraph_sizes = [3, 3]
    graphSize = 4

    nVar = 5
    with open("test.cnf", "w") as f:
        f.write("p cnf " + str(nVar) + "TODO!!! " + str(len(colors)) + "\n")
        
        write_color_clauses(f, graphSize, colors)
        
        write_nonmonochromatic_clauses(f, graphSize, colors, color_subgraph_sizes)

    print("Closed")

# Hard coded test case from "Computation of new diagonal graph Ramsey numbers"
# By Professor Richard M. Low
def write_test(fileName):
    graphSize = 4
    red = 0
    blue = 1
    with open(fileName, "w") as f:
        # Color Clauses
        f.write(f"{edge2(1, 2, red, graphSize)} {edge2(1, 2, blue, graphSize)} 0\n")
        f.write(f"-{edge2(1, 2, red, graphSize)} -{edge2(1, 2, blue, graphSize)} 0\n")
        f.write(f"{edge2(1, 3, red, graphSize)} {edge2(1, 3, blue, graphSize)} 0\n")
        f.write(f"-{edge2(1, 3, red, graphSize)} -{edge2(1, 3, blue, graphSize)} 0\n")
        f.write(f"{edge2(1, 4, red, graphSize)} {edge2(1, 4, blue, graphSize)} 0\n")
        f.write(f"-{edge2(1, 4, red, graphSize)} -{edge2(1, 4, blue, graphSize)} 0\n")
        f.write(f"{edge2(2, 3, red, graphSize)} {edge2(2, 3, blue, graphSize)} 0\n")
        f.write(f"-{edge2(2, 3, red, graphSize)} -{edge2(2, 3, blue, graphSize)} 0\n")
        f.write(f"{edge2(2, 4, red, graphSize)} {edge2(2, 4, blue, graphSize)} 0\n")
        f.write(f"-{edge2(2, 4, red, graphSize)} -{edge2(2, 4, blue, graphSize)} 0\n")
        f.write(f"{edge2(3, 4, red, graphSize)} {edge2(3, 4, blue, graphSize)} 0\n")
        f.write(f"-{edge2(3, 4, red, graphSize)} -{edge2(3, 4, blue, graphSize)} 0\n")

        # Non-monochromatic subgraph clauses
        f.write(f"{edge2(1, 2, red, graphSize)} {edge2(1, 3, red, graphSize)} {edge2(2, 3, red, graphSize)} 0\n")
        f.write(f"{edge2(1, 2, red, graphSize)} {edge2(1, 4, red, graphSize)} {edge2(2, 4, red, graphSize)} 0\n")
        f.write(f"{edge2(1, 3, red, graphSize)} {edge2(1, 4, red, graphSize)} {edge2(3, 4, red, graphSize)} 0\n")
        f.write(f"{edge2(2, 3, red, graphSize)} {edge2(2, 4, red, graphSize)} {edge2(3, 4, red, graphSize)} 0\n")

        f.write(f"{edge2(1, 2, blue, graphSize)} {edge2(1, 3, blue, graphSize)} {edge2(2, 3, blue, graphSize)} 0\n")
        f.write(f"{edge2(1, 2, blue, graphSize)} {edge2(1, 4, blue, graphSize)} {edge2(2, 4, blue, graphSize)} 0\n")
        f.write(f"{edge2(1, 3, blue, graphSize)} {edge2(1, 4, blue, graphSize)} {edge2(3, 4, blue, graphSize)} 0\n")
        f.write(f"{edge2(2, 3, blue, graphSize)} {edge2(2, 4, blue, graphSize)} {edge2(3, 4, blue, graphSize)} 0\n")


def edge2(i, j, c, graphSize):
    return str(edge(i, j, c, graphSize))

# Write color clauses to cnf for each edge of graph
def write_color_clauses(f, graphSize, colors):
    # For (i, j) s.t. 1 <= i < j <= N
    for i in range(1, graphSize + 1):
        for j in range(i + 1, graphSize + 1):
            colorStr1 = ""
            colorStr2 = ""
            for c in range(len(colors)):
                # FIX XOR on 3 colors
                colorStr1 += str(edge(i, j, c, graphSize)) + " "
                colorStr2 += "-" + str(edge(i, j, c, graphSize)) + " "

            f.write(colorStr1 + "0\n")
            f.write(colorStr2 + "0\n")

# Write noon-monochromatic subgraph clauses to cnf for each colored K_s
def write_nonmonochromatic_clauses(f, graphSize, colors, color_subgraph_sizes):
    # Non-monochromatic subgraph clauses
    for c in range(len(colors)):
        # Get subgraph size s for the current color
        subgraphSize = color_subgraph_sizes[c]

        # Get all unique subsets of N choose S, where S = subgraph size
        combinations = generate_combinations(graphSize, subgraphSize)

        # Write clauses of form "!red(1, 2) || !red(1, 3) || !red(2, 3)..."
        for combination in combinations:
            colorStr = ""

            # Get each unique (i, j) from the combination
            for i in range(len(combination)):
                for j in range(i + 1, len(combination)):
                    colorStr += str(edge(combination[i], combination[j], c, graphSize)) + " "
            f.write(colorStr + "0\n")


# Get the set of N Choose K combinations
def generate_combinations(n, k):
    # 0..N
    elements = list(range(1, n + 1))

    # Generate combinations
    combinations = list(itertools.combinations(elements, k))

    return combinations


# Get a unique variable (integer) corresponding to the given edge
def edge(i, j, c, graphSize):
    # Validate input
    if not (1 <= i < j <= graphSize):
        raise ValueError(f"Invalid value for i or j: ({i}, {j})")

    # Adjust the indices to be zero-based for calculation purposes
    i -= 1
    j -= 1

    # Calculate unique index based on combination formula
    # Total number of edges in the graph (combinations of two nodes)
    total_edges = graphSize * (graphSize - 1) // 2
    
    # Calculate the base index for the color
    color_base_index = total_edges * c

    # Calculate the unique index for the edge (i, j)
    edge_index = (i * (2 * graphSize - i - 1)) // 2 + (j - i - 1)

    # Combine the indices
    unique_index = color_base_index + edge_index
    
    # Add 1 to start indexing variables at 1
    return unique_index + 1
    

# # Get a unique variable (integer) corresponding to the given edge
# def edge(i, j, c, graphSize):
#     # Validate input
#     if not (1 <= i < j <= graphSize):
#         raise ValueError(f"Invalid value for i or j: ({i}, {j})")
#
#     # Calculate unique index based on combination formula
#     # Triangle numbers formula: T(n) = n * (n + 1) / 2
#     index = (graphSize * (graphSize - 1) // 2) * c  # Base index for colors
#     index += (graphSize - i) * (graphSize - i - 1) // 2  # Increment based on i
#     index += (j - i - 1)  # Increment based on j
#     return index


if __name__ == "__main__":
    main()
