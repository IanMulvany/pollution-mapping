from xml.dom import minidom
from xml.dom.minidom import Document
import glob 

test_csv_file = 'data/100510_ianwalk_8.csv'
test_gpx = 'data/Data.gpx.xml'

def read_pollution_data():
    p_data = open(test_csv_file, 'r').readlines()  
    p_data_point={"time":'','total_particles':0,'pm10':0,'pm2.5':0,'pm1':0}
    p_points=[]
    for measurement in p_data[2:]: #first two rows describe data format
        items=measurement.split(',')
        time=items[0]
        total_particles=items[1]
        pmten=items[2]
        pmtwopointfive=items[3]
        pmone=items[4]
        p_points.append({"time":time,'total_particles':total_particles,'pm10':pmten,'pm2.5':pmtwopointfive,'pm1':pmone})
    return p_points
        
def read_geo_data():
    xmldata = minidom.parse('test_gpx')
    t_points_xml = xmldata.getElementsByTagName('trkpt')
    
    def get_data_from_trippoint(point):
        lat=point.attributes['lat'].value
        lon=point.attributes['lon'].value
        elevation = point.getElementsByTagName('ele')[0].firstChild.data.encode('latin-1')
        time = point.getElementsByTagName('time')[0].firstChild.data.encode('latin-1')
        return {'time':time, 'lat':lat, 'lon':lon, 'elevation':elevation}
    
    t_points=[]
    for point in t_points_xml:
        t_data_point=get_data_from_trippoint(point)
        t_points.append(t_data_point)
    
    return t_points

# ok now we try to match some of the points together
# instead of creating an inverted data object indexed on the time,
# I'm not going to worry about it, as we are dealing with such a small amount of data

# data_keys are represented in p_points.keys()
#data_key='pm10'
data_key='total_particles'
def zip_location_and_geo(data_key):
    def time_from_t_point(point):
        return point['time'].split('T')[1   ][0:-4]
    
    def data_at_time(time, data_key):
        # this function is problematic as we call a static data object directly into this function
        time_pmten_values = []
        for point in p_points:  
            #print time, point
            #print point['time']#.split()[1]
            if point['time'].split()[1] == time:
                pmten=point[data_key]
                time_pmten_values.append(pmten)
        if time_pmten_values:
            return time_pmten_values
        else:
            return None 

    for location in t_points:
        lat=location['lat']
        lon=location['lon']
        elevation=location['elevation']
        time=time_from_t_point(location)
        if data_at_time(time, data_key):
            #print lat, lon, elevation, data_at_time(time, data_key)
            height=data_at_time(time, data_key)[0]
            print 'ge.getFeatures().appendChild(createPolygon(%s,%s,%s));' % (lat,lon,height)
        else:
            continue

p_points=read_pollution_data()
t_points=read_geo_data()
zip_location_and_geo(data_key)