# coding: utf-8
from __future__ import unicode_literals

import itertools
import random
import string
import time
import json

from .common import InfoExtractor
from ..utils import (
    ExtractorError,
    int_or_none,
    str_or_none,
    traverse_obj,
    try_get,
    qualities,
)


class TikTokBaseIE(InfoExtractor):
    _APP_VERSION = '20.9.3'
    _MANIFEST_APP_VERSION = '291'
    QUALITIES = ('360p', '540p', '720p')

    def _call_api(self, ep, query, video_id, fatal=True,
                  note='Downloading API JSON', errnote='Unable to download API page'):
        real_query = {
            **query,
            'version_name': self._APP_VERSION,
            'version_code': self._MANIFEST_APP_VERSION,
            'build_number': self._APP_VERSION,
            'manifest_version_code': self._MANIFEST_APP_VERSION,
            'update_version_code': self._MANIFEST_APP_VERSION,
            'openudid': ''.join(random.choice('0123456789abcdef') for i in range(16)),
            # Some endpoints don't like randomized device_id, while some require it.
            # 'device_id': ''.join(random.choice(string.digits) for i in range(19)),
            'uuid': ''.join([random.choice(string.digits) for num in range(16)]),
            '_rticket': int(time.time() * 1000),
            'ts': int(time.time()),
            'device_brand': 'Google',
            'device_type': 'Pixel 4',
            'device_platform': 'android',
            'resolution': '1080*1920',
            'dpi': 420,
            'os_version': '10',
            'os_api': '29',
            'carrier_region': 'US',
            'sys_region': 'US',
            'region': 'US',
            'app_name': 'trill',
            'app_language': 'en',
            'language': 'en',
            'timezone_name': 'America/New_York',
            'timezone_offset': '-14400',
            'channel': 'googleplay',
            'ac': 'wifi',
            'mcc_mnc': '310260',
            'is_my_cn': 0,
            'aid': 1180,
            'ssmix': 'a',
            'as': 'a1qwert123',
            'cp': 'cbfhckdckkde1',
        }
        self._set_cookie('.tiktokv.com', 'odin_tt', ''.join(random.choice('0123456789abcdef') for i in range(160)))
        return self._download_json(
            'https://api-t2.tiktokv.com/aweme/v1/%s/' % ep, video_id=video_id,
            fatal=fatal, note=note, errnote=errnote, headers={
                'User-Agent': f'com.ss.android.ugc.trill/{self._MANIFEST_APP_VERSION} (Linux; U; Android 10; en_US; Pixel 4; Build/QQ3A.200805.001; Cronet/58.0.2991.0)',
                'Accept': 'application/json',
            }, query=real_query)

    def _parse_aweme_video(self, aweme_detail):
        aweme_id = aweme_detail['aweme_id']
        video_info = aweme_detail['video']

        def parse_url_key(url_key):
            format_id, codec, res, bitrate = self._search_regex(
                r'v[^_]+_(?P<id>(?P<codec>[^_]+)_(?P<res>\d+p)_(?P<bitrate>\d+))', url_key,
                'url key', default=(None, None, None, None), group=('id', 'codec', 'res', 'bitrate'))
            if not format_id:
                return {}, None
            return {
                'format_id': format_id,
                'vcodec': 'h265' if codec == 'bytevc1' else codec,
                'tbr': int_or_none(bitrate, scale=1000) or None,
                'quality': qualities(self.QUALITIES)(res),
            }, res

        known_resolutions = {}

        def extract_addr(addr, add_meta={}):
            parsed_meta, res = parse_url_key(addr.get('url_key', ''))
            if res:
                known_resolutions.setdefault(res, {}).setdefault('height', add_meta.get('height'))
                known_resolutions[res].setdefault('width', add_meta.get('width'))
                parsed_meta.update(known_resolutions.get(res, {}))
                add_meta.setdefault('height', int_or_none(res[:-1]))
            return [{
                'url': url,
                'filesize': int_or_none(addr.get('data_size')),
                'ext': 'mp4',
                'acodec': 'aac',
                **add_meta, **parsed_meta
            } for url in addr.get('url_list') or []]

        # Hack: Add direct video links first to prioritize them when removing duplicate formats
        formats = []
        if video_info.get('play_addr'):
            formats.extend(extract_addr(video_info['play_addr'], {
                'format_id': 'play_addr',
                'format_note': 'Direct video',
                'vcodec': 'h265' if traverse_obj(
                    video_info, 'is_bytevc1', 'is_h265') else 'h264',  # Always h264?
                'width': video_info.get('width'),
                'height': video_info.get('height'),
            }))
        if video_info.get('download_addr'):
            formats.extend(extract_addr(video_info['download_addr'], {
                'format_id': 'download_addr',
                'format_note': 'Download video%s' % (', watermarked' if video_info.get('has_watermark') else ''),
                'vcodec': 'h264',
                'width': video_info.get('width'),
                'height': video_info.get('height'),
                'source_preference': -2 if video_info.get('has_watermark') else -1,
            }))
        if video_info.get('play_addr_h264'):
            formats.extend(extract_addr(video_info['play_addr_h264'], {
                'format_id': 'play_addr_h264',
                'format_note': 'Direct video',
                'vcodec': 'h264',
            }))
        if video_info.get('play_addr_bytevc1'):
            formats.extend(extract_addr(video_info['play_addr_bytevc1'], {
                'format_id': 'play_addr_bytevc1',
                'format_note': 'Direct video',
                'vcodec': 'h265',
            }))

        for bitrate in video_info.get('bit_rate', []):
            if bitrate.get('play_addr'):
                formats.extend(extract_addr(bitrate['play_addr'], {
                    'format_id': bitrate.get('gear_name'),
                    'format_note': 'Playback video',
                    'tbr': try_get(bitrate, lambda x: x['bit_rate'] / 1000),
                    'vcodec': 'h265' if traverse_obj(
                        bitrate, 'is_bytevc1', 'is_h265') else 'h264',
                }))

        self._remove_duplicate_formats(formats)
        self._sort_formats(formats, ('quality', 'source', 'codec', 'size', 'br'))

        thumbnails = []
        for cover_id in ('cover', 'ai_dynamic_cover', 'animated_cover', 'ai_dynamic_cover_bak',
                         'origin_cover', 'dynamic_cover'):
            cover = video_info.get(cover_id)
            if cover:
                for cover_url in cover['url_list']:
                    thumbnails.append({
                        'id': cover_id,
                        'url': cover_url,
                    })

        stats_info = aweme_detail.get('statistics', {})
        author_info = aweme_detail.get('author', {})
        music_info = aweme_detail.get('music', {})
        user_id = str_or_none(author_info.get('nickname'))

        contained_music_track = traverse_obj(
            music_info, ('matched_song', 'title'), ('matched_pgc_sound', 'title'), expected_type=str)
        contained_music_author = traverse_obj(
            music_info, ('matched_song', 'author'), ('matched_pgc_sound', 'author'), 'author', expected_type=str)

        is_generic_og_trackname = music_info.get('is_original_sound') and music_info.get('title') == 'original sound - %s' % music_info.get('owner_handle')
        if is_generic_og_trackname:
            music_track, music_author = contained_music_track or 'original sound', contained_music_author
        else:
            music_track, music_author = music_info.get('title'), music_info.get('author')

        return {
            'id': aweme_id,
            'title': aweme_detail['desc'],
            'description': aweme_detail['desc'],
            'view_count': int_or_none(stats_info.get('play_count')),
            'like_count': int_or_none(stats_info.get('digg_count')),
            'repost_count': int_or_none(stats_info.get('share_count')),
            'comment_count': int_or_none(stats_info.get('comment_count')),
            'uploader': str_or_none(author_info.get('unique_id')),
            'creator': user_id,
            'uploader_id': str_or_none(author_info.get('uid')),
            'uploader_url': f'https://www.tiktok.com/@{user_id}' if user_id else None,
            'track': music_track,
            'album': str_or_none(music_info.get('album')) or None,
            'artist': music_author,
            'timestamp': int_or_none(aweme_detail.get('create_time')),
            'formats': formats,
            'thumbnails': thumbnails,
            'duration': int_or_none(traverse_obj(video_info, 'duration', ('download_addr', 'duration')), scale=1000)
        }


