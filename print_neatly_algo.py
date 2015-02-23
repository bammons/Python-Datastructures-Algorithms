import sys
INFINITY = sys.maxint

'''
    Takes in a text file and uses memoization to format the file and optomizing
    the words per line.
    @author Bailey Ammons
'''


def calc_least_cost(remaining, count, index):
    val = 0
    if remaining < 0:
        val = INFINITY
    elif index == count - 1 and remaining >= 0:
        val = 0
    else:
        val = remaining**3

    return val


def create_tables(words, M):
    count = len(words)
    extras = [[0 for i in range(count)] for i in range(count)]
    least_cost = [[0 for i in range(count)] for j in range(count)]
    cost_table = [0 for i in range(0, count)]
    text_table = [0 for i in range(0, count)]

    for i in range(0, count):
        extras[i][i] = M - len(words[i])
        least_cost[i][i] = calc_least_cost(extras[i][i], count, i)
        for j in range(i + 1, count):
            extras[i][j] = extras[i][j - 1] - len(words[j]) - 1
            least_cost[i][j] = calc_least_cost(extras[i][j], count, j)

    for j in range(0, count):
        cost_table[j] = INFINITY
        for i in range(0, j):
            if (cost_table[i - 1] + least_cost[i][j]) < cost_table[j]:
                cost_table[j] = cost_table[i - 1] + least_cost[i][j]
                text_table[j] = i

    return text_table, cost_table[-1]


def print_neatly(words, M):
    """ Print text neatly.

    Parameters
    ----------
    words: list of str
        Each string in the list is a word from the file.
    M: int
        The max number of characters per line including spaces

    Returns
    -------
    cost: number
        The optimal value as described in the textbook.
    text: str
        The entire text as one string with newline characters.
        It should not end with a blank line.

    Details
    -------
    Look at print_neatly_test for some code to test the solution.
    """
    count = len(words)
    text = ''

    (text_table, cost) = create_tables(words, M)

    previous = count
    while previous >= 0:
        current = text_table[previous - 1]
        line = words[current]
        for j in range(current + 1, previous):
            line = line + ' ' + words[j]
        if previous != count:
            text = line + '\n' + text
        else:
            text = line

        previous = current

        if previous == 0:
            previous = -1

    return cost, text
