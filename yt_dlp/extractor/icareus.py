# coding: utf-8
from __future__ import unicode_literals

import re

from .common import InfoExtractor
from ..utils import (
    clean_html,
    determine_ext,
    get_element_by_class,
    int_or_none,
    parse_bitrate,
    parse_resolution,
    remove_end,
    traverse_obj,
    urlencode_postdata,
    url_or_none,
)


class IcareusIE(InfoExtractor):
    _DOMAINS = '|'.join(map(re.escape, (
        'asahitv.fi',
        'helsinkikanava.fi',
        'hyvinvointitv.fi',
        'inez.fi',
        'permanto.fi',
        'suite.icareus.com',
        'videos.minifiddlers.org',
    )))
    _VALID_URL = rf'(?P<base_url>https?://(?:www\.)?(?:{_DOMAINS}))/[^?#]+/player/[^?#]+\?(?:[^#]+&)?(?:assetId|eventId)=(?P<id>\d+)'
    _TESTS = [{
        'url': 'https://www.helsinkikanava.fi/fi_FI/web/helsinkikanava/player/vod?assetId=68021894',
        'md5': 'ca0b62ffc814a5411dfa6349cf5adb8a',
        'info_dict': {
            'id': '68021894',
            'ext': 'mp4',
            'title': 'Perheiden parhaaksi',
            'description': 'md5:295785ea408e5ac00708766465cc1325',
            'thumbnail': 'https://www.helsinkikanava.fi/image/image_gallery?img_id=68022501',
            'upload_date': '20200924',
            'timestamp': 1600938300,
        },
    }, {  # Recorded livestream
        'url': 'https://www.helsinkikanava.fi/fi/web/helsinkikanava/player/event/view?eventId=76241489',
        'md5': '014327e69dfa7b949fcc861f6d162d6d',
        'info_dict': {
            'id': '76258304',
            'ext': 'mp4',
            'title': 'Helsingin kaupungin ja HUSin tiedotustilaisuus koronaepidemiatilanteesta 24.11.2020',
            'description': 'md5:3129d041c6fbbcdc7fe68d9a938fef1c',
            'thumbnail': 'https://icareus-suite.secure2.footprint.net/image/image_gallery?img_id=76288630',
            'upload_date': '20201124',
            'timestamp': 1606206600,
        },
    }, {  # Non-m3u8 stream
        'url': 'https://suite.icareus.com/fi/web/westend-indians/player/vod?assetId=47567389',
        'md5': '72fc04ee971bbedc44405cdf16c990b6',
        'info_dict': {
            'id': '47567389',
            'ext': 'mp4',
            'title': 'Omatoiminen harjoittelu - Laukominen',
            'description': '',
            'thumbnail': 'https://suite.icareus.com/image/image_gallery?img_id=47568162',
            'upload_date': '20200319',
            'timestamp': 1584658080,
        },
    }, {
        'url': 'https://asahitv.fi/fi/web/asahi/player/vod?assetId=89415818',
        'only_matching': True
    }, {
        'url': 'https://hyvinvointitv.fi/fi/web/hyvinvointitv/player/vod?assetId=89149730',
        'only_matching': True
    }, {
        'url': 'https://inez.fi/fi/web/inez-media/player/vod?assetId=71328822',
        'only_matching': True
    }, {
        'url': 'https://www.permanto.fi/fi/web/alfatv/player/vod?assetId=135497515',
        'only_matching': True
    }, {
        'url': 'https://videos.minifiddlers.org/web/international-minifiddlers/player/vod?assetId=1982759',
        'only_matching': True
    }]

    def _real_extract(self, url):
        base_url, maybe_id = self._match_valid_url(url).groups()
        page = self._download_webpage(url, maybe_id)
        video_id = self._search_regex(
            r"_icareus\['itemId'\]\s*=\s*'(\d+)'", page, "video_id")
        api_base = self._search_regex(
            r'var\s+publishingServiceURL\s*=\s*"(http[^"]+)";', page, "api_base")
        organization_id = self._search_regex(
            r"_icareus\['organizationId'\]\s*=\s*'(\d+)'", page, "organization_id")
        token = self._search_regex(
            r"_icareus\['token'\]\s*=\s*'([a-f0-9]+)'", page, "token")
        token2 = self._search_regex(
            r"""data\s*:\s*{action:"getAsset".*?token:'([a-f0-9]+)'}""", page,
            "token2", default=None, fatal=False)
        livestream_title = get_element_by_class(
            'unpublished-info-item future-event-title', page)
        metad = self._search_json_ld(page, video_id, default=None)

        duration = None
        thumbnail = None
        if metad:
            title = metad.get('title')
            description = metad.get('description')
            timestamp = metad.get('timestamp')
            thumbnail = traverse_obj(metad, ('thumbnails', 0, 'url'))
        elif token2:
            data = {
                "version": "03",
                "action": "getAsset",
                "organizationId": organization_id,
                "assetId": video_id,
                "languageId": "en_US",
                "userId": "0",
                "token": token2,
            }
            metad = self._download_json(
                base_url + '/icareus-suite-api-portlet/publishing',
                video_id, data=urlencode_postdata(data))
            title = metad.get('name')
            description = metad.get('description')
            timestamp = int_or_none(metad.get('date'), scale=1000)
            duration = int_or_none(metad.get('duration'))
            thumbnail = url_or_none(metad.get('thumbnailMedium'))
        elif livestream_title:  # Recorded livestream
            title = livestream_title
            description = get_element_by_class(
                'unpublished-info-item future-event-description', page)
            timestamp = int_or_none(self._search_regex(
                r"var startEvent\s*=\s*(\d+);", page, "uploadDate",
                fatal=False), scale=1000)
        else:
            self.report_warning("Could not extract metadata", video_id)
            description = None
            timestamp = None

        title = title if title else video_id
        description = clean_html(description)

        data = {
            "version": "03",
            "action": "getAssetPlaybackUrls",
            "organizationId": organization_id,
            "assetId": video_id,
            "token": token,
        }
        jsond = self._download_json(
            api_base, video_id, data=urlencode_postdata(data))

        if thumbnail is None:
            thumbnail = url_or_none(jsond.get('thumbnail'))

        formats = []
        for item in jsond.get('urls') or []:
            video_url = url_or_none(item.get('url'))
            if video_url is None:
                continue
            ext = determine_ext(video_url)
            if ext == 'm3u8':
                formats.extend(self._extract_m3u8_formats(
                    video_url, video_id, 'mp4',
                    entry_protocol='m3u8_native', m3u8_id='hls',
                    fatal=False))
            else:
                fmt = item.get('name')
                fd = {
                    'url': video_url,
                    'format': fmt,
                    'tbr': parse_bitrate(fmt),
                    'format_id': str(item.get('id', '')) or None,
                }
                fd.update(parse_resolution(fmt))
                formats.append(fd)

        formats.extend({
            'format': item.get('name'),
            'format_id': 'audio',
            'vcodec': 'none',
            'url': url_or_none(item.get('url')),
            'tbr': int_or_none(self._search_regex(
                r"\((\d+)\s*k\)", item.get('name', ''), 'audio bitrate',
                default=None)),
        } for item in jsond.get('audio_urls') or []
            if url_or_none(item.get('url')) is not None)

        subtitles = {
            remove_end(sdesc.split(' ')[0], ':'): [{"url": url_or_none(surl)}]
            for scode, sdesc, surl in jsond.get('subtitles') or []
        }

        info = {
            'id': video_id,
            'title': title,
            'description': description,
            'thumbnail': thumbnail,
            'timestamp': timestamp,
            'formats': formats,
            'duration': duration,
            'subtitles': subtitles,
        }

        return info
