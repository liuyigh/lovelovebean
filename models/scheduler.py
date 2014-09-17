import datetime
from gluon.scheduler import Scheduler
from datetime import timedelta as timed

sche_db = DAL('sqlite://sched.sqlite')

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

def matchPrice(priceToMatch):
    if priceToMatch <= priceScale[1]:
        priceMatched = 1
    elif priceToMatch <= priceScale[2]:
        priceMatched = 2
    elif priceMatched <= priceScale[3]:
        priceMatched = 3
    db((db.auth_criteria.salePrice>=priceMatched)|(db.auth_criteria.salePrice==0)).update(toSend=1)
    db.commit()

def sendBean():
    import mandrill
    mandrill_client = mandrill.Mandrill('0HLwKIwvpC_In6QveAuviw')
    emailList = []
    message = {}
    rowsToSend = db(db.auth_criteria.toSend==1).select()
    for row in rowsToSend:
        emailList.append(row.user_id.email)
    if emailList:
        message = json.dumps({'global_merge_vars':[{'name':'verifylink','content':'lovelovebean.com'}],
               'to':[{'email':email} for email in emailList]
              })
        #template_content = []
        result = mandrill_client.messages.send_template(template_name='llb-bean',template_content=[], message=message)
    db(db.auth_criteria.toSend==1).update(toSend=0)
    db.commit()
    return None

def fetchBean():
    import lxml.html as lh
    import lxml, requests
    from StringIO import StringIO

    #fetch html
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    r = requests.get('http://www.llbean.com/llb/shop/504987', stream=True, headers=hdr)
    if r.status_code == 200:
        # repeat if not 200
        # repeat if no sales
        html = lh.parse(StringIO(r.text))
        info = {} 
        info['itemTitle'] = html.xpath('//div[@id="ppHeader"]/h1/text()')
        info['itemDetails'] = html.xpath('//div[@id="ppDetails"]//text()')
        info['prodID'] = html.xpath('//span[@itemprop="productID"]/text()')
        info['revNum'] = html.xpath('//span[@class="reviewsNumber"]/text()')
        info['aveRev'] = html.xpath('//span[@id="ATBProdStarReviews"]/img/@alt')
        info['oriPrice'] = html.xpath('//h2[@class="toOrderItemPrice toOrderItemStrikeOutPrice"]/text()')
        info['salePrice'] = html.xpath('//h2[@class="toOrderItemSalePrice"]/text()')
        info['absSave'] = html.xpath('//p[@class="toOrderItemSaleText"][1]/text()')
        info['percSave'] = html.xpath('//p[@class="toOrderItemSaleText" and @itemprop="description"]/text()')

        info = {k: [x.strip('$()\n\t\r ') for x in v] for (k, v) in info.iteritems()}
        info = {k: filter(None, v) for (k, v) in info.iteritems()}

        info['absSave'] = float(info['absSave'][0].strip(u'Save\xa0$'))
        info['percSave'] = float(info['percSave'][0].strip('% Off'))
        info['itemTitle'][0] = info['itemTitle'][0].encode('ascii','ignore')
        info['itemDetails'] = json.dumps(info['itemDetails'][:-1])
        if info['aveRev']:
            info['aveRev'] = float(info['aveRev'][0][8:-15])
            info['revNum'] = int(info['revNum'][0])
        else:
            info['aveRev'] = None
            info['revNum'] = 0
        info['oriPrice'] = float(info['oriPrice'][0])
        info['salePrice'] = float(info['salePrice'][0])

        info['saleID'] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M')

    db.saleItems.insert(**info)
    db.commit()

    matchPrice(info['salePrice'])
    sendBean()

def matchBean():
    return None

scheduler = Scheduler(sche_db, dict(fetchBean=fetchBean))
