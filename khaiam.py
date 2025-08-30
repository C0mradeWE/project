from termcolor import colored

def khaiam(x):
    triangle = []

    for i in range(x):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
        triangle.append(row)

    return triangle

def Print_khiam(x):
    for row in x:
        row_str = []
        for num in row:
            if num % 2 == 0:
                row_str.append(colored(num, 'red'))
            else:
                row_str.append(colored(num, 'green'))
        print(' '.join(row_str))


x = 20
triangle = khaiam(x)
Print_khiam(triangle)
