from collections import defaultdict
import glob 
csvfiles = glob.glob("*.csv")



def getdate(line):
	timestamp = line.split(",")[0]
	date = timestamp.split("T")[0]
	return_date = date.replace("/","_")
	return return_date
	
def is_morning(line):
	timestamp = line.split(",")[0]
	hour = timestamp.split("T")[1][:2]
	if hour < '12':
		return True
	else:
		return False

def parse_measurement(infile):
	testlines = open(infile, 'r').readlines()
	day_data = defaultdict(list)
	headline = testlines[0]
	measurement = headline.split(",")[-1].strip()
	for line in testlines[1:]:
	    date = getdate(line)
	    if is_morning(line):
	    	time_key = date + '_am_' + measurement + ".csv"
	        day_data[time_key].append(line)   	
	    else:
	    	time_key = date + '_pm_' + measurement + ".csv"
	        day_data[time_key].append(line)
		    
	keys = day_data.keys()
	print keys
	for key in keys:
		printdata = day_data[key]	
		f=open(key, "w")
		f.write(headline)
		for line in printdata:
			print line
			f.write(line)
		f.close()

for infile in csvfiles:
	parse_measurement(infile)