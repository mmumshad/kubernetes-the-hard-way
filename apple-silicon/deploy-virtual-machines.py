#!/usr/bin/env python3
"""
Python implementation of deploy-virtual-machines.sh with added support for
disabling VM recreation via a command-line parameter.
"""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


# ANSI color codes
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
GREEN = "\033[1;32m"
BLUE = "\033[1;34m"
NC = "\033[0m"  # No Color


def print_color(color, message):
    """Print colored message"""
    print(f"{color}{message}{NC}")


def run_command(command, shell=False):
    """Run shell command and return output"""
    if shell:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
    else:
        result = subprocess.run(command, text=True, capture_output=True)
    
    if result.returncode != 0:
        print_color(RED, f"Command failed: {command}")
        print_color(RED, f"Error: {result.stderr}")
        sys.exit(1)
    
    return result.stdout.strip()


def check_command_exists(command):
    """Check if a command exists in PATH"""
    if not shutil.which(command):
        print_color(RED, f"Cannot find {command}. Did you install it as per the instructions?")
        sys.exit(1)
    return True


def get_memory_gb():
    """Get system memory in GB"""
    if platform.system() == "Darwin":  # macOS
        mem_bytes = int(run_command("sysctl hw.memsize | cut -d ' ' -f 2", shell=True))
        return mem_bytes // (1024 * 1024 * 1024)
    else:
        print_color(RED, "This script is designed for macOS")
        sys.exit(1)


def get_vm_specs(mem_gb):
    """Define VM specifications based on available memory"""
    cp_mem = "2048M"
    wn_mem = "2048M"
    
    if mem_gb < 15:
        cp_mem = "768M"
        wn_mem = "512M"
        print_color(YELLOW, f"System RAM is {mem_gb}GB. VM size is reduced.")
        print_color(YELLOW, "It will not be possible for you to run E2E tests (final step).")
    
    return [
        {"name": "controlplane01", "cpus": 2, "ram": cp_mem, "disk": "10G"},
        {"name": "controlplane02", "cpus": 2, "ram": cp_mem, "disk": "5G"},
        {"name": "loadbalancer", "cpus": 1, "ram": "512M", "disk": "5G"},
        {"name": "node01", "cpus": 2, "ram": wn_mem, "disk": "5G"},
        {"name": "node02", "cpus": 2, "ram": wn_mem, "disk": "5G"}
    ]


def multipass_list_vms():
    """List existing Multipass VMs"""
    try:
        output = run_command(["multipass", "list", "--format", "json"])
        return json.loads(output)["list"]
    except (json.JSONDecodeError, KeyError):
        return []


def check_existing_vms(vm_specs, force_recreate):
    """Check if VMs are running and ask to delete/rebuild if needed"""
    existing_vms = multipass_list_vms()
    vm_names = [vm["name"] for vm in existing_vms]
    
    for spec in vm_specs:
        if spec["name"] in vm_names:
            if not force_recreate:
                answer = input(f"{RED}VMs are running. Delete and rebuild them (y/n)? {NC}")
                if answer.lower() != 'y':
                    sys.exit(1)
            return True
    
    return False


def delete_vm(vm_name):
    """Delete a VM"""
    print_color(YELLOW, f"Deleting {vm_name}")
    run_command(["multipass", "delete", vm_name])
    run_command(["multipass", "purge"])


def launch_vm(vm_spec):
    """Launch a VM with specified resources"""
    print_color(BLUE, f"Launching {vm_spec['name']}. CPU: {vm_spec['cpus']}, MEM: {vm_spec['ram']}")
    run_command([
        "multipass", "launch", 
        "--disk", vm_spec["disk"], 
        "--memory", vm_spec["ram"], 
        "--cpus", str(vm_spec["cpus"]), 
        "--name", vm_spec["name"], 
        "jammy"
    ])
    print_color(GREEN, f"{vm_spec['name']} booted!")


def get_vm_ip(vm_name):
    """Get IP address of a VM"""
    output = run_command(["multipass", "info", vm_name, "--format", "json"])
    vm_info = json.loads(output)
    return vm_info["info"][vm_name]["ipv4"][0]


def create_host_entries(vm_specs):
    """Create host entries file with VM IPs"""
    host_entries_path = "/tmp/hostentries"
    
    with open(host_entries_path, "w") as f:
        for spec in vm_specs:
            ip = get_vm_ip(spec["name"])
            f.write(f"{ip} {spec['name']}\n")
    
    return host_entries_path


def provision_vms(vm_specs, host_entries_path):
    """Provision VMs with host entries and scripts"""
    script_dir = Path(__file__).parent / "scripts"
    tools_dir = Path(__file__).parent.parent / "tools"
    
    for spec in vm_specs:
        vm_name = spec["name"]
        # Transfer host entries
        run_command(["multipass", "transfer", host_entries_path, f"{vm_name}:/tmp/"])
        
        # Transfer and run setup scripts
        run_command(["multipass", "transfer", f"{script_dir}/01-setup-hosts.sh", f"{vm_name}:/tmp/"])
        run_command(["multipass", "transfer", f"{script_dir}/cert_verify.sh", f"{vm_name}:/home/ubuntu/"])
        run_command(["multipass", "exec", vm_name, "--", "chmod", "u+x", "/tmp/01-setup-hosts.sh"])
        run_command(["multipass", "exec", vm_name, "--", "/tmp/01-setup-hosts.sh"])
    
    # Transfer additional script to controlplane01
    run_command(["multipass", "transfer", f"{tools_dir}/approve-csr.sh", "controlplane01:/home/ubuntu/"])


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Deploy Kubernetes VMs using Multipass")
    parser.add_argument("--no-recreate", action="store_true", 
                      help="Don't recreate VMs if they already exist")
    
    args = parser.parse_args()
    force_recreate = not args.no_recreate
    
    print_color(BLUE, "Checking system compatibility")
    
    # Check prerequisites
    check_command_exists("multipass")
    check_command_exists("jq")
    
    # Get system memory
    mem_gb = get_memory_gb()
    
    # Define VM specs
    vm_specs = get_vm_specs(mem_gb)
    
    print_color(GREEN, "System OK!")
    
    # Check for existing VMs
    vms_exist = check_existing_vms(vm_specs, force_recreate)
    
    # Deploy or recreate VMs
    for spec in vm_specs:
        vm_name = spec["name"]
        
        # Check if VM exists
        existing_vms = multipass_list_vms()
        vm_exists = any(vm["name"] == vm_name for vm in existing_vms)
        
        if vm_exists:
            if force_recreate:
                delete_vm(vm_name)
                launch_vm(spec)
            # Otherwise skip (keep existing VM)
        else:
            launch_vm(spec)
    
    # Create host entries
    print_color(BLUE, "Provisioning...")
    host_entries_path = create_host_entries(vm_specs)
    
    # Provision VMs
    provision_vms(vm_specs, host_entries_path)
    
    print_color(GREEN, "Done!")


if __name__ == "__main__":
    main()