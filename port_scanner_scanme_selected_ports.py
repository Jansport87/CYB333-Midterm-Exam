import socket
from datetime import datetime

def port_scanner(target_host, ports_to_scan):

    # Validate target hostname or IP address
    if not isinstance(target_host, str) or not target_host.strip():
        print("[ERROR] Invalid target hostname or IP address.")
        return

    # Validate port list
    if not isinstance(ports_to_scan, (list, tuple)):
        print("[ERROR] Ports must be provided as a list or tuple.")
        return

    if not ports_to_scan:
        print("[ERROR] No ports were provided for scanning.")
        return

    # Display scan information
    print("=" * 50)
    print(f"Starting port scan on: {target_host}")
    print(f"Ports to scan: {', '.join(map(str, ports_to_scan))}")
    print(f"Scan started: {datetime.now()}")
    print("=" * 50)

    # Resolve hostname to IP address
    try:
        target_ip = socket.gethostbyname(target_host)
        print(f"Target IP address: {target_ip}")

    except socket.gaierror:
        print("[ERROR] Unable to resolve hostname.")
        return

    except OSError as error:
        print(f"[ERROR] Network resolution failed: {error}")
        return

    open_ports = []
    invalid_ports = []
    scanned_ports = 0

    # Scan each port in the specified list
    for port in ports_to_scan:

        # Validate port number
        if (not isinstance(port, int) or isinstance(port, bool)
                or port < 1 or port > 65535):

            print(f"[INVALID] Port {port} is not a valid port number.")
            invalid_ports.append(port)
            continue

        try:
            # Create a TCP socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

                # Set connection timeout
                sock.settimeout(1)

                # Attempt connection to the target port
                result = sock.connect_ex((target_ip, port))

                scanned_ports += 1

                # Check whether the connection succeeded
                if result == 0:
                    print(f"[OPEN] Port {port}")
                    open_ports.append(port)

                else:
                    print(f"[CLOSED/FILTERED] Port {port}")

        except socket.timeout:
            print(f"[TIMEOUT] Port {port}")

        except OSError as error:
            print(f"[ERROR] Port {port}: {error}")

        except Exception as error:
            print(f"[UNEXPECTED ERROR] Port {port}: {error}")

    # Display scan results
    print("\n" + "=" * 50)
    print("PORT SCAN SUMMARY")
    print("=" * 50)

    if open_ports:
        print("Open ports discovered:")
        for port in open_ports:
            print(f"Port {port}: OPEN")
    else:
        print("No open ports discovered.")

    # Display summary of scanned and invalid ports
    print(f"\nTotal ports scanned: {scanned_ports}")
    print(f"Total invalid ports: {len(invalid_ports)}")
    print(f"Total open ports: {len(open_ports)}")
    print(f"Scan completed: {datetime.now()}")


# Main program
if __name__ == "__main__":

    try:
        # Target host to scan
        target_host = "scanme.nmap.org"

        # Specify the ports to scan
        ports_to_scan = [80, 443, 22, 21, 25, -1, 65536]

        # Start the scanner
        port_scanner(target_host, ports_to_scan)

    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Port scan stopped by user.")

    except Exception as error:
        print(f"[FATAL ERROR] An unexpected error occurred: {error}")
