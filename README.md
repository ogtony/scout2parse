# scout2-to-csv
Parses Scout2 JSON to create CSV files for reports.
~~~~
  Usage: s2p [OPTIONS] COMMAND [ARGS]...

  Options:
    --help  Show this message and exit.

  Commands:
    buckets_without_logging  Reports buckets without logging enabled.
    nsg                      Reports network security group findings.
    vpcs_without_flowlogs    Reports VPCs without flowlogs enabled.
~~~~

Get help on a specific command:
~~~~
s2p nsg --help
Usage: s2p nsg [OPTIONS] FILEPATH

  Reports network security group findings. :param filepath: Scout2
  aws_config.js filepath for input. :param min_count: Findings that occur
  less than this number of times will be omitted from the csv output.
  Defaults to 0. :param wanted_findings: Which findings are wanted in the
  csv output. A list can be found in findings.py. Defaults to all. :param
  output_name: Filename / path for output file. Defaults to
  network_security_groups.csv

Options:
  -m, --min-count INTEGER     Don't record findings with less than this many
                              instances
  -w, --wanted-findings TEXT  Finding names to include. Defaults to all. Can
                              specify multiple times
  --output_name TEXT          Output filename. Defaults to
                              network_security_groups.csv
  --help                      Show this message and exit.

~~~~
To install:
~~~~
pip install git+git://github.com/ogtony/scout2parse.git@master
~~~~
To remove
~~~~
pip uninstall scout2-to-csv
~~~~
