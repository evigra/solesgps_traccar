# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime
import requests
import random
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
class vehicle(models.Model):
    _inherit = "fleet.vehicle"    
    def create(self,vals):
        print('CREATE LALO====================')        

        #sql="INSERT INTO tc_devices (name,uniqueid,phone,disabled,speed) VALUES ('",vals["name"]"','",vals["uniqueid"],"','",vals["phone"],"','",vals["disabled"],"','",vals["speed"],"')"
        #sql="INSERT INTO tc_devices (name,uniqueid,phone,speed) VALUES ('",vals["name"]"','",vals["uniqueid"],"','",vals["phone"],"','",vals["speed"],"')"
        #sql="INSERT INTO tc_devices VALUES ('id','name','uniqueid','lastupdate','positionid','groupid','attributes','phone','model','contact','category','disabled','speed')"
        #vals = {'name': 'ABC', 'standard':10}
        #print(sql)        
        return super(vehicle, self).create(vals)

    def write(self,vals):
        print('WRITE LALO====================')        

        #sql="INSERT INTO tc_devices (name,uniqueid,phone,disabled,speed) VALUES ('",vals["name"]"','",vals["uniqueid"],"','",vals["phone"],"','",vals["disabled"],"','",vals["speed"],"')"
        #sql='INSERT INTO tc_devices (name,uniqueid,phone,speed) VALUES ("',vals["name"],'","',vals["uniqueid"],'","',vals["phone"],'","',vals["speed"],'")'
        #sql="INSERT INTO tc_devices VALUES ('id','name','uniqueid','lastupdate','positionid','groupid','attributes','phone','model','contact','category','disabled','speed')"
        #vals = {'name': 'ABC', 'standard':10}
        print(vals)

        fields_name =""
        fields_value=""

        if vals:
            if 'name' in vals:
                fields_name =fields_name,"name,"
                fields_value=fields_value,"'",vals["name"],"',"
            if 'uniqueid' in vals:
                fields_name =fields_name,"uniqueid,"
                fields_value=fields_value,"'",vals["uniqueid"],"',"
            if fields_name!='':
                sql="INSERT INTO tc_devices (", fields_name ,") VALUES (",fields_value,")"
                print(sql)                     
                #nov 18  sep 18 ene 19                 
        
        return super(vehicle, self).write(vals)
