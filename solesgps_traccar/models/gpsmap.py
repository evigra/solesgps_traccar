# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime
import requests
import random
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _

"""
class tc_devices(models.Model):
    _name = "tc_devices"
    _description = 'Traccar devices'

    name            = fields.Char('Name', size=128)
    uniqueid        = fields.Char('Description', size=128)
"""
    
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
       
        fields      =""
        fields_value=""

        if('name' in vals):
            vals            =vals["name"]
            fields          ="{fields}, name"            
            fields_value    ="{fields_value},'{vals}'"
        if('imei' in vals):
            vals            =vals["imei"]
            fields          ="{fields}, uniqueid"            
            fields_value    ="{fields_value},'{vals}'"

        if(fields!= False):
            sql="INSERT INTO tc_devices ({fields}) VALUES({fields_value})"
            print(sql)                     
            #nov 18  sep 18 ene 19                 

            return super(vehicle, self).write(vals)
