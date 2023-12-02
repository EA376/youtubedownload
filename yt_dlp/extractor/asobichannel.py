import datetime

from .common import InfoExtractor
from ..utils import ExtractorError, clean_html, merge_dicts, parse_iso8601, traverse_obj


class AsobiChannelIE(InfoExtractor):
    _VALID_URL = r'https?://asobichannel\.asobistore\.jp/watch/(?P<id>[a-z0-9-_]+)'
    _TESTS = [{
        'url': 'https://asobichannel.asobistore.jp/watch/1ypp48qd32p',
        'md5': '39df74e872afe032c4eb27b89144fc92',
        'info_dict': {
            'id': '1ypp48qd32p',
            'ext': 'mp4',
            'title': 'アイドルマスター ミリオンライブ！ 765プロch 原っぱ通信 #1',
            'description': 'md5:b930bd2199c9b2fd75951ce4aaa7efd2',
            'thumbnail': 'https://images.microcms-assets.io/assets/d2420de4b9194e11beb164f99edb1f95/a8e6f84119f54eb9ab4ce16729239905/%E3%82%B5%E3%83%A0%E3%83%8D%20(1).png',
            'release_timestamp': 1697098247,
            'release_date': '20231012',
            'modified_timestamp': 1698381162,
            'modified_date': '20231027',
            'channel': 'アイドルマスター',
            'channel_id': 'idolmaster',
        },
    }, {
        'url': 'https://asobichannel.asobistore.jp/watch/redigiwnjzqj',
        'md5': '229fa8fb5c591c75ce8c37a497f113f6',
        'info_dict': {
            'id': 'redigiwnjzqj',
            'ext': 'mp4',
            'title': '【おまけ放送】アイドルマスター ミリオンライブ！ 765プロch 原っぱ通信 #1',
            'description': 'md5:7d9cd35fb54425a6967822bd564ea2d9',
            'thumbnail': 'https://images.microcms-assets.io/assets/d2420de4b9194e11beb164f99edb1f95/20e5c1d6184242eebc2512a5dec59bf0/P1_%E5%8E%9F%E3%81%A3%E3%81%B1%E3%82%B5%E3%83%A0%E3%83%8D.png',
            'modified_timestamp': 1697797125,
            'modified_date': '20231020',
            'release_timestamp': 1697261769,
            'release_date': '20231014',
            'channel': 'アイドルマスター',
            'channel_id': 'idolmaster',
        },
    }]

    def _get_survapi_header(self, video_id):
        request_token = self._download_json(
            'https://asobichannel-api.asobistore.jp/api/v1/vspf/token', video_id,
            note='Retrieving API token')
        return {'Authorization': f'Bearer {request_token}'}

    def _process_vod(self, video_id, metadata):
        content_id = metadata['contents']['video_id']

        vod_data = self._download_json(
            f'https://survapi.channel.or.jp/proxy/v1/contents/{content_id}/get_by_cuid', video_id,
            headers=self._get_survapi_header(video_id), note='Downloading vod data')

        m3u8_url = vod_data['ex_content']['streaming_url']

        return {
            'formats': self._extract_m3u8_formats(m3u8_url, video_id),
        }

    def _process_live(self, video_id, metadata):
        now_ts = datetime.datetime.now().timestamp()

        content_id = metadata['contents']['video_id']

        live_start = traverse_obj(metadata, ('period', 'start', {parse_iso8601}))
        if live_start is None:
            live_status = None
        elif now_ts < live_start:
            live_status = 'is_upcoming'
        else:
            live_status = 'is_live'

        event_data = self._download_json(
            f'https://survapi.channel.or.jp/ex/events/{content_id}?embed=channel', video_id,
            headers=self._get_survapi_header(video_id), note='Downloading event data')

        live_url = event_data['data']['Channel']['Custom_live_url']

        return {
            'live_status': live_status,
            'formats': self._extract_m3u8_formats(live_url, video_id),
        }

    def _real_extract(self, url):
        video_id = self._match_id(url)

        metadata = self._download_json(
            f'https://channel.microcms.io/api/v1/media/{video_id}', video_id,
            headers={'X-MICROCMS-API-KEY': 'qRaKehul9AHU8KtL0dnq1OCLKnFec6yrbcz3'})

        info = {
            'id': video_id,
            **traverse_obj(metadata, {
                'title': 'title',
                'description': ('body', {clean_html}),
                'thumbnail': ('contents', 'video_thumb', 'url'),
                'release_timestamp': ('publishedAt', {parse_iso8601}),
                'modified_timestamp': ('updatedAt', {parse_iso8601}),
                'channel': ('channel', 'name'),
                'channel_id': ('channel', 'id'),
            }),
        }

        video_type = traverse_obj(metadata, ('contents', 'video_type', 0))
        if video_type == 'VOD':
            return merge_dicts(info, self._process_vod(video_id, metadata))
        if video_type == 'LIVE':
            return merge_dicts(info, self._process_live(video_id, metadata))

        raise ExtractorError(f'Unexpected video type {video_type}', expected=False)
