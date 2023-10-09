import json
import logging
from .models import World

log_filename = 'game.log'

def init_logs():
    logging.basicConfig(filename=log_filename,
                        level=logging.DEBUG,
                        format='%(asctime)s%(msecs)03d|%(levelname)s|%(message)s',
                        datefmt='%Y%m%d%H%M%S')

def log(msg1, msg2=None, msg3=None):
    current_tick = World.objects.get(pk=1).current_tick
    messages = [str(msg1)]
    
    if msg2 is not None:
        messages.append(str(msg2))
    if msg3 is not None:
        messages.append(str(msg3))
        
    formatted_messages = " | ".join(messages)
    logging.debug(f"Tick {current_tick} | {formatted_messages}")

def parse_logs():
    parsed_logs = []
    last_tick_info = 0  # Initialize a variable to keep track of the last known tick

    with open(log_filename, 'r') as file:
        for line in file:
            try:
                # Initialize default values
                timestamp = 'N/A'
                msg1 = 'N/A'
                msg2 = 'N/A'
                msg3 = 'N/A'

                # Split the line by pipe character to get all parts
                parts = line.strip().split("|")

                # Timestamp (kept as a numerical string)
                timestamp = parts[0].strip()

                if len(parts) >= 4:
                    # Extract tick info from the third part, if it exists
                    if "Tick" in parts[2]:
                        last_tick_info = parts[2].strip().split(" ")[1]  # Update the last known tick

                    # Get the actual messages
                    msg1 = parts[3].strip()
                    if len(parts) > 4:
                        msg2 = parts[4].strip()
                    if len(parts) > 5:
                        msg3 = parts[5].strip()
                else:
                    msg1 = parts[1].strip()
                    msg2 = parts[2].strip()

                parsed_logs.append({
                    "timestamp": timestamp,
                    "tick": last_tick_info,  # Use the last known tick
                    "msg1": msg1,
                    "msg2": msg2,
                    "msg3": msg3
                })

            except Exception as e:
                print(f"Failed to parse line: {line}. Error: {e}")

    return parsed_logs  # Return list of dictionaries

def clear_logs():
    # Clear the log file
    with open('game.log', 'w'):
        pass
