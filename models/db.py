# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

auth.messages.label_first_name = 'Nickname' ### My settings

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
from gluon.tools import Mail
from functools import partial
import json
mail = Mail()
mail.settings.server = 'smtp.mandrillapp.com:587'
mail.settings.sender = 'we@lovelovebean.com'
mail.settings.login = 'vievie@gmail.com:0HLwKIwvpC_In6QveAuviw'
'''
emailheaders = {}
if request.args(0)=='register':
    verifylink = request.env.http_host + URL(r=request,c='default',f='user',args=['verify_email']) + '/%(key)s'
    emailheaders = {'X-MC-Template':'llb-reg', 'X-MC-MergeVars': json.dumps({"verifylink": verifylink})}
## reset password emails
elif request.args(0)=='request_reset_password' and #require verification:
    emailheaders = {}
mail.send = partial(mail.send, headers=emailheaders)
'''

## configure auth policy
auth.settings.mailer = mail
auth.settings.email_case_sensitive = False
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.messages.verify_email = 'Click on the link http://' +     request.env.http_host +     URL(r=request,c='default',f='user',args=['verify_email']) +     '/%(key)s to verify your email'
auth.messages.reset_password = 'Click on the link http://' +     request.env.http_host +     URL(r=request,c='default',f='user',args=['reset_password']) +     '/%(key)s to reset your password'
auth.settings.login_next = URL('user',args='profile')
auth.settings.register_next = URL('user',args='login')
auth.messages.email_sent = 'Email sent. Please check your email.'

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
db.auth_user.last_name.readable = False
db.auth_user.last_name.writable = False
db.auth_user.first_name.comment = 'such as Bean Lover.'
db.auth_user.email.comment = 'This is your ID. Required.'

priceScale = {1:14.99,2:19.99,3:34.99}
tgScale = {1:24.99,2:49.99,3:74.99}
aveRevScale = {1:3.3,2:4.0,3:4.7}
percSaveScale = {1:42,2:56,3:67}

salePrice = {
    0: 'All Deals | 2 lovely beans per day',
    1: 'below (<=) ${}'.format(priceScale[1]),
    2: 'below (<=) ${}'.format(priceScale[2]),
    3: 'below (<=) ${}'.format(priceScale[3]),
    -1: 'Nope. More filters please! :)'
}

tgPrice = {
    0: 'All Deals | 1 lovely bean per day',
    1: 'below (<=) ${}'.format(tgScale[1]),
    2: 'below (<=) ${}'.format(tgScale[2]),
    3: 'below (<=) ${}'.format(tgScale[3]),
    -1: 'Nope. More filters please! :)'
}

aveRev = {
    0: 'Not specified.',
    1: 'above (>=) {} stars. Exclude the bottom 10%'.format(aveRevScale[1]),
    2: 'above (>=) {} stars. Above average.'.format(aveRevScale[2]),
    3: 'above (>=) {} stars. Top 10% Deals'.format(aveRevScale[3])
}

percSave = {
    0: 'Not specified.',
    1: 'above (>=) {} %. Exclude the bottom 10%'.format(percSaveScale[1]),
    2: 'above (>=) {} %. Above average.'.format(percSaveScale[2]),
    3: 'above (>=) {} %. Top 10% Deals'.format(percSaveScale[3])
}

db.define_table('auth_criteria',
   Field('user_id', 'reference auth_user', readable=False, writable=False),
   Field('salePrice', 'integer', widget=SQLFORM.widgets.radio.widget, requires = IS_IN_SET(salePrice)),
   Field('tgPrice', 'integer', widget=SQLFORM.widgets.radio.widget, requires = IS_IN_SET(tgPrice)),
   Field('aveRev', 'integer', requires = IS_IN_SET(aveRev)),
   Field('percSave', 'integer', requires = IS_IN_SET(percSave)),
   Field('toSend','integer', readable=False, writable=False))
db.auth_criteria.user_id.requires = IS_IN_DB(db, db.auth_user.id)
db.auth_criteria.id.readable=False 

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
