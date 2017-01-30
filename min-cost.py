# min-max flow: min-cost LP
# this model is intended to minimize the cost to transport through a network of arcs and nodes

# ---- setup the model ----

from pyomo.environ import *    # imports the pyomo envoirnment
model = AbstractModel()    # creates an abstract model
model.name = "Minimum Cost LP Model"    # gives the model a name

# ---- define set(s) ----

model.N = Set()    # a set of nodes
model.A = model.N * model.N    # a set of arcs within the elements of set N
model.O = Set()    # the origin nodes of set N
model.T = Set()    # the transshipment nodes of set N
model.D = Set()    # the destination nodes of set N

# ---- define parameter(s) ----

model.c = Param(model.A, initialize = 0)    # the cost of an arc
model.l = Param(model.A, initialize = 0)    # the flow limit of an arc
model.d = Param(model.N, initialize = 0)    # the demand of items at a node
model.s = Param(model.N, initialize = 0)    # the initial supply of items at a node

# ---- define variable(s) ----

def xbounds_rule(model, i, j):
    return(0, model.l[i,j])    # non-negativity and upper limit constraint on 'x'

model.x = Var(model.A, bounds = xbounds_rule, domain = NonNegativeReals)    # the total amount of items sent on an arc

# ---- define objective function(s) ----

def obj(model):
    return sum(model.c[i,j] * model.x[i,j] for [i,j] in model.A)    # the cost to transport items from suppliers to consumers

model.obj = Objective(rule = obj, sense = minimize)    # a minimization problem of the function defined above

# ---- define constraint(s) ----

def Supp(model, i):
    return sum(model.x[i,j] for j in model.N) <= model.s[i]    # a supplier node cannot satisfy a consumer node with items it doesn't have

def Cons(model, j):
    return sum(model.x[i,j] for i in model.N) >= model.d[j]    # a consumer node's demands must be satisfied

def Tran(model, i):
    return sum(model.x[k,i] for k in model.N) - sum(model.x[i,j] for j in model.N) == 0    # defines node i as a transshipment node

model.Suppliers = Constraint(model.O, rule = Supp)    # the constraint for supplier nodes
model.Transshipment = Constraint(model.T, rule = Tran)    # the constraint for transshipment nodes
model.Consumers = Constraint(model.D, rule = Cons)    # the constraint for consumer nodes

# ---- execute solver ----

from pyomo.opt import SolverFactory
opt = SolverFactory("glpk")
# opt = SolverFactory('ipopt',solver_io='nl')
instance = model.create_instance("min-cost.dat")
results = opt.solve(instance)
instance.display()