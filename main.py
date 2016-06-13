import random
import pygame
from multiprocessing import Queue , Process
import os
import time
from  matplotlib import pyplot
current_milli_time = lambda: int(round(time.time() * 1000))
def generateRandomPoints(n):

    P = []
    for i in range(n):
        x= random.randint(0,1024)
        y= random.randint(0,720)
        P.append((x,y))
    points = map(None,P)
    points.sort()
    return points
def Det(p, q, r):
    sum1 = q[0]*r[1] + p[0]*q[1] + r[0]*p[1]
    sum2 = q[0]*p[1] + r[0]*q[1] + p[0]*r[1]
    return sum1 - sum2
def isRightTurn((p, q, r)):
    #assert p != q and q != r and p != r
    if Det(p, q, r) < 0:
        return 1
    else:
        return 0
def ConvexHullUpper(P,ans):
    #info("upper convexhull")
    upper=[]
    upper.append(P[0])
    upper.append(P[1])
    for i in range(3,len(P)):
        upper.append(P[i])
        l = len(upper)
        while l > 2 and isRightTurn((upper[l-1], upper[l-2], upper[l-3]))==0:
            del upper[l-2]
            l = len(upper)
    ans.put(upper)
def ConvexHullLower(P,ans):
    #info("lower convexhull")
    lower =[]
    lower.append(P[len(P)-1])
    lower.append(P[len(P)-2])
    for j in range(len(P)-2,0,-1):
        lower.append(P[j])
        l = len(lower)
        while(l >2 and isRightTurn((lower[l-1], lower[l-2], lower[l-3]))==0):
            del lower[l-2]
            l = len(lower)
    ans.put(lower)
def info(title):
    print title
    if hasattr(os, 'getppid'):  # only available on Unix
        print 'parent process:', os.getppid()
    print 'process id:', os.getpid()
def ConvexHullSeq(P):
    t1 = current_milli_time()
    upper=[]
    upper.append(P[0])
    upper.append(P[1])
    for i in range(3,len(P)):
        upper.append(P[i])
        l = len(upper)
        while l > 2 and isRightTurn((upper[l-1], upper[l-2], upper[l-3]))==0:
            del upper[l-2]
            l = len(upper)
    lower =[]
    lower.append(P[len(P)-1])
    lower.append(P[len(P)-2])
    for j in range(len(P)-2,0,-1):
        lower.append(P[j])
        l = len(lower)
        while(l >2 and isRightTurn((lower[l-1], lower[l-2], lower[l-3]))==0):
            del lower[l-2]
            l = len(lower)
    del lower[0]
    del lower[-1]
    t2=current_milli_time()
    return tuple(upper + lower) , (t2-t1)

def ConvexHullParallel(P):
    t1 = current_milli_time()
    ans =Queue()
    upperp = Process(target=ConvexHullUpper, args=(P,ans))
    lowerp = Process(target=ConvexHullLower , args=(P,ans))
    upperp.start()
    lowerp.start()
    upperp.join()
    lowerp.join()
    upper = ans.get()
    lower = ans.get()
    del lower[0]
    del lower[-1]
    t2=current_milli_time()
    return tuple(upper + lower) ,t2-t1
#exp
time_parallel =[]
time_seq=[]
pointsn=[]
for i in range(10,100000,1000):
    points = generateRandomPoints(i)
    [sp,tp]=  ConvexHullParallel(points)
    [sq,tq]= ConvexHullSeq(points)
    time_parallel.append(tp)
    time_seq.append(tq)
    pointsn.append(i)
print len(pointsn) , len(time_parallel)
pyplot.xlabel('Number of points')
pyplot.ylabel('Time')
pyplot.plot(pointsn,time_parallel, "rs" , pointsn , time_seq,"g^")
pyplot.show()
points = generateRandomPoints(100)
s,t= ConvexHullParallel(points)
pygame.init()
screen = pygame.display.set_mode((1024,720))
red = (255,0,0)
white = (255,255,255)
for p in points:
    pygame.draw.circle(screen, red , p , 10, 10)
    pygame.display.update()
s = list(s)
pygame.draw.lines(screen,white , True, s, 10)
pygame.display.update()
running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

