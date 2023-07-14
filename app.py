import streamlit as st
import prepocessor, helper

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8") # converted byte data to the string
    # st.text(data)
    df = prepocessor.preprocess(data)
    # st.dataframe(df)
    
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
        
        if user == 'Overall':
            st.dataframe(df)
        else:
            st.dataframe(df[df['user'] == user])
        
        
        msges_num, no_of_words = helper.fetch_stats(user,df)
        
        col1, col2, col3, col4 = st.columns(4)
       
        with col1:
            st.header("Total messages")
            st.title(msges_num)
        with col2:
            st.header("Total words")
            st.title(no_of_words)