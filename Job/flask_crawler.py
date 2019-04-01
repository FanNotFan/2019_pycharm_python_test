from flask import Flask, request, render_template, make_response

# 如果你想要返回列表,字典之类的数据,就需要先转换为json数据返回
from flask import jsonify
from lxml.html.clean import Cleaner
import requests
import re
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

SIZETYPES = [
    'km',
    'ha',
    'acre',
    'mile',
    'm',
    'ft',
    'in',
    'cm',
    'yd',
    'mile',
    'm²'
]

BEDTYPES = [
    'Bunk',
    'Crib',
    'Day',
    'Double',
    'Futon',
    'King',
    'Large Twin',
    'Murphy',
    'Queen',
    'Rollaway',
    'Sofa',
    'Trundle',
    'Twin',
    'Water']
ROOMTYPES = ['Townhome'
    , 'Bungalow'
    , 'Cabin'
    , 'Chalet'
    , 'Condo'
    , 'Cottage'
    , 'Double or Twin Room'
    , 'Double Room'
    , 'Double Room Single Use'
    , 'Duplex'
    , 'House'
    , 'Loft'
    , 'Mobile Home'
    , 'Penthouse'
    , 'Quadruple Room'
    , 'Shared Dormitory'
    , 'Dormitory'
    , 'Single Room'
    , 'Studio'
    , 'Studio Suite'
    , 'Suite'
    , 'Tent'
    , 'Tree House'
    , 'Triple Room'
    , 'Twin Room'
    , 'Villa'
    , 'Apartment'
    , 'Room'
    , 'Quintuple', 'Sextuple', 'Septuple', 'Octuple'  # , 'Premium'
             ]
BOOKING_ROOMTYPES = [
    'Single Room'
    , 'Double Room'
    , 'Twin Room'
    , 'Twin or Double Room'
    , 'Triple Room'
    , 'Quadruple'
    # , 'Family' # By Bcom standards, this is a room, but let's move this to class
    , 'Suite'
    , 'Studio'
    , 'Apartment'
    , 'Dormitory room'
    , 'Bed in Dormitory'
]
BOOKING_ROOMCLASS = [
    'Basic'
    , 'Budget'
    , 'Business'
    , 'Classic'
    , 'Comfort'
    , 'Deluxe'
    , 'Duplex'
    , 'Economy'
    , 'Executive'
    , 'Japanese-Style'
    , 'Junior'
    , 'King'
    , 'Large'
    , 'Luxury'
    , 'Premium'
    , 'Presidential'
    , 'Queen'
    , 'Small'
    , 'Standard'
    , 'Superior'
    , 'Family'  # Was type, but works better if we use it as Class
]

ROOMCLASS = ['Basic'
    , 'Business'
    , 'City'
    , 'Classic'
    , 'Club'
    , 'Comfort'
    , 'Deluxe'
    , 'Design'
    , 'Economy'
    , 'Elite'
    , 'Exclusive'
    , 'Executive'
    , 'Family'
    , 'Gallery'
    , 'Grand'
    , 'Honeymoon'
    , 'Junior'
    , 'Luxury'
    , 'Panoramic'
    , 'Premier'
    , 'Premium'
    , 'Presidential'
    , 'Romantic'
    , 'Royal'
    , 'Senior'
    , 'Signature'
    , 'Standard'
    , 'Superior'
    , 'Traditional'
             ]

ROOMCLASS_OCCUPANCY = ['Single', 'Double', 'Triple', 'Quadruple', 'Quintuple', 'Sextuple', 'Septuple', 'Octuple']

ROOMCLASSBED = ['Queen', 'King', 'Bunk']  # Don't include in Bedding what could be giving the room type

ROOMVIEWS = ['Water', 'Valley', 'Pool', 'Resort', 'City', 'Park', 'Hill', 'Marina', 'Garden', 'Desert', 'Golf',
             'Mountain', 'Canal',
             'Bay', 'Sea', 'Lagoon', 'Harbor', 'Ocean', 'Partial ocean', 'Courtyard', 'Partial sea', 'Vineyard',
             'Partial lake',
             'Lake', 'Beach', 'River', 'Creek', 'View']

