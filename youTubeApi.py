
from googleapiclient.discovery import build
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob


YOUTUBE_API_KEY = "AIzaSy**********************************"
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

request = youtube.videos().list(
    part="snippet,statistics",
    chart="mostPopular",
    regionCode="US",
    maxResults=10
)
response = request.execute()

## **📊 Step 5: Store Data in a DataFrame**

video_data = []
for item in response["items"]:
    video_data.append({
        "Title": item["snippet"]["title"],
        "Views": int(item["statistics"]["viewCount"]),
        "Likes": int(item["statistics"].get("likeCount", 0)),
        "Comments": int(item["statistics"].get("commentCount", 0))
})

video_df = pd.DataFrame(video_data)
video_df.head()


# plt.figure(figsize=(10,5))
# plt.bar(video_df["Title"], video_df["Likes"], color='blue')
# plt.xlabel("Video Title")
# plt.ylabel("Likes")
# plt.title("Likes on Trending Videos")
# plt.xticks(rotation=45, ha='right')
# plt.show()



video_id = response["items"][0]["id"] # Get first video's ID

comment_request = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    maxResults=20
)
comment_response = comment_request.execute()

comments = []
sentiments = []

for item in comment_response["items"]:
    comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
    sentiment = TextBlob(comment).sentiment.polarity  # Analyzes sentiment
    comments.append(comment)
    sentiments.append(sentiment)

comment_df = pd.DataFrame({"Comment": comments, "Sentiment": sentiments})
# print(comment_df.head())

plt.hist(comment_df["Sentiment"], bins=20, color='green', alpha=0.7)
plt.xlabel("Sentiment Score")
plt.ylabel("Frequency")
plt.title("YouTube Comment Sentiment Analysis")
plt.show()