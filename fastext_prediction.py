import re
import requests
import fasttext
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, words
from w3lib.util import to_bytes
import json
import datetime
try:
    import httplib
except:
    import http.client as httplib


# function to check internet availability
def have_internet():
    conn = httplib.HTTPSConnection("www.google.com", timeout=120)
    try:
        conn.request("HEAD", "/")
        conn.close()
        print("Internet Connection is Fine")
        return True
    except:
        raise Exception("INTERNET IS DOWN !!")

# checking Internet connection
# have_internet()
# scheduling Internet check a every 1 minutes
# schedule.every(1).minutes.do(have_internet)

urls = []
titles = []
lemmatizer = WordNetLemmatizer()
STOPWORDS = stopwords.words('english')
EnglishWords = words.words()

stopwords1 = ['add', 'align', 'alt', 'amp', 'app', 'arc', 'aria', 'article', 'author', 'auto', 'background', 'banner',
              'blank', 'block', 'border', 'box', 'brand', 'btn', 'button', 'card', 'carousel', 'cdn', 'center', 'class',
              'click', 'code', 'col', 'color', 'column', 'com', 'component', 'container', 'coupon', 'crop', 'cs', 'cta',
              'custom', 'data', 'date', 'default', 'desktop', 'detail', 'display', 'div', 'document', 'dropdown', 'element',
              'ellipsiscell', 'event', 'false', 'feature', 'fff', 'field', 'file', 'fill', 'filter', 'flex', 'font',
              'footer', 'form', 'format', 'full', 'function', 'fusion', 'gaevent', 'grid', 'group', 'header', 'heading',
              'headline', 'height', 'hidden', 'home', 'homepage', 'hover', 'href', 'html', 'http', 'https', 'icon',
              'image', 'images', 'img', 'important', 'index', 'info', 'inline', 'inner', 'input', 'isarray', 'item',
              'javascript', 'jpeg', 'jpg', 'key', 'label', 'layout', 'left', 'level', 'line', 'link', 'list', 'logo',
              'main', 'margin', 'max', 'media', 'medium', 'menu', 'meta', 'min', 'mobile', 'module', 'name', 'nav', 'net',
              'new', 'news', 'ngcontent', 'none', 'noscript', 'null', 'object', 'onclick', 'open', 'option', 'org',
              'padding', 'page', 'path', 'pbwfnzs', 'photo', 'pic', 'picture', 'pleft', 'png', 'position', 'post',
              'pright', 'primary', 'product', 'push', 'quot', 'rel', 'rem', 'return', 'rgba', 'right', 'role', 'row',
              'sans', 'screen', 'script', 'search', 'section', 'self', 'share', 'site', 'slide', 'smntxt', 'social',
              'source', 'spacing', 'span', 'src', 'srcset', 'start', 'static', 'story', 'style', 'sub', 'svg', 'tab',
              'tabindex', 'table', 'tag', 'target', 'text', 'theme', 'thumbnail', 'tile', 'time', 'title', 'top',
              'topic', 'track', 'transform', 'true', 'txt', 'type', 'typename', 'typeof', 'uitk', 'uploads', 'url',
              'use', 'user', 'utm', 'value', 'var', 'video', 'view', 'viewbox', 'webkit', 'webp', 'weight', 'widget',
              'width', 'window', 'wrap', 'wrapper', 'www', 'xmlns', 'zbl', 'datedeleted', 'datecreated', 'dateupdated',
              'textcolorerrorstep', 'bgcolorerrorstep', 'textcolorsuccessstep', 'bgcolorsuccessstep',
              'textcolorwarningstep', 'bgcolorwarningstep', 'bgcolorprimarystep', 'textcolorprimarystep', 'attribute',
              'autoplay', 'backgroundcolor', 'backgroundsize', 'backgroundtype', 'backgroundwrapperblock', 'badge',
              'base', 'blockbgcolor', 'blockheaderbar', 'borderroundness', 'bordersize', 'buttonalignment',
              'buttonblock', 'buttonsize', 'byi', 'byq', 'byy', 'bzi', 'bzq', 'canonical', 'cardtitlelinkcolor', 'cdec',
              'chat', 'closedformat', 'common', 'contain', 'contentdef', 'contentseparatorcolor', 'continuity',
              'contractstar', 'day', 'defaultstate', 'dropdownsubmenubackground', 'dropdowntextcolor', 'dtd', 'ebc',
              'elementor', 'enablecontinuity', 'enablecookie', 'enabled', 'end', 'expandcollapse', 'faffiliates',
              'fassets', 'fbca', 'fblackbg', 'fbzday', 'fcarouselbanners', 'fcommon', 'fcontractstars', 'featuredblock',
              'featuredscenelistblock', 'fexpired', 'ffffff', 'ffull', 'fid', 'fimages', 'fimageservice',
              'fineeditnow', 'flogos', 'fmas', 'fmo', 'fontsizemo', 'fontsizepc', 'fonttype', 'fontweightbold', 'fpc',
              'fpress', 'fpromos', 'fscenes', 'fsite', 'fsites', 'fsubsites', 'ftags', 'ftgp', 'ftour', 'ftp', 'ftrial',
              'fupdate', 'fview', 'fwww', 'fzz', 'gallery', 'general', 'generic', 'gif', 'groupids', 'hasanchor',
              'hasbackgroundcolor', 'hasbackgroundgradient', 'hascontrols', 'hasdropshadow', 'haslistitemsplit',
              'haspaddingoverride', 'hasslider', 'hastextcolor', 'head', 'headertag', 'hoverbackgroundcolor',
              'hoverbordercolor', 'hovercolor', 'httpcode', 'iconsize', 'iconstrokewidth', 'imageblock', 'instance',
              'isnofollow', 'ispagination', 'isupdated', 'join', 'keywords', 'labelposition', 'lang', 'loading', 'login',
              'maddos', 'manualfilter', 'matchparentheight', 'menubg', 'menuend', 'menustart', 'metadescription',
              'metatags', 'metatagsconfig', 'metatitle', 'minheight', 'nbsp', 'nodename', 'nofollow', 'noopener',
              'original', 'paddingmultiplier', 'pagecolorconfig', 'pagegutterconfig', 'pageskinconfig', 'parentid',
              'parentstructure', 'pattern', 'php', 'playerblocks', 'popunder', 'poster', 'preview', 'priority', 'project',
              'range', 'rating', 'ratio', 'recent', 'redirects', 'releasetype', 'resultslimit', 'resultsperpage',
              'review', 'route', 'routetype', 'rte', 'rtecontent', 'sibling', 'sort', 'spaced', 'secondaryfont',
              'segment', 'shouldopennewtab', 'showmorebutton', 'status', 'spacingmultiplier', 'string', 'structure',
              'structureconfigs', 'tagids', 'tgp', 'themeconfig', 'transitiontime', 'usecustomcolors', 'usecustomskin',
              'usepagegutter', 'verticalalign', 'verticalpadding', 'xml', 'january', 'february', 'march', 'april', 'may',
              'june', 'july', 'august', 'september', 'october', 'november', 'december', 'ago', 'aug', 'textcolor',
              'bgcolor', 'tabsectionborder', 'tabsectionborder', 'bottom', 'tabborder', 'tabactiveborder', 'cloudflare',
              'jquery', 'datalayer', 'googletagmanager', 'getelementsbytagname', 'createelement', 'createstylesheet']

