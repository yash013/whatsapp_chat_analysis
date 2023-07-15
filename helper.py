from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(user,df):
    
    if user!='Overall':
        df = df[df['user'] == user]
    
    # fetch number of words
    no_of_msges = df.shape[0] 
    
    #fetch the number of words
    words = []
    for msg in df['message']:
        words.extend(msg.split())
        
    # count how many times each word is appearing in the list via built-in function
    # freqs = Counter(words).most_common()[::-1][:20]
    
    no_of_words = len(words)
    
    # fetch number of media messages
    media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    
    # fetch number of links shared
    links = df[df['message'].str.contains('http')].shape[0]
            
    return no_of_msges, no_of_words, media_messages, links

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0])*100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percentage'})
    return x, df

def create_wordcloud(user, df):
    
    if user!='Overall':
        df = df[df['user'] == user]
    
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    f = open('stopwords_hinglish.txt', 'r')
    stop_words = f.read()
    
        
    def remove_stop_words(msg):
        ls =  []
        for word in msg.lower().split():
            if word not in stop_words:
                ls.append(word)
        return " ".join(ls)
    
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(user, df):
    
    if user!='Overall':
        df = df[df['user'] == user]
        
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    f = open('stopwords_hinglish.txt', 'r')
    stop_words = f.read()
    
    words = []
    for msg in temp['message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)
    
    return pd.DataFrame(Counter(words).most_common(20))

def emoji_analysis(user, df):
    
    if user!='Overall':
        df = df[df['user'] == user]
    
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

def monthly_timeline(user, df):
    
    if user!='Overall':
        df = df[df['user'] == user]
    
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+ '-' + str(timeline['year'][i]))
    
    timeline['time'] = time
    
    return timeline

def daily_timeline(user, df):
    
    if user!='Overall':
        df = df[df['user'] == user]
    
    df['only_date'] = df['date'].dt.date
    
    daily_timeline = df.groupby(['only_date']).count()['message'].reset_index()
    
    return daily_timeline
    
    
    
    
    
    
    