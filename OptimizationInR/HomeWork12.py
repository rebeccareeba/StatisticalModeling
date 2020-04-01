#!/usr/bin/env python
# coding: utf-8

# # HomeWork 12
# # ISYE 6501
# ## Question 15.2
# 
#  In the videos, we saw the “diet problem”. (The diet problem is one of the first large-scale optimization 
# problems to be studied in practice. Back in the 1930’s and 40’s, the Army wanted to meet the nutritional 
# requirements of its soldiers while minimizing the cost.) In this homework you get to solve a diet problem with real data. The data is given in the file diet.xls.
# 1.Formulate an optimization model (a linear program) to find the cheapest diet that satisfies the maximum and minimum daily nutrition constraints, and solve it using PuLP. Turn in your code and the solution. (The optimal solution should be a diet of air-popped popcorn, poached eggs, oranges, raw iceberg lettuce, raw celery, and frozen broccoli. UGH!) 
# ## Answer:
# 

# In[2]:


# Import PuLP modeler functions
from pulp import *
import pandas as pd
import numpy as np


data = pd.read_excel("diet.xls", header = 0) # read all data

#food data is stored in rows 1-65 in the excel sheet
data = data[0:64]


# In[3]:


#Convert the dataframe into a dictionaries
costs= dict(zip(data.Foods, data['Price/ Serving']))

Calories = dict(zip(data.Foods, data['Calories']))

Cholesterol = dict(zip(data.Foods, data['Cholesterol mg']))

Total_Fat = dict(zip(data.Foods, data['Total_Fat g']))

Sodium = dict(zip(data.Foods, data['Sodium mg']))

Carbohydrates = dict(zip(data.Foods, data['Carbohydrates g']))

Dietary_Fiber = dict(zip(data.Foods, data['Dietary_Fiber g']))

Protein = dict(zip(data.Foods, data['Protein g']))

Vit_A = dict(zip(data.Foods, data['Vit_A IU']))

Vit_C = dict(zip(data.Foods, data['Vit_C IU']))

Calcium = dict(zip(data.Foods, data['Calcium mg']))

Iron = dict(zip(data.Foods, data['Iron mg']))


# In[4]:


# It may be easier to convert dataframe to list
data = data.values.tolist()
#data


# In[5]:


# stor the food names in a seperate list
Foods = [x[0] for x in data]

#costs= data.set_index('')


# In[6]:


# create the optimization problem framework - minimization problem
prob = LpProblem("The Diet", LpMinimize)

# define the variables - continous
amountVars = LpVariable.dicts("Food",Foods,0)


# The objective function is added to 'prob' first
prob += lpSum([costs[i]*amountVars[i] for i in Foods]), "Total Cost of Foods per person"

# The 22 constraints are added to 'prob'

prob += lpSum([Calories[i] * amountVars[i] for i in Foods]) >= 1500, "Caloriesmin"
prob += lpSum([Calories[i] * amountVars[i] for i in Foods]) <= 2500, "CaloriesMax"

prob += lpSum([Cholesterol[i] * amountVars[i] for i in Foods]) >= 30, "Cholesterolmin"
prob += lpSum([Cholesterol[i] * amountVars[i] for i in Foods]) <= 240, "CholesterolMax"

prob += lpSum([Total_Fat[i] * amountVars[i] for i in Foods]) >= 20, "Total_Fatmin"
prob += lpSum([Total_Fat[i] * amountVars[i] for i in Foods]) <= 70, "Total_FatMax"

prob += lpSum([Sodium[i] * amountVars[i] for i in Foods]) >= 800, "Sodiummin"
prob += lpSum([Sodium[i] * amountVars[i] for i in Foods]) <= 2000, "SodiumMax"

prob += lpSum([Carbohydrates[i] * amountVars[i] for i in Foods]) >= 130, "Carbohydratesmin"
prob += lpSum([Carbohydrates[i] * amountVars[i] for i in Foods]) <= 450, "CarbohydratesMax"

prob += lpSum([Dietary_Fiber[i] * amountVars[i] for i in Foods]) >= 125, "Fibersmin"
prob += lpSum([Dietary_Fiber[i] * amountVars[i] for i in Foods]) <= 250, "FiberMax"

prob += lpSum([Protein[i] * amountVars[i] for i in Foods]) >= 60, "Proteinmin"
prob += lpSum([Protein[i] * amountVars[i] for i in Foods]) <= 100, "ProteinMax"

prob += lpSum([Vit_A[i] * amountVars[i] for i in Foods]) >= 1000, "Vit_Amin"
prob += lpSum([Vit_A[i] * amountVars[i] for i in Foods]) <= 10000, "Vit_AMax"

prob += lpSum([Vit_C[i] * amountVars[i] for i in Foods]) >= 400, "Vit_Cmin"
prob += lpSum([Vit_C[i] * amountVars[i] for i in Foods]) <= 5000, "Vit_CMax"

prob += lpSum([Calcium[i] * amountVars[i] for i in Foods]) >= 700, "Calciummin"
prob += lpSum([Calcium[i] * amountVars[i] for i in Foods]) <= 1500, "CalciumMax"

prob += lpSum([Iron[i] * amountVars[i] for i in Foods]) >= 10, "Ironmin"
prob += lpSum([Iron[i] * amountVars[i] for i in Foods]) <= 40, "IronMax"