STOPWORDS.extend(stopwords1)

# Loading Fasttext Model
model = fasttext.load_model(
    "./Fasttext_model_new_default.bin")


def transform(url):
    req = None
    if 'https' in url:
        html_output_name = url[8:]
    else:
        html_output_name = url[7:]

    if (url[-1].isalpha() or url[-1] == "/"):
        html_output_name = html_output_name.replace('.', '_')
        html_output_name = html_output_name.replace('/', '')
        print(html_output_name)

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    try:
        req = requests.get(url, 'html.parser', headers=headers, timeout=4)
        print(f"URL_STATUS: {req.status_code}")
    except Exception as e:
        print(e)
        return "Can't Reach the Website!"

    text = req.text
    # Remove top headers from the file
    text = re.sub('^[^<]+', "", text)
    try:
        data_bs = BeautifulSoup(text, 'html.parser')
        text = data_bs.get_text()
    except Exception as e:
        print("**** HTML Parser Exception ****")
        print(e)
        return 99

    # Remove all punctuations from the data
    text = re.sub(r'[^A-Za-z]+', ' ', text)
    # Replace new line with space
    text = text.replace("\n", " ")
    # Remove all digits from the text
    text = re.sub("\d", " ", text)
    # Replace multiple space with single space
    text = re.sub("[\s]{2,}", " ", text).lower()
    # Get list of words
    text_lst = text.split(" ")

    text_lst = [lemmatizer.lemmatize(word) for word in text_lst if len(lemmatizer.lemmatize(word)) > 2 and
                word not in STOPWORDS and lemmatizer.lemmatize(word) not in STOPWORDS]

    # Getting list of words
    text = " ".join(text_lst)

    # Predicting Result
    result1 = model.predict(text)
    result = result1[0][0]
    if result == "__label__notporn":
        print(0, "- Non Pornographic Site")
        return "Non Pornographic Site"
    elif result == "__label__porn":
        print(1, "- Pornographic Site")
        return "Pornographic Site"

# transform("https://www.supercartoons.net/cartoon/chaser-on-the-rocks/")