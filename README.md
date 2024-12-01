## DNS Resolver

This project implements a simple DNS resolver in Python using UDP sockets. It listens on a specified port and responds to DNS queries for mappings defined in a local hosts file.

### Features
- Responds to A-type DNS queries (IPv4 addresses).
- Handles multiple queries concurrently using threading.
- Configurable host file and server parameters.