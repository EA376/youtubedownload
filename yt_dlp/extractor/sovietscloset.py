# coding: utf-8
from __future__ import unicode_literals

import datetime

from ..utils import js_to_json
from .common import InfoExtractor


class SovietsClosetBaseIE(InfoExtractor):
    MEDIADELIVERY_REFERER = {'Referer': 'https://iframe.mediadelivery.net/'}

    def parse_nuxt_jsonp(self, nuxt_jsonp_url, video_id, name):
        NUXT_JSONP_RE = r'__NUXT_JSONP__\(.*?\(function\((?P<arg_keys>.*?)\)\{return\s(?P<js>\{.*?\})\}\((?P<arg_vals>.*?)\)'
        nuxt_jsonp = self._download_webpage(nuxt_jsonp_url, video_id, note=f'Downloading {name} __NUXT_JSONP__')

        js, arg_keys, arg_vals = self._search_regex(NUXT_JSONP_RE, nuxt_jsonp, '__NUXT_JSONP__', group=['js', 'arg_keys', 'arg_vals'])

        arg_keys = arg_keys.split(',')
        arg_vals = arg_vals.split(',')
        args = {key: val for key, val in zip(arg_keys, arg_vals)}

        for key, val in args.items():
            if val in ('undefined', 'void 0'):
                args[key] = 'null'

        return self._parse_json(js_to_json(js, args), video_id)['data'][0]

    def video_meta(self, video_id, stream_date, game_name, category_name, episode_number):
        title = f'SovietWomble {stream_date} - {game_name}'
        if category_name != 'Misc':
            title += f' - {category_name}'
        title += f' #{episode_number}'

        stream_date_parsed = datetime.datetime.strptime(f'{stream_date} GMT', '%Y-%m-%d %H:%M %Z')
        stream_date_yyyymmdd = stream_date_parsed.strftime('%Y%m%d')
        timestamp = int(stream_date_parsed.timestamp())

        return {
            'id': video_id,
            'title': title,
            'http_headers': self.MEDIADELIVERY_REFERER,
            'uploader': 'SovietWomble',
            'creator': 'SovietWomble',
            'release_timestamp': timestamp,
            'release_date': stream_date_yyyymmdd,
            'timestamp': timestamp,
            'upload_date': stream_date_yyyymmdd,
            'uploader_id': 'SovietWomble',
            'uploader_url': 'https://www.twitch.tv/SovietWomble',
            'channel': 'SovietWomble',
            'channel_id': 'SovietWomble',
            'channel_url': 'https://www.twitch.tv/SovietWomble',
            'was_live': True,
            'availability': 'public',
            'series': game_name,
            'season': category_name,
            'episode_number': episode_number,
        }