# The problem data is written to an .lp file
prob.writeLP("DietModel1.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print ("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    if v.varValue != 0.0:
        print (v.name, "=", v.varValue)

# The optimised objective function value is printed to the screen    
print ("Total Cost of Foods per person = ", value(prob.objective))


# Part 2
# The Second part of our problem is very similar with a few additions before we call prob.solve(). Add the following lines to add binary variables or switches to the code. This will allow us to say, 'If variable is selected, the amount must be at least 0.1', or the like.

# In[8]:


# create the optimization problem framework - minimization problem
prob2 = LpProblem('Constraints trial', LpMinimize)

# define the variables - continous
amountVars = LpVariable.dicts("Food",Foods,0)
# define the variables - binary
chosenVars = LpVariable.dicts("Chosen",Foods,0,1,LpBinary)

# define the objective function
prob2 += lpSum([costs[f] * amountVars[f] for f in Foods])


# The 22 constraints are added to 'prob'

prob2 += lpSum([Calories[i] * amountVars[i] for i in Foods]) >= 1500, "Caloriesmin"
prob2 += lpSum([Calories[i] * amountVars[i] for i in Foods]) <= 2500, "CaloriesMax"

prob2 += lpSum([Cholesterol[i] * amountVars[i] for i in Foods]) >= 30, "Cholesterolmin"
prob2 += lpSum([Cholesterol[i] * amountVars[i] for i in Foods]) <= 240, "CholesterolMax"

prob2 += lpSum([Total_Fat[i] * amountVars[i] for i in Foods]) >= 20, "Total_Fatmin"
prob2 += lpSum([Total_Fat[i] * amountVars[i] for i in Foods]) <= 70, "Total_FatMax"

prob2 += lpSum([Sodium[i] * amountVars[i] for i in Foods]) >= 800, "Sodiummin"
prob2 += lpSum([Sodium[i] * amountVars[i] for i in Foods]) <= 2000, "SodiumMax"

prob2 += lpSum([Carbohydrates[i] * amountVars[i] for i in Foods]) >= 130, "Carbohydratesmin"
prob2 += lpSum([Carbohydrates[i] * amountVars[i] for i in Foods]) <= 450, "CarbohydratesMax"

prob2 += lpSum([Dietary_Fiber[i] * amountVars[i] for i in Foods]) >= 125, "Fibersmin"
prob2 += lpSum([Dietary_Fiber[i] * amountVars[i] for i in Foods]) <= 250, "FiberMax"

prob2 += lpSum([Protein[i] * amountVars[i] for i in Foods]) >= 60, "Proteinmin"
prob2 += lpSum([Protein[i] * amountVars[i] for i in Foods]) <= 100, "ProteinMax"

prob2 += lpSum([Vit_A[i] * amountVars[i] for i in Foods]) >= 1000, "Vit_Amin"
prob2 += lpSum([Vit_A[i] * amountVars[i] for i in Foods]) <= 10000, "Vit_AMax"

prob2 += lpSum([Vit_C[i] * amountVars[i] for i in Foods]) >= 400, "Vit_Cmin"
prob2 += lpSum([Vit_C[i] * amountVars[i] for i in Foods]) <= 5000, "Vit_CMax"

prob2 += lpSum([Calcium[i] * amountVars[i] for i in Foods]) >= 700, "Calciummin"
prob2 += lpSum([Calcium[i] * amountVars[i] for i in Foods]) <= 1500, "CalciumMax"

prob2 += lpSum([Iron[i] * amountVars[i] for i in Foods]) >= 10, "Ironmin"
prob2 += lpSum([Iron[i] * amountVars[i] for i in Foods]) <= 40, "IronMax"

    
# If a food is eaten, must eat at least 0.1 serving

for food in Foods:
    prob2 += amountVars[food] >= 0.1 * chosenVars[food]
    
for food in Foods:
    prob2 += chosenVars[food] >= amountVars[food]*0.0000001 
# Include at most 1 of celery and frozen brocolli

# add contraints to eat at most one of a group of foods    
prob2 += chosenVars['Frozen Broccoli'] + chosenVars['Celery, Raw'] <= 1, 'At most one Broccoli / Celery'


# eat as least 1 from group of food
prob2 += chosenVars['Roasted Chicken'] + chosenVars['Poached Eggs'] +   chosenVars['Scrambled Eggs'] + chosenVars['Frankfurter, Beef'] +   chosenVars['Kielbasa,Prk'] + chosenVars['Hamburger W/Toppings'] +   chosenVars['Hotdog, Plain'] + chosenVars['Pork'] +   chosenVars['Bologna,Turkey'] + chosenVars['Ham,Sliced,Extralean'] +   chosenVars['White Tuna in Water']   >= 3, 'At least three proteins'


# solve the optimization problem!
prob2.solve()


# print the foods of the optimal diet
print('Optimization Solution:')
for var in prob2.variables():
    if var.varValue > 0:
        if str(var).find('Chosen'):
            print(str(var.varValue) + " units of " + str(var))
            
# print the costs of the optimal diet             
print("Total cost of food = $%.2f" % value(prob2.objective))


# In[ ]:




