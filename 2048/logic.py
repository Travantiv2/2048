import pygame  # pygame addon
import math    # math functions
import random  # random number generation

pygame.init()  # initialize pygame

FPS = 60  # Regulate the frame rate. Keep it at 60 for smoothness.

WIDTH, HEIGHT = 400, 400  # Keeps the window size a constant square.
ROWS, COLS = 4, 4  # Number of rows and columns in the grid.

RECT_HEIGHT = HEIGHT // ROWS  # Equation to calculate the height of each rectangle.
RECT_WIDTH = WIDTH // COLS  # Equation to calculate the width of each rectangle.

OUTLINE_COLOR = (187, 173, 160)  # Color of the outline of the rectangles.
OUTLINE_THICKNESS = 10  # Thickness of the outline.
BACKGROUND_COLOR = (205, 192, 180)  # Color of the background.
FONT_COLOR = (119, 110, 101)  # Color of the font.

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the window with the specified width and height.
pygame.display.set_caption("2048")  # Set the title of the window.

FONT = pygame.font.SysFont("comicsans", 60, bold=True)  # Set the font and size for the text. We choose comic sans because people hate it.
MOVE_VEL = 20

class Tile:  # Class to represent a tile in the grid.
    COLORS = [
        (237, 229, 218),  # colors for 2
        (238, 225, 201),  # colors for 4
        (243, 178, 122),  # colors for 8
        (246, 150, 101),  # colors for 16
        (247, 124, 95),   # colors for 32
        (247, 94, 59),    # colors for 64
        (237, 208, 115),  # colors for 128
        (237, 204, 99),   # colors for 256
        (237, 202, 80),   # colors for 512
        (237, 197, 63),   # colors for 1024
        (237, 194, 46)    # colors for 2048
    ]
    
    def __init__(self, value, row, col):  # Initialize the tile with a value and its position in the grid.
        self.value = value  # Set the value of the tile.
        self.row = row  # Set the row of the tile.
        self.col = col  # Set the column of the tile.
        self.x = col * RECT_WIDTH  # Calculate the x-coordinate based on the column.
        self.y = row * RECT_HEIGHT  # Calculate the y-coordinate based on the row.

    def get_color(self):  # Function to get the color of the tile based on its value.
        color_index = int(math.log2(self.value)) - 1  # Calculate the index of the color based on the value of the tile.
        color = self.COLORS[color_index]  # Ensure the value is a power of 2 and within the range of defined colors.
        return color  # Return the color of the tile based on its value.

    def draw(self, window):  # Function to draw the tile on the window.
        color = self.get_color()  # Get the color of the tile.
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))  # Draw the rectangle for the tile with the calculated color.

        text = FONT.render(str(self.value), True, FONT_COLOR)  # Render the text for the tile value.
        window.blit(text, (self.x + (RECT_WIDTH - text.get_width()) // 2,
                           self.y + (RECT_HEIGHT - text.get_height()) // 2))  # Draw the text in the center of the tile.

    def set_pos(self, ceil=False):  # Function to set the position of the tile based on its row and column.
        if ceil:  # If ceil is True, round the position to the nearest integer.
            self.row = math.ceil(self.y / RECT_HEIGHT) # Round the row to the nearest integer.
            self.col = math.ceil(self.x / RECT_WIDTH) # Round the column to the nearest integer.
        else:  # If ceil is False, round the position to the nearest integer.
            self.row = math.floor(self.y / RECT_HEIGHT) # Round the row down to the nearest integer.
            self.col = math.floor(self.x / RECT_WIDTH) # Round the column down to the nearest integer.     


    def move(self, delta):  # Function to move the tile by a certain delta.
        self.x += delta[0]  # Update the x-coordinate by the delta value in the x direction.
        self.y += delta[1]  # Update the y-coordinate by the delta value in the y direction.

def draw_grid(window):  # Function to draw the grid.
    for row in range(1, ROWS):  # Loop through each row.
        y = row * RECT_HEIGHT  # Calculate the y-coordinate for the rectangle.
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)  # Draw horizontal lines for the grid.

    for col in range(1, COLS):  # Loop through each column.
        x = col * RECT_WIDTH  # Calculate the x-coordinate for the rectangle.
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)  # Draw vertical lines for the grid.

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)  # Draw the outer rectangle with the outline color and thickness.

