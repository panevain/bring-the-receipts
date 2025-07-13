from datetime import datetime
import json
import os
import zoneinfo

message_filename = 'messages.txt'


def is_valid_iso8601(iso_string: str) -> bool:
    try:
        datetime.fromisoformat(iso_string)
    except (ValueError, TypeError):
        return False

    return True


def format_utc_to_local_time(utc_iso_string: str, iana_timezone: str) -> str:
    try:
        utc_dt = datetime.fromisoformat(utc_iso_string)
        target_tz = zoneinfo.ZoneInfo(iana_timezone)
        local_dt = utc_dt.astimezone(target_tz)
        return local_dt.strftime("%-I:%M %p (%Z)")

    except zoneinfo.ZoneInfoNotFoundError:
        return f"Error: Timezone '{iana_timezone}' not found."
    except ValueError:
        return f"Error: Invalid ISO string '{utc_iso_string}'."


def log_message(message: str, datetime: str, timezone: str):
    if (len(message) > 255):
        raise Exception("Message exceeds maximum length.")

    if (not is_valid_iso8601(datetime)):
        raise Exception("Timestamp is not valid ISO 8601.")

    with open(message_filename, 'a') as file:
        dict = {'text': message, 'datetime': datetime, 'timezone': timezone}
        file.write(f'{json.dumps(dict)}\n')


def process_messages():
    if not os.path.exists(message_filename):
        print(f'{message_filename} does not exist. Aborting.')
        return

    messages = []
    with open(message_filename, 'r') as file:
        for line_num, line in enumerate(file, 1):
            messages.append(json.loads(line))

    for message in messages:
        text = message["text"]

        try:
            print(
                f'Stored log: {text} at {format_utc_to_local_time(message["datetime"], message["timezone"])}')
        except:
            print('Unparseable data.')

    if os.path.exists(message_filename):
        os.remove(message_filename)
