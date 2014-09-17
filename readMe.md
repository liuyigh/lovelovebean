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
* brush up UI, launch beta
    - optimal price scale
    - _all deals_  
* _run @reboot worker at screen_


# Second Priorities:
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
* Automatic database backup
* Big Data: present deal distributions
* API deal mail
    - username merge
    - iter every 100 recepients
* UI: 
    - logo; LoveLoveBean
    - Web Design CSS
    - homepage show current item
    - SMTP mailer issue email template:   
        - register email
        - reset pwd email
        - use auth() verification codes
* Marketing:
    - Twitter
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


# Solved problems:
* APP Overwrite problem:
    pack custom: exclude .git .DS_STORE database
* radio widget
* dynamic mailer
* split every: http://bit.ly/X2vFmx