from datetime import datetime

def convert(example: str) -> str:
    try:
        date, time = example.split()
        
        # Convert time to 12-hour format with AM/PM
        twenty_four = datetime.strptime(time, "%H:%M")
        formatted_time = twenty_four.strftime("%I:%M %p")
        
        # Combine date and formatted time into final string
        reformatted_date_time = f"{date} {formatted_time}"
        return reformatted_date_time
    
    except Exception as e:
        return f"Error converting date and time: {e}"

example = '2023-10-03 15:10'
print(convert(example))  # Output should be '2023-10-03 03:10 PM'
