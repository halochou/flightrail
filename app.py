#!/usr/local/bin/python

import string

DELTA = 25.0 / 60.0

profile = open('airport/32.txt').readlines()
tir = map(string.atoi, profile[0].split(','))
tir = map(lambda x:x/60.0, tir)

tit = map(string.atoi, profile[1].split(','))
tit = map(lambda x:x/60.0, tit)

tie = map(string.atoi, profile[2].split(','))

dep_point = {}
cond = {}

for line in profile[3:]:
    dep_point[string.atoi(line.split()[0])] = map(string.atoi, line.split()[1].split(','))
    cond[string.atoi(line.split()[0])] = []

hour, land, port = input()
land = land + tir[port-1]

for i in range(0,len(dep_point[hour])):
    cond[hour].append((dep_point[hour][i],'B', dep_point[hour][i]+1))
    try:
        if dep_point[hour][i]+1 < dep_point[hour][i+1]-1:
            cond[hour].append( (dep_point[hour][i]+1, 'W', dep_point[hour][i+1]-1) )
        cond[hour].append((dep_point[hour][i+1]-1,'G', dep_point[hour][i+1]))
    except:
        pass

current = 0
for r in cond[hour]:
    if (r[0] < land) and (land <= r[2]):
        if r[1] == 'W':
            print 'C', tit[port-1] * 60
        else:
            for i in range(current+1, len(cond[hour])):
                if cond[hour][i][1] == 'W': # or cond[hour][i][1] == 'G':
                    break
            wc_time = (tit[port-1] + cond[hour][i][0] - land + DELTA ) * 60
            if wc_time < tie[port-1] : # 3 replaced by tie
                print 'W-C', wc_time
            else:
                print 'EAT', tie[port-1]
        break
    current += 1
