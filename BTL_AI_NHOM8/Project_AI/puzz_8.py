from colorama import Fore, Style, Back
from copy import deepcopy

#Ki tu unicode de ve khung cau do 8 so
left_down_angle = '\u2514'      #Nó có hình dạng như sau: └.
right_down_angle = '\u2518'     #Nó có hình dạng như sau: ┘.
right_up_angle = '\u2510'       #Nó có hình dạng như sau: ┐.
left_up_angle = '\u250C'        #Nó có hình dạng như sau: ┌.
middle_junction = '\u253C'      #Nó có hình dạng như sau: ┼.
top_junction = '\u252C'         #Nó có hình dạng như sau: ┬.
bottom_junction = '\u2534'      #Nó có hình dạng như sau: ┴.
right_junction = '\u2524'       #Nó có hình dạng như sau: ┤.
left_junction = '\u251C'        #Nó có hình dạng như sau: ├.

#bar color
# bar = Style.BRIGHT + Fore.CYAN + '\u2502' + Fore.RESET + Style.RESET_ALL
bar = Style.BRIGHT + Fore.YELLOW + '\u2502' + Fore.RESET + Style.RESET_ALL#Nó có hình dạng như sau: |
dash = '\u2500' #Nó có hình dạng như sau: -
tripdash = dash + dash + dash

#Tao khung 9 o nhu game 8 so
first_line =Style.BRIGHT + Fore.YELLOW + left_up_angle + tripdash + top_junction + tripdash + top_junction + tripdash + right_up_angle + Fore.RESET + Style.RESET_ALL
middel_line = Style.BRIGHT + Fore.YELLOW + left_junction + tripdash + middle_junction + tripdash + middle_junction + tripdash + right_junction + Fore.RESET + Style.RESET_ALL
last_line = Style.BRIGHT + Fore.YELLOW + left_down_angle +tripdash + bottom_junction + tripdash + bottom_junction + tripdash + right_down_angle + Fore.RESET + Style.RESET_ALL

# print(first_line)
# print(middel_line)
# print(middel_line)
# print(last_line)

#Khoi tao ma tran
initial_state_matrix = [] # ma tran khoi tao ban dau
goal = []                 # ma tran dich

#Ham input ma tran
def input_matrix_initial():
    print("Nhap ma tran ban dau:")
    for row in range(3):
        while True:
            row_values = [int(x) for x in input().split()]
            if len(row_values)==3:
                break
            else:
                print("Yeu cau nhap lai dung 3 so tren 1 hang")
        initial_state_matrix.append(row_values)
    return initial_state_matrix

def input_matrix_goal():
    print("Nhap ma tran dich:")
    for row in range(3):
        while True:
            row_values = [int(x) for x in input().split()]
            if len(row_values) == 3:
                break
            else:
                print("Yeu cau nhap lai dung 3 so tren 1 hang")
        goal.append(row_values)
    return goal
#input_matrix()

#Ham hien thi cau do va ket qua cau do
def show_puzz(array):
    print(first_line)
    for i in range(len(array)):
        for j in array[i]:
            if j == 0:
                print(bar, Back.RED + ' ' + Back.RESET, end=' ')
            else:
                print(bar, j, end=' ')
        print(bar)
        if i == 2:
            print(last_line)
        else:
            print(middel_line)
# goal = [[1,2,3],[4,5,6],[7,8,0]]
# show_puzz(goal)





# Hàm trả về vị trí của 1 phần tử gồm row và col
def get_index_element(current_state, element):
    for row in range(len(current_state)):
        if element in current_state[row]:
            return (row, current_state[row].index(element))



#Hàm tính toán chi phí
def cost_calculation(current_state):

    cost = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[0])):
            index_element = get_index_element(goal, current_state[row][col])
            cost += abs(index_element[0] - row) + abs(index_element[1] - col)
    return cost
# a =[]
# a = [[2, 1, 3], [7, 5, 8], [6, 0, 4]]
# show_puzz(a)
# print(cost_calculation(a))


#direction: Mo ta huong di ma tran key: [row,col]
DIRECTION = {"U": [-1, 0], "D": [1, 0], "R": [0, 1], "L": [0, -1]}


# Class node lưu trữ data các trạng thái của puzzle
class Node:
    def __init__(self, current_node, before_node, g, h, direction):
        self.current_node = current_node
        self.before_node = before_node
        self.g = g
        self.h = h
        self.direction = direction
    def f(self):
        return self.g + self.h

# g là số cấp cây tăng dần từ 0-n
# h là số phần từ khác vị trí với goal hoac kc element den element dich
# f = g+h : lấy f nhỏ nhất làm ma trận tiep theo


