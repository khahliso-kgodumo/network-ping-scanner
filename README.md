# Host Availability Scanner

# Description
This is a python-based network monitoring tool checks the availability of a list of hosts using ICMP ping requests.
It processes hosts in manageable chunks, retries failed pings, and generates a detailed JSON availability report along with a formatted terminal summary.

# Features
- Read IP addresses from a text file
- Ignores comments and empty lines
- Processes hosts in chunks
- Retries failed ping attemps
- Cross-platform support on Linux/macOS and Windows
- Generates timestamped JSON report
- Calculates availability percentage
- Displays a colour-coded terminal summary

# Installation Instructions
Clone the repository
`
	git clone https://github.com/your-username/host-availability-scanner.git
	
	cd host-availability-scanner
`
Ensure the script is executable on Linux/macOS
`
	chmod +x host_availability.py
`

# Usage
`
	python3 host_availabilty.py /path/to/hosts.txt
`
Example of hosts.txt
`
	# Production servers
	8.8.8.8
	1.1.1.1

	# Internal servers
	192.168.1.1
`
# Technology Stack
- Python 3.12


