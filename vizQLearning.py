from pyamaze import maze, agent, COLOR
import time
import numpy as np
from pygame.time import delay

m=maze(20,20)
start=(1,1)
end=(m.rows,m.cols)
m.CreateMaze(saveMaze=True,loopPercent=100)
open=m.maze_map
directions=["W","N","S","E"]
def update_q(current_state,action,next_state,alpha, gamma, q_table):
    if next_state == (m.rows, m.cols):
        reward = 100
    else:
        reward = -1
    available_actions = [action for action in directions if open[next_state][action]]
    best_action=max(available_actions, key=q_table[next_state].get)
    q_table[current_state][action] = q_table[current_state][action] + alpha*(reward + gamma * q_table[next_state][best_action] - q_table[current_state][action])
def Qlearning(m,start,epsilon,directions,open,episodes,max_steps,alpha,gamma):
    end=(m.rows,m.cols)
    q_table = {}
    for row in range(start[0], m.rows + 1):
        for col in range(start[1], m.cols + 1):
            q_table[(row, col)] = {}
            for direction in directions:
                q_table[(row, col)][direction] = 0
    end_checks=0
    for i in range(episodes):
        current_state = start
        steps=0
        while current_state != end and steps<max_steps:
            steps+=1
            randomizer=np.random.rand()
            if randomizer<=epsilon:
                available_actions=[action for action in directions if open[current_state][action]]
                action=np.random.choice(available_actions)
            else:
                available_actions = [action for action in directions if open[current_state][action]]
                action = max(available_actions, key=q_table[current_state].get)
            if action == "N" and open[current_state][action]:
                next_state= (current_state[0]-1, current_state[1])
            elif action == "S" and open[current_state][action]:
                next_state =(current_state[0]+1, current_state[1] )
            elif action == "E" and open[current_state][action]:
                next_state= (current_state[0] , current_state[1]+1)
            elif action == "W" and open[current_state][action]:
                next_state= (current_state[0] , current_state[1]-1)
            else:
                next_state = current_state
            update_q(current_state,action,next_state,alpha,gamma,q_table)
            current_state=next_state
        if current_state==end:
            end_checks+=1
        if i % 100 ==0:
            print('current ends reached:',end_checks,f'in {i} episodes \n')
        if i==(episodes//2):
            for state, actions in q_table.items():
                rounded_actions = {action: round(value, 2) for action, value in actions.items()}
                print(f"State: {state}, Q-values: {rounded_actions}")
    return q_table
def extract_path_dict(q_table, start, end, directions, open_doors, max_steps=10000):
    child_map = {}
    current_state = start
    steps = 0
    while current_state != end and steps < max_steps:
        steps += 1
        available_actions = [action for action in directions if open_doors[current_state][action]]
        q_values = [q_table[current_state][action] for action in available_actions]
        max_q = max(q_values)
        best_actions = []
        for i in range(len(available_actions)):
            if q_values[i] == max_q:
                best_actions.append(available_actions[i])
        action = np.random.choice(best_actions)
        row, col = current_state
        if action == "N":
            child_map[(current_state[0] - 1, current_state[1])] = current_state
            current_state = (current_state[0] - 1, current_state[1])
        elif action == "S":
            child_map[(current_state[0] + 1, current_state[1])] = current_state
            current_state = (current_state[0] + 1, current_state[1])
        elif action == "E":
            child_map[(current_state[0], current_state[1] + 1)] = current_state
            current_state = (current_state[0], current_state[1] + 1)
        elif action == "W":
            child_map[(current_state[0], current_state[1] - 1)] = current_state
            current_state = (current_state[0], current_state[1] - 1)
    return child_map


time1=time.time()
q_table=Qlearning(m,start,0.2,directions,open,20000,3000,alpha=0.1,gamma=0.9)
time2=time.time()
print("Time taken for Qlearning is: ",time2-time1)
for state, actions in q_table.items():
    rounded_actions = {action: round(value, 2) for action, value in actions.items()}
    print(f"State: {state}, Q-values: {rounded_actions}")
path_dict = extract_path_dict(q_table, start, end, directions, open, 10000)
print("Path found :", path_dict)
a = agent(m, footprints=True)
m.tracePath({a: path_dict},delay=100)
m.run()
