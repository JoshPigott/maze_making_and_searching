import tkinter as tk
import making_a_maze 
import searching_algorithms
from collections import deque

GRID_WIDTH_IN_SQUARES = 20
GRID_WIDTH_IN_CELLS = GRID_WIDTH_IN_SQUARES * 2 + 1

SQUARE_LEN = 35  
WALL_LEN = 3
SQUARE_PLUS_WALL_LEN = SQUARE_LEN + WALL_LEN
CANVAS_WIDTH = (SQUARE_PLUS_WALL_LEN * GRID_WIDTH_IN_SQUARES) + WALL_LEN # This is very unreadable


WALL = "green"
OPEN = "black"
CURRENT_CELL = "lightblue"
START = "darkblue"
END = "gold"
PATH = "purple"

DELAY_TIME= 50

class Cell: 
    """I need to look at this funcaiton somtime and see if I need all thoose these attributes"""
    def __init__(self, canvas, row, col): # Is it better to also make canvas a class attribaute or somthing
        self.row = row
        self.col = col
        self.make_cell_object(canvas)
        self.give_cell_number()
        
    
    def give_cell_number(self):
        if self.row % 2 == 0 or self.col % 2 == 0:
            self.cell_num = None
        else:
            square_row = (self.row - 1) // 2
            square_col = (self.col - 1) // 2
            
            self.cell_num = square_row * GRID_WIDTH_IN_SQUARES + square_col
        
    def update_colour(self, canvas, colour):
        canvas.itemconfig(self.GUI_square, fill=colour)
        


    def get_start_position_of_cell(self): # This is not very readable
        y_start = (self.row // 2) * SQUARE_PLUS_WALL_LEN
        x_start = (self.col // 2) * SQUARE_PLUS_WALL_LEN

        if self.row % 2 == 1:
            y_start += WALL_LEN
            y_end = y_start + SQUARE_LEN
        else:
            y_end = y_start + WALL_LEN

        if self.col % 2 == 1:
            x_start += WALL_LEN
            x_end = x_start + SQUARE_LEN
        else:
            x_end = x_start + WALL_LEN

        return x_start, y_start, x_end, y_end


    def make_cell_object(self, canvas):
        self.get_dimensions()
        colour = self.setup_grid_colour()
        x_start, y_start, x_end, y_end = self.get_start_position_of_cell()
        self.GUI_square = canvas.create_rectangle(x_start, y_start, x_end, y_end, fill=colour, outline="")




    def setup_grid_colour(self):
        if self.width == SQUARE_LEN and self.height == SQUARE_LEN:
            return "black"
        else:
            return "green"

    def get_dimensions(self):
        if self.row % 2 == 0:
            self.height = WALL_LEN
        else: 
            self.height = SQUARE_LEN

        if self.col % 2 == 0:
            self.width = WALL_LEN     
        else:
            self.width = SQUARE_LEN



class DisplayMaze:
    def __init__(self):
        self.the_maze = making_a_maze.Maze(GRID_WIDTH_IN_SQUARES)
        self.found_end = False

        self.start = None
        self.end = None

    def make_cells_and_walls(self):
        self.grid = []

        for row in range(GRID_WIDTH_IN_CELLS):
            self.grid.append([])

            for col in range(GRID_WIDTH_IN_CELLS):
                cell = Cell(self.canvas, row, col)
                self.grid[row].append(cell)

    def square_grid_to_cell_grid(self, row, col):
        row = (row * 2) + 1
        col = (col * 2) + 1
        return row, col
    
    def num_to_grid(self, num): 
        row = num // GRID_WIDTH_IN_SQUARES
        col = num % GRID_WIDTH_IN_SQUARES

        row, col = self.square_grid_to_cell_grid(row, col)     
        return row, col
    
  
    def remove_walls_between_connected_cells(self, node_connections): 
        for cell_num, connected_nodes in node_connections.items():
            cell_row, cell_col = self.num_to_grid(cell_num)

            for neighbor_num in connected_nodes:
                neighbor_row, neighbor_col = self.num_to_grid(neighbor_num)

                if cell_row < neighbor_row: 
                    self.grid[neighbor_row-1][neighbor_col].update_colour(self.canvas, OPEN)

                elif cell_col < neighbor_col: 
                    self.grid[neighbor_row][neighbor_col-1].update_colour(self.canvas, OPEN)
    


    def is_on_wall(self, position_x, position_y):
        if (position_x % SQUARE_PLUS_WALL_LEN) < WALL_LEN: 
            return True
        if (position_y % SQUARE_PLUS_WALL_LEN) < WALL_LEN: 
            return True 
        return False
        
    def draw_start(self):   
        self.start.update_colour(self.canvas, START)

    def draw_end(self):
        self.end.update_colour(self.canvas, END)

    
    def get_clicked_square(self, position_x, position_y):
        row = position_y // SQUARE_PLUS_WALL_LEN
        col = position_x // SQUARE_PLUS_WALL_LEN
        row, col = self.square_grid_to_cell_grid(row, col)
        return row, col
    
    def update_start_and_end(self, event):
        if self.is_on_wall(event.x, event.y):
            return
        
        row, col = self.get_clicked_square(event.x, event.y) 
        square = self.grid[row][col]

        if self.start is None:
            self.start = square
            self.current = self.start
            self.draw_start() # Idk if need this line could I just use this self.start.update_colour(START)

        elif self.end is None and square != self.start:
            self.end = square
            self.draw_end()
            self.canvas.unbind("<Button-1>")
            
            



    def check_if_found_end(self):
        if self.current == self.end:
            return True
        else:
            return False

    def draw_path(self, current, came_from):
        while current.cell_num in came_from:
            if current != self.end:
                current.update_colour(self.canvas, PATH)

            next_cell_num = came_from[current.cell_num] 
            row, col = self.num_to_grid(next_cell_num)
            current = self.grid[row][col]

    def move_square(self, move_to, came_from): 
            if self.found_end:
                return
            
            if self.current != self.start:  
                self.current.update_colour(self.canvas, OPEN)

            nex_row, nex_col = self.num_to_grid(move_to)
            self.current = self.grid[nex_row][nex_col]

            if self.check_if_found_end():
                self.draw_path(self.end, came_from)
                self.found_end = True

            elif self.current != self.start: 
                self.current.update_colour(self.canvas, CURRENT_CELL)


    def animate_path(self, path_list, came_from):
        delay = DELAY_TIME
        for neighbour in path_list:                
            self.canvas.after(delay, self.move_square, neighbour, came_from) 
            delay += DELAY_TIME

    def run_searching_algorithm(self, event=None): 
        if self.start is None or self.end is None:
            return
        
        self.canvas.unbind('<space>') 
        # Are the next two lines of code to long?
        path_list, came_from = searching_algorithms.DFS(self.the_maze.node_connections, current_node=self.start.cell_num)
        #path_list, came_from = searching_algorithms.BFS(self.the_maze.node_connections, current_nodes=deque([self.start.cell_num]))
        self.animate_path(path_list, came_from)
 
        

    def main(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=CANVAS_WIDTH, height=CANVAS_WIDTH, highlightthickness=0)
        self.canvas.pack()
        
        
        self.make_cells_and_walls()
        self.remove_walls_between_connected_cells(self.the_maze.node_connections) 

        self.canvas.bind("<Button-1>", self.update_start_and_end)
        self.root.bind('<space>', self.run_searching_algorithm)


        self.root.mainloop()
        

maze = DisplayMaze()
maze.main()





# Next time



"""
This I stil want to do untill the project is done
Make A_star search

"""


