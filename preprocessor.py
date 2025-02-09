import re
import pandas as pd
import calendar

def preprocessing(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\u202f(?:AM|PM) - '
    # Split messages and extract dates
    messages = re.split(pattern, data)
    dates = re.findall(pattern, data)

    # Remove the first empty string from messages (due to the split)
    if messages[0] == "":
        messages = messages[1:]

    # Create a DataFrame
    df = pd.DataFrame({"user_message": messages, "message_date": dates})

    users=[]
    chat=[]
    for message in df['user_message']:
        entry = re.split(r'([\w\s]+?):\s', message)

        if entry[1:]:
            users.append(entry[1])
            chat.append(entry[2])

        else:
            users.append('notification')
            chat.append(entry[0])

    df['user']=users
    df['chat']=chat
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['message_date'].str.split('/').str[-1].str[:2]

    df['month'] = df['message_date'].str.split('/').str[0]  # Extract month
    df['month'] = df['month'].apply(lambda x: calendar.month_name[int(x)])

    df['day'] = df['message_date'].str.split('/').str[1]    # Extract day

    df['time'] = df['message_date'].str.extract(r'(\d{1,2}:\d{2})')
    df['hour'] = df['time'].str.split(':').str[0]  # Extract hour
    df['minute'] = df['time'].str.split(':').str[1]  # Extract minute

    df['AM_PM'] = df['message_date'].str.extract(r'(\bAM\b|\bPM\b)')  # Extract AM or PM

    return df


