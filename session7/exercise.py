import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()  # also print to console
    ]
)

def process_data(data):
    logging.debug(f"Processing data: {data}")

    if not data:
        logging.warning("Empty data received")
        return None

    try:
        result = sum(data) / len(data)
        logging.info(f"Average calculated: {result}")
        return result
    except TypeError as e:
        logging.error(f"Invalid data type: {e}")
        return None

if __name__ == "__main__":
    logging.info("Application started")
    process_data([10, 20, 30])
    process_data([])
    process_data(None)
    logging.info("Application finished")