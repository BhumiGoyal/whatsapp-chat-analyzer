import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s(?:am|pm)\s\-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    cleaned_dates = [date.replace('\u202f', ' ').strip(' - ') for date in dates]
    if len(messages) == len(cleaned_dates):
        df = pd.DataFrame({'user_messages': messages, 'date_of_message': cleaned_dates})

        # Convert date_of_message type
        df['date_of_message'] = pd.to_datetime(df["date_of_message"], format='%d/%m/%y, %I:%M %p')

        # Rename the column
        df.rename(columns={'date_of_message': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_messages'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['month_num'] = df['date'].dt.month
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str("00"))
        elif hour == 00:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df["period"] = period

    return df
