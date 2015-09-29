#!/usr/bin/env python
import csv
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
            'package_license': this_req_list[4]
            })
    for req_file in lib_dict:
        # this is pass-by-ref, and modifies the list
        check_for_direct(req_file, lib_dict[req_file])
    return lib_dict

def write_csv(csv_dict):
    outfile = '/tmp/python_libs.csv'
    fieldnames = [
        'req_file',
        'package_name',
        'package_version',
        'package_home_page',
        'package_license',
        'direct_req'
        ]
    with open(outfile, 'w') as csvfile:
        click.echo("Writing python csv to {}".format(outfile))
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for req_file in csv_dict:
            writer.writerow({'req_file': req_file})
            for record in csv_dict[req_file]:
                writer.writerow(record)


@click.command()
@click.argument('filename')
def gencsv(filename):
    click.echo("Creating csv...")
    with open(filename) as f:
        source_list = f.readlines()

    csv_dict = make_dict_from_list(source_list)
    write_csv(csv_dict)

if __name__ == '__main__':
    gencsv()
