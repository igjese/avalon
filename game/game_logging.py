import json
import logging

log_filename = 'game.log'

def init_logs():
    logging.basicConfig(filename=log_filename,
                        level=logging.DEBUG,
                        format='%(asctime)s%(msecs)03d|%(levelname)s|%(message)s',
                        datefmt='%Y%m%d%H%M%S')

def log(message):
    from .ctrl import current_tick
    logging.debug(f"Tick {current_tick}| {message}")

def parse_logs():
    parsed_logs = []
    last_tick_info = 'N/A'  # Initialize a variable to keep track of the last known tick

    with open(log_filename, 'r') as file:
        for line in file:
            try:
                # Initialize default values
                timestamp = 'N/A'
                level = 'N/A'
                message = 'N/A'

                # Split the line by pipe character to get all parts
                parts = line.strip().split("|")
                if len(parts) >= 4:
                    # Timestamp (kept as a numerical string)
                    timestamp = parts[0].strip()

                    # Get the level
                    level = parts[1].strip()

                    # Extract tick info from the third part, if it exists
                    if "Tick" in parts[2]:
                        last_tick_info = parts[2].strip().split(" ")[1]  # Update the last known tick

                    # Get the actual message
                    message = parts[3].strip()

                parsed_logs.append({
                    "timestamp": timestamp,
                    "tick": last_tick_info,  # Use the last known tick
                    "level": level,
                    "message": message
                })

            except Exception as e:
                print(f"Failed to parse line: {line}. Error: {e}")

    return parsed_logs  # Return list of dictionaries

def clear_logs():
    # Clear the log file
    with open('game.log', 'w'):
        pass
