#!/bin/bash

JSON_BIN=`which json`
if [ $? -ne 0 ]
then
    echo "Missing json command"
    echo "See http://trentm.com/json/#INSTALL-PROJECT-BUGS"
    exit 1
fi

PACKAGE_INFO_BIN=`which package-info`
if [ $? -ne 0 ]
then
    echo "Missing package-info command"
    echo "See https://www.npmjs.com/package/package-info"
    exit 1
fi

for require_file in `cat python_requirements_list`
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

for require_file in `cat javascript_requirements_list`
do
    cat $require_file | json dependencies | sed '/[\{\}]/d' | while read i
    do
        package_name=`echo $i | cut -d: -f1 | sed -e 's/\s\+"//' -e 's/"//g'`
        package_version=`echo $i | cut -d: -f2 | sed -e 's/\s\+"//' -e 's/["\,]//g'`
        package_homepage=`package-info $package_name | grep homepage | awk '{print $2}' | sed -e "s/[\s\\',]//g"`
        package_license=`package-info $package_name | grep license | cut -d: -f2 | sed -e "s/[\s\\',]//g"`
        echo "$require_file $package_name $package_version $package_homepage $package_license" >> /tmp/javascript_oss_info.txt
    done
done
