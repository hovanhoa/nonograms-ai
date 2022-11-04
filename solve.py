#!/bin/python3
from re import S
import sys
import os
import json
from typing import List, Dict, Any
from Parse import Parse
from PuzzleSolver import PuzzleSolver as Solver
from State import State as State
import numpy as np
import time
################################################################################################
import pygame
import sys
# from random import random
###############################################################################################
from numpy import random
from nonogame import Game, Rules, checkSolution
from fitness     import readRulesFile, printSol, createConstraints, fitness as evaluateFitness

class Item:  
    def __init__(self, pos_x, pos_y, leng):
        self.rect = pygame.draw.rect(screen, white, [pos_x, pos_y, leng, leng], 0)
        self.state = False


def create_chessboard():    
    item_lst = []
    for v in range(size):
        for h in range(size):
            rect = Item(start_x + h*length, start_y + v*length, length)
            item_lst.append(rect)
    return item_lst



def draw_line():  
    for n in range(size+1):
        start = (start_x, start_y + n * length)
        end = (start_x + square, start_y + n * length)
        pygame.draw.line(screen, gray, start, end, 2)
    for n in range(size+1):
        start = (start_x + n * length, start_y)
        end = (start_x + n * length, start_y + square)
        pygame.draw.line(screen, gray, start, end, 2)


def check_click(item_lst, pos_x, pos_y): 
    global count
    for i in item_lst:
        if i.rect.collidepoint(pos_x, pos_y):
            count += 1
            i.state = bool(1 - i.state)
            if i.state:
                click_on_sound.play()
            else:
                click_off_sound.play()


def change_color(item_lst):  
    for i in item_lst:
        if i.state:
            pygame.draw.rect(screen, blue, i.rect, 0)
        else:
            pygame.draw.rect(screen, white, i.rect, 0)


def get_player_array(item_lst): 
    return [1 if i.state else 0 for i in item_lst]


def create_answer_array():  
    lst = [1 if random.random() > 0.5 else 0 for _ in range(size*size)]
    if list(set(lst))[0] == 0:
        lst[0] = 1
    return lst


def get_line_remind(_line): 
    remind = []  
    num = 0

    def fun(line):
        nonlocal remind, num
        flag = 0  
        if len(line) > 1:
            if line[0] == 0 and line[1] == 1:
                flag += 1
            elif line[0] == line[1] == 0:
                flag += 2
            elif line[0] == 1 and line[1] == 0:
                num += 1
                remind.append(num)
                num = 0
                flag += 2
            elif line[0] == line[1] == 1:
                num += 1
                flag += 1
            fun(line[flag:])
        elif len(line) and line[0]:
            if num:
                remind.append(num + 1)
            else:
                remind.append(1)
    fun(_line)
    return remind


def get_w_remind(answer_lst):  
    h_remind = []
    v_remind = []
    h_array = [answer_lst[i: i+size] for i in range(0, len(answer_lst), size)]  
    for h in h_array:
        h_remind.append(get_line_remind(h))
    v_array = list(map(list, zip(*h_array))) 
    for v in v_array:
        v_remind.append(get_line_remind(v))
    return h_remind, v_remind


def show_remind(answer_lst):  
    h_remind, v_remind = get_w_remind(answer_lst)
    for i, h in enumerate(h_remind):
        for j, num in enumerate(h[::-1]):
            text = font.render(f"{num}", True, black)
            screen.blit(text, (start_x - 20 * (j + 1), start_y + i * length + length / 2 - 10))
    for i, v in enumerate(v_remind):
        for j, num in enumerate(v[::-1]):
            text = font.render(f"{num}", True, black)
            screen.blit(text, (start_x + i * length + length / 2 - 5, start_y - 30 * (j + 1)))


def change_difficulty(delta): 
    global size, length, items, answer
    if size > 7 and delta < 0:
        size += delta
    elif size < 3 and delta > 0:
        size += delta
    elif 3 <= size <= 7:
        size += delta
    length = int(square / size)
    re_start()
    answer = create_answer_array() 
    items = create_chessboard() 


def re_start(): 
    global items, win_flag, win_y, count
    for i in items:
        i.state = False
    win_flag = False
    win_y = count = 0


