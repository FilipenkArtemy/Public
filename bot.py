import sys
import math

def firststep(field, player):
    for elem in field:
        if player in elem:
            return False
    return True

def bestdeffence(matrix_len, count_of_steps, enemy_field):
    answer = []
    pseans =[]
    for i in range(10):
        for k in range(10):
            range_to_enemy = min([min(abs(i - elem[0]), abs(k - elem[1])) for elem in enemy_field])
            if matrix_len[i][k] == 1 and range_to_enemy > 3:
                answer.append([i,k])
            elif matrix_len[i][k] == 1:
                pseans.append([i,k])
            if len(answer) == count_of_steps:
                break
        if len(answer) == count_of_steps:
            break
    if len(answer) < count_of_steps:
        answer.extend(pseans[0:count_of_steps - len(answer)])
    return answer

def aroundzero(matrix_len, i, k):
    index = []
    for a in range(i-1,i+2):
        for b in range(k-1,k+2):
            if 10 > a >= 0 and 10 > b >= 0 and (a != i or b != k):
                index.append([a,b])
    for elem in index:
        if matrix_len[elem[0]][elem[1]] == 0:
            return True
    return False

def index_best_around(matrix_len, i, k, matrix_eat):
    index = []
    for a in range(i-1,i+2):
        for b in range(k-1,k+2):
            if 10 > a >= 0 and 10 > b >= 0 and (a != i or b != k):
                index.append([a,b])
    max_eat = 0
    for elem in index:
        if matrix_eat[elem[0]][elem[1]] > max_eat:
            max_eat = matrix_eat[elem[0]][elem[1]]
    best_index = [0,0]
    lowlen = math.inf
    for elem in index:
        if matrix_eat[elem[0]][elem[1]] == max_eat and lowlen > matrix_len[elem[0]][elem[1]]:
            best_index = elem
            lowlen = matrix_len[elem[0]][elem[1]]
    return best_index
    
    

def bestattack(matrix_eat, matrix_len,len_step):
    max_eat = 0
    max_eat_index = 0
    for i in range(10):
        for k in range(10):
            if matrix_len[i][k] <= len_step:
                if matrix_eat[i][k] > max_eat:
                    max_eat = matrix_eat[i][k]
                    max_eat_index = [i,k]
    return max_eat_index


def possiblesteps(field, player_num):
    enemy = [2,1][player_num-1]
    enemy_field = []
    for i in range(10):
        for k in range(10):
            if field[i][k] == enemy or field[i][k] == (player_num + 2):
                enemy_field.append([i,k])
    matrix_len = [[math.inf for i in range(10)] for k in range(10)]
    matrix_eat = [[0 for i in range(10)] for k in range(10)]
    matrix_priv = [[[i,k] for k in range(10)] for i in range(10)]
    for i in range(10):
        for k in range(10):
            if field[i][k] == player_num:
                matrix_len[i][k] = 0;
    for m in range(9):
        for i in range(10):
            for k in range(10):
                if field[i][k] == (enemy + 2):
                    if aroundzero(matrix_len, i, k):
                        matrix_len[i][k] = 0
                else:
                    index = index_best_around(matrix_len, i, k, matrix_eat)
                    if matrix_len[i][k] != 0 and field[i][k] != (player_num + 2) and 3 > matrix_len[index[0]][index[1]] and (matrix_eat[i][k] < matrix_eat[index[0]][index[1]] or (matrix_len[i][k] > matrix_len[index[0]][index[1]] and matrix_eat[i][k] == matrix_eat[index[0]][index[1]])) and matrix_priv[index[0]][index[1]] != [i,k]:
                        matrix_len[i][k] = matrix_len[index[0]][index[1]] + 1
                        matrix_priv[i][k] = index
                        if field[i][k] == enemy:
                            matrix_eat[i][k] = matrix_eat[index[0]][index[1]] + 1
    count_of_steps = 3
    end_of_steps = []
    answer = []
    while count_of_steps != 0:
        best_step = bestattack(matrix_eat, matrix_len, count_of_steps)
        if best_step:
            end_of_steps.append(best_step)
            count_of_steps -= matrix_len[best_step[0]][best_step[1]]
        else:
            best_step = bestdeffence(matrix_len, count_of_steps, enemy_field)
            answer.extend(best_step)
            count_of_steps = 0
    for elem in end_of_steps:
        elem_now = elem
        while elem_now != matrix_priv[elem_now[0]][elem_now[1]]:
            answer.append(elem_now)
            elem_now = matrix_priv[elem_now[0]][elem_now[1]]
    return answer

                    
def makestep(field, player_num):
    steps = possiblesteps(field, player_num)
    for elem in steps:
        if field[elem[0]][elem[1]] == 0:
            field[elem[0]][elem[1]] = player_num
        else:
            field[elem[0]][elem[1]] += 2
    return field

if "--name" in sys.argv:
    print("Artem Filipenko")
else:
    field = []
    for line in sys.stdin:
        if len(field) < 10:
            field.append([int(x) for x in line[:-1]])
        else:
            player = int(line)
            if firststep(field, player):
                if player == 1:
                    for i in range(7,10):
                        field[i][9 - i] = 1
                else:
                    for i in range(7,10):
                        field[9-i][i] = 2
            else:
                field = makestep(field, player)
            sys.stdout.write('\n'.join([''.join(list(map(str, elem))) for elem in field]))
            break
