# README

## DNS Resolver

This project implements a simple DNS resolver in Python using UDP sockets. It listens on a specified port and responds to DNS queries for mappings defined in a local hosts file.

### Features
- Responds to A-type DNS queries (IPv4 addresses).
- Handles multiple queries concurrently using threading.
- Configurable host file and server parameters.

### Prerequisites
- Python 3.x

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Create the host mapping file at `/etc/myhosts` or modify the path in the code to a custom location.
3. Add host entries in the format:
   ```
   <IP Address> <Domain>
   ```
   Example:
   ```
   192.168.1.1 example.com
   127.0.0.1 localhost
   ```

### Usage
1. Run the server:
   ```bash
   python dns_server.py
   ```
2. Send DNS queries to the server using a tool like `dig`:
   ```bash
   dig @127.0.0.1 -p 5354 example.com
   ```

### Configuration
- **File:** Modify the `FILE` constant in the script to change the path of the hosts file.
- **Port:** Modify the `PORT` constant to change the server's listening port.
- **Host:** Modify the `HOST` constant to bind to a specific network interface.

### Notes
- The server returns NXDOMAIN for unresolved queries.
- Ensure the hosts file is properly formatted and does not contain comments or malformed entries.