#Lấy danh sách node kề
def get_list_node(node):
    listNode = []
    index_empty = get_index_element(node.current_node, 0)
    for dir in DIRECTION.keys():
        new_index_empty = (index_empty[0] + DIRECTION[dir][0], index_empty[1] + DIRECTION[dir][1])
        if 0 <= new_index_empty[0] < len(node.current_node) and 0 <= new_index_empty[1] < len(node.current_node[0]):
            new_state_matrix = deepcopy(node.current_node)
            new_state_matrix[index_empty[0]][index_empty[1]] = node.current_node[new_index_empty[0]][new_index_empty[1]]
            new_state_matrix[new_index_empty[0]][new_index_empty[1]] = 0
            listNode.append(Node(new_state_matrix, node.current_node, node.g + 1, cost_calculation(new_state_matrix), dir))
    return listNode

#Tim node tốt nhất trong danh sách list node có f min
def get_best_node(openSet):
    first = True
    for node in openSet.values():
        if first or node.f() < minF:
            first = False
            bestNode = node
            minF = node.f()
    return bestNode


#Hàm tạo đường đi ngắn nhất cho bài toán
def buildPath(closedSet):
    node = closedSet[str(goal)]
    branch = list()
    while node.direction:
        branch.append({
            'direction': node.direction,
            'node': node.current_node
        })
        node = closedSet[str(node.before_node)]
    branch.append({
        'direction': '',
        'node': node.current_node
    })
    branch.reverse()
    return branch

def a_star(puzzle):
    open_set = {str(puzzle): Node(puzzle, puzzle, 0, cost_calculation(puzzle), "")}
    close_set = {}
    while True:
        testNode = get_best_node(open_set)
        close_set[str(testNode.current_node)] = testNode
        if testNode.current_node == goal:
            return buildPath(close_set)
        list_Node = get_list_node(testNode)
        for node in list_Node:
            if str(node.current_node) in close_set.keys() or str(node.current_node) in open_set.keys() and open_set[
                str(node.current_node)].f() < node.f():
                continue
            open_set[str(node.current_node)] = node
        del open_set[str(testNode.current_node)]

# Covert  ma tran sang arr va đếm số lương đảo chiều
def get_reverse_count(arr):
    reverse_count = 0
    empty_value = 0
    for i in range(0,9):
        for j in range(i+1, 9):
            if arr[i] != empty_value and arr[j] != empty_value and arr[i] > arr[j]:
                reverse_count += 1
    return reverse_count

#Hàm kiểm tra xem co quay lui về trang thái đich hay ko
def is_backtracking_goal(matrix):
    #chuyển ma trân về mảng
    array = []
    for row in matrix:
        array.extend(row)
    #Lấy số lương đảo chiều
    reverse_count = get_reverse_count(array)
    # Chia hết cho 2, tức là số lượng đảo chiều chẵn thì quay lui về trạng thái đích thành công!
    return (reverse_count % 2 ==0)
# goal = [[1,2,3],[4,5,6],[7,8,0]]

# Convert ma trận để kiểm tra trạng thái đầu có thể tiến tới trạng thái đích được hay không
def process_matrix(TEST, INIT):
    n = len(TEST)
    index_dict = {}
    cnt = 1
    for row in range(n):
        for col in range(n):
            value = TEST[row][col]
            # TMP[cnt - 1] = value  # Chỉ số của TMP giảm đi 1
            index_dict[value] = cnt  # Lưu chỉ số vào từ điển
            cnt += 1
    index_dict[TEST[2][2]] = 0
    # Khởi tạo ma trận CHECK với các phần tử ban đầu là 0
    CHECK = [[0 for _ in range(n)] for _ in range(n)]
    for row in range(n):
        for col in range(n):
            value = INIT[row][col]
            CHECK[row][col] = index_dict[value]  # Sử dụng từ điển để lấy chỉ số

    return CHECK
# tes2( đến được đích)- 25 bước
# ma trận ban đầu:
# [2,0,6],[8,7,5],[4,3,1]
# ma trận đích
# [1,2,3],[4,5,6],[7,8,0]

# dau = [
#     [5, 6, 1],
#     [2, 4, 0],
#     [8, 3, 7]
# ]
#
# dich = [
#     [1, 3, 4],
#     [7, 8, 6],
#     [0, 5, 2]
# ]

if __name__ == '__main__':
    initial_state_matrix = input_matrix_initial()
    goal = input_matrix_goal()
    check_matrix = process_matrix(goal, initial_state_matrix)
    if is_backtracking_goal(check_matrix):
        print("Ma trận khởi tạo có thể trở thành ma trận đích!")
    else:
        print("Ma trận khởi tạo không thể trở thành ma trận đích!")
        exit()

    br =  a_star(initial_state_matrix)
    print("Tổng số bước di chuyển: ", len(br)-1)
    print()
    print("----------INPUT----------")
    for b in br:
        if b['direction'] == '':
            dir = ''
        elif b['direction'] == 'U':
            dir = 'UP'
        elif b['direction'] == 'D':
            dir = 'DOWN'
        elif b['direction'] == 'R':
            dir = 'RIGHT'
        elif b['direction'] == 'L':
            dir = 'LEFT'
        print(tripdash + dir + tripdash)
        show_puzz(b['node'])
        print()

    print("Đã đạt trạng thái đích xin cảm ơn!")