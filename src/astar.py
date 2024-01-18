class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Cost from start to current node
        self.h = 0  # Estimated cost from current node to goal
        self.f = 0  # Total cost

def heuristic(a, b):
    # Using Manhattan distance as heuristic
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(occupancy_grid, start_node, goal_node):
    # Initialize both open and closed list
    open_list = []
    closed_list = set()

    # Add the start node
    start = Node(start_node)
    start.g = start.h = start.f = 0
    open_list.append(start)

    # Loop until you find the end
    while open_list:
        # Get the current node (the node with the lowest f value)
        current_node = open_list[0]
        print(f"Node: {current_node.position}")
        print(f"OL Size: {len(open_list)}")
        print(f"CL Size: {len(closed_list)}\n")
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.add(current_node.position)

        # Found the goal
        if current_node.position == goal_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range and walkable
            if node_position[0] > (len(occupancy_grid) - 1) or node_position[0] < 0 or node_position[1] > (len(occupancy_grid[0]) - 1) or node_position[1] < 0:
                continue
            if occupancy_grid[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node and set parent
            new_node = Node(node_position, current_node)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if child.position in closed_list:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = heuristic(child.position, goal_node)
            child.f = child.g + child.h

            # Child is already in the open list and has larger g
            if any(open_node.position == child.position and child.g > open_node.g for open_node in open_list):
                continue

            # Add the child to the open list
            open_list.append(child)

    # Return an empty list if no path is found
    return []

# Usage

