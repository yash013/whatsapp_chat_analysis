def fetch_stats(user,df):
    
    if user!='Overall':
        df = df[df['user'] == user]
    
    no_of_msges = df.shape[0] 
    #fetch the number of words
    words = []
    for msg in df['message']:
        words.extend(msg.split())
    
    no_of_words = len(words)
            
    return no_of_msges, no_of_words
    
    
    