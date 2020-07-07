import mtl


# Assumes piece wise constant interpolation.
data = {
    'a': [(0, True), (1, False), (3, False)],
    'b': [(0, False), (0.2, True), (4, False)]
}

phi = mtl.parse('F(a | b)')
print(phi(data, quantitative=False))
# output: True

phi = mtl.parse('F(a | b)')
print(phi(data))
# output: True

# Note, quantitative parameter defaults to False

# Evaluate at t=3.
print(phi(data, time=3, quantitative=False))
# output: False

# Compute sliding satisifaction.
print(phi(data, time=None, quantitative=False))
# output: [(0, True), (0.2, True), (4, False)]

# Evaluate with discrete time
phi = mtl.parse('X b')
print(phi(data, dt=0.2, quantitative=False))
# output: True

def testclick(a):
    print('testOK!'+a)
