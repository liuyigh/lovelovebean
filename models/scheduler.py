import datetime
from gluon.scheduler import Scheduler
from datetime import timedelta as timed
import lxml.html as lh
import lxml, requests, mandrill, logging, sys, traceback

sche_db = DAL('sqlite://sched.sqlite')
mandrill_client = mandrill.Mandrill('0HLwKIwvpC_In6QveAuviw')

db.define_table('saleItems', 
        Field('saleID', 'string',unique=True),
        Field('itemTitle','string'),
        Field('itemDetails','json'), #json list
        Field('prodID','string'),
        Field('revNum','integer'),
        Field('aveRev','double'),
        Field('oriPrice','double'),
        Field('salePrice','double'),
        Field('absSave','double'),
        Field('percSave','double'),
        )

db.define_table('tgItems', 
        Field('saleID', 'string',unique=True),
        Field('itemTitle','string'),
        Field('itemDetails','json'), #json list
        Field('prodID','string'),
        Field('revNum','integer'),
        Field('aveRev','double'),
        Field('oriPrice','double'),
        Field('salePrice','double'),
        Field('absSave','double'),
        Field('percSave','double'),
        )

def notifyException():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    pre = ''.join('!> ' + line for line in lines)
    pre = pre.replace('>','&gt;')
    pre = pre.replace('<','&lt;')
    html = '<pre>'+pre+'</pre>'
    message = {'subject':'LLB Scheduler Error',
                'from_email':'we@lovelovebean.com',
                'html':html,
                'to':[{'email':'yi@liuyi.co'}]
                }
    result = mandrill_client.messages.send(message=message)

def matchPrice(priceToMatch):
    if priceToMatch <= priceScale[1]:
        priceMatched = 1
    elif priceToMatch <= priceScale[2]:
        priceMatched = 2
    elif priceToMatch <= priceScale[3]:
        priceMatched = 3
    else:
        priceMatched = 4
    db((db.auth_criteria.salePrice>=priceMatched)|(db.auth_criteria.salePrice==0)).update(toSend=1)
    db.commit()

def matchTGPrice(priceToMatch):
    if priceToMatch <= tgScale[1]:
        priceMatched = 1
    elif priceToMatch <= tgScale[2]:
        priceMatched = 2
    elif priceToMatch <= tgScale[3]:
        priceMatched = 3
    else:
        priceMatched = 4
    db((db.auth_criteria.tgPrice>=priceMatched)|(db.auth_criteria.tgPrice==0)).update(toSend=1)
    db.commit()

def match(field, scale, valueToMatch):
    if valueToMatch >= scale[3]:
        valueMatched = 3
    elif valueToMatch >= scale[2]:
        valueMatched = 2
    elif valueToMatch >= scale[1]:
        valueMatched = 1
    else:
        valueMatched = 0
    db((field<=valueMatched)&(field!=None)).update(toSend=1)
    db.commit()

def matchGender(titleToMatch):
    titleWords = titleToMatch.lower().split()
    if "men's" in titleWords:
        db((db.auth_criteria.genderPref==1)&(db.auth_criteria.toSend==1)).update(toSend=0)
    if "men's" not in titleWords:
        db((db.auth_criteria.genderPref==3)&(db.auth_criteria.toSend==1)).update(toSend=0)
    if "women's" in titleWords:
        db((db.auth_criteria.genderPref==2)&(db.auth_criteria.toSend==1)).update(toSend=0)
    if "women's" not in titleWords:
        db((db.auth_criteria.genderPref==4)&(db.auth_criteria.toSend==1)).update(toSend=0)

def sendBean(info, piclink, pageID):
    emailList = []
    rowsToSend = db(db.auth_criteria.toSend==1).select()
    for row in rowsToSend:
        emailList.append(row.user_id.email)
    message = {'global_merge_vars':[{'name':k,'content':v} for (k,v) in info.iteritems()]+[{'name':'piclink','content':piclink}]+[{'name':'pageID','content':pageID}], 
               'to':[{'email':email} for email in emailList]
              }
    #template_content = []
    result = mandrill_client.messages.send_template(template_name='llb-bean',template_content=[], message=message)
    db(db.auth_criteria.toSend==1).update(toSend=0)
    db.commit()
    return None

