from flask import Flask, request, jsonify
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
import joblib
import matplotlib.pyplot as plt

app = Flask(__name__)

# Function to process comments and categorize them (replace with your logic)
def categorize_comments(video_url):
    # Process comments and categorize them
    # Replace this with your actual code for processing comments

    # Sample categorized comments

    api_service_name = 'youtube'
    api_version = 'v3'
    developer_key = 'AIzaSyDssIxO4pqiiTrkeIgm1_DjazziBlODkMY'

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=developer_key)


    comments = []

    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_url,
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

    sen_df = df.copy()  # Make a copy to avoid modifying the original DataFrame
    sen_text = sen_df['text'].tolist()

    svm_classifier = joblib.load('svm_model.pkl')
    tfidf = joblib.load('tfidf_vectorizer.pkl')

    sent_features = tfidf.transform(sen_text)

    predicted_labels = svm_classifier.predict(sent_features)
    sen_df['predicted_sentiment'] = predicted_labels
    create_sentiment_bar_chart(sen_df)

    positive_list = sen_df[sen_df['predicted_sentiment'] == 2]['text'].tolist()
    negative_list = sen_df[sen_df['predicted_sentiment'] == 0]['text'].tolist()
    neutral_list = sen_df[sen_df['predicted_sentiment'] == 1]['text'].tolist()

    print("Positive List:", positive_list)
    print("Negative List:", negative_list)
    print("Neutral List:", neutral_list)




    return {
        "positive_comments": positive_list,
        "negative_comments": negative_list,
        "neutral_comments": neutral_list,

    }
def categorize_spam_non_spam_comments(video_url):
    video_id = video_url.split('=')[1]

    api_service_name = 'youtube'
    api_version = 'v3'
    developer_key = 'AIzaSyDssIxO4pqiiTrkeIgm1_DjazziBlODkMY'

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=developer_key)

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

    spam_df = df.copy()  # Make a copy to avoid modifying the original DataFrame
    spam_text = spam_df['text'].tolist()

    spam_model = joblib.load('spam_model.pkl')
    spam_vectorizer = joblib.load('spam_vectorizer.pkl')

    spam_features = spam_vectorizer.transform(spam_text)

    predicted_labels = spam_model.predict(spam_features)
    spam_df['predicted_sentiment'] = predicted_labels
    spam_list = spam_df[spam_df['predicted_sentiment'] == 'Spam Comment']['text'].tolist()
    non_spam_list = spam_df[spam_df['predicted_sentiment'] == 'Not Spam']['text'].tolist()
    return {
        "spam_comments": spam_list,
        "not_spam_comments": non_spam_list,
    }


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
    # Instead of showing the chart, save it to a file
    plt.savefig('sentiment_chart.png')

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
    # Instead of showing the chart, save it to a file
    plt.savefig('spam_chart.png')


@app.route('/analyze_video', methods=['POST'])
def analyze_video():
    try:
        # Get the video URL from the POST request
        video_url = request.form.get('video_url')

        # Call the function to categorize comments
        categorized_comments = categorize_comments(video_url)

        # Return categorized comments in JSON format
        return jsonify(categorized_comments)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/fetch_spam_non_spam_comments', methods=['POST'])
def fetch_spam_non_spam_comments():
    try:
        # Get the video URL from the POST request
        video_url = request.form.get('video_url')

        # Call the function to categorize comments
        categorized_data = categorize_spam_non_spam_comments(video_url)

        # Return categorized comments in JSON format
        return jsonify(categorized_data)
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)