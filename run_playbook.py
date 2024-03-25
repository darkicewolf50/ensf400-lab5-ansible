import ansible_runner

def run_playbook():
    playbook_path = './hello.yml'
    inventory_path = './hosts.yml'
    r = ansible_runner.run(private_data_dir='.', playbook=playbook_path, inventory=inventory_path)
    
    # Print playbook run results
    print("\nPlaybook Results:")
    for each_host_event in r.events:
        print(each_host_event['event'], each_host_event['stdout'])

if __name__ == "__main__":
    run_playbook()
