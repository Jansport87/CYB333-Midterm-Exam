import socket
from datetime import datetime

def port_scanner(target_host, start_port, end_port):

    # Validate target hostname or IP address
    if not isinstance(target_host, str) or not target_host.strip():
        print("[ERROR] Invalid target hostname or IP address.")
        return

    # Validate port numbers
    if (not isinstance(start_port, int) or isinstance(start_port, bool)
            or not isinstance(end_port, int) or isinstance(end_port, bool)):
        print("[ERROR] Port numbers must be integers.")
        return

    if start_port < 1 or end_port > 65535:
        print("[ERROR] Ports must be between 1 and 65535.")
        return

    if start_port > end_port:
        print("[ERROR] Starting port cannot exceed ending port.")
        return

    # Display scan information
    print("=" * 50)
    print(f"Starting port scan on: {target_host}")
    print(f"Port range: {start_port}-{end_port}")
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
    scanned_ports = 0
    timed_out_ports = 0

    # Scan each port in the specified range
    for port in range(start_port, end_port + 1):

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
            timed_out_ports += 1

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

    # Display summary of scanned and timed-out ports
    print(f"\nTotal ports scanned: {scanned_ports}")
    print(f"Total open ports: {len(open_ports)}")
    print(f"Total timed-out ports: {timed_out_ports}")
    print(f"Scan completed: {datetime.now()}")


# Main program
if __name__ == "__main__":

    try:
        # Target host to scan
        target_host = "127.0.0.1"

        # Specify the starting and ending ports
        start_port = 1
        end_port = 25

        # Start the scanner
        port_scanner(target_host, start_port, end_port)

    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Port scan stopped by user.")

    except Exception as error:
        print(f"[FATAL ERROR] Unexpected error: {error}")
