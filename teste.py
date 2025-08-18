def quicksort(arr, left, right):
    if len(arr) <=1:
        return arr
    else:
        pivot = arr[0]
        less_than_pivot = [x for x in arr[1:] if x <= pivot]

    



arr = [3, 2, 4, 1, 5, 6, 7, 23, 6, 4, 3]
print(quicksort(arr, 0, len(arr)-1))