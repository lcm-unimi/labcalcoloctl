# labcalcoloctl
Simple tool to handle LabCalcolo's VMs.

usage: labcalcolo [{status,start,stop}] [options]

positional arguments:
  {status,start,stop}  Specify command to execute, default is 'status'

optional arguments:
  -h, --help           show this help message and exit
  -a, --all            All LCM nodes are considered
  -n NODE [NODE ...]   Select one or more nodes (at least one)
  -1, --lcm1           LCM1 nodes are considered
  -2, --lcm2           LCM2 nodes are considered
  -v, --version        Print program version
