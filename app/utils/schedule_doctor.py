import random


def schedule_appointment():
    """fake data to get doctor details"""
    # List of available doctors
    doctors = ["Dr. Smith", "Dr. Johnson", "Dr. Brown", "Dr. Davis", "Dr. Wilson", "Dr. Lee", "Dr. White", "Dr. Harris", "Dr. Clark", "Dr. Turner"]

    # List of available weekdays
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    # Randomly select a doctor
    selected_doctor = random.choice(doctors)

    # Randomly select a weekday
    selected_weekday = random.choice(weekdays)

    # Randomly select a time slot between 9 AM and 5 PM in 15-minute intervals
    start_hour = random.randint(9, 16)  # 9 AM to 4 PM
    start_minute = random.choice([0, 15, 30, 45])
    end_hour = start_hour
    end_minute = start_minute + 45  # Add 45 minutes for the slot duration

    # Format the time slot
    start_time = f"{start_hour:02d}:{start_minute:02d}"
    end_time = f"{end_hour:02d}:{end_minute:02d}"

    # Print the selected doctor, weekday, and time slot
    doctor_details = {"doctor": selected_doctor, "date": selected_weekday, "time": f"{start_time} - {end_time}"}
    return doctor_details
