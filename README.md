# scout2-to-csv
Parses Scout2 JSON to create CSV files for reports.
~~~~
  Usage: scout2-parse.py [OPTIONS] COMMAND [ARGS]...

  Options:
    --help  Show this message and exit.

  Commands:
    buckets_without_logging  Reports buckets without logging enabled.
    nsg                      Reports network security group findings.
    vpcs_without_flowlogs    Reports VPCs without flowlogs enabled.
~~~~

To install:
~~~~
pip install git+git://github.com/ogtony/scout2parse.git@master
~~~~
To remove
~~~~
pip uninstall scout2-to-csv
~~~~