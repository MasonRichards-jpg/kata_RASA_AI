from datetime import datetime

def convert(example: str) -> str:
    date, time = example.split()
    twenty_four = datetime.strptime(time, "%H:%M")
    formatted_time = twenty_four.strftime("%I:%M %p")
    reformatted_date_time = f"{date} {formatted_time}"
    return reformatted_date_time


example = '2023-10-03 15:10'
print(convert(example))  
