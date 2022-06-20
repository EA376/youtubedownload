import contextlib
import os

from ..utils import load_plugins

_LAZY_LOADER = False
if not os.environ.get('YTDLP_NO_LAZY_EXTRACTORS'):
    with contextlib.suppress(ImportError):
        from .lazy_extractors import *  # noqa: F403
        from .lazy_extractors import _ALL_CLASSES
        _LAZY_LOADER = True

if not _LAZY_LOADER:
    from ._extractors import *  # noqa: F403
    _ALL_CLASSES = [  # noqa: F811
        klass
        for name, klass in globals().items()
        if name.endswith('IE') and name != 'GenericIE'
    ]
    _ALL_CLASSES.append(GenericIE)  # noqa: F405

from .itv import (
    ITVIE,
    ITVBTCCIE,
)
from .ivi import (
    IviIE,
    IviCompilationIE
)
from .ivideon import IvideonIE
from .iwara import (
    IwaraIE,
    IwaraPlaylistIE,
    IwaraUserIE,
)
from .izlesene import IzleseneIE
from .jable import (
    JableIE,
    JablePlaylistIE,
)
from .jamendo import (
    JamendoIE,
    JamendoAlbumIE,
)
from .jeuxvideo import JeuxVideoIE
from .jove import JoveIE
from .joj import JojIE
from .jwplatform import JWPlatformIE
from .kakao import KakaoIE
from .kaltura import KalturaIE
from .karaoketv import KaraoketvIE
from .karrierevideos import KarriereVideosIE
from .keezmovies import KeezMoviesIE
from .kelbyone import KelbyOneIE
from .ketnet import KetnetIE
from .khanacademy import (
    KhanAcademyIE,
    KhanAcademyUnitIE,
)
from .kickstarter import KickStarterIE
from .kinja import KinjaEmbedIE
from .kinopoisk import KinoPoiskIE
from .konserthusetplay import KonserthusetPlayIE
from .koo import KooIE
from .krasview import KrasViewIE
from .ku6 import Ku6IE
from .kusi import KUSIIE
from .kuwo import (
    KuwoIE,
    KuwoAlbumIE,
    KuwoChartIE,
    KuwoSingerIE,
    KuwoCategoryIE,
    KuwoMvIE,
)
from .la7 import (
    LA7IE,
    LA7PodcastEpisodeIE,
    LA7PodcastIE,
)
from .laola1tv import (
    Laola1TvEmbedIE,
    Laola1TvIE,
    EHFTVIE,
    ITTFIE,
)
from .lastfm import (
    LastFMIE,
    LastFMPlaylistIE,
    LastFMUserIE,
)
from .lbry import (
    LBRYIE,
    LBRYChannelIE,
)
from .lci import LCIIE
from .lcp import (
    LcpPlayIE,
    LcpIE,
)
from .lecture2go import Lecture2GoIE
from .lecturio import (
    LecturioIE,
    LecturioCourseIE,
    LecturioDeCourseIE,
)
from .leeco import (
    LeIE,
    LePlaylistIE,
    LetvCloudIE,
)
from .lego import LEGOIE
from .lemonde import LemondeIE
from .lenta import LentaIE
from .libraryofcongress import LibraryOfCongressIE
from .libsyn import LibsynIE
from .lifenews import (
    LifeNewsIE,
    LifeEmbedIE,
)
from .likee import (
    LikeeIE,
    LikeeUserIE
)
from .limelight import (
    LimelightMediaIE,
    LimelightChannelIE,
    LimelightChannelListIE,
)
from .line import (
    LineLiveIE,
    LineLiveChannelIE,
)
from .linkedin import (
    LinkedInIE,
    LinkedInLearningIE,
    LinkedInLearningCourseIE,
)
from .linuxacademy import LinuxAcademyIE
from .litv import LiTVIE
from .livejournal import LiveJournalIE
from .livestream import (
    LivestreamIE,
    LivestreamOriginalIE,
    LivestreamShortenerIE,
)
from .lnkgo import (
    LnkGoIE,
    LnkIE,
)
from .localnews8 import LocalNews8IE
from .lovehomeporn import LoveHomePornIE
from .lrt import (
    LRTVODIE,
    LRTStreamIE
)
from .lynda import (
    LyndaIE,
    LyndaCourseIE
)
from .m6 import M6IE
from .magentamusik360 import MagentaMusik360IE
from .mailru import (
    MailRuIE,
    MailRuMusicIE,
    MailRuMusicSearchIE,
)
from .mainstreaming import MainStreamingIE
from .malltv import MallTVIE
from .mangomolo import (
    MangomoloVideoIE,
    MangomoloLiveIE,
)
from .manoto import (
    ManotoTVIE,
    ManotoTVShowIE,
    ManotoTVLiveIE,
)
from .manyvids import ManyVidsIE
from .maoritv import MaoriTVIE
from .markiza import (
    MarkizaIE,
    MarkizaPageIE,
)
from .massengeschmacktv import MassengeschmackTVIE
from .masters import MastersIE
from .matchtv import MatchTVIE
from .mdr import MDRIE
from .medaltv import MedalTVIE
from .mediaite import MediaiteIE
from .mediaklikk import MediaKlikkIE
from .mediaset import (
    MediasetIE,
    MediasetShowIE,
)
from .mediasite import (
    MediasiteIE,
    MediasiteCatalogIE,
    MediasiteNamedCatalogIE,
)
from .medici import MediciIE
from .megaphone import MegaphoneIE
from .meipai import MeipaiIE
from .melonvod import MelonVODIE
from .meta import METAIE
from .metacafe import MetacafeIE
from .metacritic import MetacriticIE
from .mgoon import MgoonIE
from .mgtv import MGTVIE
from .miaopai import MiaoPaiIE
from .microsoftstream import MicrosoftStreamIE
from .microsoftvirtualacademy import (
    MicrosoftVirtualAcademyIE,
    MicrosoftVirtualAcademyCourseIE,
)
from .mildom import (
    MildomIE,
    MildomVodIE,
    MildomClipIE,
    MildomUserVodIE,
)
from .minds import (
    MindsIE,
    MindsChannelIE,
    MindsGroupIE,
)
from .ministrygrid import MinistryGridIE
from .minoto import MinotoIE
from .miomio import MioMioIE
from .mirrativ import (
    MirrativIE,
    MirrativUserIE,
)
from .mit import TechTVMITIE, OCWMITIE
from .mitele import MiTeleIE
from .mixch import (
    MixchIE,
    MixchArchiveIE,
)
from .mixcloud import (
    MixcloudIE,
    MixcloudUserIE,
    MixcloudPlaylistIE,
)
from .mlb import (
    MLBIE,
    MLBVideoIE,
)
from .mlssoccer import MLSSoccerIE
from .mnet import MnetIE
from .moevideo import MoeVideoIE
from .mofosex import (
    MofosexIE,
    MofosexEmbedIE,
)
from .mojvideo import MojvideoIE
from .morningstar import MorningstarIE
from .motherless import (
    MotherlessIE,
    MotherlessGroupIE
)
from .motorsport import MotorsportIE
from .movieclips import MovieClipsIE
from .moviepilot import MoviepilotIE
from .moviezine import MoviezineIE
from .movingimage import MovingImageIE
from .msn import MSNIE
from .mtv import (
    MTVIE,
    MTVVideoIE,
    MTVServicesEmbeddedIE,
    MTVDEIE,
    MTVJapanIE,
    MTVItaliaIE,
    MTVItaliaProgrammaIE,
)
from .muenchentv import MuenchenTVIE
from .murrtube import MurrtubeIE, MurrtubeUserIE
from .musescore import MuseScoreIE
from .musicdex import (
    MusicdexSongIE,
    MusicdexAlbumIE,
    MusicdexArtistIE,
    MusicdexPlaylistIE,
)
from .mwave import MwaveIE, MwaveMeetGreetIE
from .mxplayer import (
    MxplayerIE,
    MxplayerShowIE,
)
from .mychannels import MyChannelsIE
from .myspace import MySpaceIE, MySpaceAlbumIE
from .myspass import MySpassIE
from .myvi import (
    MyviIE,
    MyviEmbedIE,
)
from .myvideoge import MyVideoGeIE
from .myvidster import MyVidsterIE
from .n1 import (
    N1InfoAssetIE,
    N1InfoIIE,
)
from .nate import (
    NateIE,
    NateProgramIE,
)
from .nationalgeographic import (
    NationalGeographicVideoIE,
    NationalGeographicTVIE,
)
from .naver import (
    NaverIE,
    NaverLiveIE,
)
from .nba import (
    NBAWatchEmbedIE,
    NBAWatchIE,
    NBAWatchCollectionIE,
    NBAEmbedIE,
    NBAIE,
    NBAChannelIE,
)
from .nbc import (
    NBCIE,
    NBCNewsIE,
    NBCOlympicsIE,
    NBCOlympicsStreamIE,
    NBCSportsIE,
    NBCSportsStreamIE,
    NBCSportsVPlayerIE,
)
from .ndr import (
    NDRIE,
    NJoyIE,
    NDREmbedBaseIE,
    NDREmbedIE,
    NJoyEmbedIE,
)
from .ndtv import NDTVIE
from .nebula import (
    NebulaIE,
    NebulaSubscriptionsIE,
    NebulaChannelIE,
)
from .nerdcubed import NerdCubedFeedIE
from .netzkino import NetzkinoIE
from .neteasemusic import (
    NetEaseMusicIE,
    NetEaseMusicAlbumIE,
    NetEaseMusicSingerIE,
    NetEaseMusicListIE,
    NetEaseMusicMvIE,
    NetEaseMusicProgramIE,
    NetEaseMusicDjRadioIE,
)
from .newgrounds import (
    NewgroundsIE,
    NewgroundsPlaylistIE,
    NewgroundsUserIE,
)
from .newstube import NewstubeIE
from .newsy import NewsyIE
from .nextmedia import (
    NextMediaIE,
    NextMediaActionNewsIE,
    AppleDailyIE,
    NextTVIE,
)
from .nexx import (
    NexxIE,
    NexxEmbedIE,
)
from .nfb import NFBIE
from .nfhsnetwork import NFHSNetworkIE
from .nfl import (
    NFLIE,
    NFLArticleIE,
)
from .nhk import (
    NhkVodIE,
    NhkVodProgramIE,
    NhkForSchoolBangumiIE,
    NhkForSchoolSubjectIE,
    NhkForSchoolProgramListIE,
)
from .nhl import NHLIE
from .nick import (
    NickIE,
    NickBrIE,
    NickDeIE,
    NickNightIE,
    NickRuIE,
)
from .niconico import (
    NiconicoIE,
    NiconicoPlaylistIE,
    NiconicoUserIE,
    NiconicoSeriesIE,
    NiconicoHistoryIE,
    NicovideoSearchDateIE,
    NicovideoSearchIE,
    NicovideoSearchURLIE,
    NicovideoTagURLIE,
)
from .ninecninemedia import (
    NineCNineMediaIE,
    CPTwentyFourIE,
)
from .ninegag import NineGagIE
from .ninenow import NineNowIE
from .nintendo import NintendoIE
from .nitter import NitterIE
from .njpwworld import NJPWWorldIE
from .nobelprize import NobelPrizeIE
from .nonktube import NonkTubeIE
from .noodlemagazine import NoodleMagazineIE
from .noovo import NoovoIE
from .normalboots import NormalbootsIE
from .nosvideo import NosVideoIE
from .nova import (
    NovaEmbedIE,
    NovaIE,
)
from .novaplay import NovaPlayIE
from .nowness import (
    NownessIE,
    NownessPlaylistIE,
    NownessSeriesIE,
)
from .noz import NozIE
from .npo import (
    AndereTijdenIE,
    NPOIE,
    NPOLiveIE,
    NPORadioIE,
    NPORadioFragmentIE,
    SchoolTVIE,
    HetKlokhuisIE,
    VPROIE,
    WNLIE,
)
from .npr import NprIE
from .nrk import (
    NRKIE,
    NRKPlaylistIE,
    NRKSkoleIE,
    NRKTVIE,
    NRKTVDirekteIE,
    NRKRadioPodkastIE,
    NRKTVEpisodeIE,
    NRKTVEpisodesIE,
    NRKTVSeasonIE,
    NRKTVSeriesIE,
)
from .nrl import NRLTVIE
from .ntvcojp import NTVCoJpCUIE
from .ntvde import NTVDeIE
from .ntvru import NTVRuIE
from .nytimes import (
    NYTimesIE,
    NYTimesArticleIE,
    NYTimesCookingIE,
)
from .nuvid import NuvidIE
from .nzherald import NZHeraldIE
from .nzz import NZZIE
from .odatv import OdaTVIE
from .odnoklassniki import OdnoklassnikiIE
from .oktoberfesttv import OktoberfestTVIE
from .olympics import OlympicsReplayIE
from .on24 import On24IE
from .ondemandkorea import OnDemandKoreaIE
from .onefootball import OneFootballIE
from .onet import (
    OnetIE,
    OnetChannelIE,
    OnetMVPIE,
    OnetPlIE,
)
from .onionstudios import OnionStudiosIE
from .ooyala import (
    OoyalaIE,
    OoyalaExternalIE,
)
from .opencast import (
    OpencastIE,
    OpencastPlaylistIE,
)
from .openrec import (
    OpenRecIE,
    OpenRecCaptureIE,
    OpenRecMovieIE,
)
from .ora import OraTVIE
from .orf import (
    ORFTVthekIE,
    ORFFM4IE,
    ORFFM4StoryIE,
    ORFOE1IE,
    ORFOE3IE,
    ORFNOEIE,
    ORFWIEIE,
    ORFBGLIE,
    ORFOOEIE,
    ORFSTMIE,
    ORFKTNIE,
    ORFSBGIE,
    ORFTIRIE,
    ORFVBGIE,
    ORFIPTVIE,
)
from .outsidetv import OutsideTVIE
from .packtpub import (
    PacktPubIE,
    PacktPubCourseIE,
)
from .palcomp3 import (
    PalcoMP3IE,
    PalcoMP3ArtistIE,
    PalcoMP3VideoIE,
)
from .pandoratv import PandoraTVIE
from .panopto import (
    PanoptoIE,
    PanoptoListIE,
    PanoptoPlaylistIE
)
from .paramountplus import (
    ParamountPlusIE,
    ParamountPlusSeriesIE,
)
from .parliamentliveuk import ParliamentLiveUKIE
from .parlview import ParlviewIE
from .patreon import (
    PatreonIE,
    PatreonUserIE
)
from .pbs import PBSIE
from .pearvideo import PearVideoIE
from .peekvids import PeekVidsIE, PlayVidsIE
from .peertube import (
    PeerTubeIE,
    PeerTubePlaylistIE,
)
from .peertv import PeerTVIE
from .peloton import (
    PelotonIE,
    PelotonLiveIE
)
from .people import PeopleIE
from .performgroup import PerformGroupIE
from .periscope import (
    PeriscopeIE,
    PeriscopeUserIE,
)
from .philharmoniedeparis import PhilharmonieDeParisIE
from .phoenix import PhoenixIE
from .photobucket import PhotobucketIE
from .piapro import PiaproIE
from .picarto import (
    PicartoIE,
    PicartoVodIE,
)
from .piksel import PikselIE
from .pinkbike import PinkbikeIE
from .pinterest import (
    PinterestIE,
    PinterestCollectionIE,
)
from .pixivsketch import (
    PixivSketchIE,
    PixivSketchUserIE,
)
from .pladform import PladformIE
from .planetmarathi import PlanetMarathiIE
from .platzi import (
    PlatziIE,
    PlatziCourseIE,
)
from .playfm import PlayFMIE
from .playplustv import PlayPlusTVIE
from .plays import PlaysTVIE
from .playstuff import PlayStuffIE
from .playsuisse import PlaySuisseIE
from .playtvak import PlaytvakIE
from .playvid import PlayvidIE
from .playwire import PlaywireIE
from .plutotv import PlutoTVIE
from .pluralsight import (
    PluralsightIE,
    PluralsightCourseIE,
)
from .podchaser import PodchaserIE
from .podomatic import PodomaticIE
from .pokemon import (
    PokemonIE,
    PokemonWatchIE,
)
from .pokergo import (
    PokerGoIE,
    PokerGoCollectionIE,
)
from .polsatgo import PolsatGoIE
from .polskieradio import (
    PolskieRadioIE,
    PolskieRadioCategoryIE,
    PolskieRadioPlayerIE,
    PolskieRadioPodcastIE,
    PolskieRadioPodcastListIE,
    PolskieRadioRadioKierowcowIE,
)
from .popcorntimes import PopcorntimesIE
from .popcorntv import PopcornTVIE
from .porn91 import Porn91IE
from .porncom import PornComIE
from .pornflip import PornFlipIE
from .pornhd import PornHdIE
from .pornhub import (
    PornHubIE,
    PornHubUserIE,
    PornHubPlaylistIE,
    PornHubPagedVideoListIE,
    PornHubUserVideosUploadIE,
)
from .pornotube import PornotubeIE
from .pornovoisines import PornoVoisinesIE
from .pornoxo import PornoXOIE
from .pornez import PornezIE
from .puhutv import (
    PuhuTVIE,
    PuhuTVSerieIE,
)
from .presstv import PressTVIE
from .projectveritas import ProjectVeritasIE
from .prosiebensat1 import ProSiebenSat1IE
from .prx import (
    PRXStoryIE,
    PRXSeriesIE,
    PRXAccountIE,
    PRXStoriesSearchIE,
    PRXSeriesSearchIE
)
from .puls4 import Puls4IE
from .pyvideo import PyvideoIE
from .qqmusic import (
    QQMusicIE,
    QQMusicSingerIE,
    QQMusicAlbumIE,
    QQMusicToplistIE,
    QQMusicPlaylistIE,
)
from .r7 import (
    R7IE,
    R7ArticleIE,
)
from .radiko import RadikoIE, RadikoRadioIE
from .radiocanada import (
    RadioCanadaIE,
    RadioCanadaAudioVideoIE,
)
from .radiode import RadioDeIE
from .radiojavan import RadioJavanIE
from .radiobremen import RadioBremenIE
from .radiofrance import RadioFranceIE
from .radiozet import RadioZetPodcastIE
from .radiokapital import (
    RadioKapitalIE,
    RadioKapitalShowIE,
)
from .radlive import (
    RadLiveIE,
    RadLiveChannelIE,
    RadLiveSeasonIE,
)
from .rai import (
    RaiPlayIE,
    RaiPlayLiveIE,
    RaiPlayPlaylistIE,
    RaiPlaySoundIE,
    RaiPlaySoundLiveIE,
    RaiPlaySoundPlaylistIE,
    RaiIE,
)
from .raywenderlich import (
    RayWenderlichIE,
    RayWenderlichCourseIE,
)
from .rbmaradio import RBMARadioIE
from .rcs import (
    RCSIE,
    RCSEmbedsIE,
    RCSVariousIE,
)
from .rcti import (
    RCTIPlusIE,
    RCTIPlusSeriesIE,
    RCTIPlusTVIE,
)
from .rds import RDSIE
from .redbulltv import (
    RedBullTVIE,
    RedBullEmbedIE,
    RedBullTVRrnContentIE,
    RedBullIE,
)
from .reddit import RedditIE
from .redgifs import (
    RedGifsIE,
    RedGifsSearchIE,
    RedGifsUserIE,
)
from .redtube import RedTubeIE
from .regiotv import RegioTVIE
from .rentv import (
    RENTVIE,
    RENTVArticleIE,
)
from .restudy import RestudyIE
from .reuters import ReutersIE
from .reverbnation import ReverbNationIE
from .rice import RICEIE
from .rmcdecouverte import RMCDecouverteIE
from .rockstargames import RockstarGamesIE
from .rokfin import (
    RokfinIE,
    RokfinStackIE,
    RokfinChannelIE,
    RokfinSearchIE,
)
from .roosterteeth import RoosterTeethIE, RoosterTeethSeriesIE
from .rottentomatoes import RottenTomatoesIE
from .rozhlas import RozhlasIE
from .rtbf import RTBFIE
from .rte import RteIE, RteRadioIE
from .rtlnl import RtlNlIE
from .rtl2 import (
    RTL2IE,
    RTL2YouIE,
    RTL2YouSeriesIE,
)
from .rtnews import (
    RTNewsIE,
    RTDocumentryIE,
    RTDocumentryPlaylistIE,
    RuptlyIE,
)
from .rtp import RTPIE
from .rtrfm import RTRFMIE
from .rts import RTSIE
from .rtve import (
    RTVEALaCartaIE,
    RTVEAudioIE,
    RTVELiveIE,
    RTVEInfantilIE,
    RTVETelevisionIE,
)
from .rtvnh import RTVNHIE
from .rtvs import RTVSIE
from .ruhd import RUHDIE
from .rule34video import Rule34VideoIE
from .rumble import (
    RumbleEmbedIE,
    RumbleChannelIE,
)
from .rutube import (
    RutubeIE,
    RutubeChannelIE,
    RutubeEmbedIE,
    RutubeMovieIE,
    RutubePersonIE,
    RutubePlaylistIE,
    RutubeTagsIE,
)
from .glomex import (
    GlomexIE,
    GlomexEmbedIE,
)
from .megatvcom import (
    MegaTVComIE,
    MegaTVComEmbedIE,
)
from .ant1newsgr import (
    Ant1NewsGrWatchIE,
    Ant1NewsGrArticleIE,
    Ant1NewsGrEmbedIE,
)
from .rutv import RUTVIE
from .ruutu import RuutuIE
from .ruv import (
    RuvIE,
    RuvSpilaIE
)
from .safari import (
    SafariIE,
    SafariApiIE,
    SafariCourseIE,
)
from .saitosan import SaitosanIE
from .samplefocus import SampleFocusIE
from .sapo import SapoIE
from .savefrom import SaveFromIE
from .sbs import SBSIE
from .screencast import ScreencastIE
from .screencastomatic import ScreencastOMaticIE
from .scrippsnetworks import (
    ScrippsNetworksWatchIE,
    ScrippsNetworksIE,
)
from .scrolller import ScrolllerIE
from .scte import (
    SCTEIE,
    SCTECourseIE,
)
from .seeker import SeekerIE
from .senategov import SenateISVPIE, SenateGovIE
from .sendtonews import SendtoNewsIE
from .servus import ServusIE
from .sevenplus import SevenPlusIE
from .sexu import SexuIE
from .seznamzpravy import (
    SeznamZpravyIE,
    SeznamZpravyArticleIE,
)
from .shahid import (
    ShahidIE,
    ShahidShowIE,
)
from .shared import (
    SharedIE,
    VivoIE,
)
from .shemaroome import ShemarooMeIE
from .showroomlive import ShowRoomLiveIE
from .simplecast import (
    SimplecastIE,
    SimplecastEpisodeIE,
    SimplecastPodcastIE,
)
from .sina import SinaIE
from .sixplay import SixPlayIE
from .skeb import SkebIE
from .skyit import (
    SkyItPlayerIE,
    SkyItVideoIE,
    SkyItVideoLiveIE,
    SkyItIE,
    SkyItAcademyIE,
    SkyItArteIE,
    CieloTVItIE,
    TV8ItIE,
)
from .skylinewebcams import SkylineWebcamsIE
from .skynewsarabia import (
    SkyNewsArabiaIE,
    SkyNewsArabiaArticleIE,
)
from .skynewsau import SkyNewsAUIE
from .sky import (
    SkyNewsIE,
    SkyNewsStoryIE,
    SkySportsIE,
    SkySportsNewsIE,
)
from .slideshare import SlideshareIE
from .slideslive import SlidesLiveIE
from .slutload import SlutloadIE
from .snotr import SnotrIE
from .sohu import SohuIE
from .sonyliv import (
    SonyLIVIE,
    SonyLIVSeriesIE,
)
from .soundcloud import (
    SoundcloudEmbedIE,
    SoundcloudIE,
    SoundcloudSetIE,
    SoundcloudRelatedIE,
    SoundcloudUserIE,
    SoundcloudTrackStationIE,
    SoundcloudPlaylistIE,
    SoundcloudSearchIE,
)
from .soundgasm import (
    SoundgasmIE,
    SoundgasmProfileIE
)
from .southpark import (
    SouthParkIE,
    SouthParkDeIE,
    SouthParkDkIE,
    SouthParkEsIE,
    SouthParkNlIE
)
from .sovietscloset import (
    SovietsClosetIE,
    SovietsClosetPlaylistIE
)
from .spankbang import (
    SpankBangIE,
    SpankBangPlaylistIE,
)
from .spankwire import SpankwireIE
from .spiegel import SpiegelIE
from .spike import (
    BellatorIE,
    ParamountNetworkIE,
)
from .stitcher import (
    StitcherIE,
    StitcherShowIE,
)
from .sport5 import Sport5IE
from .sportbox import SportBoxIE
from .sportdeutschland import SportDeutschlandIE
from .spotify import (
    SpotifyIE,
    SpotifyShowIE,
)
from .spreaker import (
    SpreakerIE,
    SpreakerPageIE,
    SpreakerShowIE,
    SpreakerShowPageIE,
)
from .springboardplatform import SpringboardPlatformIE
from .sprout import SproutIE
from .srgssr import (
    SRGSSRIE,
    SRGSSRPlayIE,
)
from .srmediathek import SRMediathekIE
from .stanfordoc import StanfordOpenClassroomIE
from .startv import StarTVIE
from .steam import SteamIE
from .storyfire import (
    StoryFireIE,
    StoryFireUserIE,
    StoryFireSeriesIE,
)
from .streamable import StreamableIE
from .streamanity import StreamanityIE
from .streamcloud import StreamcloudIE
from .streamcz import StreamCZIE
from .streamff import StreamFFIE
from .streetvoice import StreetVoiceIE
from .stretchinternet import StretchInternetIE
from .stripchat import StripchatIE
from .stv import STVPlayerIE
from .sunporno import SunPornoIE
from .sverigesradio import (
    SverigesRadioEpisodeIE,
    SverigesRadioPublicationIE,
)
from .svt import (
    SVTIE,
    SVTPageIE,
    SVTPlayIE,
    SVTSeriesIE,
)
from .swrmediathek import SWRMediathekIE
from .syfy import SyfyIE
from .sztvhu import SztvHuIE
from .tagesschau import TagesschauIE
from .tass import TassIE
from .tbs import TBSIE
from .tdslifeway import TDSLifewayIE
from .teachable import (
    TeachableIE,
    TeachableCourseIE,
)
from .teachertube import (
    TeacherTubeIE,
    TeacherTubeUserIE,
)
from .teachingchannel import TeachingChannelIE
from .teamcoco import TeamcocoIE
from .teamtreehouse import TeamTreeHouseIE
from .techtalks import TechTalksIE
from .ted import (
    TedEmbedIE,
    TedPlaylistIE,
    TedSeriesIE,
    TedTalkIE,
)
from .tele5 import Tele5IE
from .tele13 import Tele13IE
from .telebruxelles import TeleBruxellesIE
from .telecinco import TelecincoIE
from .telegraaf import TelegraafIE
from .telegram import TelegramEmbedIE
from .telemb import TeleMBIE
from .telemundo import TelemundoIE
from .telequebec import (
    TeleQuebecIE,
    TeleQuebecSquatIE,
    TeleQuebecEmissionIE,
    TeleQuebecLiveIE,
    TeleQuebecVideoIE,
)
from .teletask import TeleTaskIE
from .telewebion import TelewebionIE
from .tennistv import TennisTVIE
from .tenplay import TenPlayIE
from .testurl import TestURLIE
from .tf1 import TF1IE
from .tfo import TFOIE
from .theintercept import TheInterceptIE
from .theplatform import (
    ThePlatformIE,
    ThePlatformFeedIE,
)
from .thestar import TheStarIE
from .thesun import TheSunIE
from .theta import (
    ThetaVideoIE,
    ThetaStreamIE,
)
from .theweatherchannel import TheWeatherChannelIE
from .thisamericanlife import ThisAmericanLifeIE
from .thisav import ThisAVIE
from .thisoldhouse import ThisOldHouseIE
from .threespeak import (
    ThreeSpeakIE,
    ThreeSpeakUserIE,
)
from .threeqsdn import ThreeQSDNIE
from .tiktok import (
    TikTokIE,
    TikTokUserIE,
    TikTokSoundIE,
    TikTokEffectIE,
    TikTokTagIE,
    TikTokVMIE,
    DouyinIE,
)
from .tinypic import TinyPicIE
from .tmz import TMZIE
from .tnaflix import (
    TNAFlixNetworkEmbedIE,
    TNAFlixIE,
    EMPFlixIE,
    MovieFapIE,
)
from .toggle import (
    ToggleIE,
    MeWatchIE,
)
from .toggo import (
    ToggoIE,
)
from .tokentube import (
    TokentubeIE,
    TokentubeChannelIE
)
from .tonline import TOnlineIE
from .toongoggles import ToonGogglesIE
from .toutv import TouTvIE
from .toypics import ToypicsUserIE, ToypicsIE
from .traileraddict import TrailerAddictIE
from .trilulilu import TriluliluIE
from .trovo import (
    TrovoIE,
    TrovoVodIE,
    TrovoChannelVodIE,
    TrovoChannelClipIE,
)
from .trueid import TrueIDIE
from .trunews import TruNewsIE
from .trutv import TruTVIE
from .tube8 import Tube8IE
from .tubitv import (
    TubiTvIE,
    TubiTvShowIE,
)
from .tumblr import TumblrIE
from .tunein import (
    TuneInClipIE,
    TuneInStationIE,
    TuneInProgramIE,
    TuneInTopicIE,
    TuneInShortenerIE,
)
from .tunepk import TunePkIE
from .turbo import TurboIE
from .tv2 import (
    TV2IE,
    TV2ArticleIE,
    KatsomoIE,
    MTVUutisetArticleIE,
)
from .tv2dk import (
    TV2DKIE,
    TV2DKBornholmPlayIE,
)
from .tv2hu import (
    TV2HuIE,
    TV2HuSeriesIE,
)
from .tv4 import TV4IE
from .tv5mondeplus import TV5MondePlusIE
from .tv5unis import (
    TV5UnisVideoIE,
    TV5UnisIE,
)
from .tva import (
    TVAIE,
    QubIE,
)
from .tvanouvelles import (
    TVANouvellesIE,
    TVANouvellesArticleIE,
)
from .tvc import (
    TVCIE,
    TVCArticleIE,
)
from .tver import TVerIE
from .tvigle import TvigleIE
from .tvland import TVLandIE
from .tvn24 import TVN24IE
from .tvnet import TVNetIE
from .tvnoe import TVNoeIE
from .tvnow import (
    TVNowIE,
    TVNowFilmIE,
    TVNowNewIE,
    TVNowSeasonIE,
    TVNowAnnualIE,
    TVNowShowIE,
)
from .tvopengr import (
    TVOpenGrWatchIE,
    TVOpenGrEmbedIE,
)
from .tvp import (
    TVPEmbedIE,
    TVPIE,
    TVPStreamIE,
    TVPWebsiteIE,
)
from .tvplay import (
    TVPlayIE,
    ViafreeIE,
    TVPlayHomeIE,
)
from .tvplayer import TVPlayerIE
from .tweakers import TweakersIE
from .twentyfourvideo import TwentyFourVideoIE
from .twentymin import TwentyMinutenIE
from .twentythreevideo import TwentyThreeVideoIE
from .twitcasting import (
    TwitCastingIE,
    TwitCastingLiveIE,
    TwitCastingUserIE,
)
from .twitch import (
    TwitchVodIE,
    TwitchCollectionIE,
    TwitchVideosIE,
    TwitchVideosClipsIE,
    TwitchVideosCollectionsIE,
    TwitchStreamIE,
    TwitchClipsIE,
)
from .twitter import (
    TwitterCardIE,
    TwitterIE,
    TwitterAmplifyIE,
    TwitterBroadcastIE,
    TwitterShortenerIE,
)
from .udemy import (
    UdemyIE,
    UdemyCourseIE
)
from .udn import UDNEmbedIE
from .ufctv import (
    UFCTVIE,
    UFCArabiaIE,
)
from .ukcolumn import UkColumnIE
from .uktvplay import UKTVPlayIE
from .digiteka import DigitekaIE
from .dlive import (
    DLiveVODIE,
    DLiveStreamIE,
)
from .drooble import DroobleIE
from .umg import UMGDeIE
from .unistra import UnistraIE
from .unity import UnityIE
from .uol import UOLIE
from .uplynk import (
    UplynkIE,
    UplynkPreplayIE,
)
from .urort import UrortIE
from .urplay import URPlayIE
from .usanetwork import USANetworkIE
from .usatoday import USATodayIE
from .ustream import UstreamIE, UstreamChannelIE
from .ustudio import (
    UstudioIE,
    UstudioEmbedIE,
)
from .utreon import UtreonIE
from .varzesh3 import Varzesh3IE
from .vbox7 import Vbox7IE
from .veehd import VeeHDIE
from .veo import VeoIE
from .veoh import VeohIE
from .vesti import VestiIE
from .vevo import (
    VevoIE,
    VevoPlaylistIE,
)
from .vgtv import (
    BTArticleIE,
    BTVestlendingenIE,
    VGTVIE,
)
from .vh1 import VH1IE
from .vice import (
    ViceIE,
    ViceArticleIE,
    ViceShowIE,
)
from .vidbit import VidbitIE
from .viddler import ViddlerIE
from .videa import VideaIE
from .videocampus_sachsen import VideocampusSachsenIE
from .videodetective import VideoDetectiveIE
from .videofyme import VideofyMeIE
from .videomore import (
    VideomoreIE,
    VideomoreVideoIE,
    VideomoreSeasonIE,
)
from .videopress import VideoPressIE
from .vidio import (
    VidioIE,
    VidioPremierIE,
    VidioLiveIE
)
from .vidlii import VidLiiIE
from .vier import VierIE, VierVideosIE
from .viewlift import (
    ViewLiftIE,
    ViewLiftEmbedIE,
)
from .viidea import ViideaIE
from .vimeo import (
    VimeoIE,
    VimeoAlbumIE,
    VimeoChannelIE,
    VimeoGroupsIE,
    VimeoLikesIE,
    VimeoOndemandIE,
    VimeoReviewIE,
    VimeoUserIE,
    VimeoWatchLaterIE,
    VHXEmbedIE,
)
from .vimm import (
    VimmIE,
    VimmRecordingIE,
)
from .vimple import VimpleIE
from .vine import (
    VineIE,
    VineUserIE,
)
from .viki import (
    VikiIE,
    VikiChannelIE,
)
from .viqeo import ViqeoIE
from .viu import (
    ViuIE,
    ViuPlaylistIE,
    ViuOTTIE,
)
from .vk import (
    VKIE,
    VKUserVideosIE,
    VKWallPostIE,
)
from .vlive import (
    VLiveIE,
    VLivePostIE,
    VLiveChannelIE,
)
from .vodlocker import VodlockerIE
from .vodpl import VODPlIE
from .vodplatform import VODPlatformIE
from .voicerepublic import VoiceRepublicIE
from .voicy import (
    VoicyIE,
    VoicyChannelIE,
)
from .voot import (
    VootIE,
    VootSeriesIE,
)
from .voxmedia import (
    VoxMediaVolumeIE,
    VoxMediaIE,
)
from .vrt import VRTIE
from .vrak import VrakIE
from .vrv import (
    VRVIE,
    VRVSeriesIE,
)
from .vshare import VShareIE
from .vtm import VTMIE
from .medialaan import MedialaanIE
from .vuclip import VuClipIE
from .vupload import VuploadIE
from .vvvvid import (
    VVVVIDIE,
    VVVVIDShowIE,
)
from .vyborymos import VyboryMosIE
from .vzaar import VzaarIE
from .wakanim import WakanimIE
from .walla import WallaIE
from .washingtonpost import (
    WashingtonPostIE,
    WashingtonPostArticleIE,
)
from .wasdtv import (
    WASDTVStreamIE,
    WASDTVRecordIE,
    WASDTVClipIE,
)
from .wat import WatIE
from .watchbox import WatchBoxIE
from .watchindianporn import WatchIndianPornIE
from .wdr import (
    WDRIE,
    WDRPageIE,
    WDRElefantIE,
    WDRMobileIE,
)
from .webcaster import (
    WebcasterIE,
    WebcasterFeedIE,
)
from .webofstories import (
    WebOfStoriesIE,
    WebOfStoriesPlaylistIE,
)
from .weibo import (
    WeiboIE,
    WeiboMobileIE
)
from .weiqitv import WeiqiTVIE
from .willow import WillowIE
from .wimtv import WimTVIE
from .whowatch import WhoWatchIE
from .wistia import (
    WistiaIE,
    WistiaPlaylistIE,
)
from .worldstarhiphop import WorldStarHipHopIE
from .wppilot import (
    WPPilotIE,
    WPPilotChannelsIE,
)
from .wsj import (
    WSJIE,
    WSJArticleIE,
)
from .wwe import WWEIE
from .xbef import XBefIE
from .xboxclips import XboxClipsIE
from .xfileshare import XFileShareIE
from .xhamster import (
    XHamsterIE,
    XHamsterEmbedIE,
    XHamsterUserIE,
)
from .xiami import (
    XiamiSongIE,
    XiamiAlbumIE,
    XiamiArtistIE,
    XiamiCollectionIE
)
from .ximalaya import (
    XimalayaIE,
    XimalayaAlbumIE
)
from .xinpianchang import XinpianchangIE
from .xminus import XMinusIE
from .xnxx import XNXXIE
from .xstream import XstreamIE
from .xtube import XTubeUserIE, XTubeIE
from .xuite import XuiteIE
from .xvideos import XVideosIE
from .xxxymovies import XXXYMoviesIE
from .yahoo import (
    YahooIE,
    YahooSearchIE,
    YahooGyaOPlayerIE,
    YahooGyaOIE,
    YahooJapanNewsIE,
)
from .yandexdisk import YandexDiskIE
from .yandexmusic import (
    YandexMusicTrackIE,
    YandexMusicAlbumIE,
    YandexMusicPlaylistIE,
    YandexMusicArtistTracksIE,
    YandexMusicArtistAlbumsIE,
)
from .yandexvideo import (
    YandexVideoIE,
    YandexVideoPreviewIE,
    ZenYandexIE,
    ZenYandexChannelIE,
)
from .yapfiles import YapFilesIE
from .yesjapan import YesJapanIE
from .yinyuetai import YinYueTaiIE
from .ynet import YnetIE
from .youjizz import YouJizzIE
from .youku import (
    YoukuIE,
    YoukuShowIE,
)
from .younow import (
    YouNowLiveIE,
    YouNowChannelIE,
    YouNowMomentIE,
)
from .youporn import YouPornIE
from .yourporn import YourPornIE
from .yourupload import YourUploadIE
from .youtube import (
    YoutubeIE,
    YoutubeClipIE,
    YoutubeFavouritesIE,
    YoutubeNotificationsIE,
    YoutubeHistoryIE,
    YoutubeTabIE,
    YoutubeLivestreamEmbedIE,
    YoutubePlaylistIE,
    YoutubeRecommendedIE,
    YoutubeSearchDateIE,
    YoutubeSearchIE,
    YoutubeSearchURLIE,
    YoutubeMusicSearchURLIE,
    YoutubeSubscriptionsIE,
    YoutubeStoriesIE,
    YoutubeTruncatedIDIE,
    YoutubeTruncatedURLIE,
    YoutubeYtBeIE,
    YoutubeYtUserIE,
    YoutubeWatchLaterIE,
)
from .zapiks import ZapiksIE
from .zattoo import (
    BBVTVIE,
    EinsUndEinsTVIE,
    EWETVIE,
    GlattvisionTVIE,
    MNetTVIE,
    NetPlusIE,
    OsnatelTVIE,
    QuantumTVIE,
    SaltTVIE,
    SAKTVIE,
    VTXTVIE,
    WalyTVIE,
    ZattooIE,
    ZattooLiveIE,
    ZattooMoviesIE,
    ZattooRecordingsIE,
)
from .zdf import ZDFIE, ZDFChannelIE
from .zee5 import (
    Zee5IE,
    Zee5SeriesIE,
)
from .zhihu import ZhihuIE
from .zingmp3 import (
    ZingMp3IE,
    ZingMp3AlbumIE,
    ZingMp3ChartHomeIE,
    ZingMp3WeekChartIE,
    ZingMp3ChartMusicVideoIE,
    ZingMp3UserIE,
)
from .zoom import ZoomIE
from .zype import ZypeIE

_PLUGIN_CLASSES = load_plugins('extractor', 'IE', globals())
_ALL_CLASSES = list(_PLUGIN_CLASSES.values()) + _ALL_CLASSES