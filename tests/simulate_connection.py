import socket, time

# server on port 4444
server = socket.socket()
server.bind(("127.0.0.1", 4444))
server.listen(1)

# client connects and stays open for 10 seconds
client = socket.socket()
client.connect(("127.0.0.1", 4444))
conn, _ = server.accept()
print("Connection open on port 4444 for 10 seconds...")
time.sleep(10)

client.close(); conn.close(); server.close()
print("Done")
