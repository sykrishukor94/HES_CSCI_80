
def hill_climb(list, start_index):
    curr = list[start_index]
    while True:
        left = start_index - 1
        right = start_index + 1
        if left < 0 or right > len(list):
            break
        neighbor = max(list[left], list[right])
        if neighbor <= curr:
            return curr
        curr = neighbor

list = [1, 3, 6, 6, 5, 4, 5, 7, 2, 1]
print(hill_climb(list, 5))