def fixed_icon():
    click_icon = pygame.image.load(r'./images/click_icon.png')
    click_icon = pygame.transform.scale(click_icon, icon_size)
    screen.blit(click_icon, (10, 8))
    fresh_icon = pygame.image.load(r'./images/fresh.png')  
    fresh_icon = pygame.transform.scale(fresh_icon, icon_size)
    fresh = screen.blit(fresh_icon, (330, 10))
    up_icon = pygame.image.load(r'./images/up.png')  
    up_icon = pygame.transform.scale(up_icon, (15, 15))
    up = screen.blit(up_icon, (370, 6))
    down_icon = pygame.image.load(r'./images/down.png')  
    down_icon = pygame.transform.scale(down_icon, (15, 15))
    down = screen.blit(down_icon, (370, 23))
    result_icon = pygame.image.load(r'./images/result.png')
    result_icon = pygame.transform.scale(result_icon, icon_size)
    res = screen.blit(result_icon, (5, 480))
    
    dfs_text = font.render("DFS Solver", True, black)
    screen.blit(dfs_text, (30, 480))
    
    result_icon = pygame.image.load(r'./images/result.png')
    result_icon = pygame.transform.scale(result_icon, icon_size)
    res_2 = screen.blit(result_icon, (600, 480))
    
    dfs_text = font.render("Heuristic Solver", True, black)
    screen.blit(dfs_text, (625, 480))
    
    return fresh, up, down, res, res_2


def win_anime():  
    global win_y
    if win_y < 220:
        win_y += 20
    win_text = win_font.render("YOU WIN!", True, black)
    screen.blit(win_text, (255, win_y))
    # if win_y > 200 and count > answer.count(1):  
        # text = mes_font.render("need to improve =v=", True, black)
        # screen.blit(text, (250, 280))
    # elif win_y > 200:
        # text = mes_font.render("wow~ perfect 0.0", True, black)
        # screen.blit(text, (275, 280))


def show_click_count():  
    count_text = mes_font.render(f"{count}", True, gold)
    screen.blit(count_text, (42, 3))


def show_aim_count():
    pygame.draw.rect(screen, blue, [80, 8, *icon_size], 0)
    count_text = mes_font.render(f"{answer.count(1)}", True, gold)
    screen.blit(count_text, (115, 3))


def show_result():
    count_text = font.render(f"{answer}", True, black)
    screen.blit(count_text, (40, 480))
################################################################################################
def print_usage() -> None:
    """
    Prints usage information on how to run this program.
    """

    # TODO
    print("usage")

def process_puzzle(path: str):
    """
    Processes one puzzle.
    The necessary steps are: Check the file, validate the contents, run the solver and 
    print the solutions, if any are found.
    """
    if not os.path.isfile(path):
        print("{} is not a regular file.".format(path))
        return

    try:
        f = open(path)
        json_object = json.load(f)
    except OSError as error:
        print("An error occurred while opening the file {}".format(path),
              file=sys.stderr)
        print(error.strerror, file=sys.stderr)
        return
    except json.JSONDecodeError as error:
        print("An error occurred while parsing the JSON file {}".format(path),
              file=sys.stderr)
        return
    else:
        f.close()

    errors, instance = Parse.validate_json(json_object)
    if errors:
        print("The configuration file is not valid.", file=sys.stderr)
        print("Errors:", file=sys.stderr)
        print("\t", end="", file=sys.stderr)
        print("\n\t".join(errors), file=sys.stderr)
        return

    solver: Solver = Solver(instance)
    solutions: List[State] = solver.solve()[0]
    steps: List[State] = solver.solve()[1]
    
    
    solution_array = []
    # first = True
    for index, solution in enumerate(solutions):
        # if not first:
        #     print()
        # first = False
        # print("Solution {}/{}".format(index + 1, len(solutions)))
        
        num = np.array(solution).flatten().tolist()
        for index, a in enumerate(num):
            if a == True: num[index] = 1
            if a == False: num[index] = 0
            if a == None: num[index] = 0
        solution_array.append(num)
        
    # first = True
    steps_array = []
    for index, solution in enumerate(steps):
        num = np.array(solution).flatten().tolist()
        for index, a in enumerate(num):
            if a == True: num[index] = 1
            if a == False: num[index] = 0
            if a == None: num[index] = 0
        steps_array.append(num)
    return steps_array, solution_array
############################################################################
class Solution:
    def __init__(self, points, constraints):
        self.points  = points
        self.fitness = evaluateFitness(points, constraints)

iterations = 0
# def GA(constraints):
#     rules, nLines, nColumns, nPoints, nPopulation = constraints

#     P = randomSolutions(constraints)
#     steps_array = []
#     while not converge(P, constraints):
#         PP  = crossover(P, constraints)
#         PPP = mutation(PP, constraints)
#         P   = select(P, PPP, constraints)
#         global iterations
#         iterations += 1

