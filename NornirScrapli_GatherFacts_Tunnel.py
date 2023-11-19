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
        # Modify the below logic based on the specific details you are looking for
        specific_interface_info = extract_specific_interface_info(interface_result.result, "GigabitEthernet1/0")
        specific_tunnel_info = extract_specific_tunnel_info(tunnel_result.result, "Tunnel0")

        # Save the gathered facts to the result_dict
        result_dict[task.host.name] = {
            "specific_interface_info": specific_interface_info,
            "specific_tunnel_info": specific_tunnel_info,
        }

def extract_specific_interface_info(interface_output, interface_name):
    # Implement logic to extract information about a specific interface
    # Modify this based on the specific details you want to extract
    pass

def extract_specific_tunnel_info(tunnel_output, tunnel_name):
    # Implement logic to extract information about a specific tunnel
    # Modify this based on the specific details you want to extract
    pass

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
        print(f"Facts: {facts}\n")

if __name__ == "__main__":
    main()
