import serial
import time

# Adjust this to your actual port and baud rate
SERIAL_PORT = '/dev/ttyUSB0'  # Replace with '/dev/ttyUSB0' or similar on Linux/Mac
BAUD_RATE = 115200

def parse_line(line):
    try:
        line = line.strip()
        if not line:
            return
        prefix = line[0]
        value = line[1:]
        
        if prefix == 'b':
            print(f"[BRAKE] {'Pressed' if value == '1' else 'Released'}")
        elif prefix == 'c':
            print(f"[CLUTCH] {'Pressed' if value == '1' else 'Released'}")
        elif prefix == 's':
            print(f"[SPEED] {float(value):.2f} km/h")
        elif prefix == 'r':
            print(f"[RPM] {float(value):.0f}")
        else:
            print(f"[UNKNOWN] {line}")
    except Exception as e:
        print(f"[ERROR] Failed to parse line: {line} ({e})")

def main():
    print(f"Connecting to {SERIAL_PORT} at {BAUD_RATE} baud...")
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.01) as ser:
        print("Connected. Waiting for data...\n")
        buffer = ''
        last_time = time.time()
        while True:
            if ser.in_waiting > 0:
                byte = ser.read().decode(errors='ignore')
                if byte == '\n':
                    parse_line(buffer)
                    buffer = ''
                elif byte != '\r':
                    buffer += byte

            # Optional: throttle refresh rate if needed
            now = time.time()
            if now - last_time >= 1/60.0:
                last_time = now

if __name__ == "__main__":
    main()
