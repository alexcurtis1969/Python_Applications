import datetime

class TollBooth:
    def __init__(self, booth_id, toll_rate):
        self.booth_id = booth_id
        self.toll_rate = toll_rate
        self.transactions = []  # List to store transaction records

    def process_toll(self, vehicle_id, vehicle_type, timestamp=None):
        """
        Processes a toll transaction.

        Args:
            vehicle_id (str): The unique ID of the vehicle.
            vehicle_type (str): The type of vehicle (e.g., "car", "truck").
            timestamp (datetime, optional): The time of the transaction. Defaults to now.
        """
        if timestamp is None:
            timestamp = datetime.datetime.now()

        toll_amount = self.toll_rate  # Basic toll, can be extended for vehicle type

        # Example: Vary toll based on vehicle type (extend as needed)
        if vehicle_type == "truck":
            toll_amount *= 2  # Trucks pay double (example)

        transaction = {
            "vehicle_id": vehicle_id,
            "vehicle_type": vehicle_type,
            "timestamp": timestamp,
            "toll_amount": toll_amount,
        }
        self.transactions.append(transaction)
        print(f"Toll processed: Vehicle {vehicle_id}, Amount: ${toll_amount:.2f}")

    def generate_daily_report(self, date=None):
        """
        Generates a daily toll collection report.

        Args:
            date (datetime.date, optional): The date for the report. Defaults to today.
        """
        if date is None:
            date = datetime.date.today()

        total_collected = 0
        daily_transactions = []

        for transaction in self.transactions:
            if transaction["timestamp"].date() == date:
                total_collected += transaction["toll_amount"]
                daily_transactions.append(transaction)

        print(f"\nDaily Toll Report - {date}")
        print("-" * 30)
        for transaction in daily_transactions:
            print(
                f"Vehicle: {transaction['vehicle_id']}, "
                f"Type: {transaction['vehicle_type']}, "
                f"Time: {transaction['timestamp'].time()}, "
                f"Amount: ${transaction['toll_amount']:.2f}"
            )
        print("-" * 30)
        print(f"Total Collected: ${total_collected:.2f}")

# Sample Data Generation (now outside the class)
def generate_sample_data(booth, num_transactions=20):
    """Generates sample toll transactions."""
    vehicle_types = ["car", "truck", "motorcycle", "bus"]
    vehicle_ids = [f"VEH-{i:04d}" for i in range(1, 101)]  # Sample vehicle IDs

    for _ in range(num_transactions):
        vehicle_id = vehicle_ids[datetime.datetime.now().microsecond % len(vehicle_ids)] #make it random.
        vehicle_type = vehicle_types[datetime.datetime.now().microsecond % len(vehicle_types)] #make it random.
        # Random timestamp within the last few days
        days_ago = datetime.timedelta(days=datetime.datetime.now().microsecond % 3) #random 0-3 days.
        hours_ago = datetime.timedelta(hours=datetime.datetime.now().microsecond % 24) #random 0-24 hours.
        minutes_ago = datetime.timedelta(minutes=datetime.datetime.now().microsecond % 60) #random 0-60 minutes
        seconds_ago = datetime.timedelta(seconds=datetime.datetime.now().microsecond % 60) #random 0-60 seconds.

        random_time = datetime.datetime.now() - days_ago - hours_ago - minutes_ago - seconds_ago
        booth.process_toll(vehicle_id, vehicle_type, timestamp=random_time)

# Example Usage with Sample Data
booth1 = TollBooth(booth_id="Booth A", toll_rate=5.00)
booth2 = TollBooth(booth_id="Booth B", toll_rate=5.00)

generate_sample_data(booth1, num_transactions=30)
generate_sample_data(booth2, num_transactions=25)

booth1.generate_daily_report()
booth2.generate_daily_report()

# Example of generating a report for a specific date (e.g., yesterday)
yesterday = datetime.date.today() - datetime.timedelta(days=1)
booth1.generate_daily_report(date=yesterday)