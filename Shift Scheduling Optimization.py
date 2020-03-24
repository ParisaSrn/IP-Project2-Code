'''
Shift Scheduling Optimization Model
Advisor: Dr. Baski Balasundaram
Parisa Sahraeian
'''
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd

#Importing Data
datafile = "demand_1.csv"
file = "IP Project2 Data.TXT"
X=np.loadtxt(file, skiprows=2).astype(int)
R = pd.read_csv(datafile,header=None)

#Parameters:
#minimum and maximum duration of shifts
d_min = X[0,0]
d_max=X[0,1]
#number of shifts, number of schedules
n=X[1,0]
m=X[1,1]
print(n)
#number of time slots 
T = X[2,0]
#Getting Time limit in seconds
tl= X[3,0]
#break between the shifts
delta= X[4,0]
#Requirements of every time slot
r = np.array(R)
#Defining the model
modell = gp.Model("Shift Scheduling Optimization")

# Decision variables
startt = modell.addVars(range(1,n+1),range(1,m+1), vtype=GRB.INTEGER, obj=-1)
complt = modell.addVars(range(1,n+1),range(1,m+1), vtype=GRB.INTEGER, obj=1)
z_ijk = modell.addVars(range(1,n+1),range(1,m+1),range(1,T+1), vtype=GRB.BINARY)

# We want to minimize the total costs
modell.modelSense = GRB.MINIMIZE

#adding costraints
modell.addConstrs(startt[i+1,j]>=complt[i,j]+delta for i in range(1,n) for j in range(1,m+1))
modell.addConstrs(complt[i,j]-startt[i,j]>=d_min for i in range(1,n+1) for j in range(1,m+1))
modell.addConstrs(complt[i,j]-startt[i,j]<=d_max for i in range(1,n+1) for j in range(1,m+1))
modell.addConstrs(sum(z_ijk[i,j,k] for i in range(1,n+1) for j in range(1,m+1))>=r[k-1][0] for k in range(1,T+1))
modell.addConstrs(startt[i,j]<=k*z_ijk[i,j,k]+T*(1-z_ijk[i,j,k]) for i in range(1,n+1) for j in range(1,m+1) for k in range(1,T+1))
modell.addConstrs(complt[i,j]>=k*z_ijk[i,j,k] for i in range (1,n+1) for j in range(1,m+1) for k in range(1,T+1))

#Time limit
#modell.params.timelimit= tl

# Solve
modell.params.DualReductions = 0
#modell.feasRelaxS(0, True, False, True)
modell.optimize()
modell.computeIIS()
modell.write("model.lp")
