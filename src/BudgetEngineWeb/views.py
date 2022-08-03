from pprint import PrettyPrinter
from textwrap import indent
from flask import Blueprint,render_template,request,flash
from flask_login import login_required, current_user
from bson.json_util import dumps
import pandas as pd
import json
from bson import ObjectId, json_util
from BudgetEngine import *
import pprint
from BudgetEngine.accts import Acct

from BudgetEngine.users import User
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/accts', methods=['GET','POST'])
def accts():
    account = request.args.get('acct')
    if account != None:
        acct=Acct(acct)
    else:
        acct=account
    accts = be.listCollection("accounts")
    accts = be.convDf(accts)
    accts = list(accts.itertuples(index=True, name=None))
    output = be.getTxData(account)
    txdf = be.mongoArrayDf(output,'PostedTxs')
    txdf = list(txdf.itertuples(index=True, name=None))
    return render_template("accts.html", acct=acct, txdata=txdf, accts=accts)

@views.route('/rev', methods=['GET', 'POST'])
def rev():
    accts = be.listCollection("accounts")
    accts = be.convDf(accts)
    accts = list(accts.itertuples(index=True, name=None))
    if request.method == 'POST':
        NewRevName=request.form.get('NewRevName')
        NewRevInst=request.form.get('NewRevInst')
        NewRevAcct=request.form.get('NewRevAcct')
        NewRevAmount=request.form.get('NewRevAmount')
        NewRevFreq=request.form.get('NewRevFreq')
        NewRevStartDate=request.form.get('NewRevStartDate')
        NewRevEnd=request.form.get('NewRevEnd')

        if len(NewRevName) < 1:
            flash('NewRevName must be greater than 1 characters', category='error')
        elif len(NewRevInst) < 1:
            flash('NewRevInst must be greater than 1 characters', category='error')
        elif len(NewRevAcct) < 1:
            flash('NewRevAcct must be greater than 1 characters', category='error')
        elif len(NewRevAmount) < 1:
            flash('NewRevAmount must be greater than 1 characters', category='error')
        elif len(NewRevFreq) < 1:
            flash('NewRevFreq must be greater than 1 characters', category='error')
        elif len(NewRevStartDate) < 1:
            flash('NewRevStartDate must be greater than 1 characters', category='error')
        elif len(NewRevEnd) < 1:
            flash('NewRevEnd must be greater than 1 characters', category='error')
        else: 
            flash('Revenue Created!', category='success')
            print(NewRevName, NewRevInst, NewRevAcct, NewRevAmount, NewRevFreq, NewRevStartDate, NewRevEnd)
    return render_template("new-rev.html", accts=accts)