from pprint import pprint
from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_scrapli.tasks import send_command

nr = InitNornir(config_file="config.yaml")

# this task populates the inventory of the nornir object with
# the host's "show interface status" data

def populate_host_interface_status(task: Task) -> None:
    """
    get the live interface status from a device.
    transform the response into structured data associated with each host.
    """
    result = task.run(task=send_command, command="show ip interface brief")
    task.host["interface_status"] = result.scrapli_response.genie_parse_output()

nr.run(task=populate_host_interface_status)
router2 =nr.inventory.hosts["router2"]
pprint(router2["interface_status"])
