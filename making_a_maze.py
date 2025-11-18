import random
class Maze:
    def __init__(self, grid_size): 
        self.grid_size = grid_size
        self.total_squares = self.grid_size ** 2 
        
        self.setup_start_position()

        self.stack = [self.current_pos]
        self.visited  = {self.current_pos}
        self.node_connections = {i : [] for i in range(self.total_squares)}
        
        self.generate_maze()
    
    def setup_start_position(self):
        x = random.randint(0, self.grid_size - 1)
        y = random.randint(0, self.grid_size - 1)
        self.current_pos = (x, y)
    
    def add_next_position(self, valid_neighbours):
        next_pos = random.choice(valid_neighbours)
        self.add_connection(next_pos)
        self.stack.append(next_pos)
        self.visited.add(next_pos)


    def generate_maze(self): 
        while len(self.visited) < self.total_squares:
            self.current_pos = self.stack[-1]

            valid_neighbours = self.get_valid_neighbours()

            if valid_neighbours:
                self.add_next_position(valid_neighbours)
            else:
                self.stack.pop()           

    def get_valid_neighbours(self):
        valid_neighbours = []
        x, y = self.current_pos

        neighbours = {
            ("north", (x, y + 1)),
            ("east", (x + 1, y)),
            ("south", (x, y - 1)),
            ("west", (x - 1, y)),
        }
    
        for _, (neighbour_x, neighbour_y) in neighbours:
            if self.is_valid_position(neighbour_x, neighbour_y) and (neighbour_x, neighbour_y) not in self.visited:
                valid_neighbours.append((neighbour_x, neighbour_y))

        return valid_neighbours       

    def is_valid_position(self, x, y):
        return 0 <= x < self.grid_size and 0 <= y < self.grid_size

    def add_connection(self, next_pos):
        current_node_number = self.grid_to_num(*self.current_pos)
        next_node_number = self.grid_to_num(*next_pos)

        self.node_connections[current_node_number].append(next_node_number)
        self.node_connections[next_node_number].append(current_node_number)

    def grid_to_num(self, col, row):
        num = row * self.grid_size + col
        return num
    

#the_maze = Maze()




            

