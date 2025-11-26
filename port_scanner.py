import os
import socket
from colorama import Fore, Style, init
import time
import argparse

init(autoreset=True)

def print_banner_scanner():
    print(Fore.CYAN + Style.BRIGHT + "#################################")
    print(Fore.YELLOW + "      Port Scanner")
    print(Fore.CYAN + "#################################\n")

def scan_port(target, port, open_ports, closed_ports):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(0.1)
    result = s.connect_ex((target, port))
    if result == 0:
        os.system(f'title ✔️ Port {port} open.')
        print(Fore.GREEN + f"✔️ Port {port} open.")
        open_ports.append(port)
    else:
        print(Fore.RED + f"❌ Port {port} closed.")
        closed_ports.append(port)
    s.close()

def port_scanner(target, start_port, end_port):
    print_banner_scanner()
    print(Fore.MAGENTA + f"Scanning between {target} adress {start_port} with {end_port}...\n")
    time.sleep(1)

    open_ports = []
    closed_ports = []

    for port in range(start_port, end_port + 1):
        scan_port(target, port, open_ports, closed_ports)

    with open("openports.txt", "w") as f:
        f.write("Open ports:\n")
        for port in open_ports:
            f.write(f"Port {port} open\n")
        f.write("\nClosed ports:\n")
        for port in closed_ports:
            f.write(f"Port {port} closed\n")

    print(Fore.CYAN + "\nPort scan results saved to openports.txt.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Port Scan")
    parser.add_argument("target", help="Target IP or Domain")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start Port (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End Port (default: 1024)")

    args = parser.parse_args()

    port_scanner(args.target, args.start, args.end)