#         steps_array.append(printSol(P[0], constraints))

#     return best(P, constraints), steps_array

def randomSolutions(constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    S = []

    # print()
    for _ in range(nPopulation):
        s = []
        for _ in range(nPoints):
            if random.random() <= 0.5:
                s += [True]
            else:
                s += [False]
        S += [Solution(s, constraints)]
    return S

def crossover(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP    = []

    P = sorted(P, key = lambda s : (s.fitness, random.random()))
    n = (nPopulation*(nPopulation+1))/2
    prob=[i/n for i in range(1, nPopulation+1)]

    for _ in range(nPopulation):
        child1Points = []
        child2Points = []
        parent1, parent2 = random.choice(P, p=prob, replace=False, size=2)

        for i in range(nPoints):
            if random.random() <= 0.5:
                child1Points += [parent1.points[i]]
                child2Points += [parent2.points[i]]
            else:
                child1Points += [parent2.points[i]]
                child2Points += [parent1.points[i]]

        PP    += [Solution(child1Points, constraints), Solution(child2Points, constraints)]

    return PP

def mutation(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    PP = []

    for s in P:

        prob = 0.4/100
        if len(sys.argv) > 3:
            prob = float(sys.argv[3])

        newPoints = []

        for p in s.points:
            if random.random() > prob:
                newPoints += [p]
            else:
                newPoints += [not p]

        PP += [Solution(newPoints, constraints)]

    return PP

def select(P, PP, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    P = sorted(P, key = lambda s : (s.fitness, random.random()), reverse = True)
    PP = sorted(PP, key = lambda s : (s.fitness, random.random()), reverse = True)

    nParents  = int(2*nPopulation/10)+1
    nChildren = int(5*nPopulation/10)+1
    nRandom = nPopulation - nChildren - nParents

    bestOnes = P[:nParents] + PP[:nChildren]
    others   = P[nParents:] + PP[nChildren:]

    nextP = bestOnes + np.ndarray.tolist(random.choice(others, size=nRandom, replace=False))

    return nextP

def converge(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    for s in P:
        if s.fitness == 0:
            return True

    for i in range(len(P)-1):
        if P[i].points != P[i+1].points:
            return False

    return True

def best(P, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    for s in P:
        if s.fitness == 0:
            return s
    return P[0]
#########################################################################

if __name__ == "__main__":
    blue = (159, 197, 232)  
    gray = (217, 217, 217) 
    gold = (255, 215, 0) 
    black = (0, 0, 0)
    white = (255, 255, 255)
    start_x = 240  
    start_y = 150
    size = 2  
    square = 320  
    length = int(square / size) 
    count = 0  
    win_flag = False 
    win_y = 0  
    icon_size = (28, 28)
    size_map = {2: "TEST", 3: "C", 4: "B", 5: "A", 6: "S", 7: "SS", 8: "SSS"} 
    pygame.init()
    screen = pygame.display.set_mode((780, 520))
    pygame.display.set_icon(pygame.image.load(r'./images/logo.ico')) 
    pygame.display.set_caption("Nonogram game") 
    tick = pygame.time.Clock()  
    font = pygame.font.Font(r'./data/msyh.ttf', 20) 
    mes_font = pygame.font.Font(r'./data/msyh.ttf', 30)  
    win_font = pygame.font.Font(r'./data/msyh.ttf', 60)  
    return_icon = pygame.image.load(r'./images/return.png') 
    return_icon = pygame.transform.scale(return_icon, icon_size)
    return_rect = return_icon.get_rect(topleft=(650, 7))  
    items = create_chessboard()  
    answer = create_answer_array()  
    pygame.mixer.music.load(r'./data/bgm.wav')
    pygame.mixer.music.play(-1) 
    click_on_sound = pygame.mixer.Sound(r'./data/click_on.wav')  
    click_off_sound = pygame.mixer.Sound(r'./data/click_off.wav') 
    change_sound = pygame.mixer.Sound(r'./data/change.wav')  
    win_sound = pygame.mixer.Sound(r'./data/win.wav') 
    wait_sound = True
    
    while True:
        screen.fill(white)  
        fresh_rect, up_rect, down_rect, res_rect, res_2 = fixed_icon()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit()  
            if event.type == pygame.MOUSEBUTTONDOWN:  
                x, y = event.pos
                if not win_flag:
                    check_click(items, x, y)  
                    result = get_player_array(items)
                    if result == answer:
                        win_flag = True
                        win_sound.play()
                elif return_rect.collidepoint(x, y):
                    change_sound.play()
                    re_start()  
                if fresh_rect.collidepoint(x, y):
                    change_sound.play()
                    re_start()
                    answer = create_answer_array() 
                if up_rect.collidepoint(x, y):
                    change_sound.play()
                    change_difficulty(1)  
                if down_rect.collidepoint(x, y):
                    change_sound.play()
                    change_difficulty(-1) 
                if res_2.collidepoint(x, y):
                    nPopulation = 500
                    rules       = readRulesFile('puzzles/data.txt')
                    constraints = createConstraints(rules, nPopulation)
                    rules, nLines, nColumns, nPoints, nPopulation = constraints
                    constraints = rules, nLines, nColumns, nLines*nColumns, nPopulation

                    # mySol, steps_array = GA(constraints)
                    
                    P = randomSolutions(constraints)
                    steps_array = []
                    while not converge(P, constraints):
                        PP  = crossover(P, constraints)
                        PPP = mutation(PP, constraints)
                        P   = select(P, PPP, constraints)
                        # global iterations
                        iterations += 1

                        steps_array.append(printSol(P[0], constraints))
                        num = np.array(printSol(P[0], constraints)).flatten().tolist()
                        for index in range(len(items)):
                            items[index].state = num[index]
                        change_color(items) 
                        draw_line()
                        show_remind(answer) 
                        pygame.display.flip() 
                        time.sleep(0.2)
                        
                    mySol = best(P, constraints)
                    
                    # for i in range(len(steps_array)):
                    #     num = np.array(steps_array[i]).flatten().tolist()
                    #     for index in range(len(items)):
                    #         items[index].state = num[index]
                    #     change_color(items) 
                    #     draw_line()
                    #     show_remind(answer) 
                    #     pygame.display.flip() 
                    #     time.sleep(0.5)
                        
                    solutions_array = printSol(mySol, constraints)
                    
                    num = np.array(solutions_array).flatten().tolist()
                    for index in range(len(items)):
                        items[index].state = num[index]
                    result = get_player_array(items)
                    if result == answer:
                        win_flag = True
                        win_sound.play()
                        
                    change_color(items) 
                    draw_line()
                    show_remind(answer) 
                    pygame.display.flip()
                    
                if res_rect.collidepoint(x, y):
                    path = "puzzles/data.json"
                    steps_array, solution_array = process_puzzle(path)
                    # print(steps_array)
                    for i in range(len(steps_array)):
                        for index in range(len(items)):
                            items[index].state = steps_array[i][index]
                        change_color(items) 
                        draw_line()
                        show_remind(answer) 
                        pygame.display.flip() 
                        time.sleep(0.1)
                    
                    for i in range(len(solution_array)):
                        for index in range(len(items)):
                            items[index].state = solution_array[i][index]
                        result = get_player_array(items)
                        if result == answer:
                            win_flag = True
                            win_sound.play()
                        
                        change_color(items) 
                        draw_line()
                        show_remind(answer) 
                        pygame.display.flip() 
                    
        change_color(items)  
        draw_line()  
        show_remind(answer) 
        
        h_remind, v_remind = get_w_remind(answer)
        aDict = {
            "width": size,
            "height": size,
            "rows": h_remind,
            "columns": v_remind
        }
        jsonString = json.dumps(aDict)
        jsonFile = open("puzzles/data.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()
        
        
        with open('puzzles/data.txt', 'w') as f:
            for i in range(len(h_remind)):
                for j in range(len(h_remind[i])):
                    if j == 0: f.write(str(h_remind[i][j]))
                    else: 
                        f.write(" ")
                        f.write(str(h_remind[i][j]))
                f.write('\n')
            f.write('-\n')
            for i in range(len(v_remind)):
                for j in range(len(v_remind[i])):
                    if j == 0: f.write(str(v_remind[i][j]))
                    else: 
                        f.write(" ")
                        f.write(str(v_remind[i][j]))
                f.write('\n')
            
         
        show_click_count() 
        diff_text = mes_font.render(f"{size_map[size]}", True, gold)
        screen.blit(diff_text, (390, 3))
        if win_flag:
            win_anime() 
            show_aim_count() 
            screen.blit(return_icon, (650, 7)) 
            again_text = mes_font.render("again", True, gold)
            screen.blit(again_text, (685, 0))
        pygame.display.flip() 
        tick.tick(30)
