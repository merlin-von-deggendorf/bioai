import subprocess

# Command to call AutoDock-GPU with the --help option
command = "./bin/autodock_gpu_64wi --help"

# Specify the current working directory
cwd = "/mnt/src/AutoDock-GPU/"

# Execute the command and capture the output
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
stdout, stderr = process.communicate()

# Print the output
print(stdout.decode())
if stderr:
    print("Error:", stderr.decode())
