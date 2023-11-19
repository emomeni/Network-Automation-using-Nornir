from nornir import InitNornir
from scrapli.driver.core import IOSXEDriver
from genie import testbed

def gather_tunnel_facts(task, result_dict):
    # Use Scrapli to connect to the device
    with IOSXEDriver(
        host=task.host.hostname,
        auth_strict_key=False,  # Disable strict key checking for simplicity
    ) as conn:
        # Use Scrapli to send commands to retrieve interface and tunnel information
        interface_result = conn.send_command("show ip interface brief")
        tunnel_result = conn.send_command("show interface tunnel")

        # Extract relevant information about specific interfaces and tunnels
        specific_tunnel_info = extract_specific_tunnel_info(tunnel_result.result, "Tunnel0", "192.168.1.1")

        # Save the gathered facts to the result_dict
        result_dict[task.host.name] = {
            "specific_tunnel_info": specific_tunnel_info,
        }

def extract_specific_tunnel_info(tunnel_output, tunnel_name, desired_ip):
    specific_tunnel_info = []

    # Iterate through the lines of the command output
    for line in tunnel_output.splitlines():
        # Check if the line contains information about the desired tunnel and IP address
        if tunnel_name in line and desired_ip in line:
            specific_tunnel_info.append(line.strip())

    return specific_tunnel_info

def main():
    # Initialize Nornir with the appropriate inventory file and defaults file
    nr = InitNornir(config_file="path/to/config.yaml", defaults_file="path/to/defaults.yml")

    # Dictionary to store the gathered facts for each device
    result_dict = {}

    # Run the task on all devices in the inventory
    nr.run(task=gather_tunnel_facts, result_dict=result_dict)

    # Print the gathered facts
    for device, facts in result_dict.items():
        print(f"Device: {device}")
        print(f"Specific Tunnel Info: {facts['specific_tunnel_info']}\n")

if __name__ == "__main__":
    main()
