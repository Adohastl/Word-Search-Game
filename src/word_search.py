import os
import random

# Persian letters for filling the grid
PERSIAN_LETTERS = 'اآبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'

def normalize_word(word):
    """Normalize words."""
    return word.replace('آ', 'ا')

def load_words_from_file(file_path):
    """Load words from a given file and normalize them."""
    with open(file_path, 'r', encoding='utf-8') as file:
        words = [normalize_word(line.strip()) for line in file if len(line.strip()) > 2]
    return words

def load_bad_words():
    """Load bad words from badwords.txt file."""
    try:
        with open("badwords.txt", 'r', encoding='utf-8') as file:
            return [normalize_word(line.strip()) for line in file if line.strip()]
    except FileNotFoundError:
        return []

def choose_category():
    """Allow the user to choose a category file."""
    path = os.path.join("data", "Categories")
    files = [f for f in os.listdir(path) if f.endswith(".txt")]
    for idx, file in enumerate(files):
        print(f"{idx + 1}. {file[:-4]}")
    choice = int(input("Choose a category by number: ")) - 1
    return os.path.join(path, files[choice])

def create_grid(size):
    """Create an empty grid of given size."""
    return [['_' for _ in range(size)] for _ in range(size)]

def random_direction():
    """Return a random direction vector (dx, dy)."""
    return random.choice([
        (0, 1),   # →
        (1, 0),   # ↓
        (1, 1),   # ↘
        (-1, 1),  # ↗
        (0, -1),  # ←
        (-1, 0),  # ↑
        (-1, -1), # ↖
        (1, -1),  # ↙
    ])

def can_place_word(word, grid, x, y, dx, dy, placed_positions):
    """Check if a word can be placed at the given position and direction."""
    size = len(grid)
    word_len = len(word)
    overlap_count = 0

    for i in range(word_len):
        nx, ny = x + dx * i, y + dy * i
        if not (0 <= nx < size and 0 <= ny < size):
            return False
        if grid[nx][ny] != '_':
            if grid[nx][ny] == word[i]:
                overlap_count += 1
                if overlap_count > 1:
                    return False
            else:
                return False
        if (nx, ny) in placed_positions:
            return False
    return True

def place_word(word, grid, placed_positions):
    """Attempt to place a word in the grid."""
    size = len(grid)
    for _ in range(100):  # Try 100 random positions/directions
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        dx, dy = random_direction()
        if can_place_word(word, grid, x, y, dx, dy, placed_positions):
            for i in range(len(word)):
                nx, ny = x + dx * i, y + dy * i
                grid[nx][ny] = word[i]
                placed_positions.add((nx, ny))
            return True
    return False

def fill_grid(grid):
    """Fill empty spaces with random Persian letters."""
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '_':
                grid[i][j] = random.choice(PERSIAN_LETTERS)

def remove_bad_words(grid, bad_words):
    """Remove bad words by replacing one character."""
    size = len(grid)
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    
    for i in range(size):
        for j in range(size):
            for dx, dy in directions:
                for word_length in range(3, size+1):
                    word_chars = []
                    positions = []
                    valid = True
                    for k in range(word_length):
                        ni, nj = i + dx*k, j + dy*k
                        if 0 <= ni < size and 0 <= nj < size:
                            word_chars.append(grid[ni][nj])
                            positions.append((ni, nj))
                        else:
                            valid = False
                            break
                    if valid:
                        word = ''.join(word_chars)
                        if normalize_word(word) in bad_words:
                            replace_pos = random.choice(positions)
                            grid[replace_pos[0]][replace_pos[1]] = random.choice(PERSIAN_LETTERS)

def print_grid(grid):
    """Display the grid."""
    for row in grid:
        print(' '.join(row))
    print()

def get_word_from_grid(grid, start, end):
    """Retrieve word and its positions from grid."""
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    length = max(abs(dx), abs(dy))
    if length == 0:
        return "", []
    dx = dx // length
    dy = dy // length
    word = ""
    positions = []
    for i in range(length + 1):
        x = x1 + dx * i
        y = y1 + dy * i
        if 0 <= x < len(grid) and 0 <= y < len(grid):
            word += grid[x][y]
            positions.append((x, y))
        else:
            return "", []
    return normalize_word(word), positions

def main():
    size = int(input("Enter grid size: "))
    grid = create_grid(size)

    category_file = choose_category()
    all_words = load_words_from_file(category_file)
    dictionary = set(load_words_from_file("data\\dictionary.txt"))
    bad_words = load_bad_words()

    max_words = len(all_words)
    num_words = int(input(f"How many words to place? (1-{max_words}): "))
    words_to_place = random.sample(all_words, min(num_words, max_words))

    placed_positions = set()
    placed_words = []

    for word in words_to_place:
        if place_word(word, grid, placed_positions):
            placed_words.append(word)
        else:
            print(f"Couldn't place the word: {word}")

    fill_grid(grid)
    if bad_words:
        remove_bad_words(grid, bad_words)
    print_grid(grid)

    score = 0
    found_words = set()
    found_positions = set()

    while True:
        try:
            print("Enter your word vector:")
            x1, y1 = map(int, input("Start (row col): ").split())
            x2, y2 = map(int, input("End (row col): ").split())
            selected_word, positions = get_word_from_grid(grid, (x1, y1), (x2, y2))
            print(f"You selected: {selected_word}")

            overlap = len(found_positions & set(positions)) > 1

            if selected_word not in found_words and not overlap:
                if selected_word in placed_words:  # Main word
                    print("🎉 Found a MAIN WORD! (2× points)")
                    score += len(selected_word) * 2
                    found_words.add(selected_word)
                    found_positions.update(positions)
                elif selected_word in dictionary:  # Bonus word
                    print("⭐ Found a BONUS WORD!")
                    score += len(selected_word)
                    found_words.add(selected_word)
                    found_positions.update(positions)
                else:
                    print("❌ Not a valid word.")
            else:
                print("❌ Already found or overlaps too much.")
            print(f"Score: {score}\n")
        except Exception as e:
            print(f"Invalid input. Error: {e}. Try again.")
        if input("Continue? (y/n): ").lower() != "y":
            break

    print("\nPlaced words in this puzzle:")
    print(', '.join(placed_words))
    print(f"Game Over! Final score: {score}")

if __name__ == "__main__":
    main()