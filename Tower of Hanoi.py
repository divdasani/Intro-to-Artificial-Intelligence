
# coding: utf-8

# In[1]:


'''
Created by Div Dasani and Amy Chen
EECS 348
10/3/17
Assignment 1- Tower Of Hanoi
'''


from TOH_DFS import Solve_By_DepthFS
from TOH_BFS import Solve_By_BreadthFS
from TOH_TFS import Solve_By_BestFS


number_of_disks = 5

print ("Solve by Depth First Search method:")
Solve_By_DepthFS(number_of_disks)

print ("Solve by Breadth First Search method:")
Solve_By_BreadthFS(number_of_disks)

print ("Solve by Best First Search method:")
Solve_By_BestFS(number_of_disks)


# In[ ]:


import math
'''
Logic:
I am going to assign a numerical value to each disk as 2^n. The first disk(smallest) will have value of 2, second disk value of 4, third disk value of 8, fourth disk value of 16 and so on
Numerical Value of any Disk = 2^(n)
Value of each peg(pole) will be sum of all values of disk on that peg at given time. For e.g. if the peg currently has Disk 1 and 3, than the value of that peg is 2 + 8 = 10
Value of all disks will be 2^1 + 2^2....2^(n) = (2^n) - 2. For e.g. the total value of 4 disks will be 2^4 - 2 = 30   
I am using "Bitwise And" operator to decide if a given disk exists on the peg. For e.g. 
    -if the peg value is 20 (Disk 2 and 4) then 20 "Bitwise And" 2 will equal to 0 which means that peg doesn't have Disk 1
    -if the peg value is 20 (Disk 2 and 4) then 20 "Bitwise And" 4 will equal to 4 which means that peg does have Disk 2
To check if I am not placing bigger disk on top of smaller disk, I used the Modulus (find the remainder) operator. For e.g.
    -if the peg has value of 18(Disk 1 and 4), then 18 % 4 will be 2 which means I cannot place Disk 2 on this peg
    -if the peg has a value of 24 (Disk 3 and 4) then 24 % 4 will be 0 which means I can place Disk 2 on this peg
          
'''

# Depth First Search will use the Last In First Out logic. That way we are going to keep going deep(vertical) before we search horizontal states.
def Solve_By_DepthFS(n):
    #Declare Variables
    #Values of each Peg
    peg1_value=peg2_value=peg3_value = 0

    #LIFO List to store the adjacent states
    state_LIFO = []

    #LIFO list used to save the actions we have taken till for every LIFO item, so we can trace back. The size of this list will always be same as size of other LIFO list
    steps_till_now_LIFO = []

    #This List is to store the states which we have already encountered, so that we do not go into infinite loop
    past_states = []

    #temporary variables to store the steps for current working state and next adjacent state
    steps_till_current_state = steps_till_next_state = []

    #Temporary variable to store the value of disk being moved
    Value_of_Disk = 0

    #Temporary variable to store current state and the next adjacent state
    current_state = new_state = []

    #Temporary variable to store the disk being moved
    disk_on_top = 0

    #Boolean variables
    state_found_before = solution_found = False

    #Find the total value of all disks based on n number of disks
    Value_of_All_Disks = int(math.pow(2,n+1))-2

    #Initial state where all disks are in Peg1. Because Lists are indexed starting 0, we will just ignore the 0th index.
    current_state = [0, Value_of_All_Disks, 0, 0]

    #Insert the starting state in the LIFO list
    state_LIFO.append(current_state)
    steps_till_now_LIFO.append(steps_till_current_state)
    past_states.append(current_state)

    #Loop till we find the solution
    while solution_found == False and len(state_LIFO) > 0:
        #Get the next state based on LIFO logic
        current_state = state_LIFO.pop()
        #Get the corresponding steps on LIFO logic
        steps_till_current_state = steps_till_now_LIFO.pop()
        #Loop all pegs for source for disk movement
        for source_peg in range(3,0,-1):
            #if the peg has no disk as of now, then move on to next peg
            if (current_state[source_peg] == 0):
                continue
            # Loop all pegs for destination for disk movement
            for dest_peg in range(3, 0, -1):
                #Source Peg and Dest Peg cannot be same
                if (solution_found == True or source_peg == dest_peg):
                    continue
                #Loop for each disk size from small to big
                for disk_size in range(1,n+1):
                    Value_of_Disk = int(math.pow(2,disk_size))
                    #Using Bitwise AND operator find the disk on top of this source peg
                    if ((current_state[source_peg] & Value_of_Disk) == Value_of_Disk):
                        disk_on_top = disk_size
                        break
                #Destination peg should either be empty or top disk should be bigger than the disk being moved
                if (current_state[dest_peg] == 0 or current_state[dest_peg] % Value_of_Disk == 0):
                    #Following steps move the disk from source to dest peg, and create a new state out of current state
                    new_state = list(current_state)
                    new_state[source_peg] = new_state[source_peg] - Value_of_Disk
                    new_state[dest_peg] = new_state[dest_peg] + Value_of_Disk
                    next_step = [disk_on_top, source_peg, dest_peg]
                    steps_till_next_state = list(steps_till_current_state)
                    steps_till_next_state.append(next_step)
                    #Check if the new State is the Final Solution we are looking for (all disks on peg 3)
                    if (new_state[3] == Value_of_All_Disks):
                        steps = 1
                        output = ""
                        for aseq in steps_till_next_state:
                            output = output +  str(steps) +  ": Move Disk " + str(aseq[0]) + " From " + str(aseq[1]) + " To " + str(aseq[2]) +  "\n"
                            steps = steps + 1
                        print (output)
                        solution_found = True
                        return
                    #else - we did't find the solution yet
                    else:
                        #make sure the new state is not already discovered before
                        state_found_before = False
                        for past_state in past_states:
                            if (past_state[1] == new_state[1] and past_state[2] == new_state[2] and past_state[3] == new_state[3]):
                                state_found_before = True
                                break
                        #if this is the new state which we discovered before, then append it to the LIFO lists
                        if state_found_before == False:
                            state_LIFO.append(new_state)
                            steps_till_now_LIFO.append(steps_till_next_state)
                            past_states.append(new_state)


