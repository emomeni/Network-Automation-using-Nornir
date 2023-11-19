from nornir import InitNornir
from scrapli.driver.core import IOSXEDriver
from genie import testbed

def gather_device_facts(task, result_dict):
    # Use Scrapli to connect to the device
    with IOSXEDriver(
        host=task.host.hostname,
        auth_strict_key=False,  # Disable strict key checking for simplicity
    ) as conn:
        # Use Scrapli to send commands to retrieve platform and version information
        show_version_result = conn.send_command("show version")
        show_interface_result = conn.send_command("show ip interface brief | include Tunnel")

        # Use Genie to parse 'show version' command output
        parsed_version = testbed.parse_output(platform="cisco_iosxe", command="show version", data=show_version_result.result)

        # Extract relevant information
        platform = parsed_version["platform"]
        os_model = parsed_version["chassis"]
        os_version = parsed_version["version"]

        # Extract specific IP addresses of interface tunnels
        tunnel_ip_addresses = extract_tunnel_ip_addresses(show_interface_result.result)

        # Save the gathered facts to the result_dict
        result_dict[task.host.name] = {
            "platform": platform,
            "os_model": os_model,
            "os_version": os_version,
            "tunnel_ip_addresses": tunnel_ip_addresses,
        }

def extract_tunnel_ip_addresses(interface_output):
    tunnel_ip_addresses = []

    # Iterate through the lines of the command output
    for line in interface_output.splitlines():
        # Extract the IP address from lines that contain information about tunnels
        if "Tunnel" in line:
            parts = line.split()
            if len(parts) >= 2:
                tunnel_ip_addresses.append(parts[1].strip())

    return tunnel_ip_addresses

def main():
    # Initialize Nornir with the appropriate inventory file and defaults file
    nr = InitNornir(config_file="path/to/config.yaml", defaults_file="path/to/defaults.yml")

    # Dictionary to store the gathered facts for each device
    result_dict = {}

    # Run the task on all devices in the inventory
    nr.run(task=gather_device_facts, result_dict=result_dict)

    # Print the gathered facts
    for device, facts in result_dict.items():
        print(f"Device: {device}")
        print(f"Platform: {facts['platform']}")
        print(f"OS Model: {facts['os_model']}")
        print(f"OS Version: {facts['os_version']}")
        print(f"Tunnel IP Addresses: {facts['tunnel_ip_addresses']}\n")

if __name__ == "__main__":
    main()
