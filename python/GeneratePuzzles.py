import random

def count_inversions(sequence):
    count = 0
    size = len(sequence)
    for i in range(size):
        for j in range(i + 1, size):
            if sequence[i] and sequence[j] and sequence[i] > sequence[j]:
                count += 1
    return count

def is_solvable(sequence):
    SIZE = int(len(sequence) ** 0.5)  # Assuming it's a square grid.
    inversions = count_inversions(sequence)
    
    blank_pos = sequence.index(0)
    row_with_blank = blank_pos // SIZE # count from bottom start at 1
    
    if SIZE % 2 == 0:# grid is even width and height
        # if blank row is even and inversion count is odd or blank row is odd and inversion count is even return True
        if (row_with_blank % 2 == 0 and inversions % 2 != 0) or (row_with_blank % 2 != 0 and inversions % 2 == 0):
            return True
    else: # grid is odd width and height
        if inversions % 2 ==0:
            return True
    return False

def generate_puzzle():
    sequence = list(range(16))
    random.shuffle(sequence)
    return sequence if is_solvable(sequence) else generate_puzzle()

def main(num_puzzles, filename="puzzles.txt"):
    with open(filename, 'w') as file:
        for _ in range(num_puzzles):
            puzzle = generate_puzzle()
            file.write(' '.join(map(str, puzzle)) + '\n')

if __name__ == '__main__':
    NUM_PUZZLES = 500  # Change this to the desired number
    main(NUM_PUZZLES)
