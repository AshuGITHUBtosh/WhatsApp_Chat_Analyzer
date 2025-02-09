import re
import pandas as pd

# Load the WhatsApp chat data into a DataFrame
with open('/home/ashutosh/Desktop/data_science_project_1/WhatsApp Chat with Fan Club/WhatsApp Chat with Fan Club.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Define a regex pattern to match emojis
emoji_pattern = re.compile(
    "[\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F900-\U0001F9FF"  # supplemental symbols and pictographs
    "\U0001F1E0-\U0001F1FF"  # flags
    "]+",
    flags=re.UNICODE)

# Regex pattern to match [Date, Time] Sender: Message
pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2} [APM]{2}) - (.*?): (.*)'

data = []
for line in lines:
    match = re.match(pattern, line)
    if match:
        date, time, sender, message = match.groups()
        # Remove emojis from the message
        clean_message = emoji_pattern.sub(r'', message)
        data.append([date, time, sender, clean_message])

# Create a DataFrame from the parsed data
df = pd.DataFrame(data, columns=['Date', 'Time', 'Sender', 'Clean_Message'])

# Check the DataFrame
print(df.head())  # Display the first few rows to confirm cleaning
