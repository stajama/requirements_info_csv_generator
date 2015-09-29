#!/bin/bash

for require_file in `cat requirements_list`
do
    virtualenv /tmp/gen_os_csv
    . /tmp/gen_os_csv/bin/activate
    pip install -r $require_file 2>> /tmp/gen_os_csv.err

    pip list 2>> /tmp/gen_os_csv.err| while read i 
    do
        package_name=`echo $i | awk '{print $1}'`
        package_version=`echo $i | awk '{print $2}' | sed -e 's/[\(\)]//g'`
        package_homepage=`pip show -v $package_name 2>> /tmp/gen_os_csv.err| grep Home-page | awk '{print $2}'`
        package_license=`pip show -v $package_name 2>> /tmp/gen_os_csv.err| grep License: | cut -d: -f2 | sed -e 's/^ //'`
        echo "$require_file $package_name $package_version $package_homepage $package_license" >> /tmp/python_oss_info.txt
    done

    deactivate
    rm -r /tmp/gen_os_csv
done