class TikTokIE(TikTokBaseIE):
    _VALID_URL = r'https?://www\.tiktok\.com/@[\w\.-]+/video/(?P<id>\d+)'

    _TESTS = [{
        'url': 'https://www.tiktok.com/@leenabhushan/video/6748451240264420610',
        'md5': '34a7543afd5a151b0840ba6736fb633b',
        'info_dict': {
            'id': '6748451240264420610',
            'ext': 'mp4',
            'title': '#jassmanak #lehanga #leenabhushan',
            'description': '#jassmanak #lehanga #leenabhushan',
            'duration': 13,
            'height': 1280,
            'width': 720,
            'uploader': 'leenabhushan',
            'uploader_id': '6691488002098119685',
            'uploader_url': 'https://www.tiktok.com/@leenabhushan',
            'creator': 'facestoriesbyleenabh',
            'thumbnail': r're:^https?://[\w\/\.\-]+(~[\w\-]+\.image)?',
            'upload_date': '20191016',
            'timestamp': 1571246252,
            'view_count': int,
            'like_count': int,
            'repost_count': int,
            'comment_count': int,
        }
    }, {
        'url': 'https://www.tiktok.com/@patroxofficial/video/6742501081818877190?langCountry=en',
        'md5': '06b9800d47d5fe51a19e322dd86e61c9',
        'info_dict': {
            'id': '6742501081818877190',
            'ext': 'mp4',
            'title': 'md5:5e2a23877420bb85ce6521dbee39ba94',
            'description': 'md5:5e2a23877420bb85ce6521dbee39ba94',
            'duration': 27,
            'height': 960,
            'width': 540,
            'uploader': 'patrox',
            'uploader_id': '18702747',
            'uploader_url': 'https://www.tiktok.com/@patrox',
            'creator': 'patroX',
            'thumbnail': r're:^https?://[\w\/\.\-]+(~[\w\-]+\.image)?',
            'upload_date': '20190930',
            'timestamp': 1569860870,
            'view_count': int,
            'like_count': int,
            'repost_count': int,
            'comment_count': int,
        }
    }, {
        # Promoted content/ad
        'url': 'https://www.tiktok.com/@MS4wLjABAAAAAR29F6J2Ktu0Daw03BJyXPNoRQ-W7U5a0Mn3lVCq2rQhjOd_WNLclHUoFgwX8Eno/video/6932675057474981122',
        'only_matching': True,
    }]

    def _extract_aweme(self, props_data, webpage, url):
        video_info = try_get(
            props_data, lambda x: x['pageProps']['itemInfo']['itemStruct'], dict)
        author_info = try_get(
            props_data, lambda x: x['pageProps']['itemInfo']['itemStruct']['author'], dict) or {}
        music_info = try_get(
            props_data, lambda x: x['pageProps']['itemInfo']['itemStruct']['music'], dict) or {}
        stats_info = try_get(props_data, lambda x: x['pageProps']['itemInfo']['itemStruct']['stats'], dict) or {}

        user_id = str_or_none(author_info.get('uniqueId'))
        download_url = try_get(video_info, (lambda x: x['video']['playAddr'],
                                            lambda x: x['video']['downloadAddr']))
        height = try_get(video_info, lambda x: x['video']['height'], int)
        width = try_get(video_info, lambda x: x['video']['width'], int)
        thumbnails = [{
            'url': video_info.get('thumbnail') or self._og_search_thumbnail(webpage),
            'width': width,
            'height': height
        }]
        tracker = try_get(props_data, lambda x: x['initialProps']['$wid'])

        return {
            'id': str_or_none(video_info.get('id')),
            'url': download_url,
            'ext': 'mp4',
            'height': height,
            'width': width,
            'title': video_info.get('desc') or self._og_search_title(webpage),
            'duration': try_get(video_info, lambda x: x['video']['duration'], int),
            'view_count': int_or_none(stats_info.get('playCount')),
            'like_count': int_or_none(stats_info.get('diggCount')),
            'repost_count': int_or_none(stats_info.get('shareCount')),
            'comment_count': int_or_none(stats_info.get('commentCount')),
            'timestamp': try_get(video_info, lambda x: int(x['createTime']), int),
            'creator': str_or_none(author_info.get('nickname')),
            'uploader': user_id,
            'uploader_id': str_or_none(author_info.get('id')),
            'uploader_url': f'https://www.tiktok.com/@{user_id}',
            'track': str_or_none(music_info.get('title')),
            'album': str_or_none(music_info.get('album')) or None,
            'artist': str_or_none(music_info.get('authorName')),
            'thumbnails': thumbnails,
            'description': str_or_none(video_info.get('desc')),
            'webpage_url': self._og_search_url(webpage),
            'http_headers': {
                'Referer': url,
                'Cookie': 'tt_webid=%s; tt_webid_v2=%s' % (tracker, tracker),
            }
        }

    def _extract_aweme_app(self, aweme_id):
        aweme_detail = self._call_api('aweme/detail', {'aweme_id': aweme_id}, aweme_id,
                                      note='Downloading video details', errnote='Unable to download video details')['aweme_detail']
        return self._parse_aweme_video(aweme_detail)

    def _real_extract(self, url):
        video_id = self._match_id(url)

        try:
            return self._extract_aweme_app(video_id)
        except ExtractorError as e:
            self.report_warning(f'{e}; Retrying with webpage')

        # If we only call once, we get a 403 when downlaoding the video.
        self._download_webpage(url, video_id)
        webpage = self._download_webpage(url, video_id, note='Downloading video webpage')
        json_string = self._search_regex(
            r'id=\"__NEXT_DATA__\"\s+type=\"application\/json\"\s*[^>]+>\s*(?P<json_string_ld>[^<]+)',
            webpage, 'json_string', group='json_string_ld')
        json_data = self._parse_json(json_string, video_id)
        props_data = try_get(json_data, lambda x: x['props'], expected_type=dict)

        # Chech statusCode for success
        status = props_data.get('pageProps').get('statusCode')
        if status == 0:
            return self._extract_aweme(props_data, webpage, url)
        elif status == 10216:
            raise ExtractorError('This video is private', expected=True)

        raise ExtractorError('Video not available', video_id=video_id)


