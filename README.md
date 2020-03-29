## EEGLAB XML modifier

This script modifies Matlab EEGLab N400 event coding XML files. Its only function
is to find 'rsp+' events and change the 'rsp+' to the 'cel' value within it.

Author: Oliver Rew

To use, execute the file with python3 and specify the input xml file as the argument.
```
$ python3 events.xml
```

This will dump the output to the terminal. To save to a file, just redirect the output
to the filename of you choosing
```
$ python3 events.xml > events_modified.xml
```

NOTE: This was tested with python3 on linux. Mileage may vary on other platforms.
