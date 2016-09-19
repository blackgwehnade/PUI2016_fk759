
# coding: utf-8

# In[6]:

import sys
import json
import numpy as np
import pandas as pd
try:
    import urllib2 as urllib
except ImportError:
    import urllib.request as urllib


# In[7]:

userkey = sys.argv[1]
busnum = sys.argv[2]
outputfile = sys.argv[3]

bus_key = '8fb4f0dc-8ff5-4dcf-8f53-4fde1a25b0c7'
bus_line = 'M15'
def display_bus_approach_status(bus_key, bus_line):
    
    def get_jsonparsed_data(url):
        
        response = urllib.urlopen(url)
        data = response.read().decode("utf-8")
        return json.loads(data)
    
    """
    from http://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + bus_key + "&VehicleMonitoringDetailLevel=calls&LineRef=" + bus_line
    buses = get_jsonparsed_data(url)
    active_buses = len(buses['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'])
    my_buses = buses['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']
    
    df = pd.DataFrame([], columns=list(['Latitude', 'Longitude', 'Stop_Name', 'Distance_Away']))
    
    print ("Requested Bus Service: " + bus_line)
    print ("Total # of Buses active on route: " + str(active_buses))
    for i in range(active_buses):
        bus_pos = my_buses[i]['MonitoredVehicleJourney']['VehicleLocation']
        bus_stop_next = my_buses[i]['MonitoredVehicleJourney']['MonitoredCall']
        stations_away = my_buses[i]['MonitoredVehicleJourney']['OnwardCalls']['OnwardCall'][0]['Extensions']['Distances']
        print ("Bus number %i is at coordinates: (%f, %f). The next stop is %s, and the bus is currently %s  " % (i, bus_pos['Latitude'], bus_pos['Longitude'], bus_stop_next['StopPointName'], stations_away['PresentableDistance']))
        df.loc[len(df)] = [bus_pos['Latitude'], bus_pos['Longitude'], bus_stop_next['StopPointName'], stations_away['PresentableDistance']]
    df.to_csv(path_or_buf = outputfile)
display_bus_approach_status(bus_key, bus_line)


# In[ ]:



