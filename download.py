import shutil

source = "storage/encrypted.enc"
destination = "downloaded.enc"

shutil.copy(source, destination)

print("File downloaded from storage")