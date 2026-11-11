import os, time
os.makedirs("test_folder", exist_ok=True)
for i in range(30):
    with open(f"test_folder/file_{i}.txt", "w") as f:
        f.write("test")
    time.sleep(0.1)