# In[ ]:


import math
'''
Logic:
I am going to assign a numerical value to each disk as 2^n. The first disk(smallest) will have value of 2, second disk value of 4, third disk value of 8, fourth disk value of 16 and so on
Numerical Value of any Disk = 2^(n)
Value of each peg(pole) will be sum of all values of disk on that peg at given time. For e.g. if the peg currently has Disk 1 and 3, than the value of that peg is 2 + 8 = 10
Value of all disks will be 2^1 + 2^2....2^(n) = (2^n) - 2. For e.g. the total value of 4 disks will be 2^4 - 2 = 30   
I am using "Bitwise And" operator to decide if a given disk exists on the peg. For e.g. 
    -if the peg value is 20 (Disk 2 and 4) then 20 "Bitwise And" 2 will equal to 0 which means that peg doesn't have Disk 1
    -if the peg value is 20 (Disk 2 and 4) then 20 "Bitwise And" 4 will equal to 4 which means that peg does have Disk 2
To check if I am not placing bigger disk on top of smaller disk, I used the Modulus (find the remainder) operator. For e.g.
    -if the peg has value of 18(Disk 1 and 4), then 18 % 4 will be 2 which means I cannot place Disk 2 on this peg
    -if the peg has a value of 24 (Disk 3 and 4) then 24 % 4 will be 0 which means I can place Disk 2 on this peg
'''

