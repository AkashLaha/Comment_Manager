import googleapiclient.discovery
import googleapiclient.errors
import matplotlib.pyplot as plt
import pandas as pd
import joblib

api_service_name = 'youtube'
api_version = 'v3'
developer_key = 'AIzaSyDssIxO4pqiiTrkeIgm1_DjazziBlODkMY'

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=developer_key)

video_id = 'cNTgN4GNqdM'
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

sen_df = df.copy()  # Make a copy to avoid modifying the original DataFrame
sen_text = sen_df['text'].tolist()

svm_classifier = joblib.load('svm_model.pkl')
tfidf = joblib.load('tfidf_vectorizer.pkl')

sent_features = tfidf.transform(sen_text)

predicted_labels = svm_classifier.predict(sent_features)
sen_df['predicted_sentiment'] = predicted_labels

positive_list = sen_df[sen_df['predicted_sentiment'] == 2]['text'].tolist()
negative_list = sen_df[sen_df['predicted_sentiment'] == 0]['text'].tolist()
neutral_list = sen_df[sen_df['predicted_sentiment'] == 1]['text'].tolist()

print("Positive List:", positive_list)
print("Negative List:", negative_list)
print("Neutral List:", neutral_list)


