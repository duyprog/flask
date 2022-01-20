A = [1, 2, 3, 4, 5]

plus_two = map(lambda x: x + 1, A)
new_list = list(plus_two)
print(new_list)

even_num = list(filter(lambda x: x % 2 == 0, new_list))
print(even_num)