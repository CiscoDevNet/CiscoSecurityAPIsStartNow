### Network Objects Bulk Push
 
 This API workflow can push all three types of network objects in bulk to the FMC:
 
 - Host objects
  
 - Network Objects
  
 - Range Objects


This workflow requires CSV File as an input - Sample CSV file (networkobjects.csv) is provided in this folder itself. Fill the CSV file with required input and run the "bulkpush_networkobjects.py"


### Port Objects Bulk Push 

This API workflow can push all three types of port objects in bulk to the FMC:

 - TCP/UDP Port objects

 - ICMPv4 Objects - Please make sure the ICMP type and code have bee validated.

 - ICMPv6 Objects - Please make sure the ICMP type and code have bee validated.


This workflow requires CSV File as an input - Sample CSV file (portobjects.csv) is provided in this folder itself. Fill the CSV file with required input and run the "bulkpush_portobjects.py"

### URL Objects Bulk Push 

This API workflow can push URL objects in bulk to the FMC.

This workflow requires CSV File as an input - Sample CSV file (urlobjects.csv) is provided in this folder itself. Fill the CSV file with required input and run the "bulkpush_urlobjects.py"
