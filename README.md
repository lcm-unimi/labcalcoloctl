# labcalcoloctl
Simple tool to handle LabCalcolo's VMs.

usage: labcalcolo [{status,start,stop,doctor}] [options]

positional arguments:

    status             default. Check whether there are VMs running on the considered nodes
    
    start, stop        start and stop VMs
    
    doctor             check if qemu and spicec are running. If qemu is running, but spicec is not, ask user if (s)he wants to start it

optional arguments:

  -h, --help           show this help message and exit
  
  -a, --all            All LCM nodes are considered
  
  -n NODE [NODE ...]   Select one or more nodes (at least one)
  
  -1, --lcm1           LCM1 nodes are considered
  
  -2, --lcm2           LCM2 nodes are considered
  
  -v, --version        Print program version
