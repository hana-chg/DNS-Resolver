import socket
import struct
import threading

FILE = '/etc/myhosts'
PORT = 5354
HOST = '0.0.0.0'

def get_response(transaction_id, domain, qtype, qclass, hosts):
    if qtype == 1 and qclass == 1 and domain in hosts:
        # Header
        flags = struct.pack('!H', 0x8180)
        qdcount = struct.pack('!H', 1) 
        ancount = struct.pack('!H', 1)
        nscount = struct.pack('!H', 0)
        arcount = struct.pack('!H', 0)
        header = transaction_id + flags + qdcount + ancount + nscount + arcount

        # Question section
        question = b''
        for part in domain.split('.'):
            question += bytes([len(part)]) + part.encode()
        question += b'\x00'
        question += struct.pack('!HH', qtype, qclass)

        # Answer section
        ip = hosts[domain]
        name = struct.pack('!H', 0xC00C)
        atype = struct.pack('!H', 1)
        aclass = struct.pack('!H', 1)
        ttl = struct.pack('!I', 300)
        rdlength = struct.pack('!H', 4) 
        rdata = socket.inet_aton(ip) 
        answer = name + atype + aclass + ttl + rdlength + rdata

        return header + question + answer
    else:
        # Return response with no answers
        flags = struct.pack('!H', 0x8183)  # Query response with error (NXDOMAIN)
        qdcount = struct.pack('!H', 1)
        ancount = struct.pack('!H', 0)
        nscount = struct.pack('!H', 0)
        arcount = struct.pack('!H', 0)
        header = transaction_id + flags + qdcount + ancount + nscount + arcount

        # Question section
        question = b''
        for part in domain.split('.'):
            question += bytes([len(part)]) + part.encode()
        question += b'\x00'
        question += struct.pack('!HH', qtype, qclass)

        return header + question

def parse_query(query):
    transaction_id = query[0:2]  # First two bytes
    domain_parts = []
    index = 12  # Start of the question section
    length = query[index]

    while length != 0:
        domain_parts.append(query[index + 1: index + 1 + length].decode())
        index += length + 1
        length = query[index]

    domain = '.'.join(domain_parts)
    qtype = struct.unpack('!H', query[index + 1: index + 3])[0]
    qclass = struct.unpack('!H', query[index + 3: index + 5])[0]

    return transaction_id, domain, qtype, qclass

def process_query(query, dest, server_socket, hosts):
    transaction_id, domain, qtype, qclass = parse_query(query)
    response = get_response(transaction_id, domain, qtype, qclass, hosts)
    server_socket.sendto(response, dest)

def dns_resolver():
    # Load hosts file
    hosts = {}
    try:
        with open(FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    ip, domain = line.split()
                    hosts[domain.strip('.')] = ip
    except FileNotFoundError:
        print(f"{FILE} not found. Create the file to provide host mappings.")

    # Start the server
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((HOST, PORT))
        print(f"DNS server is running on {HOST}:{PORT}")

        while True:
            try:
                query, dest = server_socket.recvfrom(512)  # Max DNS packet size
                threading.Thread(target=process_query, args=(query, dest, server_socket, hosts)).start()
            except Exception as e:
                print(f"Error: {e}")

if __name__ == '__main__':
    dns_resolver()