ROOMEXTRAS = ['Non-smoking', 'Smoking', 'Accessible', 'Lanai', 'Balcony', 'Private Pool', 'Kitchen', 'Kitchenette',
              'Roll In Shower',
              'Fireplace', 'Patio', 'Parking', 'Connecting Rooms', 'Garden', 'Female', 'Male', 'Mixed']

SIZETYPES_JOIN = '|'.join(SIZETYPES).lower()
# REGEX_SIZETYPES = re.compile(r'(\d+?(-)?\d+\s?(?:km|ha|acre|mile|m|ft|in|cm|yd|sq|KM|HA|ACRE|MILE|M|FT|IN|CM|YD|SQ))')
REGEX_SIZETYPES = re.compile(r'(\d+?\s?(-|to)?\s?\d+\s?(square|sq\.|sq|SQ|ft²|m²)+\s?(?:mt|km|ha|acre|mile|m|feet|foot|ft|in|cm|yd|KM|HA|ACRE|MILE|M|FT|IN|CM|YD)?)')
REGEX_BEDTYPES = re.compile('(' + '|'.join(BEDTYPES).lower() + ')')
REGEX_ROOMTYPE = re.compile('\\b(' + '|'.join(ROOMTYPES).lower() + ')')
REGEX_BOOKING_ROOMTYPES = re.compile('\\b(' + '|'.join(BOOKING_ROOMTYPES).lower() + ')')
REGEX_BOOKING_ROOMCLASS = re.compile('\\b(' + '|'.join(BOOKING_ROOMCLASS).lower() + ')')
REGEX_BEDS_BCOM = re.compile(r'(?:\d+(?:\;\d \([\w ]+\))?\|)(?:([\w()\-+ ]+)\|?\|)([\w:\-+ ]+)')
REGEX_ROOMCLASS = re.compile(r'((?:(?:' + '|'.join(ROOMCLASS).lower() + ') ?)+)')
REGEX_ROOMOCCUPANCY = re.compile(r'((?:(?:' + '|'.join(ROOMCLASS_OCCUPANCY).lower() + ')))')
REGEX_ROOMCLASSBED = re.compile(r'\b((?:(?:' + '|'.join(ROOMCLASSBED).lower() + r'|\d+\-bed))+)\b')
REGEX_ROOMCLASS_TYPES = re.compile(
    r'((?:(?:' + '|'.join(ROOMCLASS).lower() + ') ?)+) (?:' + '|'.join(ROOMTYPES).lower() + ')')
REGEX_ROOMCLASS_SIMPLE = re.compile(r'((?:(?:' + '|'.join(ROOMCLASS).lower() + '))+)')
REGEX_ROOMVIEWS = re.compile(r'(' + '|'.join(ROOMVIEWS).lower() + ') (?:view)')
REGEX_EGVIEWS = re.compile(r'(?:view ?-?) (' + '|'.join(ROOMVIEWS).lower() + ')')
REGEX_VIEW = re.compile(r'view')
REGEX_BEDROOM = re.compile(r'((?:one|two|three|four|five)\-bedroom)')
BIGGER_REGEX = re.compile(r'(.*) ?(?: \– bigger than most in [\w ]+)')
BIGGER_REGEX = re.compile(r' [\–\-] bigger than most in .*')
BIGGER_REGEX_EXTRACT = re.compile(r'(.*)(?: \– bigger than most in [\w]+)')
REGEX_EXTRAS_ALL = re.compile(
    r'((?:without )?(?:nonsmoking|smoking|accessible(?! by)|lanai|balcony|terrace|private pool|jacuzzi|kitchen(?:ette)?|roll[\- ]?in shower|fireplace|patio|connecting rooms|female|male|mixed)(?! view)|\b(?:water|valley|pool|resort|city|park|hill|marina|garden|desert|golf|mountain|canal|bay|sea|lagoon|harbor|ocean|partial ocean|courtyard|partial sea|vineyard|partial lake|lake|beach|river|creek|view|road|street|north|south)? ?(?:side) ?(?:water|valley|pool|resort|city|park|hill|marina|garden|desert|golf|mountain|canal|bay|sea|lagoon|harbor|ocean|partial ocean|courtyard|partial sea|vineyard|partial lake|lake|beach|river|creek|view|road|street|north|south)?\b)')
