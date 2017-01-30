# min-max flow: max-flow LP
# this model is intended to maximize the flow through a network of arcs and nodes

# ---- setup the model ----

from pyomo.environ import *    # imports the pyomo envoirnment
model = AbstractModel()    # creates an abstract model
model.name = "Maximum Flow LP Model"    # gives the model a name

# ---- define set(s) ----

model.N = Set()    # a set of nodes
model.A = model.N * model.N    # a set of arcs within the elements of set N
model.O = Set()    # the origin nodes of set N
model.T = Set()    # the transshipment nodes of set N
model.D = Set()    # the destination nodes of set N

# ---- define parameter(s) ----

model.c = Param(model.A, initialize = 0)    # the capacity of an arc

# ---- define variable(s) ----

def xbounds_rule(model, i, j):
    return(0, model.c[i,j])    # non-negativity and upper limit constraint on 'x'

model.x = Var(model.A, bounds = xbounds_rule, domain = NonNegativeReals)    # the total amount of items sent on an arc
model.y = Var()    # the total amount of items sent to nodes in set D

# ---- define objective function(s) ----

def obj(model):
    return model.y    # the flow from nodes in set O to nodes in set D

model.obj = Objective(rule = obj, sense = maximize)    # a maximization problem of the function defined above

# ---- define constraint(s) ----

def Prod(model, i):
    return sum(model.x[k,i] for k in model.N) - sum(model.x[i,j] for j in model.N) + model.y == 0    # defines node i as a producer node

def Tran(model, i):
    return sum(model.x[k,i] for k in model.N) - sum(model.x[i,j] for j in model.N) == 0    # defines node i as a transshipment node

def Cons(model, i):
    return sum(model.x[k,i] for k in model.N) - sum(model.x[i,j] for j in model.N) - model.y == 0    # defines node i as a consumer node

model.Origin = Constraint(model.O, rule = Prod)    # the constraint for the origin nodes
model.Transshipment = Constraint(model.T, rule = Tran)    # the constraint for transshipment nodes
model.Destination = Constraint(model.D, rule = Cons)    # the constraint for the destination nodes

# ---- execute solver ----

from pyomo.opt import SolverFactory
opt = SolverFactory("glpk")
# opt = SolverFactory('ipopt', solver_io = 'nl')
instance = model.create_instance("max-flow.dat")
results = opt.solve(instance)
instance.display()










