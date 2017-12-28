#!/usr/bin/env python3
"""
Commands to parse scout2's json database into CSV's for easy reporting.
"""
import csv
import json
from collections import defaultdict

import click

from s2p.findings import ec2_findings


def parse_scout2_json(filepath):
    """
    The scout2
    :param filepath:
    :return: Dictionary containing the entire AWS config. This can use a ton of memory, be careful!
    """
    with open(filepath) as data:
        contents = data.read()
    contents = contents.replace('aws_info =\n', '')  # remove the text at the start of the json file
    return json.loads(contents)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("filepath")
@click.option("--min-count", '-m', default=0, help="Don't record findings with less than this many instances")
@click.option("--wanted-findings", '-w', default=ec2_findings, multiple=True,
              help="Finding names to include. Defaults to all. Can specify multiple times")
@click.option("--output_name", default="network_security_groups.csv",
              help="Output filename. Defaults to network_security_groups.csv")
def nsg(filepath, min_count, wanted_findings, output_name):
    """
    Reports network security group findings.
    :param filepath: Scout2 aws_config.js filepath for input.
    :param min_count: Findings that occur less than this number of times will be omitted from the csv output. Defaults to 0.
    :param wanted_findings: Which findings are wanted in the csv output. A list can be found in findings.py. Defaults to all.
    :param output_name: Filename / path for output file. Defaults to network_security_groups.csv
    """
    # open json file from scout-2
    json = parse_scout2_json(filepath)
    output_dict = defaultdict(dict)
    finding_counts = defaultdict(int)

    # Grab all the findings we care about
    all_findings = []
    for finding, data in json['services']['ec2']['findings'].items():
        all_findings.append(finding)
        if finding in wanted_findings:
            items = data['items']
            finding_counts[finding] = len(items)
            for item in items:
                _, _, region, _, vpc_id, _, security_group_id, = item.split(".")[:7]
                unique_key = (region, vpc_id, security_group_id)
                output_dict[unique_key][finding] = "X"
                output_dict[unique_key]['region'] = region
                output_dict[unique_key]['vpc-id'] = vpc_id
                output_dict[unique_key]['security-group-id'] = security_group_id

    # Remove findings from the wanted list if the total count is too low.
    unwanted_findings = {finding for finding, count in finding_counts.items() if count < min_count}
    wanted_findings = set(wanted_findings) - unwanted_findings

    # Write out data
    with open(output_name, "w") as csv_file:
        headers = ['region', 'vpc-id', 'security-group-id'] + list(wanted_findings)
        csv_writer = csv.DictWriter(csv_file, headers, restval="", extrasaction='ignore')
        csv_writer.writeheader()
        sorted_dicts = sorted(output_dict.values(), key=lambda k: (k['region'], k['vpc-id'], k['security-group-id']))
        csv_writer.writerows(sorted_dicts)


@cli.command()
@click.argument("filepath", )
@click.option("--output_name", default="buckets_without_logging.csv")
def buckets_without_logging(filepath, output_name):
    """
    Reports buckets without logging enabled.
    Parses scout2 JSON file and creates a CSV reporting buckets without logging enabled.
    :param filepath: Scout2 aws_config.js file for input
    :param output_name: Filename / path for output file. Defaults to buckets_without_logging.csv
    """
    json = parse_scout2_json(filepath)

    # create array of S3 buckets and populate
    buckets = json["services"]["s3"]["buckets"]

    # open output file
    with open(output_name, 'w') as csv_file:
        bucket_writer = csv.writer(csv_file)
        bucket_writer.writerow(['Id', 'Name', 'Region'])

        # loop through the buckets
        for bucket, data in buckets.items():
            # write name of the bucket to output file if logging is disabled
            if data["logging"] == "Disabled":
                bucket_writer.writerow([data['id'], data['name'], data['region']])


@cli.command()
@click.argument("filepath", )
@click.option("--output_name", default="vpc_without_flowlogs_enabled.csv")
def vpcs_without_flowlogs(filepath, output_name):
    """
    Reports VPCs without flowlogs enabled.
    :param filepath: Scout2 aws_config.js file for input
    :param output_name: Filename / path for output file. Defaults to buckets_without_logging.csv
    """
    json = parse_scout2_json(filepath)

    findings = json["services"]["vpc"]["findings"]["vpc-subnet-without-flow-log"]
    # open output file
    with open(output_name, 'w') as csv_file:
        flowlog_write = csv.writer(csv_file)
        flowlog_write.writerow(['Region', 'VPC', 'Subnet'])

        # loop through the findings
        for item in findings['items']:
            _, _, region, _, vpc_id, _, subnet_id = item.split(".")[:7]
            flowlog_write.writerow([region, vpc_id, subnet_id])


if __name__ == '__main__':
    cli()
