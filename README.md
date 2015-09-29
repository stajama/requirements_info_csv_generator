Quick and dirty scripting to generate a requirements listing with licenses in a csv

How to run this to generate a basic csv:

First, define the lists of requirements.txt files and package.json files.
The default (and, because fast and dirty, currently required) locaiton for this is 
in the current directory, python\_requirements\_list and javascript\_requirements\_list, respectively.  

It's literally just a list of files, but if those files don't exist or they're not in the proper format, it will fail ugly.

Then, run the shell script
./generate\_library\list.sh

This will generate files in /tmp
/tmp/python\_oss\_info.txt, and /tmp/javascript\_oss\_info.txt

Those are the default locations for the python script, so you can just run that too:

./gen\_library\_csv.py

Which will output a file to /tmp/license\_libs.csv.

Which can be imported to google spreadsheet to play with to your hearts content.
