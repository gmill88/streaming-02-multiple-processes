"""

Streaming Process: Uses port 9999

Create a fake stream of data. 
Use temperature data from the batch process.

Reverse the order of the rows to read OLDEST data first.

Important! 

We'll stream forever - or until we read the end of the file. 
Use use Ctrl-C to stop. (Hit Control key and c key at the same time.)

Explore more at 
https://wiki.python.org/moin/UdpCommunication

"""

# Import from Python Standard Library

import csv
import socket
import time
import logging

# Set up basic configuration for logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Declare program constants (typically constants are named with ALL_CAPS)

HOST = "localhost"
PORT = 9999
ADDRESS_TUPLE = (HOST, PORT)
INPUT_FILE_NAME = "batchfile_0_farenheit.csv"

# Define program functions (bits of reusable code)


def prepare_message_from_row(row):
    """Prepare a binary message from a given row."""
    Year, Month, Day, Time, TempF = row
    # use an fstring to create a message from our data
    # notice the f before the opening quote for our string?
    fstring_message = f"[{Year}, {Month}, {Day}, {Time}, {TempF}]"

    # prepare a binary (1s and 0s) message to stream
    MESSAGE = fstring_message.encode()
    logging.debug(f"Prepared message: {fstring_message}")
    return MESSAGE


def stream_row(input_file_name, address_tuple):
    """Read from input file and stream data."""
    logging.info(f"Starting to stream data from {input_file_name} to {address_tuple}.")

    try:
        # Open the input file for reading
        with open(input_file_name, "r") as input_file:
            logging.info(f"Opened for reading: {input_file_name}.")

            # Create a CSV reader object
            reader = csv.reader(input_file, delimiter=",")

            # Skip the header row
            header = next(reader)
            logging.info(f"Skipped header row: {header}")

            # Read all rows into a list
            rows = list(reader)
            logging.debug(f"Number of rows read: {len(rows)}")

            # Reverse the list of rows to read oldest data first
            rows.reverse()

            # Create a socket object for UDP communication
            ADDRESS_FAMILY = socket.AF_INET
            SOCKET_TYPE = socket.SOCK_DGRAM
            sock_object = socket.socket(ADDRESS_FAMILY, SOCKET_TYPE)

            # Iterate over the reversed list of rows and send data
            for row in rows:
                MESSAGE = prepare_message_from_row(row)
                sock_object.sendto(MESSAGE, address_tuple)
                logging.info(f"Sent: {MESSAGE} on port {PORT}. Hit CTRL-c to stop.")
                time.sleep(3)
        
        logging.info("Streaming complete!")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# ---------------------------------------------------------------------------
# If this is the script we are running, then call some functions and execute code!
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        logging.info("===============================================")
        logging.info("Starting fake streaming process.")
        stream_row(INPUT_FILE_NAME, ADDRESS_TUPLE)
        logging.info("Streaming complete!")
        logging.info("===============================================")
    except Exception as e:
        logging.error(f"An error occurred: {e}")