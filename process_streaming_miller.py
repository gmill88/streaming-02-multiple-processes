
# Import from Python Standard Library
import csv
import socket
import time
import logging

# Set up basic configuration for logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Program Constants
HOST = "localhost"
PORT = 9999
ADDRESS_TUPLE = (HOST, PORT)
INPUT_FILE_NAME = "bitcoin_historical_data.csv"
OUTPUT_FILE_NAME = "out9.txt"

# Prepare message for row
def prepare_message_from_row(row):
    return f"{','.join(row)}\n".encode()

# stream data
def stream_row(input_file_name, output_file_name, address_tuple):
    logging.info(f"Starting to stream data from {input_file_name} to {address_tuple}.")
    # Open input file for reading
    with open(input_file_name, "r") as input_file:

        # create CSV reader object
        reader = csv.reader(input_file, delimiter=",")

        # Skip header
        header = next(reader)
        logging.info(f"skipped header row: {header}")

        # Read rows into list
        rows = list(reader)
        logging.debug(f"Number of rows read: {len(rows)}")

        # Reverse rows to read oldest data first
        rows.reverse()

    
    with open(output_file_name, "w") as output_file:
        output_file.write(','.join(header) + '\n')
        # Create socket
        sock_object = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        for row in rows:
            MESSAGE = prepare_message_from_row(row)
            sock_object.sendto(MESSAGE, address_tuple)
            output_file.write(','.join(row) + '\n')
            logging.info(f"Sent: {MESSAGE} on port {PORT}. Hit CTRL-c to stop.")
            time.sleep(2)

        



if __name__ == "__main__":
    try:
        logging.info("===============================================")
        logging.info("Starting fake streaming process.")
        stream_row(INPUT_FILE_NAME, OUTPUT_FILE_NAME, ADDRESS_TUPLE)
        logging.info("Streaming complete!")
        logging.info("===============================================")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
