from pprint import pprint
from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_scrapli.tasks import send_command

nr = InitNornir(config_file="config.yaml")

def populate_host_interface_status(task: Task) -> None:
    result = task.run(task=send_command, command="show ip interface brief")
    task.host["interface_status"] = result.scrapli_response.genie_parse_output()

nr.run(task=populate_host_interface_status)
router2 =nr.inventory.hosts["router2"]
pprint(router2["interface_status"])