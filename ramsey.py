
import itertools
import argparse

def main():
    # Create commandline argument parser
    parser = argparse.ArgumentParser(description="Graph Ramsey CNF Generator.")

    parser.add_argument('fileName', type=str, help="The name of the file to write the cnf to")
    parser.add_argument('graphSize', type=int, help="The number of vertices, N, in the simple connected graph G")
    parser.add_argument('colors', type=int, nargs='+', help="The list of s, t, ... subgraphs")

    # Parse commandline arguments
    args = parser.parse_args()

    fileName = args.fileName
    graphSize = args.graphSize
    colors = args.colors

    # Write CNF to file
    with open(fileName, "w") as f:
        # Write an empty line as a placeholder for the DIMACS header
        f.write("\n")
        
        # Write CNF Clauses to file
        write_color_clauses(f, graphSize, colors)
        write_nonmonochromatic_clauses(f, graphSize, colors)

    # Read the lines from file into a buffer
    fileLines = []
    with open(fileName, "r") as f:
        fileLines = f.readlines()

    # Reopen the file to write the DIMACS header at the top
    with open(fileName, "w") as f:
        # Get the number of vars from the largest-valued edge in the graph
        numVars = edge(graphSize - 1, graphSize, len(colors) - 1, graphSize)

        # Generate DIMACS header
        dimacsHeader = f"p cnf {numVars} {len(fileLines) - 1} \n"

        # Change first line of cnf to DIMACS header
        fileLines[0] = dimacsHeader
        f.writelines(fileLines)

    print("Sucess!")


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
def write_nonmonochromatic_clauses(f, graphSize, colors):
    # Non-monochromatic subgraph clauses
    for c in range(len(colors)):
        # Get subgraph size s for the current color
        subgraphSize = colors[c]

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
    # Get the list 1..N
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

def edge2(i, j, c, graphSize):
    return str(edge(i, j, c, graphSize))


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



if __name__ == "__main__":
    main()