REGEX_PACKAGE_1 = re.compile(r'([\w ]+)(?: with ([\w\- ]+) package)')
REGEX_PACKAGE_2 = re.compile(r'([\w ]+)(?: (?:\(?)([\w\- ]+) package ?(?:\))?)')
REGEX_COMBOOCCUPANCY = re.compile(
    r'([\w\-\&,\(\) ]+)?(?:\(? ?# ?(?: ?\- ?# ?)?adults?(?: ?(?:and)? # children)? ?\)?|(?: *\(? *for # people *\)?)|(?:\( ?# ?person[s]? ?\))|(?:\(?# ?(?:- ?#)? ?person[a]?[s]?\)?)|(?:\( ?# ?people ?\)?)|(?:\(? ?#\-# people ?\)?))( ?[\w\-\#\&,\(\) ]+)?')
REGEX_SPECIAL = re.compile(
    r"((?:special|limited time|transit|chrismas|new year'?s?( eve)?|romantic|weekend|spa|package|member|tasting|[\w]+) offer ?-?)")
REGEX_BEDS_BCOM = re.compile(r'(?:\d+(?:\;\d \([\w ]+\))?\|)(?:([\w()\-+ ]+)\|?\|)([\w:\-+ ]+)')
REGEX_AMENITIES_BCOM = re.compile(
    r'(?:\d+ ?(?:\;\d \([\w ]+\) ?)?\|\|? ?)(?:([\w()\-\–+,& ]+))\|\|?([\w:\-+, ]+)\|\|?([\w(); -\/\/,\>]+)')
REGEX_AMENITIES_BCOM_NEW = re.compile(
    r'(?:\d+ ?(?:\;\d \([\w ]+\) ?)?\|\|? ?)(?:([\w()\-\–+,& ]+))\|\|?([\w:\-+, ]+)\|\|?([\w(); -\/\/,\>]+)\|\|?(\d+ (?:m²|ft²))')

