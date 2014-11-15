# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('L',SPAN('ove'),'L', SPAN('ove'),'Bean', XML('<sup> beta</sup>')),
                  _class="brand",_href="http://lovelovebean.com/")
response.title = 'LoveLoveBean - The Missing App for L.L.Bean'
response.subtitle = XML('L.L.Bean Daily Sales <br/> We Tailor to Fit You <br/> Deliver to You with Love')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'LoveLoveBean App<we@lovelovebean.com>'
response.meta.keywords = 'L.L.Bean, Daily Markdown, Sales, Alert'
response.meta.description = 'Save money on quality L.L.Bean products. LoveLoveBean App watches L.L.Bean Daily Markdown Sales, screen for the best deals YOU desire, notify you by EMail'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = 'UA-6923981-3'

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('App'), False, URL('default', 'index'), []),
    (T('Blog'), False, 'http://blog.lovelovebean.com', []),
    (T('Why LLBean?'), False, 'http://blog.lovelovebean.com/2014/10/28/why-l-l-bean-10-reasons-why-i-only-shop-at-l-l-bean/', []),
    (T('Save $'), False, 'http://blog.lovelovebean.com/2014/10/04/10-ways-to-save-money-on-l-l-bean-products/', []),
    (T('About'), False, 'http://blog.lovelovebean.com/about/', []),
    (T('Contact Us'), False, 'http://blog.lovelovebean.com/contact-us/', [])
]

if "auth" in locals(): auth.wikimenu() 
