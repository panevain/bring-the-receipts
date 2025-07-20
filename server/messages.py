from datetime import datetime
import json
import os
import zoneinfo
from escpos.printer import Usb

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
        return local_dt.strftime("%-m/%-d %-I:%M %p %Z")

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
    printer = Usb(0x0fe6, 0x811e, 0)
    printer.set(align='center',
                bold=True,
                double_height=True,
                double_width=True,
                invert=True)
    printer.textln("Notes")
    printer.ln(count=3)

    messages = []

    printer.set_with_default()
    if os.path.exists(message_filename):
        with open(message_filename, 'r') as file:
            for line_num, line in enumerate(file, 1):
                messages.append(json.loads(line))

    if len(messages) > 0:
        for message in messages:
            try:
                log = f'{format_utc_to_local_time(message["datetime"], message["timezone"])}: {message["text"]}'
                printer.textln(log)
                printer.ln(count=1)
            except:
                print('Unparseable data.')
    else:
        printer.textln("No messages.")

    printer.cut()

    if os.path.exists(message_filename):
        os.remove(message_filename)
