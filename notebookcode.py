
# coding: utf-8

# <h1>Scheduling Problem</h1><br/>
# The scheduling problem is assigning 23 classes to 3 rooms at 8 different times. The two rules for scheduling are 
# <ul>
#     <li>Two classes cannot meet in the same room at the same time.</li>
#     <li>Classes with the same first digit cannot meet at the same time, because students might take a subset of these in one semester. There is one exception to this rule. CS163 and CS164 can meet at the same time.</li>
# </ul>

# In[24]:

classes = ['CS160', 'CS163', 'CS164',
           'CS220', 'CS270', 'CS253',
           'CS320', 'CS314', 'CS356', 'CS370',
           'CS410', 'CS414', 'CS420', 'CS430', 'CS440', 'CS445', 'CS453', 'CS464',
           'CS510', 'CS514', 'CS535', 'CS540', 'CS545']

times = [' 9 am',
         '10 am',
         '11 am',
         '12 pm',
         ' 1 pm',
         ' 2 pm',
         ' 3 pm',
         ' 4 pm']

rooms = ['CSB 130', 'CSB 325', 'CSB 425']


# Min conflicts functions given to us.

# In[25]:

import random

def min_conflicts(vars, domains, constraints, neighbors, max_steps=1000): 
    """Solve a CSP by stochastic hillclimbing on the number of conflicts."""
    # Generate a complete assignment for all vars (probably with conflicts)
    current = {}
    for var in vars:
        val = min_conflicts_value(var, current, domains, constraints, neighbors)
        current[var] = val
    # Now repeatedly choose a random conflicted variable and change it
    for i in range(max_steps):
        conflicted = conflicted_vars(current,vars,constraints,neighbors)
        if not conflicted:
            return (current,i)
        var = random.choice(conflicted)
        val = min_conflicts_value(var, current, domains, constraints, neighbors)
        current[var] = val
    return (None,None)

def min_conflicts_value(var, current, domains, constraints, neighbors):
    """Return the value that will give var the least number of conflicts.
    If there is a tie, choose at random."""
    return argmin_random_tie(domains[var],
                             lambda val: nconflicts(var, val, current, constraints, neighbors)) 

def conflicted_vars(current,vars,constraints,neighbors):
    "Return a list of variables in current assignment that are in conflict"
    return [var for var in vars
            if nconflicts(var, current[var], current, constraints, neighbors) > 0]

def nconflicts(var, val, assignment, constraints, neighbors):
    "Return the number of conflicts var=val has with other variables."
    # Subclasses may implement this more efficiently
    def conflict(var2):
        val2 = assignment.get(var2, None)
        return val2 != None and not constraints(var, val, var2, val2)
    return len(list(filter(conflict, neighbors[var])))

def argmin_random_tie(seq, fn):
    """Return an element with lowest fn(seq[i]) score; break ties at random.
    Thus, for all s,f: argmin_random_tie(s, f) in argmin_list(s, f)"""
    best_score = fn(seq[0]); n = 0
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score; n = 1
        elif x_score == best_score:
            n += 1
            if random.randrange(n) == 0:
                    best = x
    return best


# <h3>constraints_ok function</h3><br/>
# Input:<br/>
# class_name_1&rightarrow;string for 1st class name<br/>
# value_1&rightarrow;tuple first value string for 1st room and second value string for 1st time<br/>
# class_name_2&rightarrow;string for 2nd class name<br/>
# value_2&rightarrow;tuple first value string for 2nd room and second value string for 2nd time<br/>
# 
# Output&rightarrow;boolean

# In[26]:

def constraints_ok(class_name_1, value_1, class_name_2, value_2):
    if (value_1[1] == value_2[1] and value_1[0] == value_2[0]):
    #checks if time slots are the same and checks if classes are the same
        return False 
    if (value_1[1] == value_2[1] and ((class_name_1 == 'cs163' and class_name_2 == 'cs164') or (class_name_1 == 'cs164' and class_name_2 == 'cs163'))):
    #checks if time slots are the same and checks if class names are cs163 and cs164
        return True
    if (class_name_1[2] == class_name_2[2] and value_1[1] == value_2[1]):
    #checks if third character in class name are the same and if time slots are the same
        return False
    return True


# <h3>display function</h3><br/>
# Input:<br/>
# assignments&rightarrow;dictionary with key as string for classes and value as tuple with string for room and string for time e.g. 'CS160': ('CSB 325', '12 pm')<br/>
# rooms&rightarrow;list of strings for rooms<br/>
# times&rightarrow;list of strings for times<br/>
# 
# Output&rightarrow;void

# In[27]:

