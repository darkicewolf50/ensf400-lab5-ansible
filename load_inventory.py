import ansible_runner
import yaml

def load_inventory():
    with open('./hosts.yml', 'r') as file:
        inventory_dict = yaml.load(file, Loader=yaml.FullLoader)
    return inventory_dict

def parse_inventory(inventory_manager):
    inventory = inventory_manager.get("all", {})
    return inventory

def print_host_info(inventory):
    print("Inventory:")
    if isinstance(inventory, dict) and 'hosts' in inventory:
        for host, host_data in inventory['hosts'].items():
            ansible_host = host_data.get('ansible_host', 'Unknown IP')
            ansible_port = host_data.get('ansible_port', 'Unknown Port')
            ansible_user = host_data.get('ansible_user', 'Unknown User')
            ansible_groups = ', '.join(host_data.get('ansible_groups', []))  # Convert list to string
            print(f"  Host: {host}, IP: {ansible_host}, Port: {ansible_port}, User: {ansible_user}, Groups: {ansible_groups}")
    else:
        print("Invalid inventory format.")


def ping_hosts(inventory_manager):
    runner = ansible_runner.run(private_data_dir='./', host_pattern='all', module='ping', inventory=inventory_manager)
    for event in runner.events:
        if event['event'] == 'runner_on_ok':
            host = event['event_data']['host']
            if host != 'localhost':
                ping_result = event['event_data']['res']
                if ping_result.get('ping', False):
                    ansible_facts = ping_result['ansible_facts']
                    discovered_interpreter_python = ansible_facts.get('discovered_interpreter_python', 'Unknown Interpreter')
                    print(f"Ping result for {host}: Host is reachable, Interpreter Python: {discovered_interpreter_python}")
                else:
                    print(f"Ping result for {host}: Host is not reachable")
        elif event['event'] == 'runner_on_failed':
            print("Failed to ping some hosts.")
            break

if __name__ == "__main__":
    inventory_manager = load_inventory()
    inventory = parse_inventory(inventory_manager)
    print_host_info(inventory)
    ping_hosts(inventory_manager)
