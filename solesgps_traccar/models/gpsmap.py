# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime
import requests
import random
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _

class tc_devices(models.Model):
    _name = "tc_devices"
    _description = 'Traccar devices'

    name                            =fields.Char('Name', size=128)
    uniqueid                        =fields.Char('Description', size=128)

    def __SAVE(self,vals):
        if('imei' in vals):
            vals.uniqueid           =vals["imei"]
            del vals["imei"]                   
        return vals
    def create(self,vals):
        vals                        =self.__SAVE(vals)
        return super(tc_devices, self).create(vals)
    def write(self,vals):
        vals                        =self.__SAVE(vals)
        return super(tc_devices, self).write(vals)
class positions(models.Model):
    _inherit = "gpsmap.positions"

    def run_scheduler_get_position2(self):
        self.env.cr.execute("""SELECT * FROM tc_positions LIMIT 10""")

        for product_data in self.env.cr.dictfetchall():
            print(product_data)            
    
class vehicle(models.Model):
    _inherit = "fleet.vehicle"    

    def __SAVE(self,vals):
        devices                         ={}        
        sql                             =""
        if('name' in vals):
            val                         =vals["name"]
            sql                         ="{sql} name='{val}',"
        if('imei' in vals):
            val                         =vals["imei"]
            sql                         ="{sql} uniqueid='{val}',"
        return sql
    def __CREATE(self,vals):
        print("CREATE ######################")
        sql                             =self.__SAVE(vals)    
        if(sql!=""):
            sql="INSERT INTO tc_devices SET {sql}"
            print(sql)

    def create(self,vals):
        self.__CREATE(vals)    
        return super(vehicle, self).create(vals)
    def write(self,vals):
        print("WRITE ######################")                
        imei                            =self.imei
        self.env.cr.execute("SELECT * FROM tc_devices WHERE uniqueid='{imei}'")        
        devices_data                    =self.env.cr.dictfetchall()
        if len(devices_data)>0:         
            for devices in devices_data:
                tc_devices_obj.write(self.__SAVE(vals))    
        else:
            self.__CREATE(vals)    

        return super(vehicle, self).write(vals)
