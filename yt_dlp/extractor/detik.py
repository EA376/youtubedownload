from .common import InfoExtractor
from ..utils import int_or_none, merge_dicts, try_call, url_basename


class DetikEmbedIE(InfoExtractor):
    _VALID_URL = False
    _WEBPAGE_TESTS = [{
        # cnn embed
        'url': 'https://www.cnnindonesia.com/embed/video/846189',
        'info_dict': {
            'id': '846189',
            'ext': 'mp4',
            'description': 'md5:ece7b003b3ee7d81c6a5cfede7d5397d',
            'thumbnail': r're:https?://akcdn\.detik\.net\.id/visual/2022/09/11/thumbnail-video-1_169.jpeg',
            'title': 'Video CNN Indonesia - VIDEO: Momen Charles Disambut Meriah usai Dilantik jadi Raja Inggris',
            'age_limit': 0,
            'tags': ['raja charles', ' raja charles iii', ' ratu elizabeth', ' ratu elizabeth meninggal dunia', ' raja inggris', ' inggris'],
            'subtitle': {},
            'release_timestamp': 1662869995,
            'release_date': '20220911',
        }
    }, {
        # 20.detik
        'url': 'https://20.detik.com/otobuzz/20220704-220704093/mulai-rp-10-jutaan-ini-skema-kredit-mitsubishi-pajero-sport',
        'info_dict': {
            'display_id': 'mulai-rp-10-jutaan-ini-skema-kredit-mitsubishi-pajero-sport',
            'id': '220704093',
            'ext': 'mp4',
            'description': 'md5:9b2257341b6f375cdcf90106146d5ffb',
            'thumbnail': r're:https?://cdnv\.detik\.com/videoservice/AdminTV/2022/07/04/5d6187e402ec4a91877755a5886ff5b6-20220704161859-0s.jpg',
            'title': 'Mulai Rp 10 Jutaan! Ini Skema Kredit Mitsubishi Pajero Sport',
            'timestamp': 1656951521,
            'upload_date': '20220704',
            'duration': 83.0,
            'tags': ['cicilan mobil', 'mitsubishi pajero sport', 'mitsubishi', 'pajero sport'],
            'release_timestamp': 1656926321,
            'release_date': '20220704',
            'age_limit': 0,
            'subtitle': {},
        }
    }, {
        # pasangmata.detik
        'url': 'https://pasangmata.detik.com/contribution/366649',
        'info_dict': {
            'id': '366649',
            'ext': 'mp4',
            'title': 'Saling Dorong Aparat dan Pendemo di Aksi Tolak Kenaikan BBM',
            'description': 'md5:7a6580876c8381c454679e028620bea7',
            'age_limit': 0,
            'tags': 'count:17',
            'subtitle': {},
            'thumbnail': 'https://akcdn.detik.net.id/community/data/media/thumbs-pasangmata/2022/09/08/366649-16626229351533009620.mp4-03.jpg',
        }
    }, {
        # insertlive embed
        'url': 'https://www.insertlive.com/embed/video/290482',
        'info_dict': {
            'id': '290482',
            'ext': 'mp4',
            'release_timestamp': 1663063704,
            'thumbnail': 'https://akcdn.detik.net.id/visual/2022/09/13/leonardo-dicaprio_169.png?w=600&q=90',
            'age_limit': 0,
            'description': 'Aktor Leonardo DiCaprio memang baru saja putus dari kekasihnya yang bernama Camilla Morrone.',
            'release_date': '20220913',
            'title': 'Diincar Leonardo DiCaprio, Gigi Hadid Ngaku Tertarik Tapi Belum Cinta',
            'subtitle': {},
            'tags': ['leonardo dicaprio', ' gigi hadid', ' hollywood'],
        }
    }, {
        # beautynesia embed
        'url': 'https://www.beautynesia.id/embed/video/261636',
        'info_dict': {
            'id': '261636',
            'ext': 'mp4',
            'age_limit': 0,
            'release_timestamp': 1662375600,
            'description': 'Menurut ramalan astrologi, tiga zodiak ini bakal hoki sepanjang September 2022.',
            'title': '3 Zodiak Paling Beruntung Selama September 2022',
            'release_date': '20220905',
            'tags': ['zodiac update', ' zodiak', ' ramalan bintang', ' zodiak beruntung 2022', ' zodiak hoki september 2022', ' zodiak beruntung september 2022'],
            'subtitle': {},
            'thumbnail': 'https://akcdn.detik.net.id/visual/2022/09/05/3-zodiak-paling-beruntung-selama-september-2022_169.jpeg?w=600&q=90',
        }
    }, {
        # cnbcindonesia embed
        'url': 'https://www.cnbcindonesia.com/embed/video/371839',
        'info_dict': {
            'id': '371839',
            'ext': 'mp4',
            'title': 'Puluhan Pejabat Rusia Tuntut Putin Mundur',
            'tags': ['putin'],
            'age_limit': 0,
            'thumbnail': 'https://awsimages.detik.net.id/visual/2022/09/13/cnbc-indonesia-tv-3_169.png?w=600&q=80',
            'subtitle': {},
            'description': 'md5:8b9111e37555fcd95fe549a9b4ae6fdc',
        }
    }]

    def _extract_from_webpage(self, url, webpage):
        display_id = url_basename(url)
        player_type, video_data = self._search_regex(
            r'<script\s*[^>]+src="https?://(aws)?cdn\.detik\.net\.id/(?P<type>flowplayer|detikVideo)[^>]+>\s*(?P<video_data>{[^}]+})',
            webpage, 'playerjs', group=('type', 'video_data'), default=(None, ''))

        json_ld_data = self._search_json_ld(webpage, display_id, default={})
        extra_info_dict = {}

        if not player_type:
            return

        elif player_type == 'flowplayer':
            video_json_data = self._parse_json(video_data.replace('\'', '"'), None)
            video_url = video_json_data['videoUrl']

            extra_info_dict = {
                'id': self._search_regex(r'identifier\s*:\s*\'([^\']+)', webpage, 'identifier'),
                'thumbnail': video_json_data.get('imageUrl'),
            }

        elif player_type == 'detikVideo':
            video_url = self._search_regex(
                r'videoUrl\s*:\s*[\'"]?([^"\']+)', video_data, 'videoUrl')
            extra_info_dict = {
                'id': self._html_search_meta(['video_id', 'dtk:video_id'], webpage),
                'thumbnail': self._search_regex(r'imageUrl\s*:\s*[\'"]?([^"\']+)', video_data, 'videoUrl'),
                'duration': int_or_none(self._html_search_meta('duration', webpage, fatal=False, default=None)),
                'release_timestamp': int_or_none(self._html_search_meta('dtk:publishdateunix', webpage, fatal=False, default=None), 1000),
                'timestamp': int_or_none(self._html_search_meta('dtk:createdateunix', webpage, fatal=False, default=None), 1000),
            }

        formats, subtitles = self._extract_m3u8_formats_and_subtitles(video_url, display_id)
        self._sort_formats(formats)

        yield merge_dicts(json_ld_data, extra_info_dict, {
            'display_id': display_id,
            'title': self._html_search_meta(['og:title', 'originalTitle'], webpage),
            'description': self._html_search_meta(['og:description', 'twitter:description', 'description'], webpage),
            'formats': formats,
            'subtitle': subtitles,
            'tags': try_call(lambda: self._html_search_meta(
                ['keywords', 'keyword', 'dtk:keywords'], webpage).split(',')),
        })
