import googleapiclient.discovery
import googleapiclient.errors
import matplotlib.pyplot as plt
import pandas as pd
import joblib


api_service_name = 'youtube'
api_version = 'v3'
developer_key = 'AIzaSyDssIxO4pqiiTrkeIgm1_DjazziBlODkMY'

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=developer_key)


comments = []

next_page_token = None

while True:
    request = youtube.commentThreads().list(
        part="snippet",
        videoId='TSSyw23fO5U',
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

    # Filter the DataFrame based on sentiment values
positive_comments = df[df['predicted_sentiment'] == 2]['comments'].tolist()
negative_comments = df[df['predicted_sentiment'] == 0]['comments'].tolist()
neutral_comments = df[df['predicted_sentiment'] == 1]['comments'].tolist()

print("Positive Comments:", positive_comments)
print("Negative Comments:", negative_comments)
print("Neutral Comments:", neutral_comments)