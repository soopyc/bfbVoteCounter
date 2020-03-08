import dateutil.parser as dp


class InvalidObject(Exception):
    pass


class Comment:
    '''Returns a custom Comment object.

    :param obj: API return object, should match Google's API.
    :return: Comment object
    '''
    def __init__(self, obj):
        p = self._parse(obj)
        self.author = p[0]
        self.text = p[1]
        self.published_at = p[2]

    def __str__(self):
        return f"Comment: {self.text}"

    @staticmethod
    def _parse(o):
        '''
        Internal Parse method

        :param o: object to be parsed.
        :return: Tuple([author, text, datetime(time)])
        '''
        try:
            a = o['snippet']['authorDisplayName']
            t = o['snippet']['textOriginal']
            ti = dp.parse(o['snippet']['publishedAt'])
        except KeyError:
            raise InvalidObject('Invalid object passed into method, check https://developers.google.com/youtube/v3/docs'
                                '/comments#resource for more information.')
        return tuple([a, t, ti])


class CommentThread:
    '''
    CommentThread object

    :param obj: API return object, should match Google's API.
    :return: CommentThread object
    '''
    def __init__(self, obj):
        p = self._parse(obj)

    @staticmethod
    def _parse(o):
        '''
        Internal parse method

        :param o: API return object, should match Google's API.
        :return: Tuple([Comment(comment), reply_count, list([Comment(replies)], ...)])
        '''
        com = Comment(o['snippet']['topLevelComment'])
        rc = o['snippet']['totalReplyCount']
        rs = []
        for i in o['replies']['comments']:
            rs.append(Comment(i))
        return tuple([com, rc, rs])


class Video:
    '''
    Video object

    :param obj: API return object, should match Google's API.
    :return: Video object
    '''
    def __init__(self, obj):
        ct = self._parse(obj)
        self.publish_time = ct[0]
        self.title = ct[1]
        self.description = ct[2]
        self.channel_name = ct[3]
        self.total_views = ct[4]
        self.comments = ct[5]

    def __str__(self):
        return f'{self.title}, {self.comments} total comments.'

    @staticmethod
    def _parse(o):
        '''
        Internal parse method.

        :param o:  object to be parsed.
        :return: Tuple([datetime(published_time), video_title, description, channel_name, views, comments])
        '''
        try:
            pub = dp.parse(o['snippet']['publishedAt'])
            title = o['snippet']['title']
            desc = o['snippet']['description']
            chnl = o['snippet']['channelTitle']
            views = o['statistics']['viewCount']
            coms = o['statistics']['commentCount']
        except KeyError:
            raise InvalidObject('Invalid object passed into method, check https://developers.google.com/youtube/v3/docs'
                                '/videos#resource-representation for more information.')
        return tuple([pub, title, desc, chnl, views, coms])


"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={id}&key={key}"  # video items
"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet,replies&videoId={id}&key={key}"  # comment snippets
