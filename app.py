import streamlit as st
import prepocessor

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
    users.remove('group_notification')
    users.sort()
    
    st.sidebar.selectbox("Show analysis wrt", users)
    
    if st.sidebar.button("Show Analysis"):
        pass