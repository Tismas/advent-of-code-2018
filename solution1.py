with open('./input1.txt') as f:
    inputs = [*map(int, f.readlines())]
    sumsHistory = []
    nextSum = 0
    iterator = 0
    while nextSum not in sumsHistory:
        sumsHistory.append(nextSum)
        nextSum = sumsHistory[-1] + inputs[iterator]
        iterator = (iterator + 1) % len(inputs)

    print('Sum:', sumsHistory[len(inputs)])
    print('Repeated sum:', nextSum)