import streamlit as st
import pandas as pd
import helper
import preprocessor

st.sidebar.title("WhatsApp Chat Analyzer")

upload_file = st.sidebar.file_uploader("Choose a chat file")
if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocessing(data)
    st.dataframe(df)
    
    # Generate user list
    user_list = df["user"].unique().tolist()
    user_list.remove("notification")  # Assuming notification is in the data
    user_list.sort()
    user_list.insert(0, "overall")

    select_user = st.sidebar.selectbox("Show analysis for", user_list)

    # Analysis button
    if st.sidebar.button("Show Analysis"):
        num_messages, num_media_messages, num_links = helper.fetch_stats(select_user, df)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Media Messages")
            st.title(num_media_messages)

        with col3:
            st.header("Links Shared")
            st.title(num_links)

        # Display the user's chat messages if specific user selected
        if select_user != "overall":
            users_chats = helper.get_user_chats(select_user, df)
            st.subheader(f"Chat Messages from {select_user}")
            st.dataframe(users_chats)  # Display chats in a column format

    # Top chatters button
    if st.sidebar.button("Top Chatters"):
        top_chatters = helper.top_users(df)  # Fetch top 5 chatters
        st.header("Top 5 Users by Number of Messages")
        st.bar_chart(top_chatters)  # Display bar chart in Streamlit
