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
    
    """
    def init(self):
        self.env.cr.execute("ALTER TABLE public.tc_positions ADD COLUMN read integer;")
        self.env.cr.execute("ALTER TABLE public.tc_positions ALTER COLUMN read SET NOT NULL;")
        self.env.cr.execute("ALTER TABLE public.tc_positions ALTER COLUMN read SET DEFAULT 0;")
    #"""
    def run_scheduler_get_position2(self):
        vehicle_obj                             =self.env['fleet.vehicle']

        devices                     ={}
        """
            SELECT 
	            CASE 				            
		            WHEN tp.attributes::json->>'alarm'!='' THEN 'alarm'
		            WHEN tp.attributes::json->>'motion'='false' THEN 'deviceStopped'
		            WHEN tp.attributes::json->>'motion'='true' THEN 'deviceOnline'
		            ELSE te.type
	            END	
                as status,            
                tp.protocol,fv.id as deviceid,tp.servertime,tp.devicetime,tp.fixtime,tp.valid,tp.latitude,tp.longitude,
                tp.altitude,tp.speed,tp.course,tp.address,tp.attributes
            FROM tc_positions tp 
                JOIN tc_devices td ON tp.deviceid=td.id 
                JOIN fleet_vehicle fv ON fv.imei=td.uniqueid
                LEFT JOIN tc_events te ON te.deviceid=td.id AND te.positionid=tp.id
            WHERE tp.read=0 
            ORDER BY tp.devicetime DESC 
        """


        self.env.cr.execute("""
            SELECT 
	            CASE 				            
		            WHEN tp.attributes::json->>'alarm'!='' THEN 'alarm'
		            WHEN tp.attributes::json->>'motion'='false' THEN 'deviceStopped'
		            WHEN tp.attributes::json->>'motion'='true' THEN 'deviceOnline'
		            ELSE 'deviceOnline'
	            END	
                as status,            
                tp.protocol,fv.id as deviceid,tp.servertime,tp.devicetime,tp.fixtime,tp.valid,tp.latitude,tp.longitude,
                tp.altitude,tp.speed,tp.course,tp.address,tp.attributes
            FROM tc_positions tp 
                JOIN tc_devices td ON tp.deviceid=td.id 
                JOIN fleet_vehicle fv ON fv.imei=td.uniqueid
            WHERE tp.read=0 
            ORDER BY tp.devicetime DESC 
        """)
        positions                   =self.env.cr.dictfetchall()
        
        self.env.cr.execute("UPDATE tc_positions SET read=1 WHERE read=0")        
        for position in positions:  
        
        
        
        
        
                  
            self.create(position)
class vehicle(models.Model):
    _inherit = "fleet.vehicle"    

    def __SAVE(self,datas):           
        vals                            =datas["new"]

        fields                          =""
        values                          =""
        fields_value                    =""
                
        if('license_plate' in vals):
            fields                      ="%s name," %(fields)             
            values                      ="%s'%s'," %(values, vals["license_plate"])
            fields_value                ="%s name='%s'," %(fields_value, vals["license_plate"])
        if('imei' in vals ):
            fields                      ="%s uniqueid," %(fields)             
            values                      ="%s'%s'," %(values, vals["imei"])
            fields_value                ="%s uniqueid='%s'," %(fields_value, vals["imei"])

        if(fields!=""):
            fields                      =fields[ :len(fields)-1]      
            values                      =values[ :len(values)-1]      
            fields_value                =fields_value[ :len(fields_value)-1]      
                        
            if(datas["method"]=="create"):
                sql="INSERT INTO tc_devices (%s) VALUES(%s)" %(fields,values)
            else:
                old                     =datas["old"]                 
                sql="UPDATE tc_devices SET %s WHERE id='%s' " %(fields_value, old["id"] )    
            
            self.env.cr.execute(sql)
    @api.model                   
    def create(self,vals):
        if len(vals)>0:
            datas                   ={}
            datas["method"]         ="create"
            datas["new"]            =vals
            self.__SAVE(datas)

        return super(vehicle, self).create(vals)
    def write(self,vals):
        if len(vals)>0:
            datas                   ={}
            datas["method"]         ="create"
            datas["new"]            =vals

            self.env.cr.execute("SELECT * FROM tc_devices WHERE uniqueid='%s'" %(self.imei))        
            devices_data                    =self.env.cr.dictfetchall()
            if len(devices_data)>0:
                datas["method"]     ="write"
                datas["old"]        =devices_data[0]         

            self.__SAVE(datas)                        
        return super(vehicle, self).write(vals)