class SovietsClosetIE(SovietsClosetBaseIE):
    _VALID_URL = r'https?://(?:www\.)?sovietscloset\.com/video/(?P<id>[0-9]+)/?'
    _TESTS = [
        {
            'url': 'https://sovietscloset.com/video/1337',
            'md5': '11e58781c4ca5b283307aa54db5b3f93',
            'info_dict': {
                'id': '1337',
                'ext': 'mp4',
                'title': 'SovietWomble 2017-04-13 13:53 - The Witcher #13',
                'thumbnail': r're:^https?://.*\.b-cdn\.net/2f0cfbf4-3588-43a9-a7d6-7c9ea3755e67/thumbnail\.jpg$',
                'uploader': 'SovietWomble',
                'creator': 'SovietWomble',
                'release_timestamp': 1492084380,
                'release_date': '20170413',
                'timestamp': 1492084380,
                'upload_date': '20170413',
                'uploader_id': 'SovietWomble',
                'uploader_url': 'https://www.twitch.tv/SovietWomble',
                'channel': 'SovietWomble',
                'channel_id': 'SovietWomble',
                'channel_url': 'https://www.twitch.tv/SovietWomble',
                'was_live': True,
                'availability': 'public',
                'series': 'The Witcher',
                'season': 'Misc',
                'episode_number': 13,
            },
        },
        {
            'url': 'https://sovietscloset.com/video/1105',
            'md5': '578b1958a379e7110ba38697042e9efb',
            'info_dict': {
                'id': '1105',
                'ext': 'mp4',
                'title': 'SovietWomble 2016-04-20 13:00 - Arma 3 - Zeus Games #3',
                'uploader': 'SovietWomble',
                'thumbnail': r're:^https?://.*\.b-cdn\.net/c0e5e76f-3a93-40b4-bf01-12343c2eec5d/thumbnail\.jpg$',
                'uploader': 'SovietWomble',
                'creator': 'SovietWomble',
                'release_timestamp': 1461150000,
                'release_date': '20160420',
                'timestamp': 1461150000,
                'upload_date': '20160420',
                'uploader_id': 'SovietWomble',
                'uploader_url': 'https://www.twitch.tv/SovietWomble',
                'channel': 'SovietWomble',
                'channel_id': 'SovietWomble',
                'channel_url': 'https://www.twitch.tv/SovietWomble',
                'was_live': True,
                'availability': 'public',
                'series': 'Arma 3',
                'season': 'Zeus Games',
                'episode_number': 3,
            },
        },
    ]

    def _extract_bunnycdn_iframe(self, video_id, bunnycdn_id):
        iframe = self._download_webpage(
            f'https://iframe.mediadelivery.net/embed/5105/{bunnycdn_id}',
            video_id, note='Downloading BunnyCDN iframe', headers=self.MEDIADELIVERY_REFERER
        )

        m3u8_url = self._search_regex(r'(https?://.*?\.m3u8)', iframe, 'm3u8 url')
        thumbnail_url = self._search_regex(r'(https?://.*?thumbnail\.jpg)', iframe, 'thumbnail url')

        m3u8_formats = self._extract_m3u8_formats(m3u8_url, video_id, headers=self.MEDIADELIVERY_REFERER)
        self._sort_formats(m3u8_formats)

        # TODO duration

        return {
            'url': m3u8_url,
            'formats': m3u8_formats,
            'thumbnail': thumbnail_url,
        }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        static_assets_base = self._search_regex(r'staticAssetsBase:\"(.*?)\"', webpage, 'staticAssetsBase')
        static_assets_base = f'https://sovietscloset.com{static_assets_base}'

        stream = self.parse_nuxt_jsonp(f'{static_assets_base}/video/{video_id}/payload.js', video_id, 'video')['stream']

        return {
            **self.video_meta(video_id, stream['date'], stream['game']['name'], stream['subcategory']['name'], stream['number']),
            **self._extract_bunnycdn_iframe(video_id, stream['bunnyId']),
        }


class SovietsClosetPlaylistIE(SovietsClosetBaseIE):
    _VALID_URL = r'https?://(?:www\.)?sovietscloset\.com/(?!video)(?P<id>.*)'
    _TESTS = [

        {
            'url': 'https://sovietscloset.com/The-Witcher',
            'info_dict': {
                'id': 'The-Witcher',
                'title': 'The Witcher',
            },
            'playlist_mincount': 31,
        },
        {
            'url': 'https://sovietscloset.com/Arma-3/Zeus-Games',
            'info_dict': {
                'id': 'Arma-3/Zeus-Games',
                'title': 'Arma 3 - Zeus Games',
            },
            'playlist_mincount': 3,
        },
        {
            'url': 'https://sovietscloset.com/arma-3/zeus-games/',
            'info_dict': {
                'id': 'arma-3/zeus-games',
                'title': 'Arma 3 - Zeus Games',
            },
            'playlist_mincount': 3,
        },
    ]

    def _real_extract(self, url):
        playlist_id = self._match_id(url)
        if playlist_id.endswith('/'):
            playlist_id = playlist_id[:-1]

        webpage = self._download_webpage(url, playlist_id)

        static_assets_base = self._search_regex(r'staticAssetsBase:\"(.*?)\"', webpage, 'staticAssetsBase')
        static_assets_base = f'https://sovietscloset.com{static_assets_base}'

        sovietscloset = self.parse_nuxt_jsonp(f'{static_assets_base}/payload.js', playlist_id, 'global')['games']

        if '/' in playlist_id:
            game_slug, category_slug = playlist_id.lower().split('/')
        else:
            game_slug = playlist_id.lower()
            category_slug = 'misc'

        entries = list()
        playlist_title = None
        for game in sovietscloset:
            if game['slug'].lower() == game_slug:
                playlist_title = game['name']
                for category in game['subcategories']:
                    if category['slug'].lower() == category_slug:
                        if category_slug != 'misc':
                            playlist_title += ' - ' + category['name']
                        for stream in category['streams']:
                            entries.append({
                                **self.url_result(f'https://sovietscloset.com/video/{stream["id"]}', ie=SovietsClosetIE.ie_key()),
                                **self.video_meta(stream['id'], stream['date'], game['name'], category['name'], len(entries) + 1),
                            })
        return self.playlist_result(entries, playlist_id, playlist_title)
