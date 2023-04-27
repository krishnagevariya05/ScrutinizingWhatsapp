import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import re


st.set_page_config(page_title="WhatsApp Chat Analyzer", page_icon=":bar_chart:", layout="wide")
st.sidebar.title("ANATOMIZING WHATSUP!!")


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data) --> Displaying data
    df = preprocessor.preprocess(data)
    # st.dataframe(df) --> Displaying data in dataframe format

    # Fetching unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')  # removing group notification
    user_list.sort()      # sorting user_list
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis with respect to ",user_list)

    if st.sidebar.button("SHOW ANALYSIS"):
        st.title("TOP STATISTICS")
        num_messages,words,num_media_messages,num_links = helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 =st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        #Displaying the monthly timeline
        # st.title("MONTHLY TIMELINE")
        # timeline = helper.monthly_timeline(selected_user,df)
        # fig, ax = plt.subplots()
        # ax.plot(timeline['time'], timeline['message'], color='red')
        # plt.xticks(rotation='vertical')
        # st.pyplot(fig)
        st.title("MONTHLY TIMELINE")
        timeline = helper.monthly_timeline(selected_user, df)
        fig = go.Figure(data=go.Scatter(x=timeline['time'], y=timeline['message'], fill='tozeroy', mode='lines',
                                        line=dict(color='#009688', width=2)))
        fig.update_layout(xaxis_title='MONTH', yaxis_title='NUMBER OF MESSAGES', title_x=0.5)
        st.plotly_chart(fig)

        # Displaying the daily timeline
        # st.title("DAILY TIMELINE")
        # daily_timeline = helper.daily_timeline(selected_user, df)
        #
        # fig, ax = plt.subplots()
        # ax.plot(daily_timeline['only_date'], daily_timeline['message'],color='blue')
        # st.pyplot(fig)
        st.title("DAILY TIMELINE")
        daily_timeline = helper.daily_timeline(selected_user, df)

        fig = go.Figure(data=go.Scatter(x=daily_timeline['only_date'], y=daily_timeline['message'], fill='tozeroy', mode='lines',line=dict(color='#4285F4', width=2)))
        fig.update_layout(xaxis_title='DATE', yaxis_title='NUMBER OF MESSAGES', title_x=0.5)
        st.plotly_chart(fig)

        #Activity Map
        # st.title("ACTIVITY MAP")
        # col1, col2 = st.columns(2)
        # with col1:
        #     st.header("MOST BUSY DAY")
        #     busy_day = helper.weekly_activity(selected_user,df)
        #     fig, ax = plt.subplots()
        #     plt.xticks(rotation='vertical')
        #     ax.bar(busy_day.index, busy_day.values, color='#597a62')
        #     st.pyplot(fig)
        # with col2:
        #     st.header("MOST BUSY MONTH")
        #     busy_month = helper.monthly_activity(selected_user,df)
        #     fig, ax = plt.subplots()
        #     plt.xticks(rotation='vertical')
        #     ax.bar(busy_month.index, busy_month.values, color='#2c757d')
        #     st.pyplot(fig)

        st.title("ACTIVITY MAP")
        # col1, col2 = st.columns(2)
        # Plot busiest day on the first column
        # with col1:
        st.header("MOST BUSY DAY")
        busy_day = helper.weekly_activity(selected_user, df)
        sns.set_palette("husl")  # set color palette
        fig, ax = plt.subplots(figsize=(6, 4))
        ax = sns.lineplot(x=busy_day.index, y=busy_day.values)
        ax.set_xlabel("Day of the Week")
        ax.set_ylabel("Number of Messages")
        ax.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        ax.grid(True)  # add grid lines
        for i, v in enumerate(busy_day.values):
            ax.text(i, v + 10, str(v), ha='center', fontsize=10, fontweight='bold')
        st.pyplot(fig)
        # Plot busiest month on the second column

        st.header("MOST BUSY MONTH")
        busy_month = helper.monthly_activity(selected_user, df)
        fig, ax = plt.subplots(figsize=(8, 6))
        ax = sns.barplot(x=busy_month.index, y=busy_month.values, color='#2c757d')
        ax.set_xlabel("MONTH")
        ax.set_ylabel("NUMBER OF MESSAGES")
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        st.pyplot(fig)

        # Heatmap of timewise usage
        st.title("USAGE HEATMAP")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # Finding the most busy users at group level
        if selected_user == 'Overall':
            st.title("MOST BUSY USERS")
            x,per_df = helper.fetch_most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='#3da1a1')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.write('Percentage of messages sent by each user:')
                st.dataframe(per_df)

        # # Displaying Wordcloud
        # st.title("WORDCLOUD")
        # df_wc = helper.generate_wordcloud(selected_user,df)
        # fig, ax = plt.subplots()
        # ax.imshow(df_wc)
        # st.pyplot(fig)

        # Displaying most common 20 words
        most_common_df = helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1], color='#44694b')
        plt.xticks(rotation='vertical')
        # st.dataframe(most_common_df)
        st.title("MOST COMMON WORDS")
        st.pyplot(fig)

        # Sentiment analysis
        # Filter out irrelevant messages
        st.title("SENTIMENT ANALYSIS OF CHAT")
        tempdf = df[(df['user'] != 'group_notification') &
                    (df['message'] != '<Media omitted>\n') &
                    (df['message'] != 'You joined using this group\'s invite link\n') &
                    (df['message'] != 'This message was deleted\n') &
                    (df['message'] != 'joined using this group\'s invitation\n')]
        sentiment_data = tempdf['message'].apply(helper.perform_sentiment_analysis)

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.countplot(x=sentiment_data, palette=['#712dd6', '#2dd3d6', '#282b27'], edgecolor='black')
        ax.set_xlabel("SENTIMENT", fontsize=14)
        ax.set_ylabel("NUMBER OF MESSAGES", fontsize=14)
        ax.tick_params(axis='both', labelsize=12)
        ax.set_xticklabels(['POSITIVE', 'NEUTRAL', 'NEGATIVE'], fontsize=12)
        sns.despine()
        plt.tight_layout()
        st.pyplot(fig)

        # Emoji analysis
        emoji_df = helper.emoji_find(selected_user,df)
        st.title("EMOJI ANALYSIS")
        # Displaying emojis
        st.header("EMOJIS USED")
        emoji_df.columns = ['Emoji', 'Number of repetitions']
        st.dataframe(emoji_df, width=300)

        #Pie chart of emojis
        st.header("TOP 10 EMOJIS")
        top_emojis = emoji_df.nlargest(10, 'Number of repetitions')
        fig = px.pie(top_emojis, values='Number of repetitions', names='Emoji', color='Emoji')
        fig.update_layout(width=800, height=600)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)