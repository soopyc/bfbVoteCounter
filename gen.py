import json

import dateutil.parser as dp
import requests as req


class InvalidObject(Exception):
    pass


class VideoNotFoundException(Exception):
    pass


class InvalidToken(Exception):
    pass


class Comment:
    """Returns a custom Comment object.

    :param obj: API return object, should match Google's API.
    :return: Comment object
    """

    def __init__(self, obj):
        p = self._parse(obj)
        self.author = p[0]
        self.text = p[1]
        self.published_at = p[2]

    def __str__(self):
        return self.text

    @staticmethod
    def _parse(o):
        """
        Internal Parse method

        :param o: object to be parsed.
        :return: Tuple([author, text, datetime(time)])
        """
        try:
            a = str(o["snippet"]["authorDisplayName"])
            t = o["snippet"]["textOriginal"]
            ti = dp.parse(o["snippet"]["publishedAt"])
        except KeyError:
            raise InvalidObject(
                "Invalid object passed into method, check https://developers.google.com/youtube/v3/docs"
                "/comments#resource for more information.")
        return a, t, ti


class CommentThread:
    """
    CommentThread object

    :param obj: API return object, should match Google's API.
    :return: CommentThread object
    """

    def __init__(self, obj):
        self.comment, self.reply_count, self.replies = self._parse(obj)

    def __str__(self):
        return f"CommentThread: {len(self.replies)} {'reply' if len(self.replies) == 1 else 'replies'}"

    @staticmethod
    def _parse(o):
        """
        Internal parse method

        :param o: API return object, should match Google's API.
        :return: Tuple([Comment(comment), reply_count, list([Comment(replies)], ...)])
        """
        com = Comment(o["snippet"]["topLevelComment"])
        rc = o["snippet"]["totalReplyCount"]
        rs = []
        if 'replies' in o:
            for i in o["replies"]["comments"]:
                rs.append(Comment(i))
        return com, rc, rs


class Video:
    """
    Video object

    :param obj: API return object, should match Google's API.
    :return: Video object
    """

    def __init__(self, obj):
        ct = self._parse(obj)
        self.publish_time = ct[0]
        self.title = ct[1]
        self.description = ct[2]
        self.channel_name = ct[3]
        self.total_views = int(ct[4])
        self.comments = int(ct[5])

    def __str__(self):
        return self.title

    @staticmethod
    def _parse(o):
        """
        Internal parse method.

        :param o:  object to be parsed.
        :return: Tuple([datetime(published_time), video_title, description, channel_name, views, comments])
        """
        try:
            pub = dp.parse(o["snippet"]["publishedAt"])
            title = o["snippet"]["title"]
            desc = o["snippet"]["description"]
            chnl = o["snippet"]["channelTitle"]
            views = o["statistics"]["viewCount"]
            coms = o["statistics"]["commentCount"]
        except KeyError:
            raise InvalidObject(
                "Invalid object passed into method, check https://developers.google.com/youtube/v3/docs"
                "/videos#resource-representation for more information.")
        return pub, title, desc, chnl, views, coms


class Fetchers:
    """Quick and easy YouTube Data API fetching functions
    :param key: Google API Token
    """

    def __init__(self, key):
        self.key = key

    def comment_thread(self, vid, npt=None):
        """
        Get a YouTube commentThread resource.

        :param vid: Video ID
        :param npt: Next page token. Will get first page result if not given.
        :return: tuple(list([CommentThread, ...]), next_page_token)
        """
        cth = []
        if npt is not None:
            next_page = f"&pageToken={npt}"
        else:
            next_page = ""
        url = f"https://www.googleapis.com/youtube/v3/commentThreads?" \
              f"part=snippet,replies&maxResults=100&videoId={vid}&key={self.key}" \
              f"{next_page}"
        temp = req.get(url)
        r = json.loads(temp.content)
        if 'error' in r:
            if r['error']['code'] == 404:
                raise VideoNotFoundException(
                    f"Cannot find any video with the ID {vid}.")
            else:
                raise NotImplementedError(str(r))
        for i in r["items"]:
            cth.append(CommentThread(i))
        if 'nextPageToken' not in r:
            r['nextPageToken'] = None
        return cth, r["nextPageToken"]

    def video(self, vid):
        """
        Get a YouTube video resource.

        :param vid: Video ID
        :return: list([Video, ...])
        """
        ret = []
        temp = req.get(f"https://www.googleapis.com/youtube/v3/videos"
                       f"?part=snippet,statistics&id={vid}&key={self.key}")
        r = json.loads(temp.content)
        if temp.status_code == 403:
            raise req.exceptions.HTTPError
        elif temp.status_code == 400:
            for i in r["error"]["errors"]:
                if i["reason"] == "keyInvalid":
                    raise InvalidToken(
                        'The token is invalid. Please check and try again.')
        if len(r["items"]) == 0:
            raise VideoNotFoundException(f"Video with ID {vid} not found.")
        for i in r["items"]:
            ret.append(Video(i))
        return ret

# "https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={id}&key={key}"  # video items
# "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet,replies&videoId={id}&key={key}"  # comment snippets
