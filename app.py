import streamlit as st
import prepocessor, helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8") # converted byte data to the string
    # st.text(data)
    df = prepocessor.preprocess(data)
    
    #fetch unique users
    users = df['user'].unique().tolist()
    users.insert(0, "Overall")
    #remove 'group_notification' from the users
    if len(users) > 3:
        users.remove('group_notification')
    else:
        pass
    
    users.sort()
    
    
    user = st.sidebar.selectbox("Show analysis wrt", users)
    
    if st.sidebar.button("Show Analysis"):
        
        msges_num, no_of_words, media_messages, links = helper.fetch_stats(user,df)
        
        st.title("Top Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
       
        with col1:
            st.header("Total messages")
            st.title(msges_num)
            
        with col2:
            st.header("Total words")
            st.title(no_of_words)
            
        with col3:
            st.header("Media Shared")
            st.title(media_messages)
            
        with col4:
            st.header("links Shared")
            st.title(links)
            
        # Daily timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(user,df)
        fig,ax = plt.subplots()
        plt.plot(daily_timeline['only_date'], daily_timeline['message'], color="brown")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        
        # Montly timeline
        st.title('Montly Timeline')
        timeline = helper.monthly_timeline(user,df)
        fig, ax = plt.subplots()
        plt.plot(timeline['time'], timeline['message'], color="red")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Find the busiest person in the chat group
        if user == 'Overall':
            st.title("Most busy Users")
            x,new_df= helper.most_busy_users(df)
            fig, ax = plt.subplots()
           
            col1, col2 = st.columns(2)
            
            with col1:
                ax.bar(x.index,x.values, color="green")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
                
            with col2:
                st.dataframe(new_df)
                
        else:
            pass
        
        # Wordcloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        # Most common words
        st.title("Most common words")
        df_mcw = helper.most_common_words(user,df)
        
        fig, ax = plt.subplots()
        ax.barh(df_mcw[0], df_mcw[1])
        plt.xticks(rotation='vertical')
        
        st.pyplot(fig)
        
        # emoji analysis
        st.title('Emoji Analysis')
        
        df_emoji = helper.emoji_analysis(user,df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(df_emoji)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(df_emoji[1].head(7), labels=df_emoji[0].head(7), autopct="%0.2f")
            
            st.pyplot(fig)
        
        
        
            
        
        