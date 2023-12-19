import googleapiclient.discovery
import googleapiclient.errors
import matplotlib.pyplot as plt
import pandas as pd
import joblib


def yt_comments_scrap(v_id):
    api_service_name = 'youtube'
    api_version = 'v3'
    developer_key = 'AIzaSyDssIxO4pqiiTrkeIgm1_DjazziBlODkMY'

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=developer_key)

    video_id = v_id
    comments = []

    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,  # You can adjust this value as needed (up to 100 per request).
            pageToken=next_page_token
        )

        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([comment['authorDisplayName'], comment['textDisplay']])

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    df = pd.DataFrame(comments, columns=['author', 'text'])
    return df


def sentiment_analysis(input_data, input_type='df'):
    if input_type == 'df':
        sen_df = input_data.copy()  # Make a copy to avoid modifying the original DataFrame
        sen_text = sen_df['text'].tolist()
    elif input_type == 'str':
        sen_df = pd.DataFrame({'text': [input_data]})
        sen_text = [input_data]
    else:
        raise ValueError("Invalid input_type. Use 'DataFrame' or 'String'.")

    svm_classifier = joblib.load('svm_model.pkl')
    tfidf = joblib.load('tfidf_vectorizer.pkl')

    sent_features = tfidf.transform(sen_text)

    predicted_labels = svm_classifier.predict(sent_features)
    sen_df['predicted_sentiment'] = predicted_labels

    if input_type == 'df':
        return sen_df
    elif input_type == 'str':
        return sen_df['predicted_sentiment'].iloc[0]


def create_sentiment_bar_chart(dataframe):
    # Count the occurrences of each sentiment value
    sentiment_counts = dataframe['predicted_sentiment'].value_counts()

    # Define labels for the sentiments
    labels = ['Neutral', 'Positive', 'Negative']

    # Create a bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(labels, sentiment_counts, color=['red', 'blue', 'green'])
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.title('Sentiment Analysis Results')
    plt.show()


def spam(input_data, input_type='df'):
    if input_type == 'df':
        spam_df = input_data.copy()  # Make a copy to avoid modifying the original DataFrame
        spam_text = spam_df['text'].tolist()
    elif input_type == 'str':
        spam_df = pd.DataFrame({'text': [input_data]})
        spam_text = [input_data]
    else:
        raise ValueError("Invalid input_type. Use 'DataFrame' or 'String'.")

    spam_model = joblib.load('spam_model.pkl')
    spam_vectorizer = joblib.load('spam_vectorizer.pkl')

    spam_features = spam_vectorizer.transform(spam_text)

    predicted_labels = spam_model.predict(spam_features)
    spam_df['predicted_sentiment'] = predicted_labels

    if input_type == 'df':
        return spam_df
    elif input_type == 'str':
        return spam_df['predicted_sentiment'].iloc[0]


def create_spam_bar_chart(dataframe):
    # Count the occurrences of each label (spam and non-spam)
    spam_counts = dataframe['predicted_sentiment'].value_counts()

    # Define labels for the sentiments
    labels = ['Non-Spam', 'Spam']

    # Create a bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(labels, spam_counts, color=['red', 'green'])
    plt.xlabel('Spam')
    plt.ylabel('Count')
    plt.title('Spam Detection Results')
    plt.show()


v_id = input("Enter id of YouTube video:")
data = yt_comments_scrap(v_id)
c = data
sen_data = sentiment_analysis(input_data=c, input_type='df')

value_counts = sen_data['predicted_sentiment'].value_counts()
print(value_counts)

create_sentiment_bar_chart(sen_data)

# spam_data = spam(input_data=c, input_type='str')
# print(spam_data)