# Breadth First Search will use the First In First Out logic. That way we are going to try all the states(nodes) which we discovered first(horizontal), before searching states(nodes) found later.
def Solve_By_BreadthFS(n):
    #Declare Variables
    #Values of each Peg
    peg1_value=peg2_value=peg3_value = 0

    #FIFO List to store the adjacent states
    state_FIFO = []

    #FIFO list used to save the actions we have taken till for every FIFO item, so we can trace back. The size of this list will always be same as size of other FIFO list
    steps_till_now_FIFO = []

    #This List is to store the states which we have already encountered, so that we do not go into infinite loop
    past_states = []

    #temporary variables to store the steps for current working state and next adjacent state
    steps_till_current_state = steps_till_next_state = []

    #Temporary variable to store the value of disk being moved
    Value_of_Disk = 0

    #Temporary variable to store current state and the next adjacent state
    current_state = new_state = []

    #Temporary variable to store the disk being moved
    disk_on_top = 0

    #Boolean variables
    state_found_before = solution_found = False

    #Find the total value of all disks based on n number of disks
    Value_of_All_Disks = int(math.pow(2,n+1))-2

    #Initial state where all disks are in Peg1. Because Lists are indexed starting 0, we will just ignore the 0th index.
    current_state = [0, Value_of_All_Disks, 0, 0]

    #Insert the starting state in the FIFO list
    state_FIFO.append(current_state)
    steps_till_now_FIFO.append(steps_till_current_state)
    past_states.append(current_state)

    #Loop till we find the solution
    while solution_found == False and len(state_FIFO) > 0:
        #Get the next state based on FIFO logic
        current_state = state_FIFO.pop(0)
        #Get the corresponding steps on FIFO logic
        steps_till_current_state = steps_till_now_FIFO.pop(0)
        #Check to see if this state is the solution we are looking for
        if (current_state[3] == Value_of_All_Disks):
            steps = 1
            output = ""
            for aseq in steps_till_current_state:
                output = output + str(steps) + ": Move Disk " + str(aseq[0]) + " From " + str(aseq[1]) + " To " + str(
                    aseq[2]) + "\n"
                steps = steps + 1
            print(output)
            solution_found = True
            return
       #Loop all pegs for source for disk movement
        for source_peg in range(3,0,-1):
            #if the peg has no disk as of now, then move on to next peg
            if (current_state[source_peg] == 0):
                continue
            # Loop all pegs for destination for disk movement
            for dest_peg in range(3, 0, -1):
                #Source Peg and Dest Peg cannot be same
                if (solution_found == True or source_peg == dest_peg):
                    continue
                #Loop for each disk size from small to big
                for disk_size in range(1,n+1):
                    Value_of_Disk = int(math.pow(2,disk_size))
                    #Using Bitwise AND operator find the disk on top of this source peg
                    if ((current_state[source_peg] & Value_of_Disk) == Value_of_Disk):
                        disk_on_top = disk_size
                        break
                #Destination peg should either be empty or top disk should be bigger than the disk being moved
                if (current_state[dest_peg] == 0 or current_state[dest_peg] % Value_of_Disk == 0):
                    #Following steps move the disk from source to dest peg, and create a new state out of current state
                    new_state = list(current_state)
                    new_state[source_peg] = new_state[source_peg] - Value_of_Disk
                    new_state[dest_peg] = new_state[dest_peg] + Value_of_Disk
                    next_step = [disk_on_top, source_peg, dest_peg]
                    steps_till_next_state = list(steps_till_current_state)
                    steps_till_next_state.append(next_step)
                    #make sure the new state is not already discovered before
                    state_found_before = False
                    for past_state in past_states:
                        if (past_state[1] == new_state[1] and past_state[2] == new_state[2] and past_state[3] == new_state[3]):
                            state_found_before = True
                            break
                    #if this is the new state which we discovered before, then append it to the FIFO lists
                    if state_found_before == False:
                        state_FIFO.append(new_state)
                        steps_till_now_FIFO.append(steps_till_next_state)
                        past_states.append(new_state)


# In[ ]:


import math

'''
Logic:
I am going to assign a numerical value to each disk as 2^n. The first disk(smallest) will have value of 2, second disk value of 4, third disk value of 8, fourth disk value of 16 and so on
Numerical Value of any Disk = 2^(n)
Value of each peg(pole) will be sum of all values of disk on that peg at given time. For e.g. if the peg currently has Disk 1 and 3, than the value of that peg is 2 + 8 = 10
Value of all disks will be 2^1 + 2^2....2^(n) = (2^n) - 2. For e.g. the total value of 4 disks will be 2^4 - 2 = 30   
I am using "Bitwise And" operator to decide if a given disk exists on the peg. For e.g. 
    -if the peg value is 20 (Disk 2 and 4) then 20 "Bitwise And" 2 will equal to 0 which means that peg doesn't have Disk 1
    -if the peg value is 20 (Disk 2 and 4) then 20 "Bitwise And" 4 will equal to 4 which means that peg does have Disk 2
To check if I am not placing bigger disk on top of smaller disk, I used the Modulus (find the remainder) operator. For e.g.
    -if the peg has value of 18(Disk 1 and 4), then 18 % 4 will be 2 which means I cannot place Disk 2 on this peg
    -if the peg has a value of 24 (Disk 3 and 4) then 24 % 4 will be 0 which means I can place Disk 2 on this peg

'''