# url = 'https://www.lesaintsulpice.com/en/our-suites/deluxe-suite'
headers = {
    'origin': 'https://be.synxis.com',
    'authority': 'be.synxis.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'cookie': r'visid_incap_1215874=mgfPqyIqTfybQhzZJSibfMxwh1wAAAAAQUIPAAAAAACJVJ8WSmVOilwWpAAC8dRV; visid_incap_1814716=4Q54Wip7QG6XOyHSkZkMLc9wh1wAAAAAQUIPAAAAAAA5f1555w1Ko5zeL0de7EJv; _vwo_uuid_v2=D5CCF43683FE4D2A34F4146C8A4A22071|7459557f69ebd1f62058b8ff6e2662cf; _ga=GA1.3.897471948.1552380053; __utmv=77553030.|4=device=pc=1; _ga=GA1.2.257448949.1552460070; nlbi_1814716=bGeWBEQOi3KArlRB6mEoJwAAAADP0vdHkkcpeGGel53luXXz; incap_ses_1205_1814716=9/hrKr7ZAGfqFViPMgW5EJ6ekVwAAAAAD6A7978jHPBcLe+otTmhuQ==; sessionID=xin7fR8TI4geEjfc1eDX7PQ9; apisession=30303131367e6162754746793474464a5a73396d766a5679535a4a6465654a7a466d49385548502f5739704f5a6a386d6b7747774c616a796e394e2b6f47504e686a337559454b6b362f6443414a57724b2b3147315331706b3439724a6c4b51514d6e7a654f6167706e3262354f4b2b5741554e766634414f444a6836784737656c5952423538396e314c74502f453738325134493642456d374e37335232334e375764554676667034447a6443334e79464f496361764671695870637a303163776f4e55632b736972426b6a726e4b4d4e43584568413268704d6f62643675346f5a786d356c565a586754776b71335248357256534561754b4839424e775651375258367678466c55324934706b3072734b50342b4c53752f5334356458464b414e75527950526364577035364f67797351435a657072344951647569415847436641426a772f6431706f6f71746a41654b727379624f546d764d596a6c6c534d5739422b744a49644170766c4475624f2b54626e666a64425461796c30487055386e414342486867552b74547a6b30614677617a577a6b384e4c46743132375a533655582b6e6a6a362b787342685874516a4c4d34382b574a33365443336457742b2b66672b70516967383056714c7279723475646d62394263676b73664778413151335871745466775030544e6334332b636b55576c7a586a516453476151357a316152337a30526242775a43762b44587633613266555265347636764f2f746332315a3166432b767078456d6b664b5530376e724e576c677352444739457459654558343847707a436839686358686b4554476c5551386846615449722f7357324876547031454d776476394245786a6a67435366587476506f4e783052502f4a48434b436c6c4270395472666946383346615668596551775256513556757576776b2f5861695043372f592f6d5779706d5361777174767662656f4c614d33444c566a2b4d486653745071526a566e45714f457869683537577356453676374d7544646b4e654b4a75696858576c66496c6f742b48464e6a4b362b726641333568355a3077424a457537544368545a793059764e744249597971314d644b67494c582b746f6357524e4633585579316357546d6a45594e6b31364d6c4b54766c555168645559414a6c367855382f71443752445433626b6d4d515938597577683061624d47796a755469414453654d31654a59306952563658576e2f7a4b4232506b6159735673394f6330714745446249416f3035424d42614c58766d307665694d4b4c706d5a58645147796231742b782f727550566448457542326b465a6434626559713832623565464e5547492f4d6a51494e5a706575414f41786b6d3262563631706e4835434d78553d; nlbi_1215874=oneWdDpY6FrhRczVXmIUwQAAAADrEzTxnk6ZIleCYDR+vcJi; incap_ses_968_1215874=TbmPPE2JaBBUOBVmdgdvDXWgkVwAAAAAoPw2LqJTq5kqUD8Wcktm2w==; _vis_opt_s=2%7C; _vis_opt_test_cookie=1; __utmc=77553030; __utmz=77553030.1553047681.2.2.utmcsr=hotelplacedarmes.com|utmccn=(referral)|utmcmd=referral|utmcct=/en/rooms/; incap_ses_542_1215874=P8dgSaWrHQUs55+TSJOFB2CQlFwAAAAA0yvQ7f+NP2qV5ITa7MsfEQ==; _gid=GA1.3.543796484.1553240165; __utma=77553030.897471948.1552380053.1553047681.1553240165.3; incap_ses_551_1814716=nafTE4olZ39nNo5cvIylB+WQlFwAAAAAyH6VpUmAST/6Seort6Fijw==; nlbi_1215874_1737171=DodjXWXBW3fRGgfbXmIUwQAAAADZTuCNOHtnoYCQwHfLQTtX; __utmb=77553030.5.10.1553240165',
    'Referer': r'https://be.synxis.com/?adult=1&arrive=2019-04-16&chain=18009&child=0&currency=CAD&depart=2019-04-17&hotel=65074&level=hotel&locale=en-US&rooms=1&sbe_ri=0',
    'Connection': 'keep-alive'
}

app = Flask(__name__)

# 打开调试模式：启用了调试支持，服务器会在代码修改后自动重新载入，并在发生错误时提供一个相当有用的调试器
# app.run(debug=True)


# @app.route("/get_crawler_result", methods=['POST'])
def get_crawler_result(crawler_url):
    if crawler_url == '':
        raise Exception('empty parameter error')
    dict_response = {}
    app.logger.debug("crawler_url = ", crawler_url)
    content = get_request_content(crawler_url)
    content_without_space = remove_space(content)
    process_data = science_method(content_without_space)
    dict_response.setdefault("bedType", getBedType(process_data))
    dict_response.setdefault("roomType", getRoomType(process_data))
    dict_response.setdefault("roomTypeAll", getRoomTypeAll(process_data))
    dict_response.setdefault("roomClass", getRoomClass(process_data))
    dict_response.setdefault("pureRoomBedding", getPureRoomBedding(process_data))
    dict_response.setdefault("package", getPackage(process_data))
    # print('content_without_space==', content_without_space)
    dict_response.setdefault("roomSize", get_room_size(str(content_without_space))[0] if get_room_size(str(content_without_space)) != 'unknown' else 'unknown')
    response = make_response(jsonify(dict_response))
    response.status = "200"
    response.headers["author"] = "Lennon"
    # return response
    # return render_template("crawler_result.html", dict_response=dict_response), 200
    return dict_response


def get_request_content(url):
    html = requests.get(url, headers=headers).text
    # 清除不必要的标签
    cleaner = Cleaner(
        remove_tags=['div', 'body', 'li', 'ul', 'a', 'span', 'img', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'i',
                     'header', 'nav', 'svg', 'tr', 'td'], forms=True, processing_instructions=True, inline_style=True,
        links=True, style=True, scripts=True, comments=True, javascript=True, page_structure=True,
        safe_attrs_only=False)

    content = cleaner.clean_html(html)
    return content


