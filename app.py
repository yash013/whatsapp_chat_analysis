import streamlit as st
import prepocessor, helper

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8") # converted byte data to the string
    # st.text(data)
    df = prepocessor.preprocess(data)
    st.dataframe(df)
    
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
        
        msges_num = helper.fetch_stats(user,df)
        
        col1, col2, col3, col4 = st.columns(4)
       
        with col1:
            st.header("Total messages")
            st.title(msges_num)