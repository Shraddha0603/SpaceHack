import socket
import csv
import os

# Define CSV filename
csv_filename = "telemetry_data.csv"

# Check if the CSV file exists, if not, create it with header
if not os.path.exists(csv_filename):
    with open(csv_filename, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["timestamp", "data"])

satellite_ip = "satteilte_ip_address"
satellite_port = 5000
ground_station_port = 6000

send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_socket.bind(("0.0.0.0", ground_station_port))

print("Ground station ready. Type 'exit' to quit.")

while True:
    try:
        command = input("Enter a command for the satellite: ")
        if command.lower() == "exit":
            print("Ground station stopped.")
            break

        send_socket.sendto(command.encode("utf-8"), (satellite_ip, satellite_port))

        data, address = recv_socket.recvfrom(1024)

        print("\nTelemetry from satellite:")
        telemetry_data = data.decode("utf-8")
        print(telemetry_data)

        # Append telemetry data to the CSV file
        with open(csv_filename, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([telemetry_data])

    except KeyboardInterrupt:
        print("Ground station stopped.")
        break

# Close the sockets
send_socket.close()
recv_socket.close()