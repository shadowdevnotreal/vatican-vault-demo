import socket
import time
import subprocess

protocols = ['SSH', 'FTP', 'SMB', 'NFS']
ports = [22, 21, 139, 2049]
destination_host = 'destination_host'
file_path = '/tmp/file.txt'
start_time = time.time()
fastest_protocol = None
fastest_time = 0

for protocol, port in zip(protocols, ports):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((destination_host, port))
    if result == 0:
        print(f"{protocol} is available on port {port}")
        if protocol == 'SSH':
            transfer_command = f'scp {file_path} user@{destination_host}:{file_path}'
        elif protocol == 'FTP':
            transfer_command = f'ftp -n {destination_host} <<EOF\nuser anonymous password\nbinary\nput {file_path}\nquit\nEOF'
        elif protocol == 'SMB':
            transfer_command = f'net use \\{destination_host}\temp password /user:user\ncopy {file_path} \\{destination_host}\temp'
        elif protocol == 'NFS':
            transfer_command = f'mount {destination_host}:/temp ~/nfs\ncp {file_path} ~/nfs\numount ~/nfs'
        # ping destination host to find transfer time
        ping_result = subprocess.run(["ping", "-c", "1", destination_host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ping_time = ping_result.stdout.decode("utf-8").split("time=")[1].split(" ")[0]
        print("The transfer time to {} via {} is {}ms".format(destination_host, protocol, ping_time))
        
        try:
            transfer_result = subprocess.run(transfer_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            elapsed_time = time.time() - start_time
            if fastest_protocol is None or elapsed_time < fastest_time:
                fastest_protocol = protocol
                fastest_time = elapsed_time
        except subprocess.CalledProcessError as e:
            print(f"Error transferring file using {protocol}: {e.stderr}")
    sock.close()

print(f"The fastest protocol for file transfer is {fastest_protocol} with a transfer time of {fastest_time:.2f} seconds")

destination_ip = "192.168.0.200"
file_path = "/tmp/file.txt"

if fastest_protocol == 'SSH':
    # use the scp command to transfer the file to the destination IP
    subprocess.run(["scp", file_path, "{}:{}".format(destination_ip, file_path)])
elif fastest