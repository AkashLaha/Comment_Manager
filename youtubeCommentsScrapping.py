import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd

api_service_name = 'youtube'
api_version = 'v3'
DEVELOPER_KEY = 'AIzaSyDssIxO4pqiiTrkeIgm1_DjazziBlODkMY'

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

video_id = "Cy-KKK3Bn2E"
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
print(df)
df.to_csv("phonereview.csv",index=False)
