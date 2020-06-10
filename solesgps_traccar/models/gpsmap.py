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
        opciones                        ={}        
        opciones["fields"]              =""
        opciones["values"]              =""
        opciones["fields_value"]        =""

        fields                          =""
        values                          =""
        fields_value                    =""
        if('license_plate' in vals):
            fields                      ="%s name," %(fields)             
            values                      ="%s'%s'," %(values, vals["license_plate"])
            fields_value                ="%s name='%s'," %(fields_value, vals["license_plate"])
        if('imei' in vals):
            fields                      ="%s uniqueid," %(fields)             
            values                      ="%s'%s'," %(values, vals["imei"])
            fields_value                ="%s uniqueid='%s'," %(fields_value, vals["imei"])
        if('id' in vals):
            opciones["id"]              =vals["id"] 
        if(fields!=""):
            opciones["fields"]          =fields[ :len(fields)-1]      
            opciones["values"]          =values[ :len(values)-1]      
            opciones["fields_value"]    =fields_value[ :len(fields_value)-1]      
        return opciones
    def __CREATE(self,vals):
        print("CREATE ######################")
        opciones                        =self.__SAVE(vals)    
        if(opciones["fields"]!=""):            
            sql="INSERT INTO tc_devices (%s) VALUES(%s)" %(opciones["fields"],opciones["values"])
            self.env.cr.execute(sql)
            print(sql)
    def __WRITE(self,vals):
        print("WRITE ######################")
        opciones                        =self.__SAVE(vals)    
        if(opciones["fields"]!=""):            
            sql="UPDATE tc_devices SET %s WHERE id='%s' " %(opciones["fields_value"], opciones["id"] )
            self.env.cr.execute(sql)
            print(sql)

    def create(self,vals):
        self.__CREATE(vals)
        return super(vehicle, self).create(vals)
    def write(self,vals):
        print("WRITE ######################")                
        imei                            =self.imei
        self.env.cr.execute("SELECT * FROM tc_devices WHERE uniqueid='%s'" %(imei))        
        devices_data                    =self.env.cr.dictfetchall()
        if len(devices_data)>0:         
            for devices in devices_data:
                vals2                   =vals
                vals2["id"]             =opciones["id"]
                self.__CREATE(vals2)
        else:
            self.__CREATE(vals)    

        return super(vehicle, self).write(vals)