def display(assignments, rooms, times):
    swap = dict((v,k) for k,v in assignments.items())           #swaps key and value in assignments
    print("", end ="       ")                                   #tab space for column header
    for room in rooms:                                          #loops through rooms
        print(room, end ="  ")                                  #print rooms as column headers
    print()                                                     #ends print line
    print("-------------------------------")                    #prints line
    for time in times:                                          #loops through time slots for each row header
        print(time, end ="    ")                                #prints row header
        for room in rooms:                                      #loops through rooms at the current time (first loop)
            print(swap.get((room, time), "     "), end ="    ") #prints class at time slot: time and room: room
        print()                                                 #ends print line


# <h3>schedule function</h3><br/>
# Input:<br/>
# classes&rightarrow;list of strings for classes<br/>
# times&rightarrow;list of strings for time slots<br/>
# rooms&rightarrow;list of strings for rooms<br/>
# max_steps&rightarrow;integer for max number of steps in min_conflicts<br/>
# 
# Output:<br/>
# solution&rightarrow;dictionary with key as string for classes and value as tuple with string for room and string for time e.g. 'CS160': ('CSB 325', '12 pm')<br/>
# steps&rightarrow;integer for number of steps to find solution 

# In[28]:

def schedule(classes, times, rooms, max_steps):
    domains = {key: [(a,b) for a in rooms for b in times] for key in classes}
    #creates dictionary where key is each class and value is list of possible combination of other classes and times
    neighbors = {var: [v for v in classes if v != var] for var in classes}
    #creates dictionary where key is each class and value is list of all other classes
    solution, steps = min_conflicts(classes, domains, constraints_ok, neighbors, max_steps=max_steps)
    #runs min conflict algorithm
    return solution, steps

assignments, steps = schedule(classes, times, rooms, 100)
print('Took', steps, 'steps')
print(assignments)
display(assignments, rooms, times)


# <h1>Extra Credit</h1>

# <h3>prefer_schedule_ok function</h3><br/>
# Input:<br/>
# classes&rightarrow;list of strings for classes<br/>
# times&rightarrow;list of strings for time slots<br/>
# rooms&rightarrow;list of strings for rooms<br/>
# max_steps&rightarrow;integer for max number of steps in min_conflicts<br/>
# iterations&rightarrow;integer for number of iterations to find optimal solution for preference
# 
# Output:<br/>
# solutionf&rightarrow;dictionary with key as string for classes and value as tuple with string for room and string for time e.g. 'CS160': ('CSB 325', '12 pm')<br/>
# stepfs&rightarrow;integer for number of steps to find solution 

# In[29]:

def prefer_schedule(classes, times, rooms, max_steps, iterations = 100):
    domains = {key: [(a,b) for a in rooms for b in times] for key in classes}
    #creates dictionary where key is each class and value is list of possible combination of other classes and times
    neighbors = {var: [v for v in classes if v != var] for var in classes}
    #creates dictionary where key is each class and value is list of all other classes
    min_preference_count = 11
    #min count for preference count set to 11 becuase max preference is 10 so must update in first iteration
    schedCheck = [('CSB 130', ' 9 am'), ('CSB 325', ' 9 am'), ('CSB 425', ' 9 am'), ('CSB 130', '12 pm'), ('CSB 325', '12 pm'), ('CSB 425', '12 pm'), ('CSB 130', ' 4 pm'), ('CSB 325', ' 4 pm'), ('CSB 425', ' 4 pm') ]
    #harcoded list of all rooms at all of the preferred times 9pm, 12pm, and 4pm
    for x in range(iterations):                                    #loops through iterations
        preference_count = 0                                       #initializes preference count as zero
        solution, steps = min_conflicts(classes, domains, constraints_ok, neighbors, max_steps=max_steps)
        #runs min conflict algorithm
        swap = dict((v,k) for k,v in solution.items())             #swaps key and values for solution from min conflicts           
        for y in schedCheck:                                       #loops through hardcoded list of preferred room and times
            if swap.get(y, 0) != 0:                                #if class occurs during preferred room and time
                preference_count += 1                              #add 1 to preference count
        if not (((solution.get('CS163', (0,0))[1] == ' 1 pm') or (solution.get('CS163', (0,0))[1] == ' 2 pm')) and ((solution.get('CS164', (0,0))[1] == ' 1 pm') or (solution.get('CS164', (0,0))[1] == ' 2 pm'))):
        #check if CS163 is at 1pm or 2pm and if CS164 is at 1pm or 2pm isn't true
            preference_count += 1                                   #add 1 to preference count
        if(preference_count < min_preference_count):                #if current preference count is less then min_preference count
            solutionf = solution                                    #update solutionf to current solution
            stepsf = steps                                          #update stepsf to current steps
            min_preference_count = preference_count                 #update min preference count to current preference count
    return solutionf, stepsf                                        #return solutionf and stepsf

assignments, steps = prefer_schedule(classes, times, rooms, 100)
print('Took', steps, 'steps')
print(assignments)
display(assignments, rooms, times)


# In[7]:

get_ipython().magic('run -i A6grader.py')

