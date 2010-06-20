from xml.dom import minidom
from xml.dom.minidom import Document
import glob 
from datetime import datetime, date, time
from datetime import timedelta

def get_all_points(filepath, file_eathing_function):
	all_points = []
	files = glob.glob(filepath)
	for data_file in files:
		points = file_eathing_function(data_file)
		all_points.extend(points)
	return all_points

def get_date_from_point(point):
	time = point["time"]
	t = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
	date = `t.year` + "-" + `t.month` + "-" +`t.day`
	hour = t.hour
	return date, hour
	
def read_geo_data(gpxfile):
    xmldata = minidom.parse(gpxfile)
    t_points_xml = xmldata.getElementsByTagName('trkpt')
    def get_data_from_trippoint(point):
        lat=point.attributes['lat'].value
        lon=point.attributes['lon'].value
        elevation = point.getElementsByTagName('ele')[0].firstChild.data.encode('latin-1')
        time = point.getElementsByTagName('time')[0].firstChild.data.encode('latin-1')
       	t = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
        return {'time':t, 'lat':lat, 'lon':lon, 'elevation':elevation}
    t_points=[]
    for point in t_points_xml:
        t_data_point=get_data_from_trippoint(point)
        t_points.append(t_data_point)
    return t_points

def get_all_dates():
	dates = []
	for p in all_points:
		date, hour = get_date_from_point(p)
		if date not in dates: dates.append(date)
	return dates

# get the csv data for every point into a single data object
def read_pollution_data(csv_file):
    p_data = open(csv_file, 'r').readlines()  
    p_data_point={"time":'','total_particles':0,'pm10':0,'pm2.5':0,'pm1':0}
    p_points=[]
    for measurement in p_data[2:]: #first two rows describe data format
        items=measurement.split(',')
        day=items[0] 
        hour=items[1]
        time = day+'T'+hour
        t = datetime.strptime(time, "%d/%m/%YT%H:%M:%S")
        total_particles=items[2]
        pmten=items[3]
        pmtwopointfive=items[4]
        pmone=items[5]
        p_points.append({"time":t,'total_particles':total_particles,'pm10':pmten,'pm2.5':pmtwopointfive,'pm1':pmone})
    return p_points

csv_filepath = "data/*.csv"
gpx_filepath = "data/*.gpx"
csv_points = get_all_points(csv_filepath, read_pollution_data)
gpx_points = get_all_points(gpx_filepath, read_geo_data)

# combine the data and split 
combined_points = []
for gpx in gpx_points:
	min_diff = timedelta(days=1)
	gpx_time = gpx['time']
	for csv in csv_points:
		csv_time = csv['time']
		times = [csv_time, gpx_time]
		times.sort()	
		diff = times[1] - times[0]
		if diff < min_diff:
			min_diff = diff
			best_csv = csv
			best_diff = diff
	if best_diff < timedelta(seconds=30):
		# chagne the time to be a string here
		str_time = gpx['time'].strftime("%Y/%m/%dT%H:%M:%S")
		print gpx['time']
		combined_point = {'lat':gpx['lat'], 'lon':gpx['lon'], 'time':str_time, 'pm1':best_csv['pm1'], 'pm2.5':best_csv['pm2.5'], 'total_particles':best_csv['total_particles'], 'pm10':best_csv['pm10']}
		
		combined_points.append(combined_point)

def mykey(item):
	return item['time']
	
combined_points.sort(key=mykey)

f_ten = open("pm10_location_points.csv","w")
f_twopointfive = open("pm2.5_location_points.csv","w")
f_total = open("total_location_points.csv","w")
f_one = open("pm1.0_location_points.csv","w")

f_ten.write("time, lat, lon, pm10\n")
f_twopointfive.write("time, lat, lon, pm2.5\n")
f_total.write("time, lat, lon, total\n")
f_one.write("time, lat, lon, pm1.0\n")

def prep_string(items):
	output = ",".join(items)
	return_output = output[1:]
	return_output = return_output + "\n"
	return return_output

for point in combined_points:
	f_ten.write(prep_string([point["time"], point['lat'], point['lon'], point['pm10']]))
	f_twopointfive.write(prep_string([point["time"] , point['lat'] , point['lon'], point['pm2.5']]))
	f_total.write(prep_string([point["time"] , point['lat'] , point['lon'], point['total_particles']]))
	f_one.write(prep_string([point["time"] , point['lat'], point['lon'] , point['pm1']]))
	
f_ten.close()
f_twopointfive.close()
f_total.close()
f_one.close()
	
# cut the data by day



# cut the data by morning and afternoon