def draw(window, tiles):  # Function to draw the grid and the background.
    window.fill(BACKGROUND_COLOR)  # Fill the window with the background color.
    
    for tile in tiles.values():  # Loop through each tile in the tiles dictionary and draw it.
        tile.draw(window)  # Call the draw method of each tile to render it on the window.

    draw_grid(window)  # Call the function to draw the grid.
    pygame.display.update()  # Update the display to show the changes based on how we wrote them.


def get_random_pos(tiles):  # Function to get a random position for a new tile.
    row = None  # Initialize row to None.
    col = None  # Initialize column to None.
    while True:
        row = random.randrange(0, ROWS) # Generate a random row index.
        col= random.randrange(0, COLS) # Generate a random column index.

        if f"{row},{col}" not in tiles:  # Check if the position is already occupied by a tile.
            break  # If the position is not occupied, break the loop.

    return row, col  # Return the random row and column indices.


def move_tiles(window, tiles, clock, direction):# Function to move tiles in the specified direction.
    updated = True # Flag to check if any tiles were moved.
    blocks = set() #tells us which blocks have been merged

    if direction == "left": # Function to move tiles to the left.
        sort_func = lambda x: x.col # Sort tiles by column for left movement.
        reverse = False # No need to reverse the order for left movement.
        delta = (-MOVE_VEL, 0 ) # Move left by MOVE_VEL pixels.
        boundary_check = lambda tile: tile.col == 0 # Check if the tile is at the left edge.
        get_next_tile = lambda tile: tiles.get(f"{tile.row},{tile.col - 1}") # Get the next tile to the left.
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL # Check if the tile can merge with the next tile.
        move_check = lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL # Check if the tile can move to the next tile's position.
        ceil = True # Set ceil to True for left movement.    

    elif direction == "right": # Function to move tiles to the right.
        sort_func = lambda x: x.col # Sort tiles by column for right movement.
        reverse = True # Reverse the order for right movement.
        delta = (MOVE_VEL, 0) # Move right by MOVE_VEL pixels.
        boundary_check = lambda tile: tile.col == COLS - 1 # Check if the tile is at the right edge.
        get_next_tile = lambda tile: tiles.get(f"{tile.row},{tile.col + 1}") # Get the next tile to the right.
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL # Check if the tile can merge with the next tile.
        move_check = lambda tile, next_tile: tile.x < next_tile.x - RECT_WIDTH - MOVE_VEL # Check if the tile can move to the next tile's position.
        ceil = False # Set ceil to False for right movement.

    elif direction == "up": # Function to move tiles up.
        sort_func = lambda x: x.row # Sort tiles by row for up movement.
        reverse = False # No need to reverse the order for up movement.
        delta = (0, -MOVE_VEL) # Move up by MOVE_VEL pixels.
        boundary_check = lambda tile: tile.row == 0 # Check if the tile is at the top edge.
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1},{tile.col}") # Get the next tile above.
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL # Check if the tile can merge with the next tile.
        move_check = lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL # Check if the tile can move to the next tile's position.
        ceil = True # Set ceil to True for up movement.

    elif direction == "down": # Function to move tiles down.
        sort_func = lambda x: x.row # Sort tiles by row for down movement.
        reverse = True # Reverse the order for down movement.
        delta = (0, MOVE_VEL) # Move down by MOVE_VEL pixels.
        boundary_check = lambda tile: tile.row == ROWS - 1 # Check if the tile is at the bottom edge.
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1},{tile.col}") # Get the next tile below.
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL # Check if the tile can merge with the next tile.
        move_check = lambda tile, next_tile: tile.y < next_tile.y - RECT_HEIGHT - MOVE_VEL # Check if the tile can move to the next tile's position.
        ceil = False # Set ceil to False for down movement.
    
    while updated:  # Continue moving tiles until no more tiles can be moved.
        clock.tick(FPS)  # Regulate the frame rate.
        updated = False  # Reset the updated flag to False for the next iteration.
        sorted_tiles = sorted(tiles.values(),key=sort_func, reverse=reverse)  # Sort the tiles based on the specified sort function.

        for i, tile in enumerate(sorted_tiles):  # Loop through each tile in the sorted list.
            if boundary_check(tile): # Check if the tile is at the boundary.
                continue  # Skip tiles that are at the boundary (left edge for left movement).
            next_tile = get_next_tile(tile)  # Get the next tile in the specified direction.
            if not next_tile:
                tile.move(delta)  # Move the tile in the specified direction if there is no next tile.
            elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks: # Check if the current tile can merge with the next tile.
                if merge_check(tile, next_tile): # Check if the tile can merge with the next tile.
                    tile.move(delta)  # Move the tile in the specified direction if it can merge with the next tile.
                else:
                    next_tile.value *= 2
                    sorted_tiles.pop(i)  # Remove the current tile from the sorted list after merging.
                    blocks.add(next_tile)  # Add the next tile to the blocks set to indicate it has been merged.
            elif move_check (tile, next_tile): # Check if the tile can move to the next tile's position.
                tile.move(delta) # Move the tile in the specified direction if it can move to the next tile's position.
            else: # If none of the conditions are met, we skip to the next tile
                continue # If none of the conditions are met, continue to the next tile.
            
            tile.set_pos(ceil)  # Set the position of the tile based on its new coordinates.
            updated = True # Set the updated flag to True to indicate that a tile has been moved or merged.

        update_tiles(window, tiles, sorted_tiles)

    return end_move(tiles)  # Call the end_move function to check if the game has ended.

