#!/usr/bin/env python
import csv
import json
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

def make_dict_from_list(source_list):
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
        this_req_list = line.strip().split()
        lib_dict[this_req_list[0]].append({
            'package_name': this_req_list[1],
            'package_version': this_req_list[2],
            'package_home_page': this_req_list[3],
            'package_license': this_req_list[4],
            'language': 'python'
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
        click.echo("Writing python csv to {}".format(outfile))
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for req_file in csv_dict:
            writer.writerow({'req_file': req_file})
            for record in csv_dict[req_file]:
                writer.writerow(record)

def add_js_from_package_json(csv_dict, package_json):
    with open(package_json, 'r') as f:
        npm_dict = json.load(f)

    


@click.command()
@click.option('--reqlist', default='requirements_list')
@click.option('--package_json', default='~/workspace/DataRobot/package.json')
@click.option('--output_file', default='/tmp/license_libs.csv')
def gencsv(reqlist, package_json, output_file):
    click.echo("Creating csv...")
    with open(reqlist) as f:
        source_list = f.readlines()

    csv_dict = make_dict_from_list(source_list)
    add_js_from_package_json(csv_dict, package_json)
    write_csv(csv_dict, output_file)

if __name__ == '__main__':
    try:
        gencsv()
    except:
        click.echo("oops, problem")
        raise
