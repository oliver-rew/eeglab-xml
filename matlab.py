import xml.etree.ElementTree as ET 
import sys

# This script modifies Matlab EEGLab N400 event coding XML files. Its only function
# is to find 'rsp+' events and change the 'rsp+' to the 'cel#' value within it.
#
# Author: Oliver Rew
#
# To use, execute the file with python3 and specify the input xml file as the argument.
# $ python3 events.xml
# 
# This will dump the output to the terminal. To save to a file, just redirect the output
# to the filename of you choosing
# $ python3 events.xml > events_modified.xml
#
# NOTE: This was tested with python3 on linux. Mileage may vary on other platforms.

# read the filename from the first argument
xmlfile = sys.argv[1]

# this could also be done by hardcoding the filename below
#xmlfile =  "/home/rew/Events_ECI TCP-IP 55513.xml"

# register the file's name space so it is not included in the output file. However
# this could vary on future files, so it might need to be modified. This came from 
# the second line the input xml file:
# <eventTrack ="http://www.egi.com/event_mff" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
ET.register_namespace('', "http://www.egi.com/event_mff")

# parse the xml file
tree = ET.parse(xmlfile) 

# get the first element 
root = tree.getroot() 

# set the schema tag. This is based on the second line of the input file:
# <eventTrack ="http://www.egi.com/event_mff" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")

# iterate through all events in the file
for event in root.findall('{http://www.egi.com/event_mff}event'): 
    
    # find the event code
    code = event.find("{http://www.egi.com/event_mff}code")

    # we only care about 'rsp+' events
    if code.text == "rsp+":
        # get the 'rsp+' keys
        keys = event.find("{http://www.egi.com/event_mff}keys")

        # loop through all the keys in the 'rsp+' event
        found = False
        for key in keys.findall("{http://www.egi.com/event_mff}key"):
            
            # get the keycode for each key
            keyCode = key.find("{http://www.egi.com/event_mff}keyCode")

            # if we can't find a key code here, fail
            if keyCode is None:
                raise ValueError("no 'keyCode' key found in key")

            # we are looking for the 'cel#' keycode
            if keyCode.text == "cel#":
                data = key.find("{http://www.egi.com/event_mff}data")

                # if we can't find data here, fail
                if data is None:
                    raise ValueError("no 'data' key found in key")
    
                # Hooray! We found the 'cel#' keycode in the 'rsp+' event. Now, write
                # the keycode in place of the 'rsp+' key
                code.text = data.text

                # flag that we found the key.
                found = True

        # check that we found the needed 'keyCode' in each 'rsp+' event. If we did not
        # then something is wrong and we should fail
        if found == False:
            raise ValueError("No 'cel# key found in 'rsp+' event")

# dump the file
print(ET.tostring(root, encoding='utf8', method='xml').decode("utf-8"))
