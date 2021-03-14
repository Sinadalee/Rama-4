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

def getedge(sensorid, vol):
    txt = '        <edge id="<EDGE_ID>" entered="<ENTERED_VEH_NUMBER>"/> <!--<DETAIL>-->\n'
    edgeid = df_sensor[df_sensor['SensorID'] == sensorid].EdgeID.to_string()[5:]
    detail = df_sensor[df_sensor['SensorID'] == sensorid].SensorDetail.to_string()[5:]
    #detail = df_lane[df_lane['id'] == "'"+laneid+"'"].name.to_string()[5:]

    txt = txt.replace("<EDGE_ID>", edgeid)
    txt = txt.replace("<ENTERED_VEH_NUMBER>", vol)
    txt = txt.replace("<DETAIL>", detail)

    xml.write(txt)
    print(txt)
    return txt

filename_vol = 'Volume_SampleData_Lane.csv'
filename_sensor = 'SensorData.csv'
filename_lane = 'namelane.csv'
filename_xml = "edgecount.xml"
df_vol = pd.read_csv(filename_vol)
df_sensor = pd.read_csv(filename_sensor)
df_lane = pd.read_csv(filename_lane)
xml = open(filename_xml, "w")

sensorlane_list = list(df_vol.columns)[1:] # list of all sensors and lanes id

now = datetime.now()
xml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
xml.write('<!--This "'+filename_xml+'" file is generated on '+str(now)+
          '\n    by "LaneCountGenerator.py" with input file 1)"'+filename_vol+'" 2)"'+filename_sensor+'"-->\n')
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

    sensorlane_list_drop = list(row.index[1:])

    count_sum = 0
    for sensorlane_id in sensorlane_list_drop: # for every sensor and lane data
        sensor_id = sensorlane_id[:-2]
        vol = row[sensorlane_id]
        count_sum += vol

        # if 1) last row or 2)new sensor in next row
        if sensorlane_list_drop.index(sensorlane_id) + 1 == len(sensorlane_list_drop) or \
            sensor_id != sensorlane_list_drop[sensorlane_list_drop.index(sensorlane_id)+1][:-2]:
            count_sum = str(count_sum)
            getedge(sensor_id, count_sum)
            count_sum = 0

    xml.write('    </interval>\n')

xml.write('</meandata>\n')
xml.close()