import logging
logger = logging.getLogger(__name__)

###############################################################################


def show_i2c_interfaces(client):

    try:
        response = requests.get('http://localhost:6742/i2c')
        response.raise_for_status()  # Raise an error for bad responses
        interfaces = response.json()  # Parse the JSON response

        if interfaces:
            logger.info("I2C Interfaces:")
            for interface in interfaces:
                logger.info(f"  - {interface}")
        else:
            logger.info("No I2C interfaces found.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error accessing I2C interfaces: {e}")
        raise
