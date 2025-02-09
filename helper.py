import re
import pandas as pd
import matplotlib.pyplot as plt

def fetch_stats(select_user, df):
    # Count total messages
    if select_user == "overall":
        num_messages = df.shape[0]
        num_media_messages = df[df['chat'] == '<Media omitted>\n'].shape[0]
        num_links = df['chat'].str.contains(r'http[s]?://\S+', na=False).sum()
    else:
        num_messages = df[df['user'] == select_user].shape[0]
        num_media_messages = df[(df['user'] == select_user) & (df['chat'] == '<Media omitted>\n')].shape[0]
        num_links = df[(df['user'] == select_user) & df['chat'].str.contains(r'http[s]?://\S+', na=False)].shape[0]
    
    return num_messages, num_media_messages, num_links

def top_users(df):
    # Count messages for each user
    user_message_count = df['user'].value_counts().head(5)
    
    # Plot bar chart
    plt.figure(figsize=(10, 6))
    user_message_count.plot(kind='bar', color='skyblue')
    plt.title('Top 5 Users by Number of Messages')
    plt.xlabel('User')
    plt.ylabel('Total Messages')
    plt.xticks(rotation=45)
    plt.show()

    return user_message_count

def get_user_chats(user, df):
    # Filter DataFrame for the specific user and select 'chat' and 'message_date' columns
    user_chats = df[df['user'] == user][['chat', 'message_date']].reset_index(drop=True)
    
    return user_chats
    

