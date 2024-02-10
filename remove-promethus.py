import os
import subprocess

# Function to uninstall Prometheus
def uninstall_prometheus():
    # Stop and disable Prometheus service
    subprocess.run(['systemctl', 'stop', 'prometheus'])
    subprocess.run(['systemctl', 'disable', 'prometheus'])

    # Remove Prometheus binaries
    subprocess.run(['rm', '/usr/local/bin/prometheus'])
    subprocess.run(['rm', '/usr/local/bin/promtool'])

    # Remove Prometheus directories
    subprocess.run(['rm', '-rf', '/etc/prometheus'])
    subprocess.run(['rm', '-rf', '/var/lib/prometheus'])

    # Remove Prometheus systemd service file
    subprocess.run(['rm', '/etc/systemd/system/prometheus.service'])

    subprocess.run(['userdel', 'prometheus'])

    # Remove firewall rule
    subprocess.run(['firewall-cmd', '--remove-port', '9090/tcp', '--permanent'])
    subprocess.run(['firewall-cmd', '--reload'])

    subprocess.run(['rm', '-rf', '/var/mail/prometheus'])


    print("Prometheus uninstallation completed successfully.")

# Main function
if __name__ == "__main__":
    uninstall_prometheus()