def end_move(tiles):  # Function to check if the game has ended.
    if len(tiles) == 16:
        return "Game Over"  # If all tiles are occupied, the game is over.

    row, col = get_random_pos(tiles)  # Get a random position for a new tile.
    tiles[f"{row},{col}"] = Tile(random.choice([2, 4]), row, col)  # Add a new tile with a random value (2 or 4) at the random position.
    return "continue"  # Return "continue" to indicate that the game can continue.

def update_tiles(window, tiles, sorted_tiles):  # Function to update the tiles in the grid.
    tiles.clear()  # Clear the existing tiles dictionary.
    for tile in sorted_tiles:  # Loop through each tile in the sorted list.
        tiles[f"{tile.row},{tile.col}"] = tile  # Add the tile to the tiles dictionary with its position as the key.

    draw(window, tiles) # Call the draw function to render the updated tiles on the window.

def generate_tiles():  # Function to generate the initial tiles in the grid.
    tiles = {}  # Dictionary to hold the tiles.
    for _ in range(2): # Loop to generate two initial tiles.
        row, col = get_random_pos(tiles)  # Get a random position for the tile.
        tiles[f"{row},{col}"] = Tile(2, row, col)  # Create a new tile with value 2 at the random position.
    return tiles  # Return the dictionary of tiles.

def main(window):  # Main function to run the game.
    clock = pygame.time.Clock()  # Create a clock to regulate the frame rate.
    run = True  # Variable to control the game loop.
    tiles = generate_tiles()  # Generate the initial tiles in the grid.

    while run:  # Main game loop.
        clock.tick(FPS)  # Limit the frame rate to FPS.

        for event in pygame.event.get():  # Check for events.
            if event.type == pygame.QUIT:  # If the quit event is triggered, set run to False.
                run = False  # If the quit event is triggered, stop the game.
                break  # Break out of the event loop.

            if event.type == pygame.KEYDOWN: # If a key is pressed, check which key it is.
                if event.key == pygame.K_LEFT: # If the left arrow key is pressed, move tiles to the left.
                    move_tiles(window, tiles, clock, "left")  # Call the move_tiles function to move tiles to the left.
                elif event.key == pygame.K_RIGHT: # If the right arrow key is pressed, move tiles to the right.
                    move_tiles(window, tiles, clock, "right") # Call the move_tiles function to move tiles to the right.
                elif event.key == pygame.K_UP: # If the up arrow key is pressed, move tiles up.
                    move_tiles(window, tiles, clock, "up")  # Call the move_tiles function to move tiles up.
                elif event.key == pygame.K_DOWN: # If the down arrow key is pressed, move tiles down.
                    move_tiles(window, tiles, clock, "down") # Call the move_tiles function to move tiles down.


        draw(window, tiles)  # Pass tiles to draw so they are rendered.

    pygame.quit()  # Quit pygame when the game loop ends.

if __name__ == "__main__":  # If this file is run directly, start the game.
    main(WINDOW)  # The main function is called to start the game.