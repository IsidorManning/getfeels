from googleapiclient.discovery import build


class FetchData:
    """
    A class to fetch data from YouTube API for a given channel.

    Attributes:
        channel_name (str): The name of the YouTube channel.
        API_KEY (str): The API key for accessing the YouTube API.
        API_SERVICE_NAME (str): The name of the API service (YouTube).
        API_VERSION (str): The version of the API (v3).
        youtube (googleapiclient.discovery.Resource): The YouTube API resource object.
    """

    def __init__(self, channel_name, API_KEY):
        self.channel_name = channel_name
        self.API_KEY = API_KEY
        self.API_SERVICE_NAME = 'youtube'
        self.API_VERSION = 'v3'
        self.youtube = self.get_youtube()

    def get_youtube(self):
        """
        Creates a YouTube API resource object.

        Returns:
            googleapiclient.discovery.Resource: The YouTube API resource object.
        """
        youtube = build(self.API_SERVICE_NAME, self.API_VERSION,
                        developerKey=self.API_KEY)
        return youtube

    def get_latest_comments(self):
        """
        Retrieves the latest comments from the channel's latest video.

        Returns:
            list: A list of strings representing the latest comments.
        """
        channel_id = self.get_channel_id()
        uploads_playlist_id = self.get_uploads_playlist_id(channel_id)
        latest_video_id = self.get_latest_video_id(uploads_playlist_id)
        comments = self.get_comments(latest_video_id)

        return comments

    def get_channel_id(self):
        """
        Retrieves the channel ID for the given channel name.

        Returns:
            str: The channel ID.
        """
        search_request = self.youtube.search().list(
            q=self.channel_name,
            part="id,snippet",
            type="channel",
            maxResults=1,
        )
        search_response = search_request.execute()
        channel_id = search_response["items"][0]["id"]["channelId"]

        return channel_id

    def get_uploads_playlist_id(self, channel_id):
        """
        Retrieves the uploads playlist ID for the given channel ID.

        Parameters:
            channel_id (str): The channel ID.

        Returns:
            str: The uploads playlist ID.
        """
        channels_request = self.youtube.channels().list(
            part="contentDetails",
            id=channel_id,
        )
        channel_response = channels_request.execute()

        channel_details = channel_response["items"][0]["contentDetails"]
        uploads_playlist_id = channel_details["relatedPlaylists"]["uploads"]
        return uploads_playlist_id

    def get_latest_video_id(self, uploads_playlist_id):
        """
        Retrieves the ID of the latest video in the given playlist.

        Parameters:
            uploads_playlist_id (str): The uploads playlist ID.

        Returns:
            str: The ID of the latest video.
        """
        playlist_items_request = self.youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=1
        )
        playlist_items_respone = playlist_items_request.execute()

        latest_video_id = playlist_items_respone["items"][0]["contentDetails"]["videoId"]
        return latest_video_id

    def get_comments(self, video_id):
        """
        Retrieves comments from the video with the given ID.

        Parameters:
            video_id (str): The ID of the video.

        Returns:
            list: A list of strings representing the comments.
        """
        comments = []  # Initialize an empty list to store comments.
        request = self.youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
        )
        # Execute the API request and retrieve comments.
        response = request.execute()
        for item in response['items']:
            # Extract the top level comment from the item's snippet.
            comment = item["snippet"]["topLevelComment"]
            # Append the text display of the comment to the 'comments' list.
            comments.append(comment["snippet"]["textDisplay"])

        print(len(comments))
        return comments
