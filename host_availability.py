#!/usr/bin/env python3
import sys
import os
import json
from datetime import datetime
import subprocess
import time

def main():
	if len(sys.argv) < 2:
		print(f"Usage: python3 {sys.argv[0]} /path/to/hosts.txt")
		sys.exit(1)

	file_path = sys.argv[1]
	try:
		hosts = inputHandler(file_path)

		chunk_size = 10

		for i in range(0, len(hosts), chunk_size): 
			chunk = hosts[i:i + chunk_size]
			print(f"\n\n[+] Processing chunk {i//chunk_size + 1}: {len(chunk)} hosts")

			chunk_results = ProbeHandler(chunk)
			if chunk_results:

				formatted_chunk = Results(chunk_results)
				report_message = Report(chunk_results)
				print(f"[+] Chunk {i//chunk_size + 1} processed: {report_message}")
			else:
				print("[!] No results from chunk")

			time.sleep(1)
	except Exception as e:
		print(f"ERROR in main: {e}")
		sys.exit(1)


def inputHandler(file_path):
	host_chunk = []
	try:
		with open(file_path, "r") as file:
			for line in file:
				host_line = line.strip()
				if host_line and not host_line.startswith("#"):
					host_chunk.append(host_line)

		print(f"[+] Successfully read {len(host_chunk)} hosts from {file_path}")
		return host_chunk
	except FileNotFoundError:
		print(f"ERROR reading file: file '{file_path}' not found.")
		sys.exit(1)
	except PermissionError:
		print(f"ERROR reading file: Permission denied for '{file_path}'.")
		sys.exit(1)
	except Exception as e:
		print(f"ERROR reading file: {e}")
		sys.exit(1)

def ProbeHandler(chunk, timeout=2, retries=2):
	if not chunk:
		print("Empty chunk recieved by ProbeHandler")
		return None
	results = []
	for host in chunk:
		result_entry = {
			"host": host,
			"timestamp": datetime.now().isoformat(),
			"status": "dead"	# default status unless successful ping
		}

		ping_success = False
		if os.name == "posix":
			command = ["ping", "-c", "1", "-W", str(timeout), host]
			
		else:
			command = ["ping", "-n", "1", "-w", str(timeout * 1000), host]

		for attempt in range(retries + 1):
			try:
				result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True, timeout=timeout+1)
				if result.returncode == 0:
					ping_success = True
					break
			except subprocess.TimeoutExpired:
				print(f"Ping to {host} timed out (attempt {attempt +1}/{retries + 1})")
			except Exception as e:
				print(f"Error pinging {host}: {e}")

			if attempt < retries:
				time.sleep(0.5)
		
		if ping_success:
			result_entry['status'] = "alive"
		results.append(result_entry)

	return results
		

def Results(results):
	if not results:
		print("No data received and no data to log.")
		return None

	network_report = {
		"subject": f"Network status report - {datetime.now().strftime('%Y-%m-%d')}",
		"summary": {
			"total_hosts": 0,
			"alive_hosts": 0,
			"dead_hosts": 0,
			"availability_rate": None
		},
		"details": results
	}

	for result in results:
		network_report["summary"]["total_hosts"] += 1
		if result["status"] == "alive":
			network_report["summary"]["alive_hosts"] += 1
		else:
			network_report["summary"]["dead_hosts"] += 1

	if network_report["summary"]["total_hosts"] > 0:
		availability = (network_report["summary"]["alive_hosts"] / network_report["summary"]["total_hosts"]) *100
		network_report["summary"]["availability_rate"] = round(availability,2)

	timestamp = datetime.now().strftime("%H%M%S")
	filename = f"./json_files/{datetime.now().strftime("%Y%m%d")}_HOST_CHECK_SUMMARY_{timestamp}.json"


	try:
		with open(filename, 'w') as json_file:
			json.dump(network_report, json_file, indent=2)
		print(f"\nReport saved to: {filename}")
	except Exception as e:
		print(f"Error saving JSON report: {e}")

	print("\n" + "=" * 50)
	print(f"SUMMARY REPORT: {datetime.now().strftime("%Y%m%d")}")
	print("=" * 50)
	print(f"Total hosts: {network_report['summary']['total_hosts']}")
	print(f"Alive hosts: {network_report['summary']['alive_hosts']}")
	print(f"Dead hosts: {network_report['summary']['dead_hosts']}")
	print(f"Availability Rate: {network_report['summary']['availability_rate']}%")
	print("="*50 + "\n")
	print("Full Network Report")
	print("\n" + "="*50)
	for host in results:
		if host['status'] == "dead":
			COLOUR = '\033[31m'
		else:
			COLOUR = '\033[36m'
		print(COLOUR + f"Host: {host['host']}\t\t| Status: {host['status']}\t| Time: {host['timestamp']}")
		COLOUR = '\033[0m'
		print(COLOUR, end="")
	return "[+] Processing results complete"

def Report(results):
	if not results:
		print("No data received. No data to report")
		return "0 dead hosts reported"

	dead_hosts = []
	
	for host in results:
		if host['status'] == "dead":
			dead_hosts.append(host)
		
	print("\n" + "="*50)

	# function to report hosts
	print(f"[+] {len(dead_hosts)} reported to admin.")

	return f"{len(dead_hosts)} dead hosts reported"

def collect_user_feedback():
	print("="*50)
	questions = [
		("How easy was the setup? (1-5)", "setup_ease"),
		("Detection accuracy? (1-5)", "accuracy"),
		("Resource usage acceptable? (yes/no)", "resource_usage"),
		("Any false positives? Please provide a description.", "false_positives"),
		("Suggestions for improvement?", "suggestions")
	]

	feedback = {}
	for q, key in questions:
		response = input(f"{q}: ")
		feedback[key] = response

	with open("feedback/user_feedback.json", "a") as f:
		json.dump(feedback, f)
		f.write("\\n")
	print("Thank you for your feedback!")
	print("="*50)

if __name__ == "__main__":
	main()