def remove_space(content):
    content_without_space = []
    lines = content.split('\n')
    # 去空格
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
        # if lines[i] == '' or lines[i] == 'n' or i == 0 or i == len(lines) - 1:
        if lines[i] == '' or lines[i] == 'n':
            continue
        else:
            lines[i] = lines[i].replace("\t", "")
            content_without_space.append(lines[i])
    return content_without_space


def science_method(content_without_space):
    vectorizer = CountVectorizer()
    # print("类型：\n", type(vectorizer.fit_transform(content_without_space)))
    # 把稀疏矩阵输出成真实矩阵
    actual_matrix_result = vectorizer.fit_transform(content_without_space).todense()
    # 该类会统计每个词语的tf-idf权值
    transformer = TfidfTransformer()
    # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(actual_matrix_result)
    # 获取词袋模型中的所有词语
    word = vectorizer.get_feature_names()

    # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    weight = tfidf.toarray()

    map = {}
    for j in range(len(word)):
        temp = 0
        for i in range(len(weight)):
            temp += weight[i][j]
        map.setdefault(word[j], temp)

    list = sorted(map.items(), key=lambda item: item[1], reverse=True)
    keys = [key for key, value in list]
    process_data = str(keys)
    return process_data


def get_room_size(mystr):
    """ Find out the room type, i.e. if it is a room or an apartment """

    try:
        return re.findall(REGEX_SIZETYPES, mystr)[0]
    except IndexError:
        return 'unknown'


def getBedType(mystr):
    """ Find out the room type, i.e. if it is a room or an apartment """

    try:
        return re.findall(REGEX_BEDTYPES, mystr)[0]
    except IndexError:
        return 'unknown'


def getRoomType(mystr):
    """ Find out the room type, i.e. if it is a room or an apartment """

    try:
        return re.findall(REGEX_ROOMTYPE, mystr)[0]
    except IndexError:
        return 'unknown'


def getRoomTypeAll(mystr):
    """ Find out the room type, i.e. if it is a room or an apartment """

    if re.findall(REGEX_ROOMTYPE, mystr):
        return (sorted(set(re.findall(REGEX_ROOMTYPE, mystr))))
    else:
        return ['unknown']


# def getBookingRoomTypeAll(mystr):
#     """ Find out the room type, i.e. if it is a room or an apartment """
#
#     if re.findall(REGEX_BOOKING_ROOMTYPES, mystr):
#         return (sorted(set(re.findall(REGEX_BOOKING_ROOMTYPES, mystr))))
#     else:
#         return ['unknown']


def getRoomClass(mystr):
    """ Find out the room class, i.e. if it is Business or Basic """

    try:
        return re.findall(REGEX_ROOMCLASS_TYPES, mystr)[0]
    except IndexError:

        try:
            return re.findall(REGEX_ROOMCLASS_SIMPLE, mystr)[0]
        except IndexError:
            return 'unknown'


def getPureRoomBedding(mystr):
    """ Get bedding information, from Room name """

    try:
        return re.findall(REGEX_ROOMCLASSBED, mystr)[0]
    except IndexError:
        return 'unknown'


def getPackage(mystr, returnPackage=True):
    """ Get packages information from Room name. When returnPackage = True, package information is provided """

    m1 = re.findall(REGEX_PACKAGE_1, mystr)
    m2 = re.findall(REGEX_PACKAGE_2, mystr)

    room, package = [], []
    if m1:
        room = m1[0][0]
        package = m1[0][1]
    elif m2:
        room = m2[0][0]
        package = m2[0][1]
    else:
        room = mystr
        package = 'none'

    if returnPackage:
        return package
    else:
        return room


if __name__ == '__main__':
    str = "BreakfastBook our breakfast inclusive rates and enjoy Grand Kitchen’s sumptuous buffet daily…Special OffersRoom DetailsSize45 m² / 485 ft²Beds1 kingRatesFrom JPY 55,000Floors8-18ViewImperial Palace and Otemon GateCapacity2 personsOther"
    result = get_room_size(str)
    print(result[0])