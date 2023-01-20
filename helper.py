import imp
from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import wordcloud
import emoji

extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    num_messges = df.shape[0]
    words = []
    for message in df["message"]:
        words.extend(message.split())

    num_media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messges, len(words), num_media_msg, len(links)


def most_busy_user(df):
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts()/df.shape[0])*100,
               2).reset_index().rename(columns={'index': 'name', 'users': 'percentage'})

    return x, df


def create_wordcloud(selected_user, df):

    f = open("stopwords.txt", 'r', encoding='utf-8')
    stopwords = f.read()
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stopwords:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10,
                   background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    dfwc = wc.generate(temp['message'].str.cat(sep=" "))
    return dfwc

    # most common words


def most_common_words(selected_user, df):
    f = open("stopwords.txt", 'r', encoding='utf-8')
    stopwords = f.read()
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    word = []
    for message in temp['message']:
        for i in message.lower().split():
            if i not in stopwords:
                word.append(i)

    most_common_df = pd.DataFrame(Counter(word).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    emojis = []
    for message in df["message"]:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()[
        'message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline


def week_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    series = df['day_name'].value_counts()
    return series


def month_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    month = df['month'].value_counts()
    return month


def heatmap(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period',
                                  values='message', aggfunc='count').fillna(0)
    return user_heatmap

    # name = x.index
    # count = x.values
    # plt.bar(name, count)
    # plt.xticks(rotation='vertical')
    # plt.show()

    # if selected_user == "Overall":
    #     num_messges = df.shape[0]
    #     words = []
    #     for message in df["message"]:
    #         words.extend(message.split())
    #     return num_messges, len(words)
    # else:
    #     new_df = df[df['users'] == selected_user]
    #     num_messges = new_df.shape[0]
    #     words = []
    #     for message in new_df["message"]:
    #         words.extend(message.split())
    #     return num_messges, len(words)
