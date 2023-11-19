from nornir import InitNornir
from scrapli.driver.core import IOSXEDriver
from genie import testbed

def gather_interface_facts(task, result_dict):
    # Use Scrapli to connect to the device
    with IOSXEDriver(
        host=task.host.hostname,
        auth_strict_key=False,  # Disable strict key checking for simplicity
    ) as conn:
        # Use Scrapli to send commands to retrieve interface information
        interface_result = conn.send_command("show ip interface brief")

        # Extract relevant information about specific interfaces
        specific_interface_info = extract_specific_interface_info(interface_result.result, "192.168.1.1")

        # Save the gathered facts to the result_dict
        result_dict[task.host.name] = {
            "specific_interface_info": specific_interface_info,
        }

def extract_specific_interface_info(interface_output, desired_ip):
    specific_interface_info = []

    # Iterate through the lines of the command output
    for line in interface_output.splitlines():
        # Check if the line contains information about the desired IP address
        if desired_ip in line:
            specific_interface_info.append(line.strip())

    return specific_interface_info

def main():
    # Initialize Nornir with the appropriate inventory file and defaults file
    nr = InitNornir(config_file="path/to/config.yaml", defaults_file="path/to/defaults.yml")

    # Dictionary to store the gathered facts for each device
    result_dict = {}

    # Run the task on all devices in the inventory
    nr.run(task=gather_interface_facts, result_dict=result_dict)

    # Print the gathered facts
    for device, facts in result_dict.items():
        print(f"Device: {device}")
        print(f"Specific Interface Info: {facts['specific_interface_info']}\n")

if __name__ == "__main__":
    main()
