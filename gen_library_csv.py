#!/usr/bin/env python
import csv
import json
from copy import deepcopy
from collections import defaultdict

import click

def check_for_direct(rfile, package_dict_list):
    with open(rfile, 'r') as f:
        req_str = f.read()
    for package in package_dict_list:
        if package['package_name'] in req_str:
            package['direct_req'] = "yes"
        else:
            package['direct_req'] = "no"

def make_dict_from_list(source_list, language):
    """ each line of the source list should have the following indices when
        split:
        0 = requirements filename (hopefully absolute)
        1 = package name
        2 = package version
        3 = home page (as listed in pypi)
        4 = license
    """
    lib_dict = defaultdict(list)
    for line in source_list:
        this_req_list = line.strip().split('|')
        try:
            package_home_page = this_req_list[3]
        except IndexError as e:
            package_home_page = 'unknown'
        try:
            package_license = this_req_list[4]
        except IndexError as e:
            package_license = 'unknown'
        lib_dict[this_req_list[0]].append({
            'package_name': this_req_list[1],
            'package_version': this_req_list[2],
            'package_home_page': package_home_page,
            'package_license': package_license,
            'language': language
            })
    for req_file in lib_dict:
        # this is pass-by-ref, and modifies the list
        check_for_direct(req_file, lib_dict[req_file])
    return lib_dict

def write_csv(csv_dict, output_file):
    fieldnames = [
        'req_file',
        'package_name',
        'package_version',
        'package_home_page',
        'package_license',
        'direct_req',
        'language'
        ]
    with open(output_file, 'w') as csvfile:
        click.echo("Writing csv to {}".format(output_file))
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for req_file in csv_dict:
            writer.writerow({'req_file': req_file})
            for record in csv_dict[req_file]:
                writer.writerow(record)

@click.command()
@click.option('--python_list', default='/tmp/python_oss_info.txt')
@click.option('--python3_list', default='/tmp/python3_oss_info.txt')
@click.option('--javascript_list', default='/tmp/javascript_oss_info.txt')
@click.option('--output_file', default='/tmp/license_libs.csv')
def gencsv(python_list, javascript_list, output_file, python3_list):
    click.echo("Creating csv...")
    with open(python_list) as f:
        python_source_list = f.readlines()

    with open(javascript_list) as f:
        javascript_source_list = f.readlines()

#    with open(python3_list) as f:
#        python3_source_list = f.readlines()

    python_dict = make_dict_from_list(python_source_list, 'python')
    javascript_dict = make_dict_from_list(javascript_source_list, 'javascript')
#    python3_dict = make_dict_from_list(python3_source_list, 'python3')
    csv_dict = deepcopy(python_dict)
    csv_dict.update(javascript_dict)
#    csv_dict.update(python3_dict)
    write_csv(csv_dict, output_file)

if __name__ == '__main__':
    gencsv()
