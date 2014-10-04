# Filters:
* All Deals (under price filter)
* sale Price (class="toOrderItemSalePrice")
    <= 24.99; <=49.99; <= 99.99; None(-1)
* Title Keywords (id="ppHeader")
    - unicode (currently ignored)
* Details Keywords (id="ppDetails")
* Review numbers (class="reviewsNumber")
    - No Review (as 0)
* Average reviews (id="ATBProdStarReviews" | title="")
    - No Review (as None)
* Original Price (class="toOrderItemStrikeOutPrice")
* abso. save (class="toOrderItemSaleText")
* percent save (class="toOrderItemSaleText" itemprop="description"")
* saleID (timestamp)
* prodID
* pictures (link only?) '//img[@name="ecm_main"]/@src'
* Regular Tall Petite
* Daily Travel Gear 510312
    
	
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
* 510312
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
* Fail proof for all steps: notify me when error.
* _Cron watchdog_
* Automatic database backup
* Big Data: present deal distributions
* API deal mail
    - username merge
    - *|itemDetails|*
    - iter every 100 recepients
* UI: 
    - logo; LoveLoveBean
    - blog: introducing LLB
    - Web Design CSS: mobile
    - homepage show current item
    - SMTP mailer issue email template:   
        - register email
        - reset pwd email
        - use auth() verification codes
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

# Notes:
* m.llbean.com scrape:
`http://m.llbean.com/webapp/wcs/stores/servlet/ShowEcmInstance?storeId=1&catalogId=1&langId=-1&nav=gn-hp&ecmCategoryId=504987&relType=AD`

* Use web developer tracker "Network"