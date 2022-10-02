try:
    import pygame

except ImportError:
    import pip

    pip.main(["install", "pygame"])

import math

pygame.init()
pygame.font.init
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 40)

w = 800
h = 800
window = pygame.display.set_mode((w, h))

# Settings
grid_size = 40
diagonals = False

# Colors
black = ((0, 0, 0))
white = ((255, 255, 255))
red = ((255, 0, 0))
green = ((0, 255, 0))
blue = ((0, 0, 255))
aqua = ((0, 255, 255))
yellow = ((255, 255, 0))
grey = ((95, 95, 95))

tile_colors = [white, black, red, green, blue, aqua, yellow]

# Misc
sqsize = round(w / grid_size)

if diagonals:
    moves = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]
else:
    moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]

class Node:
    def __init__(self, pos, came_from, steps, score):
        self.pos = pos
        self.came_from = came_from
        self.steps = steps
        self.score = score

class Game:
    def __init__(self):
        self.algs = ["A*", "Greedy", "Hybrid", "BFS"]
        self.alg = 0
        self.exp = 0
        self.path_len = 0

        # Creating board array (prolly a better way to do this lol)
        self.board = []
        for i in range(grid_size):
            self.board.append([])
            for j in range(grid_size):
                self.board[i].append(0)

        self.start = [round(grid_size/2), round(grid_size / 10) + 1]
        self.end = [self.start[0], grid_size - self.start[1]]

        self.board[self.start[0]][self.start[1]] = 2  # End pos
        self.board[self.end[0]][self.end[1]] = 3  # Start pos

        self.path_found = False

    def take_input(self):
        click_type = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            # Draw wall
            if pygame.mouse.get_pressed()[0]:
                click_type = 1

            # Remove wall
            if pygame.mouse.get_pressed()[2]:
                click_type = 0

            # Change algorithm
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                self.alg -= 1

            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.alg += 1

        # Run algorithm
        if pygame.key.get_pressed()[pygame.K_SPACE] and not self.path_found:
            self.pathfind()
            self.path_found = True

        # Move start
        if pygame.key.get_pressed()[pygame.K_s]:
                click_type = 2

        # Move end
        if pygame.key.get_pressed()[pygame.K_e]:
            click_type = 3

        # Reset
        if pygame.key.get_pressed()[pygame.K_r]:
            self.__init__()

        if pygame.key.get_pressed()[pygame.K_t]:
            self.path_found = False
            self.exp = 0
            self.path_len = 0

            for i in range(grid_size):
                for j in range(grid_size):
                    if self.board[i][j] > 3:
                        self.board[i][j] = 0

        pos = pygame.mouse.get_pos()
        board_pos = [math.floor(pos[1] / sqsize), math.floor(pos[0] / sqsize)]

        # Draw/Remove walls
        if (click_type == 1 or click_type == 0) and not self.path_found:
            if self.board[board_pos[0]][board_pos[1]] <= 1:
                self.board[board_pos[0]][board_pos[1]] = click_type

        # Move start pos
        if click_type == 2 and not self.path_found:
            if self.board[board_pos[0]][board_pos[1]] != 3:

                # Remove old start pos
                self.board[self.start[0]][self.start[1]] = 0
                self.start = [board_pos[0], board_pos[1]]

                # Add new start pos
                self.board[board_pos[0]][board_pos[1]] = click_type

        # Move end pos
        if click_type == 3 and not self.path_found:
            if self.board[board_pos[0]][board_pos[1]] != 2:

                # Remove old end pos
                self.board[self.end[0]][self.end[1]] = 0
                self.end = [board_pos[0], board_pos[1]]

                # Add new end pos
                self.board[board_pos[0]][board_pos[1]] = click_type



    def render(self):
        window.fill(black)

        # Draw grid
        for i in range(grid_size):
            for j in range(grid_size):
                pygame.draw.rect(window, tile_colors[self.board[i][j]], (j * sqsize, i * sqsize, sqsize - 1, sqsize - 1))

        label = font.render(self.algs[self.alg % 4], 1, grey)
        window.blit(label, (10, 10))

        label = font.render("Nodes Explored: " + str(self.exp), 1, grey)
        window.blit(label, (w - label.get_width() - 10, 10))

        label = font.render("Path Length: " + str(self.path_len), 1, grey)
        window.blit(label, (w - label.get_width() - 10, 40))

        # Show fps
        clock.tick(60)
        pygame.display.set_caption("Pathfinding Visualizer / " + str(round(clock.get_fps(), 2)) + " fps")

        pygame.display.update()

    # Pathfinding algorithms
    def pathfind(self):
        # Non-explored nodes
        open_list = [Node(self.start, self.start, 0, 0)]  # Current pos, prev pos, move number, score

        # Already explored nodes
        closed_list = []

        # Loop expansion
        while True:
            # Allow for app to be quit while algorithm is running
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            # Removing already explored nodes from open list
            rem = []
            for i in range(len(open_list)):
                for j in range(len(closed_list)):
                    if open_list[i] == closed_list[j] or self.board[open_list[i].pos[0]][open_list[i].pos[1]] == 4:
                        rem.insert(0, i)

            for r in rem:
                open_list.pop(r)

            # Finding next node to explore
            # A*
            if self.alg % 4 < 3:
                best_score = math.inf
                for i in range(len(open_list)):
                    if open_list[i].score < best_score:
                        best_score = open_list[i].score
                        best_i = i

            # BFS
            elif self.alg % 4 == 3:
                best_i = 0

            # Select new node
            current_node = open_list[best_i]
            open_list.pop(best_i)
            closed_list.append(current_node)
            self.exp += 1

            self.board[current_node.pos[0]][current_node.pos[1]] = 4

            # Update board
            self.board[self.start[0]][self.start[1]] = 2
            self.board[self.end[0]][self.end[1]] = 3

            # Check if path was found
            if current_node.pos == self.end:
                while True:
                    for i in range(len(closed_list)):
                        if closed_list[i].pos == current_node.came_from:
                            if closed_list[i].pos != self.start:
                                self.board[current_node.came_from[0]][current_node.came_from[1]] = 6
                                current_node = closed_list[i]
                                self.path_len += 1
                                self.render()

                            else:
                                return True

            # Evaluate new nodes
            for move in moves:
                child_node = [current_node.pos[0] + move[0], current_node.pos[1] + move[1]]

                # If in bounds
                if child_node[0] >= 0 and child_node[0] < grid_size and child_node[1] >= 0 and child_node[1] < grid_size:

                    # If not in wall or start node
                    if self.board[child_node[0]][child_node[1]] == 0 or self.board[child_node[0]][child_node[1]] == 3:

                        # Get distance to end node
                        h = abs(child_node[0] - self.end[0]) + abs(child_node[1] - self.end[1])

                        # Get final score based on algorithm
                        # A*
                        if self.alg % 4 == 0:
                            f = h + current_node.steps

                        # Greedy
                        elif self.alg % 4 == 1:
                            f = h

                        # Swarm/Hybrid
                        elif self.alg % 4 == 2:
                            f = h * current_node.steps

                        # BFS
                        elif self.alg % 4 == 3:
                            f = 0

                        open_list.append(Node(child_node, current_node.pos, current_node.steps + 1, f))
                        self.board[child_node[0]][child_node[1]] = 5

            self.render()

def main():
    game = Game()

    while True:
        game.take_input()
        game.render()

if __name__ == "__main__":
    main()