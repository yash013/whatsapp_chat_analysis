def fetch_stats(user,df):
    
    if user == "Overall":
        return df.shape[0]
    else:
        return df[df['user'] == user].shape[0]


    
    
    
    