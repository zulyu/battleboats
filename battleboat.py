"""
This module implements the game logic for Battleboats.
"""

import random
import time

def validate_grid_place_ship(grid, start_row, end_row, start_col, end_col):
    """
    Validate the grid and place a ship if valid.
    """
    all_valid = True
    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if grid[r][c] != ".":
                all_valid = False
                break
    if all_valid:
        for r in range(start_row, end_row):
            for c in range(start_col, end_col):
                grid[r][c] = "O"
    return all_valid


def place_ship(grid, ship_info):
    """
    Try to place a ship on the grid.
    """
    grid_size = len(grid)
    row, col, direction, length = ship_info
    start_row, end_row, start_col, end_col = row, row + 1, col, col + 1

    if direction == "left":
        if col - length < 0:
            return False
        start_col = col - length + 1
    elif direction == "right":
        if col + length >= grid_size:
            return False
        end_col = col + length
    elif direction == "up":
        if row - length < 0:
            return False
        start_row = row - length + 1
    elif direction == "down":
        if row + length >= grid_size:
            return False
        end_row = row + length

    return validate_grid_place_ship(grid, start_row, end_row, start_col, end_col)

def create_grid(grid_size, num_ships):
    """
    Create the grid and place ships randomly.
    """
    random.seed(time.time())

    grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]

    while num_ships > 0:
        random_row = random.randint(0, grid_size - 1)
        random_col = random.randint(0, grid_size - 1)
        direction = random.choice(["left", "right", "up", "down"])
        ship_size = random.randint(3, 5)
        ship_info = (random_row, random_col, direction, ship_size)  # Define ship_info
        if place_ship(grid, ship_info):  # Pass ship_info to place_ship
            num_ships -= 1

    return grid

def print_grid(grid):
    """
    Print the grid.
    """
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    debug_mode = False

    alphabet = alphabet[:len(grid) + 1]

    for row, row_data in enumerate(grid):
        print(alphabet[row], end=") ")
        for col_data in row_data:
            if col_data == "O":
                if debug_mode:
                    print("O", end=" ")
                else:
                    print(".", end=" ")
            else:
                print(col_data, end=" ")
        print("")

    print("  ", end=" ")
    for i in range(len(grid[0])):
        print(str(i), end=" ")
    print("")

def accept_valid_bullet_placement(grid, alphabet):
    """
    Accept valid bullet placement.
    """
    is_valid_placement = False
    row = -1
    col = -1
    while not is_valid_placement:
        placement = input("Enter row (A-J) and column (0-9) such as A3: ")
        placement = placement.upper()
        if not (0 < len(placement) <= 2 and placement[0] in alphabet and placement[1].isdigit()):
            print("Error: Please enter one row (A-J) and one column (0-9) such as A3.")
            continue
        row = alphabet.find(placement[0])
        col = int(placement[1])
        if not (0 <= row < len(grid) and 0 <= col < len(grid[0])):
            print("Error: Please enter valid row (A-J) and column (0-9).")
            continue
        if grid[row][col] in ("#", "X"):
            print("You have already shot a bullet here, pick somewhere else.")
            continue
        if grid[row][col] in (".", "O"):
            is_valid_placement = True
    return row, col

def check_for_ship_sunk(row, col, grid):
    """
    Check if a ship is sunk.
    """
    for r, row_data in enumerate(grid):
        for c, col_data in enumerate(row_data):
            if col_data == "O" and (r != row or c != col) and col_data != "X":
                return False
    return True

def shoot_bullet(grid, bullets_l):
    """
    Shoot a bullet at a specified location.
    """
    row, col = accept_valid_bullet_placement(grid, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    print("")
    print("----------------------------")

    if grid[row][col] == ".":
        print("You missed, no ship was shot.")
        grid[row][col] = "#"
    elif grid[row][col] == "O":
        print("You hit!", end=" ")
        grid[row][col] = "X"
        if check_for_ship_sunk(row, col, grid):
            print("A ship was completely sunk!")
        else:
            print("A ship was shot.")
    bullets_l -= 1

    return bullets_l

def check_for_game_over(num_ships_s, num_ships, bullets_l):
    """
    Check if the game is over.
    """
    result = None
    if num_ships == num_ships_s:
        result = "win"
    elif bullets_l <= 0:
        result = "lose"

    return result, num_ships_s, bullets_l

def calculate_accuracy_percentage(num_ships, num_ships_s):
    """
    Calculate the accuracy percentage.
    """
    return ((num_ships_s / num_ships) * 100) if num_ships > 0 else 0

def main():
    """
    Main function to start the game.
    """
    print("-----Welcome to Battleships-----")

    grid_size = int(input("Enter grid size you want to use: "))
    num_ships = int(input("Enter number of ships you want to use: "))
    bullets_l = int(input("Enter number of bullets you want to use: "))
    num_ships_s = 0

    grid = create_grid(grid_size, num_ships)

    game_over = False

    while not game_over:
        print_grid(grid)
        print("Number of ships remaining:", num_ships - num_ships_s)
        print("Number of bullets left:", bullets_l)
        bullets_l = shoot_bullet(grid, bullets_l)

        result, num_ships_s, bullets_l = check_for_game_over(num_ships_s, num_ships, bullets_l)
        if result:
            print("Game Over!")
            if result == "win":
                print("Congrats you won!")
            else:
                print("Sorry, you lost! You ran out of bullets, try again next time!")
            print("Number of ships sunk:", num_ships_s)
            accuracy = calculate_accuracy_percentage(num_ships, num_ships_s)
            print(f"Accuracy Percentage: {accuracy:.2f}%")
            game_over = True

if __name__ == "__main__":
    main()
