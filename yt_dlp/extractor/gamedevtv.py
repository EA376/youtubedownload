import json

from .common import InfoExtractor
from ..utils import (
    clean_html,
    int_or_none,
    join_nonempty,
    parse_iso8601,
    str_or_none,
    url_or_none,
)
from ..utils.traversal import traverse_obj


class GameDevTVDashboardIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?gamedev\.tv/dashboard/courses/(?P<id>\d+)'
    _NETRC_MACHINE = 'gamedevtv'
    _API_HEADERS = {}
    _TESTS = [{
        'url': 'https://www.gamedev.tv/dashboard/courses/25',
        'md5': 'ece542a1071018d5a09e0dc91a843763',
        'info_dict': {
            'playlist': 'Complete Blender Creator 3: Learn 3D Modelling for Beginners',
            'playlist_id': 25,
            'chapter_id': '01',
            'chapter': 'Introduction & Setup',
            'id': '01',
            'ext': 'mp4',
            'title': 'Section Intro - Introduction To Blender',
        },
    }]

    def _perform_login(self, username, password):
        response = self._download_json(
            'https://api.gamedev.tv/api/students/login', None, 'Logging in',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                'email': username,
                'password': password,
                'cart_items': [],
            }).encode())
        self._API_HEADERS['Authorization'] = f'{response["token_type"]} {response["access_token"]}'

    def _real_initialize(self):
        if not self._API_HEADERS.get('Authorization'):
            self.raise_login_required(
                'This content is only available with purchase', method='password')

    def _entries(self, data, course_id, course_info):
        for section in traverse_obj(data, ('sections', ..., {dict})):
            section_info = traverse_obj(section, {
                'season_id': ('id', {str_or_none}),
                'season': ('title', {str}),
                'season_number': ('order', {int_or_none}),
            })
            for lecture in traverse_obj(section, ('lectures', lambda _, v: url_or_none(v['video']['playListUrl']))):
                display_id = join_nonempty(course_id, section_info.get('season_id'), lecture.get('id'))
                formats, subtitles = self._extract_m3u8_formats_and_subtitles(
                    lecture['video']['playListUrl'], display_id, 'mp4', m3u8_id='hls')
                yield {
                    **course_info,
                    **section_info,
                    'id': display_id,  # fallback
                    'display_id': display_id,
                    'formats': formats,
                    'subtitles': subtitles,
                    'series': course_info.get('title'),
                    'series_id': course_id,
                    **traverse_obj(lecture, {
                        'id': ('video', 'guid', {str}),
                        'title': ('title', {str}),
                        'alt_title': ('video', 'title', {str}),
                        'description': ('description', {clean_html}),
                        'episode': ('title', {str}),
                        'episode_number': ('order', {int_or_none}),
                        'duration': ('video', 'duration_in_sec', {int_or_none}),
                        'timestamp': ('video', 'created_at', {parse_iso8601}),
                        'modified_timestamp': ('video', 'updated_at', {parse_iso8601}),
                        'thumbnail': ('video', 'thumbnailUrl', {url_or_none}),
                    }),
                }

    def _real_extract(self, url):
        course_id = self._match_id(url)
        data = self._download_json(
            f'https://api.gamedev.tv/api/courses/my/{course_id}', course_id,
            headers=self._API_HEADERS)['data']

        course_info = traverse_obj(data, {
            'title': ('title', {str}),
            'tags': ('tags', ..., 'name', {str}),
            'categories': ('categories', ..., 'title', {str}),
            'timestamp': ('created_at', {parse_iso8601}),
            'modified_timestamp': ('updated_at', {parse_iso8601}),
            'thumbnail': ('image', {url_or_none}),
        })

        return self.playlist_result(self._entries(data, course_id, course_info), course_id, **course_info)
