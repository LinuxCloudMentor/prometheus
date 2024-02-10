import os
import subprocess

# Function to install Prometheus
def install_prometheus():
    # Ask for Prometheus version
    prometheus_version = input("Enter Prometheus version (e.g., 2.49.1): ")

    # Create prometheus user
    subprocess.run(['useradd', '--no-create-home', '--shell', '/bin/false', 'prometheus'])

    # Create directories
    subprocess.run(['mkdir', '/etc/prometheus', '/var/lib/prometheus'])

    # Change ownership
    subprocess.run(['chown', 'prometheus:prometheus', '/etc/prometheus', '/var/lib/prometheus'])

    # Check if Prometheus archive is already downloaded
    prometheus_tar_file = f'/tmp/prometheus-{prometheus_version}.linux-amd64.tar.gz'
    if not os.path.exists(prometheus_tar_file) or os.path.getsize(prometheus_tar_file) == 0:
        # Download Prometheus
        prometheus_url = f"https://github.com/prometheus/prometheus/releases/download/v{prometheus_version}/prometheus-{prometheus_version}.linux-amd64.tar.gz"
        subprocess.run(['wget', prometheus_url, '-O', prometheus_tar_file])

    # Check if downloaded file exists and has non-zero size
    if not os.path.exists(prometheus_tar_file) or os.path.getsize(prometheus_tar_file) == 0:
        print("Error: Prometheus archive could not be downloaded or is empty.")
        return

    # Extract Prometheus
    subprocess.run(['tar', '-xvzf', prometheus_tar_file, '-C', '/tmp'])

    # Move files
    subprocess.run(['mv', f'/tmp/prometheus-{prometheus_version}.linux-amd64', '/tmp/prometheus'])

    # Copy binaries
    subprocess.run(['cp', '/tmp/prometheus/prometheus', '/usr/local/bin/'])
    subprocess.run(['cp', '/tmp/prometheus/promtool', '/usr/local/bin/'])
    subprocess.run(['chown', 'prometheus:prometheus', '/usr/local/bin/prometheus', '/usr/local/bin/promtool'])

    # Copy configuration files
    subprocess.run(['cp', '-r', '/tmp/prometheus/consoles', '/etc/prometheus'])
    subprocess.run(['cp', '-r', '/tmp/prometheus/console_libraries', '/etc/prometheus'])
    subprocess.run(['chown', '-R', 'prometheus:prometheus', '/etc/prometheus/consoles', '/etc/prometheus/console_libraries'])

    # Create and configure prometheus.yml
    with open('/etc/prometheus/prometheus.yml', 'w') as f:
        f.write("""\
global:
  scrape_interval: 10s

scrape_configs:
  - job_name: 'prometheus_master'
    scrape_interval: 5s
    static_configs:
      - targets: ['localhost:9090']
""")

    # Change ownership of prometheus.yml
    subprocess.run(['chown', 'prometheus:prometheus', '/etc/prometheus/prometheus.yml'])

    # Create and configure systemd service
    with open('/etc/systemd/system/prometheus.service', 'w') as f:
        f.write("""\
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \
--config.file /etc/prometheus/prometheus.yml \
--storage.tsdb.path /var/lib/prometheus/ \
--web.console.templates=/etc/prometheus/consoles \
--web.console.libraries=/etc/prometheus/console_libraries

[Install]
WantedBy=multi-user.target
""")

    # Reload systemd and enable prometheus service
    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', '--now', 'prometheus'])
	# Allow port in firewalld
    subprocess.run(['firewall-cmd', '--add-port', f'9090/tcp', '--permanent'])
    subprocess.run(['firewall-cmd', '--reload'])


    print("Prometheus installation completed successfully.")
    print("Access Prometheus Web Interface at http://ip_address:9090")

# Main function
if __name__ == "__main__":
    install_prometheus()

