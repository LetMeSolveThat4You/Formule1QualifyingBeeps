import socket
from scapy.all import ARP, Ether, srp

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3389]
CUSTOM_PORTS = ["1-150", "443", "445", "3389", "8080", "8888-8890"]  # Replace with your desired custom ports

def arp_scan(target_subnet):
    devices = []

    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_subnet)
    responses, _ = srp(arp_request, timeout=2, verbose=False)

    for response in responses:
        ip = response[1][ARP].psrc
        mac = response[1][Ether].src
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            hostname = "Unknown"  # If hostname cannot be resolved, use "Unknown"
        devices.append((ip, mac, hostname))

    return devices

def parse_ports(ports):
    parsed_ports = []
    for port in ports:
        if "-" in port:
            start, end = map(int, port.split("-"))
            parsed_ports.extend(range(start, end + 1))
        else:
            parsed_ports.append(int(port))
    return parsed_ports

def scan_ports(ip):
    # Toggle between COMMON_PORTS and CUSTOM_PORTS based on your preference
    # ports_to_scan = COMMON_PORTS
    ports_to_scan = parse_ports(CUSTOM_PORTS)

    open_ports = []
    for port in COMMON_PORTS:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Set a timeout for the connection attempt
            result = s.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
    return open_ports

def main():
    target_subnet = "192.168.2.0/24"  # Replace with your subnet range
    devices = arp_scan(target_subnet)

    print("IP Address\t\tMAC Address\t\tHostname\t\tOpen Ports")
    print("="*80)
    for device in devices:
        ip, mac, hostname = device
        open_ports = scan_ports(ip)
        print(f"{ip}\t\t{mac}\t\t{hostname}\t\t{open_ports}")

if __name__ == "__main__":
    main()
