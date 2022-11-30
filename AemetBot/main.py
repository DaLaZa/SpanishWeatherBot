# Imports
import sys
sys.path.append(".")
from AemetBot.aemet.final_forecast import get_complete_forecast, get_scheduled_forecast

# Main.
if __name__ == '__main__':
    print(get_complete_forecast("Teruel"))
    # print(get_scheduled_forecast("Teruel", 7, 11, "tomorrow"))
