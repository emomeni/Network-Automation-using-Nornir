from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from scrapli.driver.core import IOSXEDriver
from genie import testbed

def gather_router_facts(task):
    # Use Scrapli to connect to the device
    with IOSXEDriver(
        host=task.host.hostname,
        auth_username=task.host.username,
        auth_password=task.host.password,
        auth_strict_key=False,  # Disable strict key checking for simplicity
    ) as conn:
        # Use Genie to parse 'show version' command output
        result = conn.send_command("show version", strip_prompt=False, strip_command=False)
        parsed_output = testbed.parse_output(platform="cisco_iosxe", command="show version", data=result.result)

        # Extract relevant information
        platform = parsed_output["platform"]
        os_model = parsed_output["chassis"]
        os_version = parsed_output["version"]

        # Save the gathered facts to the Nornir task object
        task.host["platform"] = platform
        task.host["os_model"] = os_model
        task.host["os_version"] = os_version

def main():
    # Initialize Nornir with the appropriate inventory file
    nr = InitNornir(config_file="path/to/config.yaml")

    # Run the task on all devices in the inventory
    result = nr.run(task=gather_router_facts)

    # Print the gathered facts
    for host, data in result.items():
        print(f"Device: {host}")
        print(f"Platform: {data['platform']}")
        print(f"OS Model: {data['os_model']}")
        print(f"OS Version: {data['os_version']}\n")

if __name__ == "__main__":
    main()
