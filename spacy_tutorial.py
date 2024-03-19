def is_contained_in(a, b):
    return any(elem in b for elem in a)

# Example usage:
FANBOYS = ['for', 'and', 'nor', 'but', 'or', 'yet', 'so']
list_b = ['a', 'staycation', 'instead', 'of', 's']

result = is_contained_in(FANBOYS, list_b)
print(result)  # Output: True
