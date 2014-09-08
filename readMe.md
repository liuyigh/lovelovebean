# Filters:
* All Deals (under price filter)
* sale Price (class="toOrderItemSalePrice")
    <= 24.99; <=49.99; <= 99.99
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
* pictures (link only?)
* Regular Tall Petite
* Daily Travel Gear 510312
    
# Functions:
	
## First Priorities:
* Scheduler DB: monitor worker and failure
* record saleItem DB
* **User filter DB: salePrice**
* match and mark to send: toSend
* send email
    - use mandrill: SMTP and API
    - use auth verification


## Second Priorities:
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
* enrich email template
    - deal notice
    - register email
* Fail proof for all steps: notify me when error.
* Big Data: present deal distributions
* UI: 
    - logo; LoveLoveBean
    - Web Design CSS
* Marketing:
    - Twitter
* UserVoice (1000 Registered Users):
    - Feature voting

## Third Priorities:
* User priority membership DB field (0,1,2)
* match and record DB
* advanced big data
* advanced deal combinations if user desire
* Google analystics


# Solved problems:
* APP Overwrite problem:
    pack custom: exclude .git .DS_STORE database