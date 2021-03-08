import pandas as pd
from datetime import datetime
from datetime import timedelta

def getinterval(begin, end, id):
    pt = datetime.strptime(end, '%H:%M:%S')
    end_sec = pt.second + pt.minute * 60 + pt.hour * 3600
    begin_sec = end_sec - 5
    begin = str(timedelta(seconds=begin_sec))
    begin_sec = str(begin_sec)
    end_sec = str(end_sec)
    detail = begin + ' - ' + end
    txt = '    <interval begin="<INTERVAL_BEGIN>" end="<INTERVAL_END>" id="<DETECTOR_ID>"> <!--<DETAIL>-->\n'
    txt = txt.replace("<INTERVAL_BEGIN>", begin_sec)
    txt = txt.replace("<INTERVAL_END>", end_sec)
    txt = txt.replace("<DETECTOR_ID>", id)
    txt = txt.replace("<DETAIL>", detail)

    print(txt)
    xml.write(txt)
    return txt

def getedge(sensorid):
    edgeid = df_sensor[df_sensor['SensorID'] == sensorid].EdgeID.to_string()[5:]
    detail = df_sensor[df_sensor['SensorID'] == sensorid].SensorDetail.to_string()[5:]
    txt = '        <edge id="<EDGE_ID>"> <!--<DETAIL>-->\n'
    txt = txt.replace("<EDGE_ID>", edgeid)
    txt = txt.replace("<DETAIL>", detail)

    xml.write(txt)
    print(txt)
    return txt

def getlane(sensorid, lane, vol):
    txt = '            <lane id="<LANE_ID>" left="<LEFT_VEH_NUMBER>"/> <!--<DETAIL>-->\n'
    edgeid = df_sensor[df_sensor['SensorID'] == sensorid].EdgeID.to_string()[5:]
    laneid = edgeid + '_' + lane
    #detail = df_sensor[df_sensor['SensorID'] == sensorid].SensorDetail.to_string()[5:] + '_L' + lane
    detail = df_lane[df_lane['id'] == "'"+laneid+"'"].name.to_string()[5:]

    txt = txt.replace("<LANE_ID>", laneid)
    txt = txt.replace("<LEFT_VEH_NUMBER>", vol)
    txt = txt.replace("<DETAIL>", detail)

    xml.write(txt)
    print(txt)
    return txt

filename_vol = 'Volume.csv'
filename_sensor = 'SensorData.csv'
filename_lane = 'namelane.csv'
df_vol = pd.read_csv(filename_vol)
df_sensor = pd.read_csv(filename_sensor)
df_lane = pd.read_csv(filename_lane)
xml = open("edgecount.xml", "w")

sensorlane_list = list(df_vol.columns)[1:] # list of all sensors and lanes id

now = datetime.now()
xml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
xml.write('<!--This "edgecount.xml" file is generated on '+str(now)+
          '\n    by "EdgeCountGenerator.py" with input file 1)"'+filename_vol+'" 2)"'+filename_sensor+'"-->\n')
xml.write('<meandata>\n')

for index, row in df_vol.iterrows(): # for every timestamp

    # drop data for not working sensors
    row = row.drop(list(sensorlane_id for sensorlane_id in sensorlane_list if row[sensorlane_id] == -1))
    # if no data in this interval -> next interval
    if len(row) == 1: continue

    # define input for getinterval()
    begin = ''
    end = row['Time']
    id = 'generated'

    # write interval in xml
    getinterval(begin, end, id)
    currentsensor = ''

    sensorlane_list_drop = list(row.index[1:])
    for sensorlane_id in sensorlane_list_drop: # for every sensor and lane data
        sensor_id = sensorlane_id[:-2]
        lane_id = sensorlane_id[-1:]
        vol = str(row[sensorlane_id])

        if sensor_id != currentsensor: # if current id is new sensor, edge
            getedge(sensor_id)
            currentsensor = sensor_id

        getlane(sensor_id, lane_id, vol)

        # if current id is new or last sensor, edge
        if sensorlane_id == sensorlane_list_drop[-1] or sensor_id != sensorlane_list_drop[sensorlane_list_drop.index(sensorlane_id)+1][:-2]:

            xml.write('        </edge>\n')

    xml.write('    </interval>\n')

xml.write('</meandata>\n')
xml.close()