class TikTokUserIE(TikTokBaseIE):
    IE_NAME = 'tiktok:user'
    _VALID_URL = r'https?://(?:www\.)?tiktok\.com/@(?P<id>[\w\.-]+)/?(?:$|[#?])'
    _TESTS = [{
        'url': 'https://tiktok.com/@corgibobaa?lang=en',
        'playlist_mincount': 45,
        'info_dict': {
            'id': '6935371178089399301',
        },
    }, {
        'url': 'https://www.tiktok.com/@meme',
        'playlist_mincount': 593,
        'info_dict': {
            'id': '79005827461758976',
        },
    }]

    def _entries(self, webpage, user_id, username):  # TODO: Fix?
        secuid = self._search_regex(r'\"secUid\":\"(?P<secUid>[^\"]+)', webpage, username)
        verifyfp_cookie = self._get_cookies('https://www.tiktok.com').get('s_v_web_id')
        if not verifyfp_cookie:
            raise ExtractorError('Improper cookies (missing s_v_web_id).', expected=True)
        api_url = f'https://m.tiktok.com/api/post/item_list/?aid=1988&cookie_enabled=true&count=30&verifyFp={verifyfp_cookie.value}&secUid={secuid}&cursor='
        cursor = '0'
        for page in itertools.count():
            data_json = self._download_json(api_url + cursor, username, note='Downloading Page %d' % page)
            for video in data_json.get('itemList', []):
                video_id = video['id']
                video_url = f'https://www.tiktok.com/@{user_id}/video/{video_id}'
                yield self._url_result(video_url, 'TikTok', video_id, str_or_none(video.get('desc')))
            if not data_json.get('hasMore'):
                break
            cursor = data_json['cursor']

    def _entries_api(self, webpage, user_id, username):
        query = {
            'user_id': user_id,
            'count': 21,
            # 'cursor': 0,
            'max_cursor': 0,
            'min_cursor': 0,
            'retry_type': 'no_retry',
            'device_id': ''.join(random.choice(string.digits) for i in range(19)),
        }

        max_retries = self.get_param('extractor_retries', 3)
        for page in itertools.count(1):
            for retries in itertools.count():
                try:
                    post_list = self._call_api('aweme/post', query, username,
                                               note='Downloading user video list page %d%s' % (page, f' (attempt {retries})' if retries != 0 else ''),
                                               errnote='Unable to download user video list')
                except ExtractorError as e:
                    if isinstance(e.cause, json.JSONDecodeError) and e.cause.pos == 0 and retries != max_retries:
                        self.report_warning('%s. Retrying...' % str(e.cause or e.msg))
                        continue
                    raise
                break
            for video in post_list.get('aweme_list', []):
                yield {
                    **self._parse_aweme_video(video),
                    'ie_key': TikTokIE.ie_key(),
                    'extractor': 'TikTok',
                }
            if not post_list.get('has_more'):
                break
            query['max_cursor'] = post_list['max_cursor']

    def _real_extract(self, url):
        user_id = self._match_id(url)
        webpage = self._download_webpage(url, user_id, headers={
            'User-Agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'
        })
        own_id = self._html_search_regex(r'snssdk\d*://user/profile/(\d+)', webpage, 'user ID')
        return self.playlist_result(self._entries_api(webpage, own_id, user_id), user_id)
