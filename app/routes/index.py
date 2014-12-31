from app import app
from flask import request
from flask import jsonify
import os
import string

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/airports')
def airports():
    from os import listdir
    #print os.path.dirname(__file__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    profile_dir = os.path.join(basedir, 'airport')
    return jsonify({'airports': listdir(profile_dir)})

@app.route('/flight')
def flight():
    hour, minute, second, port = request.args['hour'],request.args['minute'],request.args['second'],request.args['port']
    hour, minute, second, port = map(string.atoi, [hour, minute, second, port])
    airport = request.args['airport']
    results = decide_flight_action(hour,minute,second,port,airport)


    return jsonify(results)



def decide_flight_action(hour,land,second,port,airport):

    DELTA = 25.0 / 60.0

    basedir = os.path.abspath(os.path.dirname(__file__))

    profile_path = os.path.join(basedir, 'airport/'+airport)

    profile = open(profile_path).readlines()
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

    #hour, land, port = input()


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
    arr_time = "%d:%d" % (hour, land)
    arr_time = "%02d:%02d:%02d" % (hour, (land*60+second)/60 , (land*60.0+second)%60)

    for r in cond[hour]:
        if (r[0] < land) and (land <= r[2]):
            if r[1] == 'W':
                return {'time':arr_time,'port': port ,'action':'C' , 'cost':str(tit[port-1] * 60)}
            else:
                for i in range(current+1, len(cond[hour])):
                    if cond[hour][i][1] == 'W': # or cond[hour][i][1] == 'G':
                        break
                wc_time = (tit[port-1] + cond[hour][i][0] - land + DELTA ) * 60
                if wc_time < tie[port-1] : # 3 replaced by tie
                    return {'time':arr_time,'port': port ,'action':'W-C' , 'cost':str(wc_time)}
                else:
                    return {'time':arr_time,'port': port ,'action':'EAT' , 'cost':str(tie[port-1])}
            break
        current += 1

