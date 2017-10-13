# -*- coding: utf-8 -*-
# 百度2015校招机器学习笔试题第三题
# cannot believe it's not easy
import random
import math

# sine and cosine of randome angle in 2D
# Generate u1 and u2. Then v1=2u1-1 is uniform on (-1,1), and v2=u2 is uniform
# on (0,1). Calculate r^2=v1^2+v2^2. If r^2>1, start over. Otherwise the sine(S)
# and cosine(C) of a randome angle(i.e. uniformly distributed between 0 and 2pi) are
# S = 2v1v2/r^2  and  C = (v1^2-v2^2)/r^2
# http://pdg.lbl.gov/2012/reviews/rpp2012-rev-monte-carlo-techniques.pdf
# https://stackoverflow.com/questions/31291174/buffons-needle-simulation-in-python
    

def simple_sine_cosine():
    theta = random.uniform(0,math.pi/2)
    return math.sin(theta), math.cos(theta)

# one group of parallel lines
class BuffonNeedle1Group:
    def __init__(self,x,y,n,m):
        self.x = float(x) #width of the needle
        self.y = float(y) #width of the space
        self.r = [] #the center of the needle (it could be the shortest distance to the lines or (self.y - the shortest distance to the line))
        self.z = [] #the shortest distance of the center of the needle to the lines
        self.n = n #No. of the throws
        self.m = m #No. of the simulations
        self.p = self.x/self.y
        self.pi = []

    def samples(self):
        for i in range(self.n):
            self.r.append(random.uniform(0,self.y/2.))
            s = simple_sine_cosine()[0]
            self.z.append(s*self.x/2.)
        return self.r, self.z

    def simulation(self):
        for j in range(self.m):
            self.r=[]
            self.z=[]
            self.samples()
            #n throw
            hits=0
            for i in range(self.n):
                if self.z[i]>=self.r[i]:
                    hits += 1
            est = 2*self.p*float(self.n)/float(hits)
            self.pi.append(est)
        return self.pi

# Two groups to parallel lines which are perpendicular to each other
# Suppose the length of the needle and distance of space are x, y respectively
# Suppose p,q are the shortest distances of the middle point of the needle to the horizontal lines and vertical lines respectively. Then 0 <= p < y/2 and 0 <= q < y/2
# Suppose theta are the acute angle of the needle and horizontal line which is closest to the middle point.
# Then that the needle does not follow on any lines is equivalent to:
# sin(theta)*x/2 < p <= y/2 and cos(theta)*x/2 < q <= y/2
# Then the probability of no crossing is:
# (\int_{0}^{pi/2}(y/2-sin(theta)*x/2)*(y/2-cos(theta)*x/2)d\theta) / ((pi/2)*(y^2/4))
# = 1 - 4*x/(pi*y) + x^2/(pi*y^2)
# Thus the probability of having crossing is 4*x/(pi*y) - x^2/(pi*y^2)

class BuffonNeedle2Group:
    def __init__(self,x,y,n,m):
        self.x=float(x)
        self.y=float(y)
        self.n=n
        self.m=m
        self.p=self.x/self.y
        self.r=[]
        self.z=[]
        self.pi=[]
    def samples(self):
        for i in range(self.n):
            self.r.append((random.uniform(0,self.y/2.),random.uniform(0,self.y/2.)))
            s,c = simple_sine_cosine()
            self.z.append((s*self.x/2., c*self.x/2.))
        return self.r, self.z
    def simulation(self):
        for j in range(self.m):
            self.r, self.z = [], []
            self.samples()
            hits = 0
            for i in range(self.n):
                if self.z[i][0] >= self.r[i][0] or self.z[i][1] >= self.r[i][1]:
                    hits += 1
            est = (4-self.p)*self.p*float(self.n)/float(hits)
            self.pi.append(est)
        return self.pi

B1 = BuffonNeedle1Group(1,2,500000,5)
print(B1.simulation())

B2 = BuffonNeedle2Group(1,2,500000,5)
print(B2.simulation())
