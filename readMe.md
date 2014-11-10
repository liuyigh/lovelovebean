# Filters:
* All Deals (under price filter)
* sale Price (class="toOrderItemSalePrice")
    <= 24.99; <=49.99; <= 99.99; None(-1)
* Title Keywords (id="ppHeader")
    - unicode (currently ignored)
* Details Keywords (id="ppDetails")
* Review numbers (class="reviewsNumber") #next
    - No Review (as 0)
* Average reviews (id="ATBProdStarReviews" | title="") #done 11.08.14
    - No Review (as None)
* Original Price (class="toOrderItemStrikeOutPrice")
* abso. save (class="toOrderItemSaleText")
* percent save (class="toOrderItemSaleText" itemprop="description"") #done 11.08.14
* saleID (timestamp)
* prodID
* pictures (link only?) '//img[@name="ecm_main"]/@src' #done
* Regular Tall Petite
* Daily Travel Gear 510312 #done
    
	
# First Priorities:
* _Scheduler DB: monitor worker and failure_
* _record saleItem DB_
* _User filter DB: salePrice_
* _match and mark to send: `toSend`: {0:no; 1:yes}_
* _send email_
    - use mandrill: API
    - deal notice template
    - mergetags to use deal info; beautify; 
    - picture scrape
    - reset `toSend` after sent
* _brush up UI, launch beta_
    - optimal price scale
    - all deal
* _run @reboot worker at screen_


# Second Priorities:
* _510312_ done 11.02.2014
* Scrape

```
    if no_item: # id = ecmABT
        retry in 3 minutes
    if afternoon and same item:
        retry in 3 minutes
    if no sale:
        notify me.
```
* advanced user filter DB
    - Keywords: individual word matching
    - numbers: Predefined specific range (and use numbers to represent instead of user customizing)
    - Wishlist
    - Blacklist and Whitelist (higher priority)
* _Fail proof for all steps: notify me when error._ 10/20/2014
* _Cron watchdog_ watchdog with tmux 10.28.2014
* _Automatic database backup_ 10.15.2014
* Big Data: present deal distributions
    - most popular items: averev*revnum
* API deal mail
    - username merge
    - *|itemDetails|*
    - iter every 100 recepients
* UI: 
    - logo; LoveLoveBean
    - blog: introducing LLB
    - Web Design CSS: mobile. Done 10/18/2014
    - User count. Done 11/9/2014
    - homepage show current item
    - SMTP mailer issue email template: use Jinja2
        - register email
        - reset pwd email
        - use auth() verification codes?
* Marketing:
    - Twitter
    - Blog
* UserVoice (1000 Registered Users):
    - Feature voting

# Third Priorities:
* User priority membership DB field (0,1,2)
    - paypal integration
* match and record DB
    - count sent beans
    - reset count
* advanced big data
* advanced deal combinations if user desire
* Google analystics
* monetize from the company


# Solved problems:
* APP Overwrite problem:
    pack custom: exclude .git .DS_STORE database
* radio widget
* dynamic mailer
* split every: http://bit.ly/X2vFmx
* reference in record; and record default 11.04.2014

# Notes:
* m.llbean.com scrape:
`http://m.llbean.com/webapp/wcs/stores/servlet/ShowEcmInstance?storeId=1&catalogId=1&langId=-1&nav=gn-hp&ecmCategoryId=504987&relType=AD`

* Use web developer tracker "Network"