from api_client import get_new_data
from storage import *
import threading
import time
from dash_app import app, create_layout

collector_running = True


class DataCollectorThread(threading.Thread):
    def run(self):
        while collector_running:
            add_measurements(1, get_new_data("1"))
            add_measurements(2, get_new_data("2"))
            add_measurements(3, get_new_data("3"))
            add_measurements(4, get_new_data("4"))
            add_measurements(5, get_new_data("5"))
            expire_data(600)    # Expire data after 10 minutes
            time.sleep(0.2)     # Get data 5 times per second


if __name__ == "__main__":
    # Initialization
    init_storage()

    # Start the collector
    collector = DataCollectorThread()
    collector.start()
    # Start dash app
    app.config.suppress_callback_exceptions = True
    app.run_server(debug=True)