# Best First Search will use the Last In First Out logic. That way we are going to keep going deep(vertical) before we search horizontal states.
def Solve_By_BestFS(n):
    # Declare Variables
    # Values of each Peg
    peg1_value = peg2_value = peg3_value = 0

    # List to store the adjacent states
    state_COLLECTION = []

    # list used to save the actions we have taken till for every item in previous list, so we can trace back. The size of this list will always be same as size of other COLLECTION list
    steps_till_now_COLLECTION = []

    # This List is to store the states which we have already encountered, so that we do not go into infinite loop
    past_states = []

    # temporary variables to store the steps for current working state and next adjacent state
    steps_till_current_state = steps_till_next_state = []

    # Temporary variable to store the value of disk being moved
    Value_of_Disk = 0

    # Temporary variable to store current state and the next adjacent state
    current_state = new_state = []

    # Temporary variable to store the disk being moved
    disk_on_top = 0

    # Boolean variables
    state_found_before = solution_found = False

    # Find the total value of all disks based on n number of disks
    Value_of_All_Disks = int(math.pow(2, n + 1)) - 2

    # Initial state where all disks are in Peg1. Because Lists are indexed starting 0, we will just ignore the 0th index.
    current_state = [0, Value_of_All_Disks, 0, 0]

    # Insert the starting state in the COLLECTION list
    state_COLLECTION.append(current_state)
    steps_till_now_COLLECTION.append(steps_till_current_state)
    past_states.append(current_state)

    # Loop till we find the solution
    while solution_found == False and len(state_COLLECTION) > 0:
        # Get the BEST state in stack
        best_item = - 1
        for item in range(0,len(state_COLLECTION)):
            state = state_COLLECTION[item]
            for d in range(n-1, 0, -1):
                partial_solution_val = math.pow(2, d+1)-2
                if ((n+d)%2 == 0):
                    partial_solution_peg = 3
                else:
                    partial_solution_peg = 2
                if (state[partial_solution_peg] == partial_solution_val):
                    best_item = item
                    break
            if (best_item > -1):
                break
        if best_item == -1:
            best_item = 0

        current_state = state_COLLECTION.pop(best_item)
        # Get the corresponding steps on COLLECTION logic
        steps_till_current_state = steps_till_now_COLLECTION.pop(best_item)
        # Loop all pegs for source for disk movement
        for source_peg in range(3, 0, -1):
            # if the peg has no disk as of now, then move on to next peg
            if (current_state[source_peg] == 0):
                continue
            # Loop all pegs for destination for disk movement
            for dest_peg in range(3, 0, -1):
                # Source Peg and Dest Peg cannot be same
                if (solution_found == True or source_peg == dest_peg):
                    continue
                # Loop for each disk size from small to big
                for disk_size in range(1, n + 1):
                    Value_of_Disk = int(math.pow(2, disk_size))
                    # Using Bitwise AND operator find the disk on top of this source peg
                    if ((current_state[source_peg] & Value_of_Disk) == Value_of_Disk):
                        disk_on_top = disk_size
                        break
                # Destination peg should either be empty or top disk should be bigger than the disk being moved
                if (current_state[dest_peg] == 0 or current_state[dest_peg] % Value_of_Disk == 0):
                    # Following steps move the disk from source to dest peg, and create a new state out of current state
                    new_state = list(current_state)
                    new_state[source_peg] = new_state[source_peg] - Value_of_Disk
                    new_state[dest_peg] = new_state[dest_peg] + Value_of_Disk
                    next_step = [disk_on_top, source_peg, dest_peg]
                    steps_till_next_state = list(steps_till_current_state)
                    steps_till_next_state.append(next_step)
                    # Check if the new State is the Final Solution we are looking for (all disks on peg 3)
                    if (new_state[3] == Value_of_All_Disks):
                        steps = 1
                        output = ""
                        for aseq in steps_till_next_state:
                            output = output + str(steps) + ": Move Disk " + str(aseq[0]) + " From " + str(
                                aseq[1]) + " To " + str(aseq[2]) + "\n"
                            steps = steps + 1
                        print(output)
                        solution_found = True
                        return
                    # else - we did't find the solution yet
                    else:
                        # make sure the new state is not already discovered before
                        state_found_before = False
                        for past_state in past_states:
                            if (past_state[1] == new_state[1] and past_state[2] == new_state[2] and past_state[3] ==
                                new_state[3]):
                                state_found_before = True
                                break
                        # if this is the new state which we discovered before, then append it to the COLLECTION lists
                        if state_found_before == False:
                            state_COLLECTION.append(new_state)
                            steps_till_now_COLLECTION.append(steps_till_next_state)
                            past_states.append(new_state)

