# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to LoveLoveBean!")
    response.title = 'LoveLoveBean'
    return dict(message=XML("L.L.Bean Deals for &#9792 / &#9794 : <br> Get or exclude Women's or Men's products using new gender-based filter!"))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    if request.args(0)=='profile':
        db.auth_criteria.user_id.default = auth.user.id
        record = db.auth_criteria(db.auth_criteria.user_id==auth.user.id)
        formFil=SQLFORM(db.auth_criteria, 
            record=record,
            labels = {'salePrice':XML('<h3>TWO-A-DAY Clothing & Home Goods</h3> (By Sale Price)'), 
                      'tgPrice':XML('<h3>ONE-A-DAY Travel and Gear </h3> (By Sale Price)'),
                      'aveRev':XML('<b>By Avereage Ratings</b>'),
                      'percSave':XML('<b>By Percentage Saved</b>'),
                      'genderPref':XML('<h3>By Gender of Products</h3> AND-gate. Other filters apply')
                      },
            buttons = [TAG.button('Set Mine', _class='btn-primary')])
        if formFil.process().accepted:
            response.flash = XML('Your preference is recorded. <br>Get ready for lovely beans.')
        return dict(form=auth(), formFil=formFil)
    else:
        return dict(form=auth())



@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