def fetchBean():
    #fetch html
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    try:
        r = requests.get('http://www.llbean.com/llb/shop/504987', stream=True, headers=hdr)
        if r.status_code == 200:
            # repeat if not 200
            # repeat if no sales
            html = lh.fromstring(r.text)
            info = {} 
            info['itemTitle'] = html.xpath('//div[@id="ppHeader"]/h1/text()')
            info['itemDetails'] = html.xpath('//div[@id="ppDetails"]//text()')
            info['prodID'] = html.xpath('//span[@itemprop="productID"]/text()')
            info['revNum'] = html.xpath('//span[@class="reviewsNumber"]/text()')
            info['aveRev'] = html.xpath('//span[@id="ATBProdStarReviews"]/img/@alt')
            info['oriPrice'] = html.xpath('//div[@class="toOrderItemPrice toOrderItemStrikeOutPrice"]/text()')
            info['salePrice'] = html.xpath('//div[@class="toOrderItemSalePrice"]/text()')
            info['absSave'] = html.xpath('//p[@class="toOrderItemSaleText"][1]/text()')
            info['percSave'] = html.xpath('//p[@class="toOrderItemSaleText"][2]/text()')
            
            info = {k: [x.strip('$()\n\t\r ') for x in v] for (k, v) in info.iteritems()}
            info = {k: filter(None, v) for (k, v) in info.iteritems()}

            info['absSave'] = float(info['absSave'][0].strip(u'Save\xa0$'))
            info['percSave'] = float(info['percSave'][0].strip('% Off'))
            info['itemTitle'] = info['itemTitle'][0].encode('ascii','ignore')
            info['itemDetails'] = json.dumps(info['itemDetails'][:-1])
            if info['aveRev']:
                info['aveRev'] = float(info['aveRev'][0][8:-15])
                info['revNum'] = int(info['revNum'][0])
            else:
                info['aveRev'] = None
                info['revNum'] = 0
            info['oriPrice'] = float(info['oriPrice'][0])
            info['salePrice'] = float(info['salePrice'][0])

            piclink = html.xpath('//img[@name="ecm_Front"]/@src')
            if piclink == []:
                piclink = html.xpath('//img[@name="ecm_main"]/@src')
            piclink = piclink[0][:-11]
            pageID='1ADemq3'

            info['saleID'] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M')

        db.saleItems.insert(**info)
        db.commit()

        matchPrice(info['salePrice'])
        match(db.auth_criteria.aveRev, aveRevScale, info['aveRev'])
        match(db.auth_criteria.percSave, percSaveScale, info['percSave'])
        matchGender(info['itemTitle'])
        sendBean(info, piclink, pageID)
    except:
        notifyException()

def fetchTGBean():
    #fetch travel and gear html
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    try:
        r = requests.get('http://www.llbean.com/llb/shop/510312', stream=True, headers=hdr)
        if r.status_code == 200:
            # repeat if not 200
            # repeat if no sales
            html = lh.fromstring(r.text)
            info = {} 
            info['itemTitle'] = html.xpath('//div[@id="ppHeader"]/h1/text()')
            info['itemDetails'] = html.xpath('//div[@id="ppDetails"]//text()')
            info['prodID'] = html.xpath('//span[@itemprop="productID"]/text()')
            info['revNum'] = html.xpath('//span[@class="reviewsNumber"]/text()')
            info['aveRev'] = html.xpath('//span[@id="ATBProdStarReviews"]/img/@alt')
            info['oriPrice'] = html.xpath('//div[@class="toOrderItemPrice toOrderItemStrikeOutPrice"]/text()')
            info['salePrice'] = html.xpath('//div[@class="toOrderItemSalePrice"]/text()')
            info['absSave'] = html.xpath('//p[@class="toOrderItemSaleText"][1]/text()')
            info['percSave'] = html.xpath('//p[@class="toOrderItemSaleText"][2]/text()')
            
            info = {k: [x.strip('$()\n\t\r ') for x in v] for (k, v) in info.iteritems()}
            info = {k: filter(None, v) for (k, v) in info.iteritems()}

            info['absSave'] = float(info['absSave'][0].strip(u'Save\xa0$'))
            info['percSave'] = float(info['percSave'][0].strip('% Off'))
            info['itemTitle'] = info['itemTitle'][0].encode('ascii','ignore')
            info['itemDetails'] = json.dumps(info['itemDetails'][:-1])
            if info['aveRev']:
                info['aveRev'] = float(info['aveRev'][0][8:-15])
                info['revNum'] = int(info['revNum'][0])
            else:
                info['aveRev'] = None
                info['revNum'] = 0
            info['oriPrice'] = float(info['oriPrice'][0])
            info['salePrice'] = float(info['salePrice'][0])

            piclink = html.xpath('//img[@name="ecm_Front"]/@src')
            if piclink == []:
                piclink = html.xpath('//img[@name="ecm_main"]/@src')
            piclink = piclink[0][:-11]
            pageID='1zyZEVW'

            info['saleID'] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M')

        db.tgItems.insert(**info)
        db.commit()

        matchTGPrice(info['salePrice'])
        match(db.auth_criteria.aveRev, aveRevScale, info['aveRev'])
        match(db.auth_criteria.percSave, percSaveScale, info['percSave'])
        matchGender(info['itemTitle'])
        sendBean(info, piclink, pageID)
    except:
        notifyException()

scheduler = Scheduler(sche_db, dict(fetchBean=fetchBean, fetchTGBean=fetchTGBean))
