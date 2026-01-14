import host_availability


def test_valid_ip(valid_ip):
	print("="*50)
	print("\tVALID IP TEST")
	valid_results = host_availability.ProbeHandler(valid_ip)
	print("Addresses: " + str(valid_ip))
	
	num_valid = 0
	failed_test = []
	passed_test = []
	for host in valid_results:
		if host['status'] == "alive":
			passed_test.append(host['host'])
			num_valid += 1
		else:
			failed_test.append(host['host'])
	length_valid_ip = len(valid_ip)
	print("[!] FAILED TESTS: " + str(failed_test))
	print("[+] PASSED TESTS: " + str(passed_test))
	COLOUR = '\033[31m'
	if num_valid == length_valid_ip:
		COLOUR = '\033[32m'
	print(COLOUR + f"[+] TESTS SUCCESS RATE: ({num_valid}/{length_valid_ip})" + "\033[0m")
	print('='*50)
	
def test_invalid_ip(invalid_ip):
	print('='*50)
	print("\tINVALID IP TEST")
	invalid_results = host_availability.ProbeHandler(invalid_ip)
	print("Addresses: " + str(invalid_ip))
	
	num_invalid = 0
	failed_test = []
	passed_test = []
	for host in invalid_results:
		if host['status'] == "alive":
			passed_test.append(host['host'])
		else:
			failed_test.append(host['host'])
			num_invalid += 1

	length_invalid_ip = len(invalid_ip)
	print("[!] FAILED TESTS: " + str(failed_test))
	print("[+] PASSED TESTS: " + str(passed_test))
	COLOUR = '\033[31m'
	if num_invalid == length_invalid_ip:
		COLOUR = '\033[32m'
	print(COLOUR + f"[+] TESTS SUCCESS RATE: ({num_invalid}/{length_invalid_ip})" + "\033[0m")
	print('='*50)
def self_test():
	ip = "localhost"
	results = host_availability.ProbeHandler([ip])[0]
	print("="*50)
	print("\tPOWER ON SELF TEST: ")
	print("Localhost: " + ip)
	print("Timestamp: " + results['timestamp'])
	success = False
	if(results['status'] == "alive"):
		COLOUR = '\033[32m'
		MSG = "[SUCCESS] SELF TEST WAS SUCCESSFUL"
		success = True
	else:
		COLOUR = '\033[31m'
		MSG = "[FAIL] SELF TEST FAILED"
	print(COLOUR + MSG + "\033[0m")
	print("="*50)
	return success

self_test()
test_valid_ip(["192.168.122.1", "google.com", "8.8.8.8"])
test_invalid_ip(["282.282.282.282", "192", "noexistentwebsite.nodomain", "172.10.231.1"])