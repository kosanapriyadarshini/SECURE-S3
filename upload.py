import shutil

source = "encrypted.enc"
destination = "storage/encrypted.enc"

shutil.copy(source, destination)

print("File uploaded to storage successfully")