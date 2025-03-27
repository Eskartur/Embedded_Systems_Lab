import socket
import time
import json
import matplotlib.pyplot as plt

# Socket configuration
HOST = '192.168.83.151'
PORT = 5678

# Create and bind socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
s.settimeout(1)  # Timeout for accept

# Max number of points to show on the plot
MAX_POINTS = 100

# Initialize Matplotlib
plt.ion()
fig, (ax_x, ax_y, ax_z, ax_s) = plt.subplots(4, sharex=True)

# Initialize data storage
plot_data = {
    "x": [0] * MAX_POINTS,
    "y": [0] * MAX_POINTS,
    "z": [0] * MAX_POINTS,
    "s": [0] * MAX_POINTS,
}

# Create plot lines
line_x, = ax_x.plot(plot_data["x"], "r", label="Acc X")
line_y, = ax_y.plot(plot_data["y"], "g", label="Acc Y")
line_z, = ax_z.plot(plot_data["z"], "b", label="Acc Z")
line_s, = ax_s.plot(plot_data["z"], "k", label="Sign M")

# Set fixed y-axis limits (Adjust based on expected sensor range)
ax_x.set_ylim(-2, 2)
ax_y.set_ylim(-2, 2)
ax_z.set_ylim(-2, 2)
ax_s.set_ylim(-2, 2)

# Add legends and grid
for ax in [ax_x, ax_y, ax_z, ax_s]:
    ax.legend()
    ax.grid(True)

plt.show(block=False)

def update_plot(acc):
    """ Updates the plot with new accelerometer data. """
    # Shift old data left and add new data at the end
    for axis, value in zip(["x", "y", "z", "s"], [float(acc["x"])/1024, float(acc["y"])/1024, float(acc["z"])/1024, float(acc["s"])]):
        plot_data[axis].append(value)
        if len(plot_data[axis]) > MAX_POINTS:
            plot_data[axis].pop(0)

    # Update plot lines
    line_x.set_ydata(plot_data["x"])
    line_y.set_ydata(plot_data["y"])
    line_z.set_ydata(plot_data["z"])
    line_s.set_ydata(plot_data["s"])

    # Adjust x-axis dynamically
    x_range = range(len(plot_data["x"]))
    line_x.set_xdata(x_range)
    line_y.set_xdata(x_range)
    line_z.set_xdata(x_range)
    line_s.set_xdata(x_range)

    ax_x.set_xlim(0, MAX_POINTS-1)  # Fix x-axis range

    plt.draw()
    plt.pause(0.01)  # Allow time for rendering

def get_sensor_data(data):
    """ Parses incoming JSON data. """
    try:
        _, data_json = data.decode().split("\n\n", 1)
        return json.loads(data_json.strip())
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Error parsing JSON: {e}")
        return None

# Main loop to handle connections
try:
    while True:
        try:
            conn, addr = s.accept()
            print(f"Connected to {addr}")
            while True:
                data = conn.recv(65536)
                if not data:
                    break
                sensor_data = get_sensor_data(data)
                if sensor_data:
                    try:
                        print(sensor_data)
                        acc = sensor_data["iot2tangle"][0]["data"][0]
                        update_plot(acc)
                    except (KeyError, IndexError):
                        print("Unexpected data format:", sensor_data)
                        break
        except socket.timeout:
            print("Waiting for connection...")
            time.sleep(1)
except KeyboardInterrupt:
    print("Server interrupted. Exiting...")
finally:
    s.close()
    plt.close()
