import sys


def count_inversions(sequence):
    count = 0
    for i in range(len(sequence)-1):
        j = i+1
        a = sequence[i]
        b = sequence[j]
        if (a and b) and a > b:
            count+=1
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
        
file_path = sys.argv[1]
# Get a sequence from the user
with open(file_path) as f:
    lines = f.readlines()
    for line in lines:
        sequence = [int(x) for x in line.strip().split(" ")]

        # Check if the entered sequence is solvable and print the result
        if is_solvable(sequence):
            print("The sequence is solvable." + str(sequence))
        else:
            print("The sequence is not solvable."+str(sequence))

