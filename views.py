from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.db import connections
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http.response import JsonResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.utils.encoding import smart_str
from django.http import JsonResponse
from django.db import connection as conn
from django.views.decorators.clickjacking import xframe_options_exempt

# from django.contrib.gis.geos import Point
# from django.contrib.gis.geos import GEOSGeometry
# from django.contrib.gis.measure import D

import base64
import io
import sys
import os
import json
import re
# from pandas import read_sql,DataFrame,to_numeric
import secrets
from time import sleep,time
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import logging
import requests as rqs
from blogs.models import *

from bs4 import BeautifulSoup
import boto3
import pandas as pd
import random
import plotly.express as px
import plotly.graph_objects as go
import matplotlib
import random
import numpy as np
from collections import Counter
import pickle
import shapely
import geopandas as gp
from shapely.geometry import LineString, Point, LinearRing
import pyproj
from math import sin, cos, sqrt, atan2, radians
import time
from tqdm import tqdm
from sqlite3 import Error
import sqlite3 as lite
from math import*
from scipy.spatial.distance import cdist
import h3
import geopandas as gp
from shapely.geometry import Polygon
from shapely import wkt
import psycopg2
from csp.decorators import csp
import pyproj
geod = pyproj.Geod(ellps='WGS84')
import math # or numpy

DATE2STR = psycopg2.extensions.new_type(
    psycopg2.extensions.DATE.values,
    'DATE2STR',
    lambda value, curs:
        str(value) if value is not None else None)

psycopg2.extensions.register_type(DATE2STR)

def get_last_months(start_date, months):
    for i in range(months):
        yield (start_date.year,start_date.month)
        start_date += relativedelta(months = -1)

us_state_abbrev = {
	    'Alabama': 'AL',
	    'Alaska': 'AK',
	    'American Samoa': 'AS',
	    'Arizona': 'AZ',
	    'Arkansas': 'AR',
	    'California': 'CA',
	    'Colorado': 'CO',
	    'Connecticut': 'CT',
	    'Delaware': 'DE',
	    'District of Columbia': 'DC',
	    'Florida': 'FL',
	    'Georgia': 'GA',
	    'Guam': 'GU',
	    'Hawaii': 'HI',
	    'Idaho': 'ID',
	    'Illinois': 'IL',
	    'Indiana': 'IN',
	    'Iowa': 'IA',
	    'Kansas': 'KS',
	    'Kentucky': 'KY',
	    'Louisiana': 'LA',
	    'Maine': 'ME',
	    'Maryland': 'MD',
	    'Massachusetts': 'MA',
	    'Michigan': 'MI',
	    'Minnesota': 'MN',
	    'Mississippi': 'MS',
	    'Missouri': 'MO',
	    'Montana': 'MT',
	    'Nebraska': 'NE',
	    'Nevada': 'NV',
	    'New Hampshire': 'NH',
	    'New Jersey': 'NJ',
	    'New Mexico': 'NM',
	    'New York': 'NY',
	    'North Carolina': 'NC',
	    'North Dakota': 'ND',
	    'Northern Mariana Islands':'MP',
	    'Ohio': 'OH',
	    'Oklahoma': 'OK',
	    'Oregon': 'OR',
	    'Pennsylvania': 'PA',
	    'Puerto Rico': 'PR',
	    'Rhode Island': 'RI',
	    'South Carolina': 'SC',
	    'South Dakota': 'SD',
	    'Tennessee': 'TN',
	    'Texas': 'TX',
	    'Utah': 'UT',
	    'Vermont': 'VT',
	    'Virgin Islands': 'VI',
	    'Virginia': 'VA',
	    'Washington': 'WA',
	    'West Virginia': 'WV',
	    'Wisconsin': 'WI',
	    'Wyoming': 'WY'
	}
us_state_abbrev_codes={}
for i in us_state_abbrev.items():
    us_state_abbrev_codes[i[1]]=i[0]
df1x=pd.read_sql("select * from import.loads_raw LIMIT 10;",conn)
COLOURS=list(matplotlib.colors.cnames.values()) 
np.random.shuffle(COLOURS)
loads_dtype={
         'created_week': int,
          'duration': float,
          'asset_shipment_origin_namedCoordinates_latitude': float,
          'asset_shipment_origin_namedCoordinates_longitude': float,
          'asset_shipment_destination_namedCoordinates_latitude': float,
          'asset_shipment_destination_namedCoordinates_longitude': float,
          'asset_shipment_origin_namedCoordinates_stateProvince': str,
          'asset_shipment_origin_namedCoordinates_city': str,
          'asset_shipment_destination_namedCoordinates_stateProvince': str,
          'asset_shipment_destination_namedCoordinates_city': str,
          'asset_assetId': str,
          'callback_userId': str,
          'callback_companyName': str,
         'destination_data': str,
          'travel_data': str,
         'origin_data': str,
          'created_at': str
     }
trucks_dtype={
       'created_week': int,
      'duration': float,
      'asset_equipment_origin_namedCoordinates_latitude': float,
      'asset_equipment_origin_namedCoordinates_longitude': float,
      'asset_equipment_destination_place_namedCoordinates_latitude': float,
      'asset_equipment_destination_place_namedCoordinates_longitude': float,
      'asset_equipment_origin_namedCoordinates_stateProvince': str,
      'asset_equipment_origin_namedCoordinates_city': str,
      'asset_equipment_destination_place_namedCoordinates_stateProvince': str,
      'asset_equipment_destination_place_namedCoordinates_city': str,
      'asset_assetId': str,
      'callback_userId': str,
      'callback_companyName': str,
         'destination_data': str,
      'travel_data': str,
         'origin_data': str,
      'created_at': str
     }
# dirz=f"{os.getcwd()}/loads/"
# df_load = pd.read_csv(dirz+"MAP_loads.csv",
# 		parse_dates=['asset_status_created_date'],
# 	                 dtype=loads_dtype)
df_load = pd.read_sql("select * from import.loads_raw LIMIT 1000;",conn)
# dirz=f"{os.getcwd()}/trucks/"
# df_truck = pd.read_csv(dirz+"MAP_trucks.csv",
# 				parse_dates=['asset_status_created_date'],
# 			                 dtype=trucks_dtype)
df_truck = pd.read_sql("select * from import.trucks_raw LIMIT 1000;",conn)

with open(f"{os.getcwd()}/locations_data1.txt", "rb") as fp:   # Unpickling
  locations_data1 = pickle.load(fp) 

with open(f"{os.getcwd()}/features1.txt", "rb") as fp:   # Unpickling
  features1 = pickle.load(fp) 


zone_df2=pd.read_csv(f"{os.getcwd()}/zipcode.csv",dtype={'zip':str})

zone_df2['location'] = zone_df2[['state','city']].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

zone_df2['location'] = zone_df2['location'].str.upper()

dct={}
for i in zone_df2.itertuples():
    dct[i[8]]=i[1][0]


now = datetime.now()
if len(str(now.month))<2:
	month_x='0'+str(now.month)
else:
	month_x=str(now.month)
year_x=str(now.year)
lmonths=[i for i in get_last_months(datetime.today(), 3)]
lm=[]
for x in lmonths:
    if  len(str(x[1]))<2:
        lm.append((x[0],'0'+str(x[1])))
    else:
        lm.append((x[0],x[1]))
df_gd=pd.read_csv(f"{os.getcwd()}/gold_data/gold_wanted_customer_05032021_.csv",
               parse_dates=['booked_on'])
df_gd['travel_data']=df_gd[['origin_data', 'destination_data']].agg('->'.join, axis=1)

# df_gd=pd.read_sql(f"select * from gold_oldnew \
#                       ;",conn,parse_dates={'booked_on': {'format': '%Y-%m-%d'},
#                                                                                'picked_up_by': {'format': '%Y-%m-%d %H:%M:%S'},
#                                                                                'delivered_on': {'format': '%Y-%m-%d %H:%M:%S'}})#where booked_on LIKE '{str(lm[0][0])}-{str(lm[0][1])}%' or \
#                 #   booked_on LIKE '{str(lm[1][0])}-{str(lm[1][1])}%' or booked_on LIKE '{str(lm[2][0])}-{str(lm[2][1])}%'
# df_gd['origin_data'] = df_gd[['origin_state_province','origin_city']].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

# df_gd['destination_data'] = df_gd[['destination_state_province','destination_city']].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

# df_gd['origin_data'] = df_gd['origin_data'].str.upper()
# df_gd['destination_data'] = df_gd['destination_data'].str.upper()

# df_gd['origin_zone'] = df_gd[['origin_data','id']].apply(lambda row: dct.get(row['origin_data'],'x'), axis=1)

# df_gd['destination_zone'] = df_gd[['destination_data','id']].apply(lambda row: dct.get(row['destination_data'],'x'), axis=1)

# df_gd=df_gd[~df_gd['booked_on'].astype(str).str.startswith('N')]
# # df_gd['created_at'] = df_gd['booked_on'].map(lambda x: x.strftime('%Y-%m-%d'))
# df_gd['created_week']=df_gd['booked_on'].apply(lambda x : x.strftime("%U"))#%U#%W
# df_gd['created_week']=df_gd['created_week'].astype(int)
# df_gd['created_year']=df_gd['booked_on'].apply(lambda x : x.strftime("%Y"))
# df_gd['created_year']=df_gd['created_year'].astype(int)
# df_gd['created_month']=df_gd['booked_on'].apply(lambda x : x.strftime("%B"))
# df_gd['created_month_num']=df_gd['booked_on'].apply(lambda x : x.strftime("%m"))
# df_gd['created_month_num']=df_gd['created_month_num'].astype(int)

# df_gd=df_gd[(df_gd['origin_zone']!='x') & (df_gd['destination_zone']!='x')]

# df_gd=df_gd[~((df_gd['destination_lat'].astype(str).str.startswith('nan')) |\
#                 (df_gd['origin_lat'].astype(str).str.startswith('nan')))]
# df_gd['year_week']=df_gd['created_year'].astype(str)+df_gd['created_week'].astype(str)
# df_gd['duration']=(df_gd['picked_up_by'] - df_gd['booked_on']) / pd.Timedelta(hours=1)
# df_gd['travel_data']=df_gd[['origin_data', 'destination_data']].agg('->'.join, axis=1)
# df_gd.to_csv(f"{os.getcwd()}/gold_data/gold_wanted_customer_05032021__.csv",index=[0])

with open(f"{os.getcwd()}/locations_data.txt", "rb") as fp:   # Unpickling
  locations_data = pickle.load(fp) 

with open(f"{os.getcwd()}/features.txt", "rb") as fp:   # Unpickling
  features = pickle.load(fp) 


with open(f"{os.getcwd()}/lanes/lanes.txt", "rb") as fp:   # Unpickling
  lanes = pickle.load(fp)  
with open(f"{os.getcwd()}/lanes/all_lanes.txt", "rb") as fp:   # Unpickling
  all_lanes = pickle.load(fp)
with open(f"{os.getcwd()}/lanes/all_shippers_lanes.txt", "rb") as fp:   # Unpickling
  all_shippers_lanes = pickle.load(fp)
with open(f"{os.getcwd()}/lanes/all_receivers_lanes.txt", "rb") as fp:   # Unpickling
  all_receivers_lanes = pickle.load(fp)
with open(f"{os.getcwd()}/lanes/all_prices_lanes.txt", "rb") as fp:   # Unpickling
  all_prices_lanes = pickle.load(fp)
with open(f"{os.getcwd()}/lanes/all_loads_lanes.txt", "rb") as fp:   # Unpickling
  all_loads_lanes = pickle.load(fp)


with open(f"{os.getcwd()}/customers/customers.txt", "rb") as fp:   # Unpickling
  customers = pickle.load(fp)  
with open(f"{os.getcwd()}/customers/all_customers.txt", "rb") as fp:   # Unpickling
  all_customers = pickle.load(fp)
with open(f"{os.getcwd()}/customers/all_shippers_customers.txt", "rb") as fp:   # Unpickling
  all_shippers_customers = pickle.load(fp)
with open(f"{os.getcwd()}/customers/all_receivers_customers.txt", "rb") as fp:   # Unpickling
  all_receivers_customers = pickle.load(fp)
with open(f"{os.getcwd()}/customers/all_lanes_customers.txt", "rb") as fp:   # Unpickling
  all_lanes_customers = pickle.load(fp)
with open(f"{os.getcwd()}/customers/all_prices_customers.txt", "rb") as fp:   # Unpickling
  all_prices_customers = pickle.load(fp)
with open(f"{os.getcwd()}/customers/all_loads_customers.txt", "rb") as fp:   # Unpickling
  all_loads_customers = pickle.load(fp)

dirz=f"{os.getcwd()}/cb_2018_us_nation_5m/cb_2018_us_nation_5m.shp"
usa = gp.GeoDataFrame.from_file(dirz)
usa.to_crs(epsg=4326, inplace=True)

hexes=pd.read_sql("select tile_id,ST_AsText(geom) as geom from usa_hex_3",conn)
hexes['geom'] = gp.GeoSeries.from_wkt(hexes['geom'])
hexes = gp.GeoDataFrame(hexes, geometry='geom')

locx=pd.read_sql("select distinct origin_state,origin_city, destination_state,\
               destination_city from otr_data_loads where origin_state IS NOT NULL ",conn)
states_list=list(set(locx['origin_state'].values.tolist()+locx['destination_state'].values.tolist()))
states_list=[x for x in states_list if x]
states_list=sorted(states_list)
cities_list=list(set(locx['origin_city'].values.tolist()+locx['destination_city'].values.tolist()))
cities_list=[x for x in cities_list if x]
cities_list=sorted(cities_list)
# df_otr=pd.read_sql("""SELECT odl.*,hexes.geom,hexes.tile_id,
# 				ST_AsText(odl.lane_line_str) as lane_geom
# FROM
# 	usa_hex_3 AS hexes
# 	INNER JOIN
# 	otr_data_loads AS odl
# 	ON ST_Intersects(odl.destination_geography::geometry, hexes.geom::geometry) LIMIT 10000;""",conn)



def jaccard_similarity(x,y):
 
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)

@xframe_options_exempt
def index(response):
	print(os.getcwd())
	return render(response ,'blogs/index.html')

@xframe_options_exempt
def network_graph1(response):

	dff = pd.read_csv(f"{os.getcwd()}/trucks_loads_2019_small.csv",index_col=0)
	dff['trucks']=dff['trucks'].astype(int)
	cn=list(dff[dff['trucks']==0].groupby('callback_companyName').count()['callback_userId'].sort_values(ascending=False)[10:20].index)
	tn=list(dff[dff['trucks']==1].groupby('callback_companyName').count()['callback_userId'].sort_values(ascending=False)[10:20].index)

	od=list(dff.groupby('origin_data').count()['callback_userId'].sort_values(ascending=False)[10:20].index)
	dd=list(dff.groupby('destination_data').count()['callback_userId'].sort_values(ascending=False)[10:20].index)
	cat=response.GET.get('cat',None)
	cat='company'
	company=response.GET.getlist('company[]',None)
	route=True
	if not route:
		if company:
			df = pd.read_csv(f"{os.getcwd()}/trucks_loads_2019_small.csv",index_col=0)
			frames=[]
			for i in company:
				df0 = df[df['callback_companyName']==i][0:5]
				frames.append(df0)
			df1=pd.concat(frames)
			org_dest=df1['origin_data'].values.tolist()+df1['destination_data'].values.tolist()
			df2=df[(df['origin_data'].isin(org_dest)) | \
			(df['destination_data'].isin(org_dest))]
			df4=df[(df['origin_data'].isin(df1['origin_data'].values.tolist()) | \
				 df['origin_data'].isin(df1['destination_data'].values.tolist()) ) & (df['trucks']==1)]
			df_1=pd.concat([df1,df2,df4])
		else:
			df = pd.read_csv(f"{os.getcwd()}/trucks_loads_2019_small.csv",index_col=0)
			df1=dff.head(50)
			df2=dff.tail(50)
			df_1=pd.concat([df1,df2])

		carrier=response.GET.getlist('carrier[]',None)
		if carrier:
			frames=[]
			for i in carrier:
				df0 = df[df['callback_companyName']==i][0:5]
				frames.append(df0)
			df1=pd.concat(frames)
			org_dest=df1['origin_data'].values.tolist()
			df2=df[((df['origin_data'].isin(org_dest)) | \
			(df['destination_data'].isin(org_dest))) & (df['trucks']==0)]
			df_2=pd.concat([df1,df2])
		else:
			df_2=[]

		location=response.GET.getlist('location[]',None)
		if location:
			frames=[]
			for i in location:
				df0 = df[(df['origin_data']==i) | (df['destination_data']==i)][0:10]
				frames.append(df0)
			df1=pd.concat(frames)
			df2=df[(df['origin_data'].isin(location)) | \
			(df['destination_data'].isin(location)) & (df['trucks']==1)][0:5]
			df3=df[(df['origin_data'].isin(location)) | \
			(df['destination_data'].isin(location)) & (df['trucks']==0)][0:5]
			df_3=pd.concat([df1,df2,df3])
		else:
			df_3=[]

	else:
		if company:
			df = pd.read_csv(f"{os.getcwd()}/trucks_loads_2019_small.csv",index_col=0)
			frames=[]
			for i in company:
				df0 = df[df['callback_companyName']==i][0:5]
				frames.append(df0)
			df1=pd.concat(frames)
			org_dest=df1['travel_data'].values.tolist()
			df2=df[(df['travel_data'].isin(org_dest))][0:10]
			df4=df[(df['travel_data'].isin(df1['travel_data'].values.tolist()) ) & (df['trucks']==1)]
			df_1=pd.concat([df1,df2,df4])
		else:
			df = pd.read_csv(f"{os.getcwd()}/trucks_loads_2019_small.csv",index_col=0)
			df1=dff.head(50)
			df2=dff.tail(50)
			df_1=pd.concat([df1,df2])

		carrier=response.GET.getlist('carrier[]',None)
		if carrier:
			frames=[]
			for i in carrier:
				df0 = df[df['callback_companyName']==i][0:5]
				frames.append(df0)
			df1=pd.concat(frames)
			org_dest=df1['travel_data'].values.tolist()
			df2=df[((df['travel_data'].isin(org_dest))) & (df['trucks']==0)]
			df_2=pd.concat([df1,df2])
		else:
			df_2=[]

		location=response.GET.getlist('location[]',None)
		if location:
			frames=[]
			for i in location:
				df0 = df[(df['origin_data']==i) | (df['destination_data']==i)][0:10]
				frames.append(df0)
			df1=pd.concat(frames)
			df2=df[(df['origin_data'].isin(location)) | \
			(df['destination_data'].isin(location)) & (df['trucks']==1)][0:5]
			df3=df[(df['origin_data'].isin(location)) | \
			(df['destination_data'].isin(location)) & (df['trucks']==0)][0:5]
			df_3=pd.concat([df1,df2,df3])
		else:
			df_3=[]




	framez=[df_1,df_2,df_3]
	framez=[x for x in framez if len(x)>1]
	df=pd.concat(framez)


	nodes = []
	nodes_list = []
	edges = []
	edges_list = []
	route_list=[]
	routes = True
	for i in df.itertuples():
	    if str(i[-1]) == '0':
	        if not str(i[6]) in nodes_list:
	        	if any(str(i[6]) == c for c in company):
		            dct = {}
		            dct['id'] = str(i[6])
		            dct['shape'] = 'image'
		            dct['image'] = 'https://www.flaticon.com/svg/vstatic/svg/993/993928.svg?token=exp=1619447677~hmac=104a901d7d6c1d2f1c6914783a9062d7'
		            dct['value'] = str(i[7]+1000)
		            dct['title'] = str(i[6])
		            # dct['color']='#FF4500'
		            nodes_list.append(str(i[6]))
		            nodes.append(dct)
		        else:
		            dct = {}
		            dct['id'] = str(i[6])
		            dct['shape'] = 'image'
		            dct['image'] = 'https://img.icons8.com/bubbles/100/000000/company.png'
		            dct['value'] = str(i[7])
		            dct['title'] = str(i[6])
		            # dct['color']='#FF4500'
		            nodes_list.append(str(i[6]))
		            nodes.append(dct)
	    else:
	        if not str(i[6]) in nodes_list:
	        	if any(str(i[6]) == c for c in carrier):
		            dct = {}
		            dct['id'] = str(i[6])
		            dct['shape'] = 'image'
		            dct['image'] = 'https://icons.iconarchive.com/icons/custom-icon-design/pretty-office-11/512/truck-icon.png'
		            dct['value'] = str(i[7]+1000)
		            dct['title'] = str(i[6])
		            # dct['color']='#FF4500'
		            nodes_list.append(str(i[6]))
		            nodes.append(dct)
		        else:	        		
		            dct = {}
		            dct['id'] = str(i[6])
		            dct['shape'] = 'image'
		            dct['image'] = 'https://pics.freeicons.io/uploads/icons/png/9436596671553508656-512.png'
		            dct['value'] = str(i[7])
		            dct['title'] = str(i[6])
		            # dct['color']='#FF4500'
		            nodes_list.append(str(i[6]))
		            nodes.append(dct)

	    if not routes:
	        if not str(i[2]) in nodes_list:
	            dct = {}
	            dct['id'] = str(i[2])
	            dct['shape'] = 'image'
	            dct['image'] = 'https://www.clipartmax.com/png/full/215-2158499_pushpin-clip-art.png'
	            dct['value'] = str(i[9])
	            dct['title'] = str(i[2])
	            # dct['physics']='false'
	            nodes_list.append(str(i[2]))
	            nodes.append(dct)
	        if not str(i[3]) in nodes_list:
	            dct = {}
	            dct['id'] = str(i[3])
	            dct['shape'] = 'image'
	            dct['image'] = 'https://www.clipartmax.com/png/full/215-2158499_pushpin-clip-art.png'
	            dct['value'] = str(i[10])
	            dct['title'] = str(i[3])
	            # dct['physics']='false'
	            nodes_list.append(str(i[3]))
	            nodes.append(dct)
	    else:
	        if not str(i[5]) in nodes_list:
	            dct = {}
	            dct['id'] = str(i[5])
	            dct['shape'] = 'image'
	            dct['image'] = 'https://png.pngtree.com/png-clipart/20190705/original/pngtree-vector-route-icon-png-image_4224386.jpg'
	            dct['value'] = str(i[8])
	            dct['title'] = str(i[5])
	            # dct['physics']='false'
	            nodes_list.append(str(i[5]))
	            nodes.append(dct)
	            route_list.append(str(i[5]))
	    if not routes:
	        if not (str(i[6]),str(i[2])) in edges_list:
	            if str(i[2])!='nan':
	                dct={}
	                dct['from'] = str(i[6])
	                dct['to'] = str(i[2])
	                dct['value']=str(i[11])
	                dct['title']=str(i[4])
	                edges_list.append((str(i[6]),str(i[2])))
	                edges.append(dct)
	        if not (str(i[6]),str(i[3])) in edges_list:
	            if str(i[3])!='nan':
	                dct={}
	                dct['from'] = str(i[6])
	                dct['to'] = str(i[3])
	                dct['value']=str(i[12])
	                dct['title']=str(i[4])
	                edges_list.append((str(i[6]),str(i[3])))
	                edges.append(dct)        
	    else:
	        if not (str(i[6]),str(i[5])) in edges_list:
	            if str(i[5])!='nan':
	                dct={}
	                dct['from'] = str(i[6])
	                dct['to'] = str(i[5])
	                dct['value']=str(i[13])
	                dct['title']=str(i[4])
	                edges_list.append((str(i[6]),str(i[5])))
	                edges.append(dct)
	            else:
	                if not (str(i[6]),str(i[2])) in edges_list:
	                    dct={}
	                    dct['from'] = str(i[6])
	                    dct['to'] = str(i[2])
	                    dct['value']=str(i[11])
	                    dct['title']=str(i[4])
	                    edges_list.append((str(i[6]),str(i[2])))
	                    edges.append(dct) 
	if len(nodes_list)==50:
		physics='false'
	else:
		physics='true'
	locations=od+dd
	locations=list(set(locations))
	return render(response ,'blogs/01_basic_usage.html',
		{'nodes':nodes,
		'edges':edges,
		'company':cn,
		'carriers':tn,
		'origin':od,
		'destination':dd,
		'locations':locations,
		'physics':physics})

@xframe_options_exempt
def graph_plotly(response):
	df=df_load.copy()
	df_from=df[df['origin_data']=='NE OMAHA']
	df_from=df_from[df_from['created_week']<=8]
	df_from.sort_values(by=['created_week'], inplace=True, ascending=True)

	created=df_from['created_week'].unique()
	companies_count=df_from.groupby('callback_companyName').size()
	companies_count.sort_values(ascending=False,inplace=True)
	companies_count=companies_count.head(30)
	companies_10=list(companies_count.index)
	routes_100=list(df_from['destination_data'].unique())
	routes_100=routes_100[:50]
	dff=pd.DataFrame(columns = ['created_week','company_name','loads_posted','total_loads'])
	
	# for route in tqdm(routes_100,total=len(routes_100)):
	for company in companies_10:
	        for i in created:
	            dct={}
	            dct["company_name"]=company
	            dct["created_week"]=i
	            tmp=df_from[(df_from['callback_companyName']==company)]
	            dct['loads_posted']=tmp[tmp['created_week']==i].count().max()
	            dct['total_loads']=tmp.count().max()
	            dff=dff.append(dct , ignore_index=True)
	dff[['loads_posted','total_loads']]=dff[['loads_posted','total_loads']].astype(int)
	fig = px.scatter(dff, x="company_name", y='loads_posted', 
                 animation_frame="created_week",
                 color="total_loads",size="loads_posted")
  
	fig["layout"].pop("updatemenus")
	fig.update_xaxes(
        tickangle = 45,
        title_text = "Company Name",
        title_font = {"size": 10},
        title_standoff = 25)

	fig.update_yaxes(
	        title_text = "Loads Posted",
	        title_standoff = 25)
	fig['layout']['sliders'][0]['pad']=dict(r= 10, t= 150,)
	graph = fig.to_html(full_html=False, default_height=1000, default_width=1000)
	context = {'graph': graph}
	return render(response ,'blogs/graph.html',context)

@xframe_options_exempt
def load_v_trucks(response):
	cat=response.GET.get('cat',None)
	
	ydf=df_truck.copy()
	tdf_from=tdf[tdf['origin_data']=='NE OMAHA']
	tdf_from=tdf_from[tdf_from['created_week']<=4]
	tdf_from.sort_values(by=['created_week'], inplace=True, ascending=True)

	df=df_load.copy()
	df_from=df[df['origin_data']=='NE OMAHA']
	df_from=df_from[df_from['created_week']<=4]
	df_from.sort_values(by=['created_week'], inplace=True, ascending=True)

	dff=df_from.groupby(['created_week']).count()['asset_assetId']
	tdff=tdf_from.groupby(['created_week']).count()['asset_assetId']
	fig = go.Figure(data=[
	    go.Bar(name='Loads', x=dff.index, y=list(dff.values)),
	    go.Bar(name='Trucks', x=tdff.index, y=list(tdff.values))
	])
	fig.update_xaxes(
        title_text = "Weeks",
        title_font = {"size": 20},
        title_standoff = 25)
	fig.update_yaxes(
	        title_text = "Loads/Trucks Posted",
	        title_font = {"size": 20},
	        title_standoff = 25)
	fig.update_layout(barmode='group')
	graph = fig.to_html(full_html=False, default_height=500, default_width=500)
	context = {'graph': graph}
	if cat:
		if cat=='company':
			dff=df_from.groupby(['callback_companyName']).count().sort_values(by='asset_assetId',ascending=False).reset_index()[:15]
			dff=dff[['callback_companyName','asset_assetId']]

			fig = px.bar(dff, x='callback_companyName', y='asset_assetId')
			fig.update_xaxes(
		        tickangle = 45,
		        title_text = "Company Name",
		        title_font = {"size": 20},
		        title_standoff = 25)
			fig.update_yaxes(
		        title_text = "#Loads Posted",
		        title_font = {"size": 20},
		        title_standoff = 25)
			graph1 = fig.to_html(full_html=False, default_height=500, default_width=500)
		elif cat=='location':
			dff=df_from.groupby(['destination_data']).count().sort_values(by='asset_assetId',ascending=False).reset_index()[:15]
			dff=dff[['destination_data','asset_assetId']]

			fig = px.bar(dff, x='destination_data', y='asset_assetId')
			fig.update_xaxes(
		        tickangle = 45,
		        title_text = "State and City",
		        title_font = {"size": 20},
		        title_standoff = 25)
			fig.update_yaxes(
		        title_text = "#Loads Posted",
		        title_font = {"size": 20},
		        title_standoff = 25)
			graph1 = fig.to_html(full_html=False, default_height=500, default_width=500)
		elif cat=='route':
			dff=df_from.groupby(['travel_data']).count().sort_values(by='asset_assetId',ascending=False).reset_index()[:15]
			dff=dff[['travel_data','asset_assetId']]

			fig = px.bar(dff, x='travel_data', y='asset_assetId')
			fig.update_xaxes(
		        tickangle = 45,
		        title_text = "Route",
		        title_font = {"size": 20},
		        title_standoff = 25)
			fig.update_yaxes(
		        title_text = "#Loads Posted",
		        title_font = {"size": 20},
		        title_standoff = 25)
			graph1 = fig.to_html(full_html=False, default_height=500, default_width=500)
		else:
			dff=df_from.groupby(['destination_data']).count().sort_values(by='asset_assetId',ascending=False).reset_index()[:15]
			dff=dff[['destination_data','asset_assetId']]

			fig = px.bar(dff, x='destination_data', y='asset_assetId')
			fig.update_xaxes(
		        tickangle = 45,
		        title_text = "State and City",
		        title_font = {"size": 20},
		        title_standoff = 25)
			fig.update_yaxes(
		        title_text = "#Loads Posted",
		        title_font = {"size": 20},
		        title_standoff = 25)
			graph1 = fig.to_html(full_html=False, default_height=500, default_width=500)
	else:
		dff=df_from.groupby(['destination_data']).count().sort_values(by='asset_assetId',ascending=False).reset_index()[:15]
		dff=dff[['destination_data','asset_assetId']]

		fig = px.bar(dff, x='destination_data', y='asset_assetId')
		fig.update_xaxes(
		        tickangle = 45,
		        title_text = "destination_data",
		        title_font = {"size": 20},
		        title_standoff = 25)
		graph1 = fig.to_html(full_html=False, default_height=500, default_width=500)
	context['graph1'] = graph1
	return render(response ,'blogs/loads_v_trucks.html',context)

@xframe_options_exempt
def map_arc(response):
	cat=response.GET.get('cat',None)

	tdf=df_truck.copy()

	tdf_from=tdf[tdf['origin_data']=='NE OMAHA']
	tdf_from=tdf_from[tdf_from['created_week']<=4]
	tdf_from.sort_values(by=['created_week'], inplace=True, ascending=True)

	df = pd.read_csv(f"{os.getcwd()}/omaha_loads_2021_01.csv",
		parse_dates=['asset_status_endDate','asset_status_startDate','asset_status_created_date'],
	                 dtype={
	                     'callback_userId': str,
	                     'creditScore_score': float,
	                     'asset_dimensions_weightPounds': float
	                 })

	df=df_load.copy()
	df_from=df[df['origin_data']=='NE OMAHA']
	df_from=df_from[df_from['created_week']<=4]
	df_from.sort_values(by=['created_week'], inplace=True, ascending=True)
	df_map=df_from.groupby(['asset_shipment_destination_namedCoordinates_latitude',
	                   'asset_shipment_destination_namedCoordinates_longitude',
	                        'asset_shipment_origin_namedCoordinates_latitude',
	                       'asset_shipment_origin_namedCoordinates_longitude',
	                        'asset_shipment_equipmentType']).agg({"asset_assetId":"count",
	                                                             "origin_data":"max",
	                                                             "destination_data":"max"}).reset_index()

	lat_s=list(df_map['asset_shipment_origin_namedCoordinates_latitude'].astype(float).values)
	lon_s=list(df_map['asset_shipment_origin_namedCoordinates_longitude'].astype(float).values)
	lat_e=list(df_map['asset_shipment_destination_namedCoordinates_latitude'].astype(float).values)
	lon_e=list(df_map['asset_shipment_destination_namedCoordinates_longitude'].astype(float).values)

	org=list(df_map['origin_data'].values)
	dst=list(df_map['destination_data'].values)

	scatter_size= [0]*len(org)
	scatter_size+=list(df_map['asset_assetId'].astype(float).values)
	lats=lat_s+lat_e
	lons=lon_s+lon_e
	names=org+dst

	fig = go.Figure()

	fig.add_trace(go.Scattergeo(
	    locationmode = 'USA-states',
	    lon = lons,
	    lat = lats,
	    hoverinfo = 'text',
	    text = names,
	    mode = 'markers',
	    marker = dict(
	        size = 2,
	        color = 'rgb(255, 0, 0)',
	        line = dict(
	            width = 3,
	            color = 'rgba(68, 68, 68, 0)'
	        )
	    )))

	flight_paths = []
	for i in range(len(df_map)):
	    if df_map['asset_shipment_equipmentType'][i].startswith("Van"):
	        clr='red'
	    else:
	        clr='blue'
	    fig.add_trace(
	        go.Scattergeo(
	            locationmode = 'USA-states',
	            lon = [df_map['asset_shipment_origin_namedCoordinates_longitude'][i],
	                   df_map['asset_shipment_destination_namedCoordinates_longitude'][i]],
	            lat = [df_map['asset_shipment_origin_namedCoordinates_latitude'][i],
	                   df_map['asset_shipment_destination_namedCoordinates_latitude'][i]],
	            mode = 'lines',
	            name = df_map['destination_data'][i],
	            line = dict(width = 1,color = clr),
	            opacity = float(df_map['asset_assetId'][i]) / float(df_map['asset_assetId'].max()),
	        )
	    )

	fig.update_layout(
	    title_text = 'Jan-Feb Loads',
	    showlegend = False,
	    geo = dict(
	        scope = 'north america',
	        projection_type = 'azimuthal equal area',
	        showland = True,
	        landcolor = 'rgb(243, 243, 243)',
	        countrycolor = 'rgb(204, 204, 204)',
	    ),
	)
	graph = fig.to_html(full_html=False, default_height=500, default_width=700)
	context = {'graph': graph}
	return render(response ,'blogs/map_arc.html',context)

@xframe_options_exempt
def map_heat(response):
	tdf=df_truck.copy()
	tdf_from=tdf[tdf['origin_data']=='NE OMAHA']
	tdf_from=tdf_from[tdf_from['created_week']<=4]
	tdf_from.sort_values(by=['created_week'], inplace=True, ascending=True)

	df=df_load.copy()
	df_from=df[df['origin_data']=='NE OMAHA']
	df_from.sort_values(by=['created_week'], inplace=True, ascending=True)

	df_map=df_from.groupby(['asset_shipment_destination_namedCoordinates_latitude',
	                   'asset_shipment_destination_namedCoordinates_longitude',
	                        'asset_shipment_origin_namedCoordinates_latitude',
	                       'asset_shipment_origin_namedCoordinates_longitude']).agg({"asset_assetId":"count"}).reset_index()
	df_map['intensity']=df_map.apply(lambda row : row['asset_assetId'],axis=1)#/max(df_map['asset_assetId'])
	locations=[]
	for i in df_map.itertuples():
		locations.append([i[1],i[2],i[6]])
	return render(response ,'blogs/map_heat.html',
		{'locations':locations})

@xframe_options_exempt
def map_time(response):

	state_city=response.GET.get('State_City',None)

	df=df_load.copy()

	df['state_cities'] = df[['asset_shipment_origin_namedCoordinates_stateProvince',
	 'asset_shipment_origin_namedCoordinates_city']].apply(lambda x: ' '.join(x), axis=1)
	state_cities=df['state_cities'].unique().tolist()

	df_from=df[(df['origin_data']==state_city.upper())]
	df_from=df_from[df_from['created_week']<=8]
	df_from.sort_values(by=['created_week'], inplace=True, ascending=True)
	df_map=df_from.groupby(['asset_shipment_destination_namedCoordinates_latitude',
	                   'asset_shipment_destination_namedCoordinates_longitude',
	                        'asset_shipment_origin_namedCoordinates_latitude',
	                       'asset_shipment_origin_namedCoordinates_longitude',
	                       'created_week']).agg({"asset_assetId":"count",
	                       						"destination_data":"max"}).reset_index()

	df_map.columns=['asset_shipment_destination_namedCoordinates_latitude',
	                   'asset_shipment_destination_namedCoordinates_longitude',
	                        'asset_shipment_origin_namedCoordinates_latitude',
	                       'asset_shipment_origin_namedCoordinates_longitude',
	                       'created_week','asset_assetId','destination_data']
	fig = go.Figure()

	# Add traces, one for each slider step
	for step in df['created_week'].unique():
		df_map_tmp=df_map[df_map['created_week']==step]
		fig.add_trace(
	        go.Scattergeo(
	        visible=False,
	        locationmode = 'USA-states',
	        lon = df_map_tmp['asset_shipment_destination_namedCoordinates_longitude'],
	        lat = df_map_tmp['asset_shipment_destination_namedCoordinates_latitude'],
	        text = df_map_tmp['destination_data'],
	        mode = 'markers',
	        marker = dict(
	            size = 8,
	            opacity = 0.8,
	            reversescale = True,
	            autocolorscale = False,
	            symbol = 'square',
	            line = dict(
	                width=1,
	                color='rgba(102, 102, 102)'
	            ),
	            colorscale = 'Blues',
	            cmin = 0,
	            color = df_map_tmp['asset_assetId'],
	            cmax = df_map_tmp['asset_assetId'].max(),
	            colorbar_title="Loads Posted from Omaha"
	        )))

	# Make 10th trace visible
	fig.data[0].visible = True

	# Create and add slider
	steps = []
	for i in range(len(fig.data)):
	    step = dict(
	        method="update",
	        args=[{"visible": [False] * len(fig.data)},
	              {"title": "Slider switched to Week: " + str(i+1)}],  # layout attribute
	    )
	    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
	    steps.append(step)

	sliders = [dict(
	    active=10,
	    currentvalue={"prefix": "Frequency: "},
	    pad={"t": 50},
	    steps=steps
	)]

	fig.update_layout(
			sliders=sliders,
	        title = 'Most Loads Posted From Omaha Jan-Feb',
	        geo = dict(
	            scope='usa',
	            projection_type='albers usa',
	            showland = True,
	            landcolor = "rgb(250, 250, 250)",
	            subunitcolor = "rgb(217, 217, 217)",
	            countrycolor = "rgb(217, 217, 217)",
	            countrywidth = 0.5,
	            subunitwidth = 0.5
	        ),
	    )

	graph = fig.to_html(full_html=False, default_height=1000, default_width=1000)
	context = {'graph': graph,'state_cities':state_cities}
	return render(response ,'blogs/map_time.html',context)

@xframe_options_exempt
def load_line(response):
	
	selected_states=[x[1] for x in us_state_abbrev.items()]

	state=response.GET.get('cat',None)
	city=response.GET.get('category',None)
	query_state_city=response.GET.get('query_state_city',None)
	try:
		state=city.upper().split(" ")[0]
	except:
		state=None
	if not city:
		city="NE Omaha"
	if not state:
		state='NE'
	if not state:
		query_state_city='CA'

	df=df_load.copy()

	dirz=f"{os.getcwd()}/"
	open_file = open(dirz+"ne_locations.txt", "rb")
	ne_locations = pickle.load(open_file)
	open_file = open(dirz+"il_locations.txt", "rb")
	il_locations = pickle.load(open_file)
	open_file = open(dirz+"ca_locations.txt", "rb")
	ca_locations = pickle.load(open_file)
	open_file = open(dirz+"fl_locations.txt", "rb")
	fl_locations = pickle.load(open_file)
	
	df_map2=df.groupby(['created_week','asset_shipment_destination_namedCoordinates_stateProvince']).agg({"asset_assetId":"count"}).reset_index()
	# selected_states=df_map2['asset_shipment_destination_namedCoordinates_stateProvince'].unique().tolist()
	df_map2['State']=df_map2['asset_shipment_destination_namedCoordinates_stateProvince']
	df_map2['Week']=df_map2['created_week']
	df_map2['Loads_Posted']=df_map2['asset_assetId']
	fig = px.line(df_map2, x="Week", y="Loads_Posted", color="State",
	              hover_name="State")
	fig.update_layout(legend_title_text='State')
	graph = fig.to_html(full_html=False, default_height=500, default_width=1000)

	if not query_state_city:
		query_state_city=selected_states[0]

	df=df[df['origin_data']==city.upper()]
	df=df[df['asset_shipment_destination_namedCoordinates_stateProvince']==query_state_city]
	
	if len(df)<5:
		df=df_.copy()
		df=df[df['asset_shipment_origin_namedCoordinates_stateProvince']==city.upper().split(" ")[0]]
		df=df[df['asset_shipment_destination_namedCoordinates_stateProvince']==query_state_city]

	df_map1=df.groupby(['created_week','destination_data']).agg({"asset_assetId":"count"}).reset_index()
	df_map1['Week']=df_map1['created_week']
	df_map1['Loads_Posted']=df_map1['asset_assetId']
	fig = px.line(df_map1, x="created_week", y="Loads_Posted", color="destination_data",
	             hover_name="destination_data")

	graph2 = fig.to_html(full_html=False, default_height=500, default_width=1000)
	context = {'graph': graph,'ne_locations':ne_locations,
		'il_locations':il_locations,
		'ca_locations':ca_locations,
		'fl_locations':fl_locations,
		'selected_states':selected_states,
		"graph2":graph2}
	return render(response ,'blogs/load_line.html',context)

@xframe_options_exempt
def load_line1(response):
	selected_states=[x[1] for x in us_state_abbrev.items()]

	state=response.GET.get('cat',None)
	city=response.GET.get('category',None)
	query_state_city=response.GET.get('query_state_city',None)
	try:
		state=city.upper().split(" ")[0]
	except:
		state=None
	if not city:
		city="NE Omaha"
	if not state:
		state='NE'
	if not state:
		query_state_city='CA'

	df=df_load.copy()

	dirz=f"{os.getcwd()}/"
	open_file = open(dirz+"ne_locations.txt", "rb")
	ne_locations = pickle.load(open_file)
	open_file = open(dirz+"il_locations.txt", "rb")
	il_locations = pickle.load(open_file)
	open_file = open(dirz+"ca_locations.txt", "rb")
	ca_locations = pickle.load(open_file)
	open_file = open(dirz+"fl_locations.txt", "rb")
	fl_locations = pickle.load(open_file)

	df_map2=df.groupby(['created_week','asset_shipment_destination_namedCoordinates_stateProvince']).agg({"asset_assetId":"count"}).reset_index()
	# selected_states=df_map2['asset_shipment_destination_namedCoordinates_stateProvince'].unique().tolist()
	df_map2['State']=df_map2['asset_shipment_destination_namedCoordinates_stateProvince']
	df_map2['Week']=df_map2['created_week']
	df_map2['Loads_Posted']=df_map2['asset_assetId']
	fig = px.line(df_map2, x="Week", y="Loads_Posted", color="State",
	              hover_name="State")
	fig.update_layout(legend_title_text='State')
	graph = fig.to_html(full_html=False, default_height=500, default_width=1000)

	if not query_state_city:
		query_state_city=selected_states[0]
	df=df_.copy()
	df=df[df['origin_data']==city.upper()]
	df=df[df['asset_shipment_destination_namedCoordinates_stateProvince']==query_state_city]
	
	if len(df)<5:
		df=df_.copy()
		df=df[df['asset_shipment_origin_namedCoordinates_stateProvince']==city.upper().split(" ")[0]]
		df=df[df['asset_shipment_destination_namedCoordinates_stateProvince']==query_state_city]

	df_map1=df.groupby(['created_week','destination_data']).agg({"asset_assetId":"count"}).reset_index()
	df_map1['Week']=df_map1['created_week']
	df_map1['Loads_Posted']=df_map1['asset_assetId']
	fig = px.line(df_map1, x="created_week", y="Loads_Posted", color="destination_data",
	             hover_name="destination_data")

	graph2 = fig.to_html(full_html=False, default_height=500, default_width=1000)
	context = {'graph': graph,'ne_locations':ne_locations,
		'il_locations':il_locations,
		'ca_locations':ca_locations,
		'fl_locations':fl_locations,
		'selected_states':selected_states,
		"graph2":graph2}
	return render(response ,'blogs/load_line.html',context)

@xframe_options_exempt
def just_map_heat_api(response):
	lon=response.GET.get('lon',None)
	lat=response.GET.get('lat',None)
	dist=response.GET.get('dist',None)
	"""
	df=pd.read_sql("SELECT asset_assetId,\
		asset_equipment_destination_place_namedcoordinates_latitude,\
		asset_equipment_destination_place_namedcoordinates_longitude,\
		asset_equipment_origin_namedcoordinates_latitude,\
		asset_equipment_origin_namedcoordinates_longitude\
	 FROM import.trucks_raw where cast(created_week as int)>12 and \
		cast(created_week as int)<17 and origin_zone!='x'",con=conn)
	"""
	df= pd.read_sql("select * from import.trucks_raw where \
		 created_at LIKE '2021-04%' or created_at LIKE '2021-05%' \
			   LIMIT 10000;",conn)
	df_map=df.groupby(['asset_equipment_destination_place_namedcoordinates_latitude',
	                   'asset_equipment_destination_place_namedcoordinates_longitude',
	                        'asset_equipment_origin_namedcoordinates_latitude',
	                       'asset_equipment_origin_namedcoordinates_longitude']).agg({"asset_assetid":"count"}).reset_index()
	df_map['intensity']=df_map.apply(lambda row : row['asset_assetid'],axis=1)#/max(df_map['asset_assetId'])

	# points=[Point(x[0],x[1]) for x in zip(df_map['asset_equipment_origin_namedCoordinates_longitude'].values.tolist(),
	# 	df_map['asset_equipment_origin_namedCoordinates_latitude'].values.tolist())]
	geod = pyproj.Geod(ellps='WGS84')
	# x1,y1=points[0].x, points[0].y
	x1,y1=float(lon), float(lat)
	# distances=[geod.inv(x1, y1, p.x, p.y)[2] for p in points]
	# distances=[x for x in distances if x<=float(dist)]
	locations=[]
	distances=[]
	for i in df_map.itertuples():
		distances.append(geod.inv(x1, y1, float(i[2]), float(i[1]))[2])
		if geod.inv(x1, y1, float(i[2]), float(i[1]))[2]<=(float(dist)+5)*1000:
			# locations.append([i[1],i[2],i[6]])
			locations.append([i[1],i[2],8])
	data={"locations":locations}
	return JsonResponse(data)

@xframe_options_exempt
def just_map_cities(response):
	

	deetz={
	    "type": "FeatureCollection",
	    "features": features1
	}
	return JsonResponse({"feats":deetz})

@xframe_options_exempt
def just_map(response):

	

	# with open('state_city.txt', 'w') as f:
	# 	pickle.dump(locations_data, f)
	# file1 = open("state_city.txt","w")
	# file1.write(locations_data)
	# file1.close()
	trucks_dtype={
              'created_week': int,
              'duration': float,
              'asset_equipment_origin_namedCoordinates_latitude': float,
              'asset_equipment_origin_namedCoordinates_longitude': float,
              'asset_equipment_destination_place_namedCoordinates_latitude': float,
              'asset_equipment_destination_place_namedCoordinates_longitude': float,
              'asset_equipment_origin_namedCoordinates_stateProvince': str,
              'asset_equipment_origin_namedCoordinates_city': str,
              'asset_equipment_destination_place_namedCoordinates_stateProvince': str,
              'asset_equipment_destination_place_namedCoordinates_city': str,
              'asset_assetId': str,
              'callback_userId': str,
              'callback_companyName': str,
              'destination_data': str,
              'travel_data': str,
              'origin_data': str,
              'created_at': str
             }
	# dirz=f"{os.getcwd()}/trucks/"
	# df = pd.read_csv(dirz+"MAP_trucks.csv",
	# 				parse_dates=['asset_status_created_date'],
	# 			                 dtype=trucks_dtype)
	# df=pd.read_sql("SELECT * FROM trucks where cast(created_week as int)>8 and \
	# 	cast(created_week as int)<17 and origin_zone!='x';",con=conn)
	# # df=df_truck.copy()
	# df_map=df.groupby(['asset_equipment_destination_place_namedCoordinates_latitude',
	#                    'asset_equipment_destination_place_namedCoordinates_longitude',
	#                         'asset_equipment_origin_namedCoordinates_latitude',
	#                        'asset_equipment_origin_namedCoordinates_longitude']).agg({"asset_assetId":"count"}).reset_index()
	# df_map['intensity']=df_map.apply(lambda row : row['asset_assetId'],axis=1)#/max(df_map['asset_assetId'])

	# locations=[]
	# for i in df_map.itertuples():
	# 	locations.append([i[1],i[2],i[6]])
	deetz={
	    "type": "FeatureCollection",
	    "features": features1
	}
	# return JsonResponse({"feats":deetz})
	return render(response ,'blogs/just_map1.html',{"feats":deetz})

@xframe_options_exempt
def just_map_api(response):
	

	np.random.shuffle(COLOURS)
	name=response.GET.get('name',None)
	name=name.replace('.','').replace("'",'')
	idz=response.GET.get('id',None)
	state=name.upper().split(" ")[0]
	loads_dtype={
			'created_week': int,
			'duration': float,
			'asset_shipment_origin_namedCoordinates_latitude': float,
			'asset_shipment_origin_namedCoordinates_longitude': float,
			'asset_shipment_destination_namedCoordinates_latitude': float,
			'asset_shipment_destination_namedCoordinates_longitude': float,
			'asset_shipment_origin_namedCoordinates_stateProvince': str,
			'asset_shipment_origin_namedCoordinates_city': str,
			'asset_shipment_destination_namedCoordinates_stateProvince': str,
			'asset_shipment_destination_namedCoordinates_city': str,
			'asset_assetId': str,
			'callback_userId': str,
			'callback_companyName': str,
			'destination_data': str,
			'travel_data': str,
			'origin_data': str,
			'created_at': str
		}

	# df=df_load.copy()
	df=pd.read_sql(f"select * from loads_april_2021 where origin_data='{name.upper()}';",conn)
	df=df[df['asset_shipment_origin_namedCoordinates_stateProvince'.lower()]==state]
	df=df[df['origin_data']==name.upper()]
	all_dest=df['asset_shipment_destination_namedCoordinates_stateProvince'.lower()].unique().tolist()
	all_dest={"dest":sorted(all_dest)}

	df_radar_ld=df.groupby(['asset_shipment_equipmentType'.lower()]).agg({"asset_assetId".lower():"count"}).reset_index()
	label_l=df_radar_ld['asset_shipment_equipmentType'.lower()].values.tolist()

	df_map=df.groupby(['created_week','destination_data']).agg({"asset_assetId".lower():"count"}).reset_index()
	df_map=df_map.sort_values(by=['asset_assetId'.lower()],ascending=False)
	datasets=[]
	labels=df_map['destination_data'][0:20].unique().tolist()
	weeks_int=[int(x) for x in list(np.sort(df_map['created_week'].unique()))]
	labelz=list(np.sort(df_map['created_week'].unique()))
	labelz=[datetime.strptime(f"2021-W{x}" + '-1', "%Y-W%W-%w").strftime("%B")+f" Week {x}" for x in labelz]
	labelz=[str(x) for x in labelz]
	for k in enumerate(labels):
	    i=k[1]
	    df_tmp=df_map[df_map['destination_data']==i]
	    deet=[]
	    for j in range(min(weeks_int),max(weeks_int)+1):
	    	val=df_tmp[df_tmp['created_week']==str(j)]['asset_assetId'.lower()].values
	    	if len(val)>0:
	    		deet.append(int(val[0]))
	    	else:
	    		deet.append(0)
	        # try:            
	        #     deet.append(int(df_tmp[df_tmp['created_week']==j]['asset_assetId'.lower()].values[0]))
	        # except IndexError:
	        #     deet.append(0)
	    datasets.append({
	      "label": i,
	      "data": deet,
	      "backgroundColor": COLOURS[k[0]],
	      "borderColor": COLOURS[k[0]],
	      "tension": 0.4
	    })
	final_data={"labels":labelz,#["Week "+str(x) for x in labelz]
	            "datasets":datasets}
	df_map=df.groupby(['asset_shipment_destination_namedCoordinates_latitude'.lower(),
		                   'asset_shipment_destination_namedCoordinates_longitude'.lower(),
		                        'asset_shipment_origin_namedCoordinates_latitude'.lower(),
		                       'asset_shipment_origin_namedCoordinates_longitude'.lower()]).agg({"asset_assetId".lower():"count"}).reset_index()
	lat=df_map['asset_shipment_origin_namedCoordinates_latitude'.lower()].values.tolist()[0]
	lon=df_map['asset_shipment_origin_namedCoordinates_longitude'.lower()].values.tolist()[0]
	lats=df_map['asset_shipment_destination_namedCoordinates_latitude'.lower()].values.tolist()
	lons=df_map['asset_shipment_destination_namedCoordinates_longitude'.lower()].values.tolist()
	weights=df_map['asset_assetId'.lower()].values.tolist()
	weights=[int(x) for x in weights]
	max_weight=max(weights)
	states=[[x[0],x[1],float(x[2]/max_weight)] for x in zip(lats,lons,weights)]
	arcs={"states":states}

	trucks_dtype={
			'created_week': int,
			'duration': float,
			'asset_equipment_origin_namedCoordinates_latitude': float,
			'asset_equipment_origin_namedCoordinates_longitude': float,
			'asset_equipment_destination_place_namedCoordinates_latitude': float,
			'asset_equipment_destination_place_namedCoordinates_longitude': float,
			'asset_equipment_origin_namedCoordinates_stateProvince': str,
			'asset_equipment_origin_namedCoordinates_city': str,
			'asset_equipment_destination_place_namedCoordinates_stateProvince': str,
			'asset_equipment_destination_place_namedCoordinates_city': str,
			'asset_assetId': str,
			'callback_userId': str,
			'callback_companyName': str,
			'destination_data': str,
			'travel_data': str,
			'origin_data': str,
			'created_at': str
			}

	# if name=='NE Omaha':
	# 	dirz=f"{os.getcwd()}/trucks/"
	# 	df = pd.read_csv(dirz+"MAP_NE_OMAHA_trucks.csv",
	# 					parse_dates=['asset_status_created_date'],
	# 				                 dtype=trucks_dtype)
	# else:
	# df=df_truck.copy()
	df=pd.read_sql(f"select * from trucks_april_2021 where origin_data='{name.upper()}';",conn)
	df=df[df['asset_equipment_origin_namedCoordinates_stateProvince'.lower()]==state]
	df=df[df['origin_data']==name.upper()]

	df_radar_tr=df.groupby(['asset_equipment_equipmentType'.lower()]).agg({"asset_assetId".lower():"count"}).reset_index()
	label_t=df_radar_tr['asset_equipment_equipmentType'.lower()].values.tolist()


	df_map=df.groupby(['created_week','callback_companyName'.lower()]).agg({"asset_assetId".lower():"count"}).reset_index()
	df_map=df_map.sort_values(by=['asset_assetId'.lower()],ascending=False)
	datasets=[]
	labels=df_map['callback_companyName'.lower()][0:20].unique().tolist()
	weeks_int=[int(x) for x in list(np.sort(df_map['created_week'].unique()))]
	labelz=list(np.sort(df_map['created_week'].unique()))
	labelz=[datetime.strptime(f"2021-W{x}" + '-1', "%Y-W%W-%w").strftime("%B")+f" Week {x}" for x in labelz]
	labelz=[str(x) for x in labelz]
	for k in enumerate(labels):
	    i=k[1]
	    df_tmp=df_map[df_map['callback_companyName'.lower()]==i]
	    deet=[]
	    for j in range(min(weeks_int),max(weeks_int)+1):
	    	val=df_tmp[df_tmp['created_week']==str(j)]['asset_assetId'.lower()].values
	    	if len(val)>0:
	    		deet.append(int(val[0]))
	    	else:
	    		deet.append(0)

	    datasets.append({
	      "label": i,
	      "data": deet,
	      "backgroundColor": COLOURS[k[0]],
	      "borderColor": COLOURS[k[0]],
	      "tension": 0.4
	    })
	final_data1={"labels":labelz,#["Week "+str(x) for x in labelz]
	            "datasets":datasets}


	labelk=list(set(label_l+label_t))
	data_l=[]
	data_t=[]

	for i in labelk:
		val1=df_radar_tr[df_radar_tr['asset_equipment_equipmentType'.lower()]==i]['asset_assetId'.lower()].values
		if len(val1)>0:
			data_t.append(val1[0])
		else:
			data_t.append(0)
		val1=df_radar_ld[df_radar_ld['asset_shipment_equipmentType'.lower()]==i]['asset_assetId'.lower()].values
		if len(val1)>0:
			data_l.append(val1[0])
		else:
			data_l.append(0)

	final_data3={
	  "labels": labelk,
	  "datasets": [
	    {
	      "label": 'Trucks',
	      "data": [int(x) for x in data_t],
	      "borderColor": "rgb(51, 153, 255, 1)",
	      "backgroundColor": "rgb(51, 153, 255, 0.2)"
	      
	    },
	    {
	      "label": 'Loads',
	      "data": [int(x) for x in data_l],
	      "borderColor":'rgba(255, 99, 132, 1)',
	      "backgroundColor": "rgba(255, 99, 132, 0.2)"
	      
	    }
	  ]
	}

	data={"final_data":final_data,"final_data1":final_data1,"final_data3":final_data3,
	"arcs":arcs,"lat":lat,"lon":lon,"all_dest":all_dest}
	return JsonResponse(data)

@xframe_options_exempt
def just_map_api_2(response):
	

	np.random.shuffle(COLOURS)
	name=response.GET.get('name',None)
	name=name.replace('.','').replace("'",'')
	statex=response.GET.get('state',None)
	state=name.upper().split(" ")[0]

	# df=df_load.copy()
	df=pd.read_sql(f"select * from loads_april_2021 where origin_data='{name.upper()}' \
		and asset_shipment_destination_namedCoordinates_stateProvince='{statex.upper()}';",conn)

	# df=df[df['asset_shipment_origin_namedCoordinates_stateProvince'.lower()]==state]
	# df=df[df['origin_data']==name.upper()]
	# df=df[df['asset_shipment_destination_namedCoordinates_stateProvince'.lower()]==statex]

	df_radar_ld=df.groupby(['asset_shipment_equipmentType'.lower()]).agg({"asset_assetId".lower():"count"}).reset_index()
	label_l=df_radar_ld['asset_shipment_equipmentType'.lower()].values.tolist()


	df_map=df.groupby(['created_week','destination_data']).agg({"asset_assetId".lower():"count"}).reset_index()
	df_map=df_map.sort_values(by=['asset_assetId'.lower()],ascending=False)

	datasets=[]
	labels=df_map['destination_data'][0:20].unique().tolist()
	weeks_int=[int(x) for x in list(np.sort(df_map['created_week'].unique()))]
	labelz=list(np.sort(df_map['created_week'].unique()))
	labelz=[datetime.strptime(f"2021-W{x}" + '-1', "%Y-W%W-%w").strftime("%B")+f" Week {x}" for x in labelz]
	labelz=[str(x) for x in labelz]
	for k in enumerate(labels):
	    i=k[1]
	    df_tmp=df_map[df_map['destination_data']==i]
	    deet=[]
	    for j in range(min(weeks_int),max(weeks_int)+1):
	    	val=df_tmp[df_tmp['created_week']==str(j)]['asset_assetId'.lower()].values
	    	if len(val)>0:
	    		print(val[0])
	    		deet.append(int(val[0]))
	    	else:
	    		deet.append(0)

	    datasets.append({
	      "label": i,
	      "data": deet,
	      "borderColor": COLOURS[k[0]],
	      "backgroundColor": COLOURS[k[0]],
	      "tension": 0.4
	    })
	final_data={"labels":["Week "+str(x) for x in labelz],
	            "datasets":datasets}

	# df=df_truck.copy()
	df=pd.read_sql(f"select * from trucks_april_2021 where origin_data='{name.upper()}';",conn)

	# df=df[df['asset_equipment_origin_namedCoordinates_stateProvince'.lower()]==state]
	# df=df[df['origin_data']==name.upper()]
	# # df=df[df['asset_equipment_destination_place_namedCoordinates_stateProvince']==statex]

	df_radar_tr=df.groupby(['asset_equipment_equipmentType'.lower()]).agg({"asset_assetId".lower():"count"}).reset_index()
	label_t=df_radar_tr['asset_equipment_equipmentType'.lower()].values.tolist()

	labelk=list(set(label_l+label_t))
	data_l=[]
	data_t=[]

	for i in labelk:
		val1=df_radar_tr[df_radar_tr['asset_equipment_equipmentType'.lower()]==i]['asset_assetId'.lower()].values
		if len(val1)>0:
			data_t.append(val1[0])
		else:
			data_t.append(0)
		val1=df_radar_ld[df_radar_ld['asset_shipment_equipmentType'.lower()]==i]['asset_assetId'.lower()].values
		if len(val1)>0:
			data_l.append(val1[0])
		else:
			data_l.append(0)
	final_data3={
	  "labels": labelk,
	  "datasets": [
	    {
	      "label": 'Trucks',
	      "data": [int(x) for x in data_t],
	      "borderColor": "rgb(51, 153, 255, 1)",
	      "backgroundColor": "rgb(51, 153, 255, 0.2)"
	      
	    },
	    {
	      "label": 'Loads',
	      "data": [int(x) for x in data_l],
	      "borderColor":'rgba(255, 99, 132, 1)',
	      "backgroundColor": "rgba(255, 99, 132, 0.2)"
	      
	    }
	  ]
	} 
	return JsonResponse({"data":final_data,"final_data3":final_data3})

@xframe_options_exempt
def network_graph(response):
	

	df1 = df_load.copy()

	df2 = df_truck.copy()

	companies=response.GET.getlist('company[]',None)
	if not companies:
		companies=['Armstrong Transport Group Inc','Viking Transportation Company Llc']
	carriers=response.GET.getlist('carrier[]',None)
	if not carriers:
		carriers=['Takhar Transport Services','Narwal Trucking']
	lanes=response.GET.getlist('location[]',None)
	if not lanes:
		lanes=[]
		# lanes=['NE YORK->UT OGDEN','NE LINCOLN->TX TERRELL']

	df_1=df1[df1['callback_companyName'].isin(companies)]
	df_2=df1[df1['travel_data'].isin(lanes)]
	df_3=df2[df2['callback_companyName'].isin(carriers)]

	df=pd.concat([df_1,df_2])

	cn=list(df1.groupby('callback_companyName').count()['callback_userId'].sort_values(ascending=False)[10:40].index)
	cn=list(set(cn))
	tn=list(df2.groupby('callback_companyName').count()['callback_userId'].sort_values(ascending=False)[10:40].index)
	tn=list(set(tn))
	td=list(df1.groupby('travel_data').count()['callback_userId'].sort_values(ascending=False)[10:40].index)
	td=list(set(td))

	df_1=df_1.groupby(['callback_companyName','travel_data']).agg({"asset_assetId":"count",
		                                                             "asset_shipment_equipmentType":"max"}).sort_values(by='asset_assetId',ascending=False)[['asset_assetId','asset_shipment_equipmentType']].reset_index()
	df_2=df_2.groupby(['callback_companyName','travel_data']).agg({"asset_assetId":"count",
		                                                             "asset_shipment_equipmentType":"max"}).sort_values(by='asset_assetId',ascending=False)[['asset_assetId','asset_shipment_equipmentType']].reset_index()


	nodes = []
	nodes_list = []
	edges = []
	edges_list = []
	routes_list=[]
	for i in companies:
	    df_tmp_=df_1[df_1['callback_companyName']==i]
	    df_tmp=df_tmp_[0:10]
	    for j in df_tmp.itertuples():
	        if not str(j[1]) in nodes_list:
	            dct = {}
	            dct['id'] = "_".join(str(j[1]).split(" "))
	            dct['shape'] = 'image'
	            dct['image'] = 'https://www.flaticon.com/svg/vstatic/svg/993/993928.svg?token=exp=1619447677~hmac=104a901d7d6c1d2f1c6914783a9062d7'
	            dct['value'] = str(len(df_tmp_))
	            dct['title'] = str(j[1])
	            dct['label'] = str(j[1])
	            # dct['color']='#FF4500'
	            nodes_list.append(str(j[1]))
	            nodes.append(dct)
	        if not str(j[2]) in nodes_list:
	            dct = {}
	            dct['id'] = "_".join(str(j[2]).split(" "))
	            dct['shape'] = 'image'
	            dct['image'] = 'https://www.flaticon.com/svg/vstatic/svg/608/608691.svg?token=exp=1619447792~hmac=10b3312e6ecab924effbefe71987681e'
	            dct['value'] = str(len(df_tmp_))
	            dct['title'] = str(j[2])
	            # dct['color']='#FF4500'
	            nodes_list.append(str(j[2]))
	            routes_list.append(str(j[2]))
	            nodes.append(dct)
	        if not (str(j[1]),str(j[2])) in edges_list:
	            dct={}
	            dct['from'] = "_".join(str(j[1]).split(" "))
	            dct['to'] = "_".join(str(j[2]).split(" "))
	            dct['value']=str(j[3])
	            dct['title']=str(j[4])
	            edges_list.append((str(j[1]),str(j[2])))
	            edges.append(dct)    
	origin_list=[x.split('->')[0] for x in routes_list]
	df_4=df1[df1['travel_data'].isin(routes_list)]
	df_4=df_4[~df_4['callback_companyName'].isin(companies)]
	df_4=df_4.groupby(['callback_companyName','travel_data']).agg({"asset_assetId":"count",
		                                                             "asset_shipment_equipmentType":"max"}).sort_values(by='asset_assetId',ascending=False)[['asset_assetId','asset_shipment_equipmentType']].reset_index()
	for i in df['travel_data'].unique().tolist():
	    df_tmp_=df_4[df_4['travel_data']==i]
	    df_tmp=df_tmp_[0:2]
	    for j in df_tmp.itertuples():
	        if not str(j[1]) in nodes_list:
	            dct = {}
	            dct['id'] = "_".join(str(j[1]).split(" "))
	            dct['shape'] = 'image'
	            dct['image'] = 'https://img.icons8.com/bubbles/100/000000/company.png'
	            dct['value'] = str(len(df_tmp_))
	            dct['title'] = str(j[1])
	            dct['label'] = str(j[1])
	            # dct['color']='#FF4500'
	            nodes_list.append(str(j[1]))
	            nodes.append(dct)
	        if not str(j[2]) in nodes_list:
	            dct = {}
	            dct['id'] = "_".join(str(j[2]).split(" "))
	            dct['shape'] = 'image'
	            dct['image'] = 'https://www.flaticon.com/svg/vstatic/svg/608/608691.svg?token=exp=1619447792~hmac=10b3312e6ecab924effbefe71987681e'
	            dct['value'] = str(len(df_tmp_))
	            dct['title'] = str(j[2])
	            # dct['color']='#FF4500'
	            nodes_list.append(str(j[2]))
	            routes_list.append(str(j[2]))
	            nodes.append(dct)
	        if not (str(j[1]),str(j[2])) in edges_list:
	            dct={}
	            dct['from'] = "_".join(str(j[1]).split(" "))
	            dct['to'] = "_".join(str(j[2]).split(" "))
	            dct['value']=str(j[3])
	            dct['title']=str(j[4])
	            edges_list.append((str(j[1]),str(j[2])))
	            edges.append(dct)  

	for i in lanes:
	    df_tmp_=df_2[df_2['travel_data']==i]
	    df_tmp=df_tmp_[0:10]
	    for j in df_tmp.itertuples():
	        if not str(j[1]) in nodes_list:
	            dct = {}
	            dct['id'] = "_".join(str(j[1]).split(" "))
	            dct['shape'] = 'image'
	            dct['image'] = 'https://img.icons8.com/bubbles/100/000000/company.png'
	            dct['value'] = str(len(df_tmp_))
	            dct['title'] = str(j[1])
	            dct['label'] = str(j[1])
	            # dct['color']='#FF4500'
	            nodes_list.append(str(j[1]))
	            nodes.append(dct)
	        if not str(j[2]) in nodes_list:
	            dct = {}
	            dct['id'] = "_".join(str(j[2]).split(" "))
	            dct['shape'] = 'image'
	            dct['image'] = 'https://www.flaticon.com/svg/vstatic/svg/608/608691.svg?token=exp=1619447792~hmac=10b3312e6ecab924effbefe71987681e'
	            dct['value'] = str(len(df_tmp_))
	            dct['title'] = str(j[2])
	            # dct['color']='#FF4500'
	            nodes_list.append(str(j[2]))
	            routes_list.append(str(j[2]))
	            nodes.append(dct)
	        if not (str(j[1]),str(j[2])) in edges_list:
	            dct={}
	            dct['from'] = "_".join(str(j[1]).split(" "))
	            dct['to'] = "_".join(str(j[2]).split(" "))
	            dct['value']=str(j[3])
	            dct['title']=str(j[4])
	            edges_list.append((str(j[1]),str(j[2])))
	            edges.append(dct)


	df_5=df_3.groupby(['callback_companyName','origin_data']).agg({"asset_assetId":"count",
		                                                             "asset_equipment_equipmentType":"max"}).sort_values(by='asset_assetId',ascending=False)[['asset_assetId','asset_equipment_equipmentType']].reset_index()

	for j in df_5.itertuples():
	    if not str(j[1]) in nodes_list:
	        dct = {}
	        dct['id'] = "_".join(str(j[1]).split(" "))
	        dct['shape'] = 'image'
	        dct['image'] = 'https://www.flaticon.com/svg/vstatic/svg/3273/3273327.svg?token=exp=1619445437~hmac=9089eec5436237e9ef18383155ee6574'
	        dct['value'] = str(len(df2[df2['callback_companyName']==j[1]]))
	        dct['title'] = str(j[1])
	        dct['label'] = str(j[1])
	        # dct['color']='#FF4500'
	        nodes_list.append(str(j[1]))
	        nodes.append(dct)
	    r_l=[x for x in routes_list if j[2] in x]
	    for r in r_l:
	        if not (str(j[1]),str(r)) in edges_list:
	            dct={}
	            dct['from'] = "_".join(str(j[1]).split(" "))
	            dct['to'] = "_".join(str(r).split(" "))
	            dct['value']=str(j[3])
	            dct['title']=str(j[4])
	            edges_list.append((str(j[1]),str(r)))
	            edges.append(dct)      
	for x in lanes:
	    origin_list.append(x.split('->')[0])

	df_6=df2[df2['origin_data'].isin(origin_list)]
	df_7=df_6.groupby(['callback_companyName','origin_data']).agg({"asset_assetId":"count",
		                                                             "asset_equipment_equipmentType":"max"}).sort_values(by='asset_assetId',ascending=False)[['asset_assetId','asset_equipment_equipmentType']].reset_index()
	# df_7=df_7[0:10]
	for k in origin_list:
	    df_tmp_=df_7[df_7['origin_data']==k]
	    df_tmp=df_tmp_[0:2]
	    for j in df_tmp.itertuples():
		    if not str(j[1]) in nodes_list:
		        dct = {}
		        dct['id'] = "_".join(str(j[1]).split(" "))
		        dct['shape'] = 'image'
		        dct['image'] = 'https://www.flaticon.com/svg/vstatic/svg/4231/4231188.svg?token=exp=1619451061~hmac=f0cc5bd0ccfdfbbfd28839e979a2c6ce'
		        dct['value'] = str(len(df2[df2['callback_companyName']==j[1]]))
		        dct['title'] = str(j[1])
		        # dct['color']='#FF4500'
		        nodes_list.append(str(j[1]))
		        nodes.append(dct)
		    r_l=[x for x in routes_list if j[2] in x]
		    for r in r_l:
		        if not (str(j[1]),str(r)) in edges_list:
		            dct={}
		            dct['from'] = "_".join(str(j[1]).split(" "))
		            dct['to'] = "_".join(str(r).split(" "))
		            dct['value']=str(j[3])
		            dct['title']=str(j[4])
		            edges_list.append((str(j[1]),str(r)))
		            edges.append(dct)  

	physics='true'
	return render(response ,'blogs/01_basic_usage.html',
		{'nodes':nodes,
		'edges':edges,
		'company':sorted(cn),
		'carriers':sorted(tn),
		'locations':sorted(td),
		'physics':physics})

@xframe_options_exempt
def network_graph_all(response):
	

	loads_dtype={
	         'created_week': int,
	          'duration': float,
	          'asset_shipment_origin_namedCoordinates_latitude': float,
	          'asset_shipment_origin_namedCoordinates_longitude': float,
	          'asset_shipment_destination_namedCoordinates_latitude': float,
	          'asset_shipment_destination_namedCoordinates_longitude': float,
	          'asset_shipment_origin_namedCoordinates_stateProvince': str,
	          'asset_shipment_origin_namedCoordinates_city': str,
	          'asset_shipment_destination_namedCoordinates_stateProvince': str,
	          'asset_shipment_destination_namedCoordinates_city': str,
	          'asset_assetId': str,
	          'callback_userId': str,
	          'callback_companyName': str,
	         'destination_data': str,
	          'travel_data': str,
	         'origin_data': str,
	          'created_at': str
	     }
	trucks_dtype={
	       'created_week': int,
	      'duration': float,
	      'asset_equipment_origin_namedCoordinates_latitude': float,
	      'asset_equipment_origin_namedCoordinates_longitude': float,
	      'asset_equipment_destination_place_namedCoordinates_latitude': float,
	      'asset_equipment_destination_place_namedCoordinates_longitude': float,
	      'asset_equipment_origin_namedCoordinates_stateProvince': str,
	      'asset_equipment_origin_namedCoordinates_city': str,
	      'asset_equipment_destination_place_namedCoordinates_stateProvince': str,
	      'asset_equipment_destination_place_namedCoordinates_city': str,
	      'asset_assetId': str,
	      'callback_userId': str,
	      'callback_companyName': str,
	         'destination_data': str,
	      'travel_data': str,
	         'origin_data': str,
	      'created_at': str
	     }

	df1 = df_load.copy()

	df2 = df_truck.copy()

	df_1=df1
	df_2=df1
	df_3=df2

	df=pd.concat([df_1,df_2])

	cn=list(df1.groupby('callback_companyName').count()['callback_userId'].sort_values(ascending=False)[0:20].index)
	cn=list(set(cn))
	tn=list(df2.groupby('callback_companyName').count()['callback_userId'].sort_values(ascending=False)[0:20].index)
	tn=list(set(tn))
	td=list(df1.groupby('travel_data').count()['callback_userId'].sort_values(ascending=False)[0:20].index)
	td=list(set(td))

	df_1=df_1.groupby(['callback_companyName','travel_data']).agg({"asset_assetId":"count",
		                                                             "asset_shipment_equipmentType":"max"}).sort_values(by='asset_assetId',ascending=False)[['asset_assetId','asset_shipment_equipmentType']].reset_index()
	df_2=df_2.groupby(['callback_companyName','travel_data']).agg({"asset_assetId":"count",
		                                                             "asset_shipment_equipmentType":"max"}).sort_values(by='asset_assetId',ascending=False)[['asset_assetId','asset_shipment_equipmentType']].reset_index()

	nodes = []
	nodes_list = []
	edges = []
	edges_list = []
	routes_list=[]
	for i in tqdm(cn,total=len(cn)):
	    df_tmp_=df_1[df_1['callback_companyName']==i]
	    df_tmp=df_tmp_[0:20]
	    for j in df_tmp.itertuples():
	        if not str(j[1]) in nodes_list:
	            dct = {}
	            dct['id'] = "_".join(str(j[1]).split(" "))
	            dct['shape'] = 'image'
	            dct['image'] = 'https://www.flaticon.com/svg/vstatic/svg/993/993928.svg?token=exp=1619447677~hmac=104a901d7d6c1d2f1c6914783a9062d7'
	            dct['value'] = str(len(df_tmp_))
	            dct['title'] = str(j[1])
	            dct['label'] = str(j[1])
	            # dct['color']='#FF4500'
	            nodes_list.append(str(j[1]))
	            nodes.append(dct)
	        if not str(j[2]) in nodes_list:
	            dct = {}
	            dct['id'] = "_".join(str(j[2]).split(" "))
	            dct['shape'] = 'image'
	            dct['image'] = 'https://www.flaticon.com/svg/vstatic/svg/608/608691.svg?token=exp=1619447792~hmac=10b3312e6ecab924effbefe71987681e'
	            dct['value'] = str(len(df_tmp_))
	            dct['title'] = str(j[2])
	            # dct['color']='#FF4500'
	            nodes_list.append(str(j[2]))
	            routes_list.append(str(j[2]))
	            nodes.append(dct)
	        if not (str(j[1]),str(j[2])) in edges_list:
	            dct={}
	            dct['from'] = "_".join(str(j[1]).split(" "))
	            dct['to'] = "_".join(str(j[2]).split(" "))
	            dct['value']=str(j[3])
	            dct['title']=str(j[4])
	            edges_list.append((str(j[1]),str(j[2])))
	            edges.append(dct)    
	origin_list=[x.split('->')[0] for x in routes_list]
	df_4=df1[df1['travel_data'].isin(routes_list)]
	df_4=df_4[~df_4['callback_companyName'].isin(cn)]
	df_4=df_4.groupby(['callback_companyName','travel_data']).agg({"asset_assetId":"count",
		                                                             "asset_shipment_equipmentType":"max"}).sort_values(by='asset_assetId',ascending=False)[['asset_assetId','asset_shipment_equipmentType']].reset_index()
	for i in tqdm(td,total=len(td)):
	    df_tmp_=df_4[df_4['travel_data']==i]
	    df_tmp=df_tmp_[0:20]
	    for j in df_tmp.itertuples():
	        if not str(j[1]) in nodes_list:
	            dct = {}
	            dct['id'] = "_".join(str(j[1]).split(" "))
	            dct['shape'] = 'image'
	            dct['image'] = 'https://img.icons8.com/bubbles/100/000000/company.png'
	            dct['value'] = str(len(df_tmp_))
	            dct['title'] = str(j[1])
	            dct['label'] = str(j[1])
	            # dct['color']='#FF4500'
	            nodes_list.append(str(j[1]))
	            nodes.append(dct)
	        if not str(j[2]) in nodes_list:
	            dct = {}
	            dct['id'] = "_".join(str(j[2]).split(" "))
	            dct['shape'] = 'image'
	            dct['image'] = 'https://www.flaticon.com/svg/vstatic/svg/608/608691.svg?token=exp=1619447792~hmac=10b3312e6ecab924effbefe71987681e'
	            dct['value'] = str(len(df_tmp_))
	            dct['title'] = str(j[2])
	            # dct['color']='#FF4500'
	            nodes_list.append(str(j[2]))
	            routes_list.append(str(j[2]))
	            nodes.append(dct)
	        if not (str(j[1]),str(j[2])) in edges_list:
	            dct={}
	            dct['from'] = "_".join(str(j[1]).split(" "))
	            dct['to'] = "_".join(str(j[2]).split(" "))
	            dct['value']=str(j[3])
	            dct['title']=str(j[4])
	            edges_list.append((str(j[1]),str(j[2])))
	            edges.append(dct)  

	df_5=df_3.groupby(['callback_companyName','origin_data']).agg({"asset_assetId":"count",
		                                                             "asset_equipment_equipmentType":"max"}).sort_values(by='asset_assetId',ascending=False)[['asset_assetId','asset_equipment_equipmentType']].reset_index()
	df_5=df_5[0:20]
	for j in tqdm(df_5.itertuples(),total=len(df_5)):
	    if not str(j[1]) in nodes_list:
	        dct = {}
	        dct['id'] = "_".join(str(j[1]).split(" "))
	        dct['shape'] = 'image'
	        dct['image'] = 'https://www.flaticon.com/svg/vstatic/svg/3273/3273327.svg?token=exp=1619445437~hmac=9089eec5436237e9ef18383155ee6574'
	        dct['value'] = str(len(df2[df2['callback_companyName']==j[1]]))
	        dct['title'] = str(j[1])
	        dct['label'] = str(j[1])
	        # dct['color']='#FF4500'
	        nodes_list.append(str(j[1]))
	        nodes.append(dct)
	    r_l=[x for x in routes_list if j[2] in x]
	    for r in r_l:
	        if not (str(j[1]),str(r)) in edges_list:
	            dct={}
	            dct['from'] = "_".join(str(j[1]).split(" "))
	            dct['to'] = "_".join(str(r).split(" "))
	            dct['value']=str(j[3])
	            dct['title']=str(j[4])
	            edges_list.append((str(j[1]),str(r)))
	            edges.append(dct)      
	# for x in lanes:
	#     origin_list.append(x.split('->')[0])

	df_6=df2[df2['origin_data'].isin(origin_list)]
	df_7=df_6.groupby(['callback_companyName','origin_data']).agg({"asset_assetId":"count",
		                                                             "asset_equipment_equipmentType":"max"}).sort_values(by='asset_assetId',ascending=False)[['asset_assetId','asset_equipment_equipmentType']].reset_index()
	# df_7=df_7[0:10]
	np.random.shuffle(origin_list)
	origin_list=origin_list[0:50]
	for k in tqdm(origin_list,total=len(origin_list)):
	    df_tmp_=df_7[df_7['origin_data']==k]
	    df_tmp=df_tmp_[0:20]
	    for j in df_tmp.itertuples():
		    if not str(j[1]) in nodes_list:
		        dct = {}
		        dct['id'] = "_".join(str(j[1]).split(" "))
		        dct['shape'] = 'image'
		        dct['image'] = 'https://www.flaticon.com/svg/vstatic/svg/4231/4231188.svg?token=exp=1619451061~hmac=f0cc5bd0ccfdfbbfd28839e979a2c6ce'
		        dct['value'] = str(len(df2[df2['callback_companyName']==j[1]]))
		        dct['title'] = str(j[1])
		        # dct['color']='#FF4500'
		        nodes_list.append(str(j[1]))
		        nodes.append(dct)
		    r_l=[x for x in routes_list if j[2] in x]
		    for r in r_l:
		        if not (str(j[1]),str(r)) in edges_list:
		            dct={}
		            dct['from'] = "_".join(str(j[1]).split(" "))
		            dct['to'] = "_".join(str(r).split(" "))
		            dct['value']=str(j[3])
		            dct['title']=str(j[4])
		            edges_list.append((str(j[1]),str(r)))
		            edges.append(dct)  

	physics='true'

	return render(response ,'blogs/network_graph_all.html',
		{'nodes':nodes,
		'edges':edges,
		'physics':physics})

@xframe_options_exempt
def just_map_v2(response):
	

	df=df_gd.copy()
	customer=response.GET.get('customer',None)
	
	if not customer:
		customer='DOW CHEMICAL COMPANY C/O XPO LOGISTICS'
	df1=df[(df['customer']==customer)]
	df_t=pd.read_sql("SELECT asset_assetId,\
			asset_equipment_destination_place_namedCoordinates_latitude,\
			asset_equipment_destination_place_namedCoordinates_longitude,\
			asset_equipment_origin_namedCoordinates_latitude,\
			asset_equipment_origin_namedCoordinates_longitude\
		 FROM trucks where created_month='January' and origin_zone='5'",con=conn)
	df_l=pd.read_sql("SELECT asset_assetId,\
			asset_shipment_destination_namedCoordinates_latitude,\
			asset_shipment_destination_namedCoordinates_longitude,\
			asset_shipment_origin_namedCoordinates_latitude,\
			asset_shipment_origin_namedCoordinates_longitude,origin_zone,destination_zone\
		 FROM loads where created_month='April' and origin_zone!='x' and destination_zone!='x' LIMIT 10000",con=conn)
	
	return render(response ,'blogs/just_map_v2.html',
		{"customers":sorted(df['customer'].unique().tolist()),
		"shippers":sorted(df1['shipper'].unique().tolist()),
		"receivers":sorted(df1['receiver'].unique().tolist())})

@xframe_options_exempt
def just_map_v3(response):
	

	df=df_gd.copy()
	customer=response.GET.get('customer',None)
	
	if not customer:
		customer='DOW CHEMICAL COMPANY C/O XPO LOGISTICS'
	df1=df[(df['customer']==customer)]
	df_t=pd.read_sql("SELECT asset_assetId,\
			asset_equipment_destination_place_namedCoordinates_latitude,\
			asset_equipment_destination_place_namedCoordinates_longitude,\
			asset_equipment_origin_namedCoordinates_latitude,\
			asset_equipment_origin_namedCoordinates_longitude\
		 FROM trucks where created_month='January' and origin_zone='5'",con=conn)
	df_l=pd.read_sql("SELECT asset_assetId,\
			asset_shipment_destination_namedCoordinates_latitude,\
			asset_shipment_destination_namedCoordinates_longitude,\
			asset_shipment_origin_namedCoordinates_latitude,\
			asset_shipment_origin_namedCoordinates_longitude,origin_zone,destination_zone\
		 FROM loads where created_month='April' and origin_zone!='x' and destination_zone!='x' LIMIT 10000",con=conn)
	
	return render(response ,'blogs/just_map_v3.html',
		{"customers":sorted(df['customer'].unique().tolist()),
		"shippers":sorted(df1['shipper'].unique().tolist()),
		"receivers":sorted(df1['receiver'].unique().tolist())})

@xframe_options_exempt
def just_map_v2_api(response):
	

	customer=response.GET.get('customer',None)
	shipper=response.GET.get('shipper',None)
	receiver=response.GET.getlist('receiver[]',None)
	colors={"Standard Van 53":"#FA3005",
	        "Standard Reefer 53":"#1700FF",
	        "Standard Van 48":"#FF0000",
	        "Standard Reefer 48":"#008FFF"}
	df = df_gd.copy()

	if shipper=='x':
		shipper=None
	if receiver=='x':
		receiver=None

	if not customer:
		customer='DOW CHEMICAL COMPANY C/O XPO LOGISTICS'

	if shipper and receiver:
		df1=df[(df['customer']==customer) &\
		(df['shipper']==shipper) & (df['receiver'].isin(receiver))]
	elif shipper:
		df1=df[(df['customer']==customer) &\
				(df['shipper']==shipper)]
	elif receiver:
		df1=df[(df['customer']==customer) &\
		(df['receiver'].isin(receiver))]
	else:
		df1=df[(df['customer']==customer)]

	df_map=df1.groupby(['origin_data','destination_data']).agg({"id":"count",
	                                                "origin_lat":"first",
	                                                "origin_lng":"first",
	                                                "destination_lat":"first",
	                                                "destination_lng":"first",
	                                                "equipment_type":"max"}).reset_index()

	data=[]
	max_counts=df_map['id'].max()

	for i in df_map.itertuples():
	    tmp=df1[(df1['destination_data']==i[2]) & (df1['origin_data']==i[1])]
	    df_tmp=tmp.groupby(['origin_data',
	                        'destination_data',
	                        'equipment_type']).agg({"id":"count"}).reset_index()
	    popup={'origin_data':i[1],
	        'destination_data':i[2],
	        "Standard Van 53":0,
	        "Standard Reefer 53":0,
	        "Standard Van 48":0,
	        "Standard Reefer 48":0}
	    for j in df_tmp.itertuples():
	        popup[j[3]]=j[4]
	    data.append([[i[4],i[5]],
	                  [i[6],i[7]],
	                  (int(i[3])/max_counts)*10,
	                  colors[i[8]],
	                  [popup]])
	shippers=df1.groupby("shipper").count()['id'].sort_values(ascending=False)
	receivers=df1.groupby("receiver").count()['id'].sort_values(ascending=False)

	return JsonResponse({"data":data,
		"shippers":shippers.index[0:10].tolist(),
		"receivers":receivers.index[0:10].tolist()})

@xframe_options_exempt
def just_map_v3_api(response):
	

	customer=response.GET.get('customer',None)
	shipper=response.GET.get('shipper',None)
	receiver=response.GET.getlist('receiver[]',None)
	colors={"Standard Van 53":"#FA3005",
	        "Standard Reefer 53":"#1700FF",
	        "Standard Van 48":"#FF0000",
	        "Standard Reefer 48":"#008FFF"}
	df = df_gd.copy()

	if shipper=='x':
		shipper=None
	if receiver=='x':
		receiver=None

	if not customer:
		customer='DOW CHEMICAL COMPANY C/O XPO LOGISTICS'

	if shipper and receiver:
		df1=df[(df['customer']==customer) &\
		(df['shipper']==shipper) & (df['receiver'].isin(receiver))]
	elif shipper:
		df1=df[(df['customer']==customer) &\
				(df['shipper']==shipper)]
	elif receiver:
		df1=df[(df['customer']==customer) &\
		(df['receiver'].isin(receiver))]
	else:
		df1=df[(df['customer']==customer)]

	df_map=df1.groupby(['origin_state_province','destination_state_province']).agg({"id":"count",
	                                                "origin_lat":"first",
	                                                "origin_lng":"first",
	                                                "destination_lat":"first",
	                                                "destination_lng":"first",
	                                                "equipment_type":"first"}).reset_index()

	data=[]
	max_counts=df_map['id'].max()

	for i in df_map.itertuples():
	    tmp=df1[(df1['destination_state_province']==i[2]) & (df1['origin_state_province']==i[1])]
	    df_tmp=tmp.groupby(['origin_state_province',
	                        'destination_state_province',
	                        'equipment_type']).agg({"id":"count"}).reset_index()
	    popup={'origin_data':i[1],
	        'destination_data':i[2],
	        "Standard Van 53":0,
	        "Standard Reefer 53":0,
	        "Standard Van 48":0,
	        "Standard Reefer 48":0}
	    for j in df_tmp.itertuples():
	        popup[j[3]]=j[4]
	    data.append([[i[4],i[5]],
	                  [i[6],i[7]],
	                  (int(i[3])/max_counts)*10,
	                  colors[i[8]],
	                  [popup]])


	return JsonResponse({"data":data,
		"shippers":sorted(df1['shipper'].unique().tolist()),
		"receivers":sorted(df1['receiver'].unique().tolist())})

@xframe_options_exempt
def just_map_v2_heat_api(response):
	

	customer=response.GET.get('customer',None)
	shipper=response.GET.get('shipper',None)
	receiver=response.GET.getlist('receiver[]',None)
	colors={"Standard Van 53":"#FA3005",
	        "Standard Reefer 53":"#1700FF",
	        "Standard Van 48":"#FF0000",
	        "Standard Reefer 48":"#008FFF"}
	df = df_gd.copy()

	if not customer:
		customer='DOW CHEMICAL COMPANY C/O XPO LOGISTICS'

	if shipper and receiver:
		df1=df[(df['customer']==customer) &\
		(df['shipper']==shipper) & (df['receiver'].isin(receiver))]
	elif shipper:
		df1=df[(df['customer']==customer) &\
				(df['shipper']==shipper)]
	elif receiver:
		df1=df[(df['customer']==customer) &\
		(df['receiver'].isin(receiver))]
	else:
		df1=df[(df['customer']==customer)]
	colors={"Standard Van 53":"#FA3005",
	        "Standard Reefer 53":"#1700FF",
	        "Standard Van 48":"#FF0000",
	        "Standard Reefer 48":"#008FFF"}
	receiver=[]
	shipper=[]
	dfx=df1.groupby(['shipper']).agg({"id":"count",
                    "origin_lat":"max",
                    "origin_lng":"max"}).reset_index()
	for i in dfx.itertuples():
		shipper.append([i[3],i[4],i[2]])
	dfx=df1.groupby(['receiver']).agg({"id":"count",
                    "destination_lat":"max",
                    "destination_lng":"max"}).reset_index()
	for i in dfx.itertuples():
		receiver.append([i[3],i[4],i[2]])

	return JsonResponse({"receiver":receiver,
						"shipper":shipper})

@xframe_options_exempt
def just_map_v2_circles(response):
	

	customer=response.GET.get('customer',None)
	shipper=response.GET.get('shipper',None)
	receiver=response.GET.getlist('receiver[]',None)
	colors={"Standard Van 53":"#FA3005",
	        "Standard Reefer 53":"#1700FF",
	        "Standard Van 48":"#FF0000",
	        "Standard Reefer 48":"#008FFF"}
	df = df_gd.copy()

	if not customer:
		customer='DOW CHEMICAL COMPANY C/O XPO LOGISTICS'

	if shipper and receiver:
		df1=df[(df['customer']==customer) &\
		(df['shipper']==shipper) & (df['receiver'].isin(receiver))]
	elif shipper:
		df1=df[(df['customer']==customer) &\
				(df['shipper']==shipper)]
	elif receiver:
		df1=df[(df['customer']==customer) &\
		(df['receiver'].isin(receiver))]
	else:
		df1=df[(df['customer']==customer)]
	all_locs=df1['origin_data'].values.tolist()+df1['destination_data'].values.tolist()
	all_locs=sorted(list(set(all_locs)))


	circles_=[]
	all_radiuses=[]
	for i in tqdm(all_locs,total=len(all_locs)):
	    tmp1=df1[(df1['origin_data']==i)].reset_index()
	    tmp2=df1[(df1['destination_data']==i)].reset_index()
	    if len(tmp1)>1:
	        circles_.append([[tmp1['origin_lat'][0],tmp1['origin_lng'][0]],len(tmp1)+len(tmp2),i])
	        all_radiuses.append(len(tmp1)+len(tmp2))
	    elif len(tmp2)>1:
	        circles_.append([[tmp2['destination_lat'][0],tmp2['destination_lng'][0]],len(tmp1)+len(tmp2),i])
	        all_radiuses.append(len(tmp1)+len(tmp2))
	    else:
	        continue

	circles=[]
	for i in circles_:
	    circles.append([i[0],i[1]/max(all_radiuses),i[2]])
	# with open('/home/yousuf/Downloads/scalecapacity/text_proj/gold_data/circles_gd.txt', 'rb') as f:
	#    circles = pickle.load(f)

	return JsonResponse({"circles":circles})

@xframe_options_exempt
def just_map_v4(response):
	

	deetz={
	    "type": "FeatureCollection",
	    "features": features
	}
	df=df_gd.copy()

	return render(response ,'blogs/just_map_v4.html',{"feats":deetz,
		"customers":sorted(df['customer'].unique().tolist())})

@xframe_options_exempt
def just_map_v4_shipper_api(response):
	

	customer=response.GET.get('customer',None)
	if customer=='' or customer=='x':
		customer='DOW CHEMICAL COMPANY C/O XPO LOGISTICS'
	if not customer:
		customer='DOW CHEMICAL COMPANY C/O XPO LOGISTICS'
	df = df_gd.copy()
	df1=df[(df['customer']==customer)]
	shippers=df1.groupby("shipper").count()['id'].sort_values(ascending=False)

	return JsonResponse({"shippers":shippers.index[0:10].tolist()})

@xframe_options_exempt
def just_map_v4_receiver_api(response):
	

	customer=response.GET.get('customer',None)
	if customer=='' or customer=='x':
		customer='DOW CHEMICAL COMPANY C/O XPO LOGISTICS'
	if not customer:
		customer='DOW CHEMICAL COMPANY C/O XPO LOGISTICS'
	shipper=response.GET.get('shipper',None)
	df = df_gd.copy()
	if not shipper or shipper=='x' or shipper=='':
		df1=df[(df['customer']==customer)]
	else:
		df1=df[(df['customer']==customer) &\
		(df['shipper']==shipper)]
	receivers=df1.groupby("receiver").count()['id'].sort_values(ascending=False)

	return JsonResponse({"receivers":receivers.index[0:10].tolist()})

@xframe_options_exempt
def just_map_v4_api(response):
	

	df = df_gd.copy()
	customer=response.GET.get('customer',None)
	shipper=response.GET.get('shipper',None)
	receiver=response.GET.getlist('receiver[]',None)
	name=response.GET.get('name',None)
	if not name:
		state=df['destination_state_province'].unique().tolist()+\
		df['origin_state_province'].unique().tolist()
		state=sorted(list(set(state)))
	else:
		state=name.split(" ")[0]
		state=[state]
	colors={"Standard Van 53":"#FA3005",
	        "Standard Reefer 53":"#1700FF",
	        "Standard Van 48":"#FF0000",
	        "Standard Reefer 48":"#008FFF"}
	

	if shipper=='x':
		shipper=None
	if receiver=='x':
		receiver=None

	if not customer:
		customer='DOW CHEMICAL COMPANY C/O XPO LOGISTICS'

	if shipper and receiver:
		df1=df[(df['customer']==customer) &\
		(df['shipper']==shipper) & (df['receiver'].isin(receiver))\
		 & ((df['origin_state_province'].isin(state)) |\
		  (df['destination_state_province'].isin(state)))]
	elif shipper:
		df1=df[(df['customer']==customer) &\
				(df['shipper']==shipper)\
		 & ((df['origin_state_province'].isin(state)) |\
		  (df['destination_state_province'].isin(state)))]
	elif receiver:
		df1=df[(df['customer']==customer) &\
		(df['receiver'].isin(receiver))\
		 & ((df['origin_state_province'].isin(state)) |\
		  (df['destination_state_province'].isin(state)))]
	else:
		df1=df[(df['customer']==customer)\
		 & ((df['origin_state_province'].isin(state)) |\
		  (df['destination_state_province'].isin(state)))]

	df_map=df1.groupby(['origin_state_province','destination_state_province']).agg({"id":"count",
	                                                "origin_lat":"first",
	                                                "origin_lng":"first",
	                                                "destination_lat":"first",
	                                                "destination_lng":"first",
	                                                "equipment_type":"first"}).reset_index()

	data=[]
	max_counts=df_map['id'].max()

	for i in df_map.itertuples():
	    tmp=df1[(df1['destination_state_province']==i[2]) & (df1['origin_state_province']==i[1])]
	    df_tmp=tmp.groupby(['origin_state_province',
	                        'destination_state_province',
	                        'equipment_type']).agg({"id":"count"}).reset_index()
	    popup={'origin_data':i[1],
	        'destination_data':i[2],
	        "Standard Van 53":0,
	        "Standard Reefer 53":0,
	        "Standard Van 48":0,
	        "Standard Reefer 48":0}
	    for j in df_tmp.itertuples():
	        popup[j[3]]=j[4]
	    data.append([[i[4],i[5]],
	                  [i[6],i[7]],
	                  (int(i[3])/max_counts)*10,
	                  colors[i[8]],
	                  [popup]])

	return JsonResponse({"data":data,
		"shippers":sorted(df1['shipper'].unique().tolist()),
		"receivers":sorted(df1['receiver'].unique().tolist())})

@xframe_options_exempt
def just_map_v5(response):
	deetz={
	    "type": "FeatureCollection",
	    "features": features
	}
	df=df_gd.copy()
	

	return render(response ,'blogs/just_map_v6.html',{"feats":deetz,
		"customers":sorted(df['customer'].unique().tolist())})

@xframe_options_exempt
def just_map_v5_shipper_api(response):
	customer=response.GET.getlist('customer[]',None)
	

	if customer=='' or customer==['x'] or customer==['ALL']:
		customer=[]
	if not customer:
		customer=[]
	
	df = df_gd.copy()
	df1=df[(df['customer'].isin(customer))]
	shippers=df1.groupby("shipper").count()['id'].sort_values(ascending=False)
	shippers_vals=[[x[0],str(x[0])+"  ["+str(x[1])+"]"] for x in zip(shippers.index.tolist(),shippers.values.tolist())]
	origin_data=df1['origin_data'].unique().tolist()
	origin_state_province=[x.split(" ")[0].strip().upper() for x in origin_data]
	origin_state_province=sorted(list(set(origin_state_province)))
	origin_city=[" ".join(x.split(" ")[1:]) for x in origin_data]
	origin_city=sorted(list(set(origin_city)))
	destination_data=df1['destination_data'].unique().tolist()
	destination_state_province=[x.split(" ")[0].strip().upper() for x in destination_data]
	destination_state_province=sorted(list(set(destination_state_province)))
	destination_city=[" ".join(x.split(" ")[1:]) for x in destination_data]
	destination_city=sorted(list(set(destination_city)))

	return JsonResponse({"shippers":shippers_vals,
		"origin_st":[us_state_abbrev_codes[x]+f" ({x})" for x in sorted(origin_state_province)],
	"destination_st":[us_state_abbrev_codes[x]+f" ({x})" for x in sorted(destination_state_province)],
	"origin_ct":sorted(origin_city),
	"destination_ct":sorted(destination_city)})

@xframe_options_exempt
def just_map_v5_receiver_api(response):
	

	customer=response.GET.getlist('customer[]',None)
	if customer=='' or customer==['x'] or customer==['ALL']:
		customer=[]
	if not customer:
		customer=[]		
	shipper=response.GET.getlist('shipper[]',None)
	df = df_gd.copy()
	if not shipper or shipper=='x' or shipper=='' or shipper==['ALL'] or shipper=='ALL':
		df1=df[(df['customer'].isin(customer))]
	else:
		df1=df[(df['customer'].isin(customer)) &\
		(df['shipper'].isin(shipper))]
	receivers=df1.groupby("receiver").count()['id'].sort_values(ascending=False)
	receivers_vals=[[x[0],str(x[0])+"  ["+str(x[1])+"]"] for x in zip(receivers.index.tolist(),receivers.values.tolist())]

	return JsonResponse({"receivers":receivers_vals})

@xframe_options_exempt
def just_map_v5_api(response):
	df = df_gd.copy()
	

	colors={"Standard Van 53":"#FA3005",
	        "Standard Reefer 53":"#1700FF",
	        "Standard Van 48":"#FF0000",
	        "Standard Reefer 48":"#008FFF"}
	
	customer=response.GET.getlist('customer[]',None)
	shipper=response.GET.getlist('shipper[]',None)
	print(customer,shipper)
	if shipper==['x'] or shipper==['ALL'] :
		shipper=None
	receiver=response.GET.getlist('receiver[]',None)
	print(receiver)
	if receiver==['x'] or receiver=='x' or receiver=='ALL' or receiver==['ALL'] :
		receiver=None
	if customer=='' or customer==['x'] or customer==['ALL'] :
		customer=['DOW CHEMICAL COMPANY C/O XPO LOGISTICS']
	if not customer:
		customer=['DOW CHEMICAL COMPANY C/O XPO LOGISTICS']

	if shipper and receiver:
		df1=df[(df['customer'].isin(customer)) &\
		(df['shipper'].isin(shipper)) & (df['receiver'].isin(receiver))]
	elif shipper:
		df1=df[(df['customer'].isin(customer)) &\
				(df['shipper'].isin(shipper))]
	elif receiver:
		df1=df[(df['customer'].isin(customer)) &\
		(df['receiver'].isin(receiver))]
	else:
		df1=df[(df['customer'].isin(customer))]

	df_map=df1.groupby(['origin_data','destination_data']).agg({"id":"count",
                                                "equipment_type":"max"}).reset_index()
	locs={}
	dats=list(set(df_map['origin_data'].unique().tolist()+df_map['destination_data'].unique().tolist()))
	for i in dats:
		org=df1[df1['origin_data']==i].reset_index()
		if not len(org)>0:
			dest=df1[df1['destination_data']==i].reset_index()
			latlng=dest.values[0]
			locs[i]=[latlng[17],latlng[18]]
		else:
			latlng=org.values[0]
			locs[i]=[latlng[15],latlng[16]]



	data=[]
	max_counts=df_map['id'].max()
	if len(df_map)<30:
		multiplier=3.7
	else:
		multiplier=8
	for i in df_map.itertuples():
		tmp=df1[(df1['destination_data']==i[2]) & (df1['origin_data']==i[1])]
		df_tmp=tmp.groupby(['origin_data',
							'destination_data',
							'equipment_type']).agg({"id":"count"}).reset_index()
		popup={'origin_data':i[1],
			'destination_data':i[2],
			"Standard Van 53":0,
			"Standard Reefer 53":0,
			"Standard Van 48":0,
			"Standard Reefer 48":0}
		for j in df_tmp.itertuples():
			popup[j[3]]=j[4]
		x=locs[i[1]]
		y=locs[i[2]]
		width=(int(i[3])/max_counts)*10
		if width<1:
			width=0.7
		data.append([x,
					y,
					width,
					colors[i[4]],
					[popup]])


	return JsonResponse({"data":data,
		"shippers":sorted(df1['shipper'].unique().tolist()),
		"receivers":sorted(df1['receiver'].unique().tolist())})

@xframe_options_exempt
def just_map_v5_time_api(response):
	df = df_gd.copy()
	times=response.GET.get('times',None)
	if times:
		date=times
		date1=date.split(" ")[0]
		date2=date.split(" ")[2]
		mask = (df['booked_on'] > datetime.strptime(date1, '%m/%d/%Y')) & (df['booked_on'] <= datetime.strptime(date2, '%m/%d/%Y'))
		df=df.loc[mask]
		if len(df)<1:
			return JsonResponse({"error":[True]})
			df=df_gd.copy()
	colors={"Standard Van 53":"#FA3005",
	        "Standard Reefer 53":"#1700FF",
	        "Standard Van 48":"#FF0000",
	        "Standard Reefer 48":"#008FFF"}
	
	customer=response.GET.getlist('customer[]',None)
	shipper=response.GET.getlist('shipper[]',None)
	# print(customer,shipper)
	if shipper==['x'] or shipper==['ALL'] :
		shipper=None
	receiver=response.GET.getlist('receiver[]',None)
	# print(receiver)
	if receiver==['x'] or receiver=='x' or receiver==['ALL']  or receiver=='ALL':
		receiver=None
	if customer=='' or customer==['x'] or customer==['ALL']:
		customer=['DOW CHEMICAL COMPANY C/O XPO LOGISTICS']
	if not customer:
		customer=['DOW CHEMICAL COMPANY C/O XPO LOGISTICS']

	if shipper and receiver:
		df1=df[(df['customer'].isin(customer)) &\
		(df['shipper'].isin(shipper)) & (df['receiver'].isin(receiver))]
	elif shipper:
		df1=df[(df['customer'].isin(customer)) &\
				(df['shipper'].isin(shipper))]
	elif receiver:
		df1=df[(df['customer'].isin(customer)) &\
		(df['receiver'].isin(receiver))]
	else:
		df1=df[(df['customer'].isin(customer))]
	if len(df1)<1:
		return JsonResponse({"error":[True]})
	origin_st=response.GET.getlist('origin_st[]',None)
	if origin_st:
		origin_st=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in origin_st]
	if not origin_st:
		origin_st=df1['origin_state_province'].unique().tolist()

	destination_st=response.GET.getlist('destination_st[]',None)
	if not destination_st:
		destination_st=df1['destination_state_province'].unique().tolist()
	if destination_st:
		destination_st=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in destination_st]
	# if len(origin_st)==0 and len(destination_st)==0:
	# 	return JsonResponse({"error":[True]})
	df1=df1[(df1['origin_state_province'].isin(origin_st)) & \
		(df1['destination_state_province'].isin(destination_st))]
	origin_ct=response.GET.getlist('origin_ct[]',None)
	if origin_ct:
		df1=df1[df1['origin_city'].isin(origin_ct)]
	destination_ct=response.GET.getlist('destination_ct[]',None)
	if destination_ct:
		df1=df1[df1['destination_city'].isin(destination_ct)]



	df_map=df1.groupby(['origin_data','destination_data']).agg({"id":"count",
                                                "equipment_type":"max",
												"duration":"mean"}).reset_index()
	locs={}
	dats=list(set(df_map['origin_data'].unique().tolist()+df_map['destination_data'].unique().tolist()))
	for i in dats:
		org=df1[df1['origin_data']==i].reset_index()
		if not len(org)>0:
			dest=df1[df1['destination_data']==i].reset_index()
			latlng=dest.values[0]
			locs[i]=[latlng[17],latlng[18]]
		else:
			latlng=org.values[0]
			locs[i]=[latlng[15],latlng[16]]

	data=[]
	max_counts=df_map['id'].max()
	if len(df_map)<30:
		multiplier=3.7
	else:
		multiplier=8
	for i in df_map.itertuples():
		tmp=df1[(df1['destination_data']==i[2]) & (df1['origin_data']==i[1])]
		df_tmp=tmp.groupby(['origin_data',
							'destination_data',
							'equipment_type']).agg({"id":"count"}).reset_index()
		popup={'origin_data':i[1],
			'destination_data':i[2],
			"Standard Van 53":0,
			"Standard Reefer 53":0,
			"Standard Van 48":0,
			"Standard Reefer 48":0}
		for j in df_tmp.itertuples():
			popup[j[3]]=j[4]
		x=locs[i[1]]
		y=locs[i[2]]
		width=(int(i[3])/max_counts)*10
		if width<1:
			width=0.9
		data.append([x,
					y,
					width,
					colors[i[4]],
					[popup],
					i[5],
					i[1],
					i[2]])

	return JsonResponse({"error":[False],"data":data,
		"shippers":sorted(df1['shipper'].unique().tolist()),
		"receivers":sorted(df1['receiver'].unique().tolist())})

@xframe_options_exempt
def just_map_v5_heat_api(response):
	df = df_gd.copy()
	

	colors={"Standard Van 53":"#FA3005",
	        "Standard Reefer 53":"#1700FF",
	        "Standard Van 48":"#FF0000",
	        "Standard Reefer 48":"#008FFF"}
	
	customer=response.GET.getlist('customer[]',None)
	shipper=response.GET.getlist('shipper[]',None)
	if shipper==['x'] or shipper==['ALL'] :
		shipper=None
	receiver=response.GET.getlist('receiver[]',None)
	if receiver==['x'] or receiver=='x' or receiver=='ALL' or receiver==['ALL'] :
		receiver=None
	if customer=='' or customer==['x'] or customer==['ALL'] :
		customer=['DOW CHEMICAL COMPANY C/O XPO LOGISTICS']
	if not customer:
		customer=['DOW CHEMICAL COMPANY C/O XPO LOGISTICS']

	if shipper and receiver:
		df1=df[(df['customer'].isin(customer)) &\
		(df['shipper'].isin(shipper)) & (df['receiver'].isin(receiver))]
	elif shipper:
		df1=df[(df['customer'].isin(customer)) &\
				(df['shipper'].isin(shipper))]
	elif receiver:
		df1=df[(df['customer'].isin(customer)) &\
		(df['receiver'].isin(receiver))]
	else:
		df1=df[(df['customer'].isin(customer))]
	origin_st=response.GET.getlist('origin_st[]',None)
	if origin_st:
		origin_st=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in origin_st]
	if not origin_st:
		origin_st=df1['origin_state_province'].unique().tolist()

	destination_st=response.GET.getlist('destination_st[]',None)
	if not destination_st:
		destination_st=df1['destination_state_province'].unique().tolist()
	if destination_st:
		destination_st=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in destination_st]
	# if len(origin_st)==0 and len(destination_st)==0:
	# 	return JsonResponse({"error":[True]})
	df1=df1[(df1['origin_state_province'].isin(origin_st)) & \
		(df1['destination_state_province'].isin(destination_st))]
	origin_ct=response.GET.getlist('origin_ct[]',None)
	if origin_ct:
		df1=df1[df1['origin_city'].isin(origin_ct)]
	destination_ct=response.GET.getlist('destination_ct[]',None)
	if destination_ct:
		df1=df1[df1['destination_city'].isin(destination_ct)]
	print(origin_st)
	receiver=[]
	shipper=[]
	df_map_r=df1.groupby(['origin_lat',
						'origin_lng']).agg({"id":"count"}).reset_index()
	for i in df_map_r.itertuples():
		shipper.append([i[1],i[2],i[3]])
	df_map_s=df1.groupby(['destination_lat',
						'destination_lng']).agg({"id":"count"}).reset_index()
	for i in df_map_s.itertuples():
		receiver.append([i[1],i[2],i[3]])

	return JsonResponse({"receiver":receiver,
						"shipper":shipper})

@xframe_options_exempt
def just_map_v5_time_heat_api(response):
	df = df_gd.copy()
	

	times=response.GET.get('times',None)
	if times:
		date=times
		date1=date.split(" ")[0]
		date2=date.split(" ")[2]
		mask = (df['booked_on'] > datetime.strptime(date1, '%m/%d/%Y')) & (df['booked_on'] <= datetime.strptime(date2, '%m/%d/%Y'))
		df=df.loc[mask]
		if len(df)<1:
			df=df_gd.copy()
	colors={"Standard Van 53":"#FA3005",
	        "Standard Reefer 53":"#1700FF",
	        "Standard Van 48":"#FF0000",
	        "Standard Reefer 48":"#008FFF"}
	
	customer=response.GET.getlist('customer[]',None)
	shipper=response.GET.getlist('shipper[]',None)
	# print(customer,shipper)
	if shipper==['x'] or shipper==['ALL'] :
		shipper=None
	receiver=response.GET.getlist('receiver[]',None)
	# print(receiver)
	if receiver==['x'] or receiver=='x' or receiver==['ALL']  or receiver=='ALL':
		receiver=None
	if customer=='' or customer==['x'] or customer==['ALL']:
		customer=['DOW CHEMICAL COMPANY C/O XPO LOGISTICS']
	if not customer:
		customer=['DOW CHEMICAL COMPANY C/O XPO LOGISTICS']

	if shipper and receiver:
		df1=df[(df['customer'].isin(customer)) &\
		(df['shipper'].isin(shipper)) & (df['receiver'].isin(receiver))]
	elif shipper:
		df1=df[(df['customer'].isin(customer)) &\
				(df['shipper'].isin(shipper))]
	elif receiver:
		df1=df[(df['customer'].isin(customer)) &\
		(df['receiver'].isin(receiver))]
	else:
		df1=df[(df['customer'].isin(customer))]
	origin_st=response.GET.getlist('origin_st[]',None)
	if origin_st:
		origin_st=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in origin_st]
	if not origin_st:
		origin_st=df1['origin_state_province'].unique().tolist()

	destination_st=response.GET.getlist('destination_st[]',None)
	if not destination_st:
		destination_st=df1['destination_state_province'].unique().tolist()
	if destination_st:
		destination_st=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in destination_st]
	# if len(origin_st)==0 and len(destination_st)==0:
	# 	return JsonResponse({"error":[True]})
	df1=df1[(df1['origin_state_province'].isin(origin_st)) & \
		(df1['destination_state_province'].isin(destination_st))]
	origin_ct=response.GET.getlist('origin_ct[]',None)
	if origin_ct:
		df1=df1[df1['origin_city'].isin(origin_ct)]
	destination_ct=response.GET.getlist('destination_ct[]',None)
	if destination_ct:
		df1=df1[df1['destination_city'].isin(destination_ct)]	
	receiver=[]
	shipper=[]
	df_map_r=df1.groupby(['origin_lat',
						'origin_lng']).agg({"id":"count"}).reset_index()
	for i in df_map_r.itertuples():
		shipper.append([i[1],i[2],i[3]])
	df_map_s=df1.groupby(['destination_lat',
						'destination_lng']).agg({"id":"count"}).reset_index()
	for i in df_map_s.itertuples():
		receiver.append([i[1],i[2],i[3]])

	return JsonResponse({"receiver":receiver,
						"shipper":shipper})

@xframe_options_exempt
def just_map_get_slider_values(response):
	

	year=response.GET.get('year',None)
	week_month=response.GET.get('week_month',None)
	if not year:
		year='2021'
	if not week_month:
		week_month='Week'
	df = df_gd.copy()
	df=df[df['created_year']==int(year)]
	if week_month=='Week':
		sliders=sorted(df['created_week'].unique().tolist())
	elif week_month=='Month':
		sliders=sorted(df['created_month_num'].unique().tolist())
	return JsonResponse({"sliders":sliders})

@xframe_options_exempt
def just_map_v7_slider(response):
	

	df = df_gd.copy()
	colors={"Standard Van 53":"#FA3005",
	        "Standard Reefer 53":"#1700FF",
	        "Standard Van 48":"#FF0000",
	        "Standard Reefer 48":"#008FFF"}
	
	# customer=response.GET.getlist('customer[]',None)
	# shipper=response.GET.getlist('shipper[]',None)
	# if shipper==['x'] or shipper==['ALL'] :
	# 	shipper=None
	# receiver=response.GET.getlist('receiver[]',None)
	# if receiver==['x'] or receiver=='x' or receiver=='ALL' or receiver==['ALL'] :
	# 	receiver=None
	# if customer=='' or customer==['x'] or customer==['ALL'] :
	# 	customer=['DOW CHEMICAL COMPANY C/O XPO LOGISTICS']
	# if not customer:
	# 	customer=['DOW CHEMICAL COMPANY C/O XPO LOGISTICS']

	# if shipper and receiver:
	# 	df1=df[(df['customer'].isin(customer)) &\
	# 	(df['shipper'].isin(shipper)) & (df['receiver'].isin(receiver))]
	# elif shipper:
	# 	df1=df[(df['customer'].isin(customer)) &\
	# 			(df['shipper'].isin(shipper))]
	# elif receiver:
	# 	df1=df[(df['customer'].isin(customer)) &\
	# 	(df['receiver'].isin(receiver))]
	# else:
	# 	df1=df[(df['customer'].isin(customer))]
	customer=['DOW CHEMICAL COMPANY C/O XPO LOGISTICS']
	df1=df[(df['customer'].isin(customer))]
	shp_rcv=[]
	locs={}
	dats=list(set(df1['year_week'].unique().tolist()))
	for i in dats:
		org=df1[df1['year_week']==i].reset_index()
		locs[str(i)]=[str(org['booked_on'].min()),str(org['booked_on'].max())]

	df_map=df1.groupby(['origin_lat',
						'origin_lng',
						'destination_lat',
						'destination_lng','year_week']).agg({"id":"count"}).reset_index()
	for i in df_map.itertuples():
		ed=locs[str(i[5])][1].split("-")
		sd=locs[str(i[5])][0].split("-")
		tmp={
			"type":"Feature",
			"geometry":{
			"type":"LineString",
			"coordinates":[[i[1],i[2]],[i[3],i[4]]]
			},
			"properties":{
			"endDate":str(int(ed[1]))+'/'+str(int(ed[2].split(" ")[0]))+'/'+str(int(ed[0][-2:]))+" 22:00",
			"startDate":str(int(sd[1]))+'/'+str(int(sd[2].split(" ")[0]))+'/'+str(int(sd[0][-2:]))+" 22:00"
			}
		}
		# shp_rcv.append([i[1],i[2],i[3],i[4],i[6],
		#              locs[str(i[5])]])
		shp_rcv.append(tmp)
	myData = {
	"type": "FeatureCollection",
	"features":shp_rcv
	}
	return JsonResponse({"all_sliders":[myData]})

@xframe_options_exempt
def just_map_v7(response):
	

	deetz={
	    "type": "FeatureCollection",
	    "features": features
	}
	df=df_gd.copy()

	return render(response ,'blogs/just_map_v8.html',{"feats":deetz,
		"customers":sorted(df['customer'].unique().tolist())})

@xframe_options_exempt
def just_map_v8_slider(response):
	

	df = df_gd.copy()
	times=response.GET.get('times',None)
	if times:
		date=times
		date1=date.split(" ")[0]
		date2=date.split(" ")[2]
		mask = (df['booked_on'] > datetime.strptime(date1, '%m/%d/%Y')) & (df['booked_on'] <= datetime.strptime(date2, '%m/%d/%Y'))
		df=df.loc[mask]
		if len(df)<1:
			return JsonResponse({"error":[True]})
			df=df_gd.copy()
	colors={"Standard Van 53":"#FA3005",
	        "Standard Reefer 53":"#1700FF",
	        "Standard Van 48":"#FF0000",
	        "Standard Reefer 48":"#008FFF"}
	
	customer=response.GET.getlist('customer[]',None)
	shipper=response.GET.getlist('shipper[]',None)
	if shipper==['x'] or shipper==['ALL'] :
		shipper=None
	receiver=response.GET.getlist('receiver[]',None)
	if receiver==['x'] or receiver=='x' or receiver=='ALL' or receiver==['ALL'] :
		receiver=None
	if customer=='' or customer==['x'] or customer==['ALL'] :
		customer=['DOW CHEMICAL COMPANY C/O XPO LOGISTICS']
	if not customer:
		customer=['DOW CHEMICAL COMPANY C/O XPO LOGISTICS']

	if shipper and receiver:
		df1=df[(df['customer'].isin(customer)) &\
		(df['shipper'].isin(shipper)) & (df['receiver'].isin(receiver))]
	elif shipper:
		df1=df[(df['customer'].isin(customer)) &\
				(df['shipper'].isin(shipper))]
	elif receiver:
		df1=df[(df['customer'].isin(customer)) &\
		(df['receiver'].isin(receiver))]
	else:
		df1=df[(df['customer'].isin(customer))]
	# customer=['DOW CHEMICAL COMPANY C/O XPO LOGISTICS']
	# df1=df[(df['customer'].isin(customer))]
	if len(df1)<1:
		return JsonResponse({"error":[True]})
	df_map=df1.groupby(['origin_data','destination_data','year_week']).agg({"id":"count",
												"equipment_type":"max",
												"booked_on":"first"}).reset_index()
	locs={}
	dats=list(set(df_map['origin_data'].unique().tolist()+df_map['destination_data'].unique().tolist()))
	for i in dats:
		org=df1[df1['origin_data']==i].reset_index()
		if not len(org)>0:
			dest=df1[df1['destination_data']==i].reset_index()
			latlng=dest.values[0]
			locs[i]=[latlng[17],latlng[18]]
		else:
			latlng=org.values[0]
			locs[i]=[latlng[15],latlng[16]]

	timez={}
	dats=list(set(df1['year_week'].unique().tolist()))
	for i in dats:
		org=df1[df1['year_week']==i].reset_index()
		timez[str(i)]=str(org['booked_on'].min())

	data=[]
	max_counts=df_map['id'].max()
	if len(df_map)<30:
		multiplier=3.7
	else:
		multiplier=8

	df_map.sort_values(by=['booked_on'],ascending=True,inplace=True)

	for i in df_map.itertuples():
		tmp=df1[(df1['destination_data']==i[2]) & (df1['origin_data']==i[1])]
		df_tmp=tmp.groupby(['origin_data',
							'destination_data',
						'equipment_type']).agg({"id":"count"}).reset_index()
		popup={'origin_data':i[1],
			'destination_data':i[2],
			"Standard Van 53":0,
			"Standard Reefer 53":0,
			"Standard Van 48":0,
			"Standard Reefer 48":0}
		for j in df_tmp.itertuples():
			popup[j[3]]=j[4]
		x=locs[i[1]]
		y=locs[i[2]]
		width=(int(i[4])/max_counts)*10
		if width<1:
			width=0.7
		data.append([x,
					y,
					width,
					colors[i[5]],
					[popup],
					str(timez[str(i[3])])+"+01"])

	return JsonResponse({"error":[False],"data":data,
		"shippers":sorted(df1['shipper'].unique().tolist()),
		"receivers":sorted(df1['receiver'].unique().tolist())})

@xframe_options_exempt
def just_map_v9(response):
	

	deetz={
	    "type": "FeatureCollection",
	    "features": features
	}
	df=df_gd.copy()

	return render(response ,'blogs/just_map_v9.html',{"feats":deetz,
		"customers":sorted(df['customer'].unique().tolist())})

@xframe_options_exempt
def just_map_v9_time_api(response):
	

	df = df_gd.copy()
	times=response.GET.get('times',None)
	if times:
		date=times
		date1=date.split(" ")[0]
		date2=date.split(" ")[2]
		mask = (df['booked_on'] > datetime.strptime(date1, '%m/%d/%Y')) & (df['booked_on'] <= datetime.strptime(date2, '%m/%d/%Y'))
		df=df.loc[mask]
		if len(df)<1:
			return JsonResponse({"error":[True]})
			df=df_gd.copy()
	colors={"Standard Van 53":"#FA3005",
	        "Standard Reefer 53":"#1700FF",
	        "Standard Van 48":"#FF0000",
	        "Standard Reefer 48":"#008FFF"}
	
	customer=response.GET.getlist('customer[]',None)
	shipper=response.GET.getlist('shipper[]',None)
	# print(customer,shipper)
	if shipper==['x'] or shipper==['ALL'] :
		shipper=None
	receiver=response.GET.getlist('receiver[]',None)
	# print(receiver)
	if receiver==['x'] or receiver=='x' or receiver==['ALL']  or receiver=='ALL':
		receiver=None
	if customer=='' or customer==['x'] or customer==['ALL']:
		customer=['DOW CHEMICAL COMPANY C/O XPO LOGISTICS']
	if not customer:
		customer=['DOW CHEMICAL COMPANY C/O XPO LOGISTICS']

	if shipper and receiver:
		df1=df[(df['customer'].isin(customer)) &\
		(df['shipper'].isin(shipper)) & (df['receiver'].isin(receiver))]
	elif shipper:
		df1=df[(df['customer'].isin(customer)) &\
				(df['shipper'].isin(shipper))]
	elif receiver:
		df1=df[(df['customer'].isin(customer)) &\
		(df['receiver'].isin(receiver))]
	else:
		df1=df[(df['customer'].isin(customer))]
	if len(df1)<1:
		return JsonResponse({"error":[True]})
	
	df_map=df1.groupby(['origin_data','destination_data']).agg({"id":"count",
                                                "equipment_type":"max",
												"duration":"mean"}).reset_index()
	df_map.sort_values(by=['id'],ascending=False,inplace=True)
	df_map=df_map[0:40]
	locs={}
	dats=list(set(df_map['origin_data'].unique().tolist()+df_map['destination_data'].unique().tolist()))
	for i in dats:
		org=df1[df1['origin_data']==i].reset_index()
		if not len(org)>0:
			dest=df1[df1['destination_data']==i].reset_index()
			latlng=dest.values[0]
			# locs[i]=[latlng[17],latlng[18]]
			locs[i]=[latlng[18],latlng[17]]
		else:
			latlng=org.values[0]
			# locs[i]=[latlng[15],latlng[16]]
			locs[i]=[latlng[16],latlng[15]]

	data=[]
	max_counts=df_map['id'].max()
	if len(df_map)<30:
		multiplier=3.7
	else:
		multiplier=8
	for i in df_map.itertuples():
		tmp=df1[(df1['destination_data']==i[2]) & (df1['origin_data']==i[1])]
		df_tmp=tmp.groupby(['origin_data',
							'destination_data',
							'equipment_type']).agg({"id":"count"}).reset_index()
		popup={'origin_data':i[1],
			'destination_data':i[2],
			"Standard Van 53":0,
			"Standard Reefer 53":0,
			"Standard Van 48":0,
			"Standard Reefer 48":0}
		for j in df_tmp.itertuples():
			popup[j[3]]=j[4]
		x=locs[i[1]]
		y=locs[i[2]]
		width=(int(i[3])/max_counts)*10
		if width<1:
			width=0.7
		t={
			"type": "LineString",
			"properties": {
				"popupContent": [popup],
				"width":width,
				"color": colors[i[4]]
				},
			"coordinates": [x,y]
			}
		data.append(t)

	return JsonResponse({"error":[False],"data":data,
		"shippers":sorted(df1['shipper'].unique().tolist()),
		"receivers":sorted(df1['receiver'].unique().tolist())})

@xframe_options_exempt
def just_map_v9_heat_chart(response):
	

	df = df_gd.copy()
	selector=response.GET.get('week_month',None)
	if not selector:
		selector='year_month'
	selector0=response.GET.get('selector0',None)
	if not selector0:
		selector0='customer'
	customer=response.GET.getlist('customer[]',None)
	if not customer:
		customer=['DOW CHEMICAL COMPANY C/O XPO LOGISTICS']
	df1=df[(df['customer'].isin(customer))]
	if len(df1)<1:
		return JsonResponse({"error":[True]})
	# selector='year_month'
	# selector0='customer'
	df1['created_year']=df1['created_year'].astype(str)
	df1['created_week']=df1['created_week'].astype(str)
	df1['year_month']=df1[['created_year', 'created_month']].agg(' '.join, axis=1)
	df1['travel_data']=df1[['origin_data', 'destination_data']].agg('->'.join, axis=1)
	df1['year_week_str']=df1[['created_year', 'created_week']].agg(' Week '.join, axis=1)
	df1['created_year']=df1['created_year'].astype(int)
	df1['created_week']=df1['created_week'].astype(int)
	carr=df1.groupby([selector0,selector]).agg({'id':'count',
												'year_week':'max',
                                                'created_year':'max',
                                                'created_week':'max',
                                                'created_month_num':'max'}).reset_index()
	if selector=='year_week_str':
		carr.sort_values(by=['created_year','created_week'],ascending=True,inplace=True)
	else:
		carr.sort_values(by=['created_year','created_month_num'],ascending=True,inplace=True)

	if len(carr)<5:
		return JsonResponse({"error":[True]})
	lanes=carr.groupby([selector0]).count().sort_values(by=['id'],
					ascending=False)['id'][:20].index.tolist()
	carr=carr[carr[selector0].isin(lanes)]
	year_weeks=carr[selector].unique().tolist()
	if selector=='year_week_str':
		year_weeks=year_weeks[-14:]
	# else:
	# 	year_weeks.sort()
	heats=[]
	for i in lanes:
		vals=[]
		for j in year_weeks:
			try:
				val=carr[(carr[selector]==j) &\
					 (carr[selector0]==i)]['id'].values.tolist()[0]
			except IndexError as e:
				val=0
			vals.append(val)
		heats.append({
			"name": i,
			"data": vals
			})

	ranges=[]
	lst = range(1,carr['id'].max()+1)
	nameheat=['low','medium','high','extreme']
	colorheat=['#00A100','#128FD9','#FFB200','#FF0000']
	for i in zip(np.array_split(lst, 4),nameheat,colorheat):
		ranges.append(
				{
		"from": int(i[0].min()),
		"to": int(i[0].max()),
		"name": i[1],
		"color": i[2]
	})
	if selector=='year_week_str':
		return JsonResponse({"error":[False],
			"heat_series":heats,
			"colorscale":ranges,
			"xaxis":[str(x) for x in year_weeks[-14:]]})
	else:
		return JsonResponse({"error":[False],
			"heat_series":heats,
			"colorscale":ranges,
			"xaxis":[str(x) for x in year_weeks]})

@xframe_options_exempt
def similar_lanes(response):
	

	df = df_gd.copy()
	df=df[df['created_year']==2020]
	year_weeks=df['year_week'].unique().tolist()
	year_weeks.sort()
	customer=response.GET.get('customer',None)
	if not customer:
		customer='99 CENTS ONLY STORE'
	loads_val=response.GET.get('loads_val',None)
	if not loads_val:
		loads_val=1
	price_range=response.GET.get('price_range',None)
	if not price_range:
		price_range=1
	lanes_range=response.GET.get('lanes_range',None)
	if not lanes_range:
		lanes_range=1
	shippers_range=response.GET.get('shippers_range',None)
	if not shippers_range:
		shippers_range=1
	print("xxxxxxxx",customer,"xxxxxxxx",loads_val)
	
	df2=df[df['customer']==customer]
	current_prices_customer=[]
	current_loads_customer=[]
	current_shipper_customer=[]
	current_receiver_customer=[]
	current_lanes_customer=[]

	current_shipper_customer.append(df2['shipper'].unique().tolist())
	current_receiver_customer.append(df2['receiver'].unique().tolist())
	current_lanes_customer.append(df2['travel_data'].unique().tolist())

	for year_week in year_weeks:
		p=df2[df2['year_week']==year_week]['customer_rate'].mean()
		if str(p)=='nan':
			p=0
		current_prices_customer.append(int(p))
		p=df2[df2['year_week']==year_week]
		current_loads_customer.append(int(len(p)))
	current_customer=[current_prices_customer,current_loads_customer]

	similiarity_shippers_receivers_customers=list(map(lambda x : jaccard_similarity(x,current_shipper_customer[0]),
												all_shippers_customers))
	similiarity_lanes_customers=list(map(lambda x : jaccard_similarity(x,current_lanes_customer[0]),
												all_lanes_customers))
	loads_similarity = list(map(lambda x : cdist(np.array([current_loads_customer]),
												np.array([x]),'euclidean')[0][0], all_loads_customers))
	max_loads_similarity=max(loads_similarity)
	loads_similarity = [x/max_loads_similarity for x in loads_similarity]

	price_similarity = list(map(lambda x : cdist(np.array([current_prices_customer]),
												np.array([x]),'euclidean')[0][0], all_prices_customers))
	max_price_similarity=max(price_similarity)
	price_similarity = [x/max_price_similarity for x in price_similarity]

	similarity= [(float(loads_val)*float(1-x[0]))\
				+(float(price_range)*float(1-x[1]))\
				+(float(shippers_range)*float(x[2]))\
				+(float(lanes_range)*float(x[3])) \
				for x in zip(loads_similarity,price_similarity,
							similiarity_shippers_receivers_customers,
							similiarity_lanes_customers )]
	similarity_=[x for x in similarity]# if x!=2 and x!=3 and x!=1 and x!=4
	similarity_index=[i[0] for i in sorted(enumerate(similarity_), key=lambda x:x[1])]
	similarity_index.reverse()

	custs = [customers[i] for i in similarity_index][0:20]
	custs=[x for x in custs if not x == customer]
	dfx=df[df['customer'].isin(custs)]

	dfx_map=dfx.groupby(['customer']).agg({"id":"count",
										"customer_rate":"mean",
										"buy_cost":"mean"})
	dfx_map['customer_rate']=dfx_map['customer_rate'].astype(int)
	dfx_map['buy_cost']=dfx_map['buy_cost'].astype(int)
	data=dfx_map.values.tolist()
	data=[[x[1]]+x[0] for x in zip(data,dfx_map.index)]
	return JsonResponse({"error":[False],"data":data})

@xframe_options_exempt
def just_heat_chart_v1(response):
	

	df=df_gd.copy()

	return render(response ,'blogs/just_heat_chart_v1.html',{
		"origin_st":sorted(df['origin_state_province'].unique().tolist()),
		"destination_st":sorted(df['destination_state_province'].unique().tolist()),
		"origin_ct":sorted(df['origin_city'].unique().tolist()),
		"destination_ct":sorted(df['destination_city'].unique().tolist())})

@xframe_options_exempt
def just_heat_chart_v1_api(response):
	df = df_gd.copy()
	customer=response.GET.getlist('customer[]',None)
	if customer:
		df=df[df['customer'].isin(customer)]
	selector=response.GET.get('week_month',None)
	if not selector:
		selector='year_month'
	selector0=response.GET.get('selector0',None)
	if not selector0:
		selector0='customer'
	origin_st=response.GET.getlist('origin_st[]',None)
	if origin_st:
		origin_st=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in origin_st]
	if not origin_st:
		origin_st=df['origin_state_province'].unique().tolist()
	

	destination_st=response.GET.getlist('destination_st[]',None)
	if not destination_st:
		destination_st=df['destination_state_province'].unique().tolist()
	if destination_st:
		destination_st=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in destination_st]
	# if len(origin_st)==0 and len(destination_st)==0:
	# 	return JsonResponse({"error":[True]})
	
	df1=df[(df['origin_state_province'].isin(origin_st)) & \
		(df['destination_state_province'].isin(destination_st))]
	origin_ct=response.GET.getlist('origin_ct[]',None)
	if origin_ct:
		df1=df1[df1['origin_city'].isin(origin_ct)]
	destination_ct=response.GET.getlist('destination_ct[]',None)
	if destination_ct:
		df1=df1[df1['destination_city'].isin(destination_ct)]		
		
	if len(df1)<1:
		return JsonResponse({"error":[True]})
	# selector='year_month'
	# selector0='customer'
	df1['created_year']=df1['created_year'].astype(str)
	df1['created_week']=df1['created_week'].astype(str)
	df1['year_month']=df1[['created_year', 'created_month']].agg(' '.join, axis=1)
	df1['travel_data']=df1[['origin_data', 'destination_data']].agg('->'.join, axis=1)
	df1['year_week_str']=df1[['created_year', 'created_week']].agg(' Week '.join, axis=1)
	df1['created_year']=df1['created_year'].astype(int)
	df1['created_week']=df1['created_week'].astype(int)
	carr=df1.groupby([selector0,selector]).agg({'id':'count',
												'year_week':'max',
												'created_year':'max',
												'created_week':'max',
												'created_month_num':'max',
                                                'customer_rate':['min', 'max', 'mean']}).reset_index()
	carr_columns=[]
	for x in carr.columns.ravel():
		if x[0]=="customer_rate":
			carr_columns.append("_".join(x))
		else:
			carr_columns.append(x[0])
	carr.columns = carr_columns
	if selector=='year_week_str':
		carr.sort_values(by=['created_year','created_week'],ascending=True,inplace=True)
	else:
		carr.sort_values(by=['created_year','created_month_num'],ascending=True,inplace=True)

	if len(carr)<8:
		return JsonResponse({"error":[True]})
	lanes=carr.groupby([selector0]).count().sort_values(by=['id'],
					ascending=False)['id'][:20].index.tolist()
	carr=carr[carr[selector0].isin(lanes)]
	year_weeks=carr[selector].unique().tolist()
	if selector=='year_week_str':
		year_weeks=year_weeks[-14:]
	# else:
	# 	year_weeks.sort()
	heats=[]
	all_prices={}
	for i in lanes:
		vals=[]
		prices={}
		for j in year_weeks:
			# try:
			# 	val=carr[(carr[selector]==j) &\
			# 			(carr[selector0]==i)]['id'].values.tolist()[0]
			# except IndexError as e:
			# 	val=0
			val=carr[(carr[selector]==j) &\
					(carr[selector0]==i)]['id'].values.tolist()
			if len(val)>0:
				val=val[0]
			else:
				val=0
			vals.append(val)
			val=carr[(carr[selector]==j) &\
					(carr[selector0]==i)]['customer_rate_mean'].values.tolist()
			if len(val)>0:
				val=int(val[0])
			else:
				val=0
			prices[j]=val
		all_prices[i]=prices
		heats.append({
			"name": i,
			"data": vals
			})

	ranges=[]
	lst = range(1,carr['id'].max()+1)
	nameheat=['low','medium','high','extreme']
	colorheat=['#00A100','#128FD9','#FFB200','#FF0000']
	for i in zip(np.array_split(lst, 4),nameheat,colorheat):
		ranges.append(
				{
		"from": int(i[0].min()),
		"to": int(i[0].max()),
		"name": i[1],
		"color": i[2]
	})
	if selector=='year_week_str':
		return JsonResponse({"error":[False],
			"heat_series":heats,
			"colorscale":ranges,
			"xaxis":[str(x) for x in year_weeks[-14:]],
			"lanes":lanes,
			"year_week":year_weeks,
			'all_prices':all_prices})
	else:
		return JsonResponse({"error":[False],
			"heat_series":heats,
			"colorscale":ranges,
			"xaxis":[str(x) for x in year_weeks],
			"lanes":lanes,
			"year_week":year_weeks,
			'all_prices':all_prices})

@xframe_options_exempt
def just_map_v11_time_api(response):
	df = df_gd.copy()
	times=response.GET.get('times',None)
	if times:
		date=times
		date1=date.split(" ")[0]
		date2=date.split(" ")[2]
		mask = (df['booked_on'] > datetime.strptime(date1, '%m/%d/%Y')) & (df['booked_on'] <= datetime.strptime(date2, '%m/%d/%Y'))
		df=df.loc[mask]
		if len(df)<1:
			return JsonResponse({"error":[True]})
			df=df_gd.copy()
	colors={"Standard Van 53":"#FA3005",
	        "Standard Reefer 53":"#1700FF",
	        "Standard Van 48":"#FF0000",
	        "Standard Reefer 48":"#008FFF"}
	

	customer=response.GET.getlist('customer[]',None)
	shipper=response.GET.getlist('shipper[]',None)
	# print(customer,shipper)
	if shipper==['x'] or shipper==['ALL'] :
		shipper=None
	receiver=response.GET.getlist('receiver[]',None)
	# print(receiver)
	if receiver==['x'] or receiver=='x' or receiver==['ALL']  or receiver=='ALL':
		receiver=None
	if customer=='' or customer==['x'] or customer==['ALL']:
		customer=['DOW CHEMICAL COMPANY C/O XPO LOGISTICS']
	if not customer:
		customer=['DOW CHEMICAL COMPANY C/O XPO LOGISTICS']

	if shipper and receiver:
		df1=df[(df['customer'].isin(customer)) &\
		(df['shipper'].isin(shipper)) & (df['receiver'].isin(receiver))]
	elif shipper:
		df1=df[(df['customer'].isin(customer)) &\
				(df['shipper'].isin(shipper))]
	elif receiver:
		df1=df[(df['customer'].isin(customer)) &\
		(df['receiver'].isin(receiver))]
	else:
		df1=df[(df['customer'].isin(customer))]
	if len(df1)<1:
		return JsonResponse({"error":[True]})

	df1['created_year']=df1['created_year'].astype(str)
	df1['created_week']=df1['created_week'].astype(str)
	df1['year_month']=df1[['created_year', 'created_month']].agg(' '.join, axis=1)
	df1['travel_data']=df1[['origin_data', 'destination_data']].agg('->'.join, axis=1)
	df1['year_week_str']=df1[['created_year', 'created_week']].agg(' Week '.join, axis=1)
	df1['created_year']=df1['created_year'].astype(int)
	df1['created_week']=df1['created_week'].astype(int)
	df_map=df1.groupby(['origin_data','destination_data',
					'year_week']).agg({'id':'count',
										"equipment_type":"max",
										"duration":"mean",
												'created_year':'max',
												'created_week':'max',
												'created_month_num':'max',
												'created_month':'max'}).reset_index()
	df_map.sort_values(by=['created_year','created_week'],ascending=True,inplace=True)

	weeks={}
	k=1
	for i in df_map['year_week'].unique():
		weeks[i]=k
		k=k+1
	df_map['weeks']=df_map['year_week'].apply(lambda row: weeks[row])
	weeks1={}
	k=1
	for i in df1['year_week'].unique():
		weeks1[i]=k
		k=k+1
	df1['weeks']=df1['year_week'].apply(lambda row: weeks1[row])

	df_map=df_map
	locs={}
	dats=list(set(df_map['origin_data'].unique().tolist()+df_map['destination_data'].unique().tolist()))
	for i in dats:
		org=df1[df1['origin_data']==i].reset_index()
		if not len(org)>0:
			dest=df1[df1['destination_data']==i].reset_index()
			latlng=dest.values[0]
			# locs[i]=[latlng[17],latlng[18]]
			locs[i]=[latlng[18],latlng[17]]
		else:
			latlng=org.values[0]
			# locs[i]=[latlng[15],latlng[16]]
			locs[i]=[latlng[16],latlng[15]]

	all_data={}
	for week in df_map['weeks'].unique().tolist():
		df_map_tmp=df_map[df_map['weeks']==week]
		data=[]
		max_counts=df_map_tmp['id'].max()
		if len(df_map_tmp)<30:
			multiplier=4.2
		else:
			multiplier=8
		for i in df_map_tmp.itertuples():
			tmp=df1[(df1['destination_data']==i[2]) & (df1['origin_data']==i[1])]
			df_tmp=tmp.groupby(['origin_data',
								'destination_data',
								'equipment_type']).agg({"id":"count"}).reset_index()
			popup={'origin_data':i[1],
				'destination_data':i[2],
				"Standard Van 53":0,
				"Standard Reefer 53":0,
				"Standard Van 48":0,
				"Standard Reefer 48":0}
			for j in df_tmp.itertuples():
				popup[j[3]]=j[4]
			x=locs[i[1]]
			y=locs[i[2]]
			width=(int(i[4])/max_counts)*multiplier
			if width<1:
				width=0.9
			data.append([x,
						y,
						width,
						colors[i[5]],
						[popup],
						i[1],
						i[2]])
		all_data[week]=data

	weekz={}
	for i in df_map['year_week'].unique():
		tmp_=df_map[df_map['year_week']==i].reset_index()
		weekz[i]=str(tmp_['created_month'][0])+" Week "+str(tmp_['created_week'][0])
	weeks=[weekz[x] for x in df_map['year_week'].unique().tolist()]

	return JsonResponse({"error":[False],"all_data":[all_data],
		"shippers":sorted(df1['shipper'].unique().tolist()),
		"receivers":sorted(df1['receiver'].unique().tolist()),
		"weeks":weeks})

@xframe_options_exempt
def just_map_v11(response):
	deetz={
	    "type": "FeatureCollection",
	    "features": features
	}
	df=df_gd.copy()
	

	return render(response ,'blogs/just_map_v11.html',{"feats":deetz,
		"customers":sorted(df['customer'].unique().tolist()),
		"origin_st":[us_state_abbrev_codes[x]+f" ({x})" for x in sorted(df['origin_state_province'].unique().tolist())],
		"destination_st":[us_state_abbrev_codes[x]+f" ({x})" for x in sorted(df['destination_state_province'].unique().tolist())],
		"origin_ct":sorted(df['origin_city'].unique().tolist()),
		"destination_ct":sorted(df['destination_city'].unique().tolist())})

@xframe_options_exempt
def just_map_v12(response):
	deetz={
	    "type": "FeatureCollection",
	    "features": features
	}
	df=df_gd.copy()
	

	return render(response ,'blogs/just_map_v12.html',{"feats":deetz,
		"customers":sorted(df['customer'].unique().tolist()),
		"origin_st":[us_state_abbrev_codes[x]+f" ({x})" for x in sorted(df['origin_state_province'].unique().tolist())],
		"destination_st":[us_state_abbrev_codes[x]+f" ({x})" for x in sorted(df['destination_state_province'].unique().tolist())],
		"origin_ct":sorted(df['origin_city'].unique().tolist()),
		"destination_ct":sorted(df['destination_city'].unique().tolist())})

@xframe_options_exempt
def just_heat_chart_v2(response):
	df=df_gd.copy()
	

	return render(response ,'blogs/just_heat_chart_v2.html',{
		"customers":sorted(df['customer'].unique().tolist()),
		"origin_st":sorted(df['origin_state_province'].unique().tolist()),
		"destination_st":sorted(df['destination_state_province'].unique().tolist()),
		"origin_ct":sorted(df['origin_city'].unique().tolist()),
		"destination_ct":sorted(df['destination_city'].unique().tolist())})

@xframe_options_exempt
def just_map_v13(response):
	deetz={
	    "type": "FeatureCollection",
	    "features": features
	}
	df=df_gd.copy()

	return render(response ,'blogs/just_map_v14.html',{"feats":deetz,
		"customers":sorted(df['customer'].unique().tolist()),
		"origin_st":[us_state_abbrev_codes[x]+f" ({x})" for x in sorted(df['origin_state_province'].unique().tolist())],
		"destination_st":[us_state_abbrev_codes[x]+f" ({x})" for x in sorted(df['destination_state_province'].unique().tolist())],
		"origin_ct":sorted(df['origin_city'].unique().tolist()),
		"destination_ct":sorted(df['destination_city'].unique().tolist())})

@xframe_options_exempt
def just_map_v15(response):
	deetz={
	    "type": "FeatureCollection",
	    "features": features
	}
	df=df_gd.copy()

	return render(response ,'blogs/just_map_v19.html',{"feats":deetz,
		"customers":sorted(df['customer'].unique().tolist()),
		"origin_st":[us_state_abbrev_codes[x]+f" ({x})" for x in sorted(df['origin_state_province'].unique().tolist())],
		"destination_st":[us_state_abbrev_codes[x]+f" ({x})" for x in sorted(df['destination_state_province'].unique().tolist())],
		"origin_ct":sorted(df['origin_city'].unique().tolist()),
		"destination_ct":sorted(df['destination_city'].unique().tolist())})

@xframe_options_exempt
def just_map_v14(response):
	deetz={
	    "type": "FeatureCollection",
	    "features": features
	}
	df=df_gd.copy()

	return render(response ,'blogs/just_map_v17.html',{"feats":deetz,
		"customers":sorted(df['customer'].unique().tolist()),
		"origin_st":[us_state_abbrev_codes[x]+f" ({x})" for x in sorted(df['origin_state_province'].unique().tolist())],
		"destination_st":[us_state_abbrev_codes[x]+f" ({x})" for x in sorted(df['destination_state_province'].unique().tolist())],
		"origin_ct":sorted(df['origin_city'].unique().tolist()),
		"destination_ct":sorted(df['destination_city'].unique().tolist())})

@xframe_options_exempt
def just_map_hex(response):	
	# df=df_otr.copy()
	times=response.GET.get('times',None)
	if times:
		date=times
		date1=date.split(" ")[0]
		date2=date.split(" ")[2]
		datesss='05/31/2020 xxxxx 05/31/2021'
		date1=datetime.strptime(date1, '%m/%d/%Y')
		date2=datetime.strptime(date2, '%m/%d/%Y')
		df=pd.read_sql(f"SELECT odl.*,hexes.geom,hexes.tile_id, \
				ST_AsText(odl.lane_line_str) as lane_geom \
	FROM \
	usa_hex_2 AS hexes \
	INNER JOIN \
	otr_data_loads AS odl \
	ON ST_Intersects(odl.destination_geography::geometry, hexes.geom::geometry) where odl.status='RELEASED' AND odl.delivery_date \
			BETWEEN '{date1.year}-{date1.month}-{date1.day}' AND '{date2.year}-{date2.month}-{date2.day}';",conn)
		if len(df)<10:
			date_now=datetime.now()
			date_ago = datetime.today() - timedelta(days=45)
			df=pd.read_sql(f"SELECT odl.*,hexes.geom,hexes.tile_id, \
					ST_AsText(odl.lane_line_str) as lane_geom \
	FROM \
		usa_hex_2 AS hexes \
		INNER JOIN \
		otr_data_loads AS odl \
		ON ST_Intersects(odl.destination_geography::geometry, hexes.geom::geometry) where odl.status='RELEASED' AND  odl.delivery_date \
				BETWEEN '{date_ago.year}-{date_ago.month}-{date_ago.day}' AND '{date_now.year}-{date_now.month}-{date_now.day}';",conn)

	else:
		date_now=datetime.now()
		date_ago = datetime.today() - timedelta(days=45)
		df=pd.read_sql(f"SELECT odl.*,hexes.geom,hexes.tile_id, \
				ST_AsText(odl.lane_line_str) as lane_geom \
	FROM \
	usa_hex_2 AS hexes \
	INNER JOIN \
	otr_data_loads AS odl \
	ON ST_Intersects(odl.destination_geography::geometry, hexes.geom::geometry) where odl.status='RELEASED' AND  odl.delivery_date \
			BETWEEN '{date_ago.year}-{date_ago.month}-{date_ago.day}' AND '{date_now.year}-{date_now.month}-{date_now.day}';",conn)

	df_map=df.groupby(['origin_lat','origin_lng',
						'destination_lat','destination_lng']).agg({"id":"count",
                                                "equipment_type_id":"max",
												"miles":"mean",
												"lane_line_str":"first"}).reset_index()
	coords=[]
	eq_types=df_map['equipment_type_id'].unique().tolist()
	max_counts=df_map['id'].max()
	lst = range(1,60)
	ranges=np.array_split(lst, 6)
	colorheat=['#00A100','#128FD9','#FFB200','#FF0000','#008FFF','FF8B00']
	for i in df_map.itertuples():
		# color= '#FF00F3'
		clr_ind=eq_types.index(i[6])
		color=COLOURS[clr_ind]
		# for k in enumerate(ranges):
		# 	if i[5] in k[1]:
		# 		color=colorheat[k[0]]
		width=(int(i[5])/max_counts)*10
		if width<1:
			width=0.9
		sss=[[i[1],i[2]],
		[i[3],i[4]],
		width,
		color]
		coords.append(sss)
	
	# coords=[x.__geo_interface__ for x in all_polys]
	# deetz={
	#     "type": "FeatureCollection",
	#     "features": coords
	# }

	return JsonResponse({"error":[False],"data":coords})

@xframe_options_exempt
def just_map_line_graph(response):
	origin=response.GET.get('origin',None)
	destination=response.GET.get('destination',None)
	print(origin,destination)
	if not origin and not destination:
		return JsonResponse({"error":[True]})
	# df = df_gd.copy()
	date_now=datetime.now()
	date_ago = datetime.today() - timedelta(days=190)
	df=pd.read_sql(f"SELECT * \
		FROM \
			gold_oldnew \
		where ((origin_data='{origin}' AND destination_data='{destination}') \
		OR (origin_data='{destination}' AND destination_data='{origin}')) AND (booked_on \
					BETWEEN '{date_ago.year}-{date_ago.month}-{date_ago.day}' AND '{date_now.year}-{date_now.month}-{date_now.day}')\
						 ORDER BY booked_on DESC LIMIT 1000;",conn,
					parse_dates=['booked_on'])
	if len(df)<2:
		date_ago = datetime.today() - timedelta(days=365)
		df=pd.read_sql(f"SELECT * \
			FROM \
				gold_oldnew \
			where ((origin_data='{origin}' AND destination_data='{destination}') \
			OR (origin_data='{destination}' AND destination_data='{origin}')) AND (booked_on \
						BETWEEN '{date_ago.year}-{date_ago.month}-{date_ago.day}' AND '{date_now.year}-{date_now.month}-{date_now.day}') \
							 ORDER BY booked_on DESC LIMIT 1000;",conn,
						parse_dates=['booked_on'])
	df_=df.copy()

	# df=df[((df['origin_data']==origin) & (df['destination_data']==destination)) |\
	# 	((df['origin_data']==destination) & (df['destination_data']==origin))]
	# date_ago = datetime.today() - timedelta(days=150)
	# mask = (df['booked_on'] > date_ago) & (df['booked_on'] <= date_now)
	# df=df.loc[mask]
	if len(df)<1:
		return JsonResponse({"error":[True]})
	df=df[~df['booked_on'].astype(str).str.startswith('N')]
	# df['created_at'] = df['booked_on'].map(lambda x: x.strftime('%Y-%m-%d'))
	df['created_week']=df['booked_on'].apply(lambda x : x.strftime("%U"))#%U#%W
	df['created_week']=df['created_week'].astype(int)
	df['created_year']=df['booked_on'].apply(lambda x : x.strftime("%Y"))
	df['created_year']=df['created_year'].astype(int)
	df['created_month']=df['booked_on'].apply(lambda x : x.strftime("%B"))
	df['created_month_num']=df['booked_on'].apply(lambda x : x.strftime("%m"))
	df['created_month_num']=df['created_month_num'].astype(int)
	df['created_year']=df['created_year'].astype(str)
	df['created_week']=df['created_week'].astype(str)
	df['year_week_str']=df[['created_year', 'created_week']].agg(' Week '.join, axis=1)
	df['created_year']=df['created_year'].astype(int)
	df['created_week']=df['created_week'].astype(int)

	df_map3=df_.groupby(['booked_on']).agg({"id": "count"}).reset_index()
	df_map3=df_map3.sort_values(by=['booked_on'],ascending=False)
	df_select2=df_.groupby(['booked_on','customer']).agg({"id": "count"}).reset_index()
	df_select2=df_select2.sort_values(by=['id'],ascending=False)
	df_map=df.groupby(['customer','year_week_str']).agg({"id": "count",
														"created_year":"first",
														"created_month_num":"first",
														"created_week":"first"}).reset_index()
	df_map=df_map.sort_values(by=['created_year','created_month_num','created_week'])
	labels=df_map['year_week_str'].unique().tolist()[0:7]
	all_data=[]
	chart_colors=['#E74C3C','#884EA0','#3498DB','#1ABC9C','#1E8449','#F1C40F','#F39C12','#E67E22','#BA4A00','#2E4053','#82E0AA','#17202A']
	for i in enumerate(df_map['customer'].unique().tolist()):
		df_tmp=df_map[df_map['customer']==i[1]]
		deet=[]
		for l in labels:
			p=df_tmp[df_tmp['year_week_str']==l]['id'].values
			if len(p)>0:
				deet.append(int(p[0]))
			else:
				deet.append(0)
		if i[0]>10:
			ind=11
		else:
			ind=i[0]
		dct={
		'label': i[1],
		'data': deet,
		'borderColor': chart_colors[ind],
		'backgroundColor': chart_colors[ind],
		'tension':0.5
		}
		all_data.append(dct)
	final_data={
	  "labels": labels,
	  "datasets": all_data
	}
	df=df_.copy()
	df_map2=df.groupby(['customer']).agg({"id": "count"}).reset_index()
	# if len(df_map2['customer'].unique())>12:
	# 	labels_colors=chart_colors+['#FFCE56']*(len(df_map2['customer'].unique())-12)
	# else:
	# 	labels_colors=chart_colors[0:len(df_map2['customer'].unique())]
	# labels=df_map2['customer'].values.tolist()
	# data=df_map2['id'].values.tolist()
	# polar_data={
	# 	'datasets':[{'data': data,
	# 				'backgroundColor': labels_colors,
	# 				'label': 'Loads per cusotmer'}],
	# 	'labels':labels
	# 	}
		
	donut_data=[]
	for i in df_map2.itertuples():
		donut_data.append({"carrier":i[1],"value":i[2]})
	# line_data=[]
	# for i in enumerate(df_select2['customer'].unique().tolist()):
	# 	df_tmp=df_select2[df_select2['customer']==i[1]]
	# 	loads=df_tmp['id'].values.tolist()
	# 	df_tmp['dd_year']=df_tmp['booked_on'].apply(lambda x: x.strftime('%Y'))
	# 	df_tmp['dd_month']=df_tmp['booked_on'].apply(lambda x: x.strftime('%m'))
	# 	df_tmp['dd_day']=df_tmp['booked_on'].apply(lambda x: x.strftime('%d'))
	# 	years=df_tmp['dd_year'].values.tolist()
	# 	months=df_tmp['dd_month'].values.tolist()
	# 	days=df_tmp['dd_day'].values.tolist()
	# 	dct=[{"year":x[1],"month":x[2],"day":x[3],"value":x[0]} for x in zip(loads,years,months,days)]
	# 	line_data.append([i[0],i[1],dct])
	amt_chart1=[]
	for i in df_map3.itertuples():
		amt_chart1.append({"country":str(i[1])[:10],"visits":i[2]})
	return JsonResponse({"error":[False],
		"myChart1":final_data,
		# "myChart2":polar_data,
		"donut_data":donut_data,
		# "line_data":line_data,
		"amt_chart1":amt_chart1})

@xframe_options_exempt
def just_map_hexagons(response):
	times=response.GET.get('times',None)
	if times:
		date=times
		date1=date.split(" ")[0]
		date2=date.split(" ")[2]
		if date1==date2:
			date2=datetime.now()
			date1 = datetime.today() - timedelta(days=90)
		else:
			date1=datetime.strptime(date1, '%m/%d/%Y')
			date2=datetime.strptime(date2, '%m/%d/%Y')
	else:
		date2=datetime.now()
		date1 = datetime.today() - timedelta(days=90)
	origin_st=response.GET.getlist('origin_st[]',None)
	if origin_st:
		origin_st=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in origin_st]
	if not origin_st:
		origin_st=states_list
	origin_ct=response.GET.getlist('origin_ct[]',None)
	if origin_ct:
		origin_ct=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in origin_ct]
	if not origin_ct:
		origin_ct=cities_list
		
	# destination_st=response.GET.getlist('destination_st[]',None)
	# if destination_st:
	# 	destination_st=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in destination_st]
	# if not destination_st:
	# 	destination_st=states_list
	# destination_ct=response.GET.getlist('destination_ct[]',None)
	# if destination_ct:
	# 	destination_ct=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in destination_ct]
	# if not destination_ct:
	# 	destination_ct=cities_list
	origin_ct=[x.replace("'","").replace('"',"") for x in origin_ct]
	# destination_ct=[x.replace("'","").replace('"',"") for x in destination_ct]
	origin_st=str(origin_st)[1:-1]
	origin_ct=str(origin_ct)[1:-1]
	# destination_st=str(destination_st)[1:-1]
	# destination_ct=str(destination_ct)[1:-1]
	going=response.GET.get('going',None)
	if going:
		if going=='both':
			intersect="(ST_Intersects(odl.origin_geography::geometry, hexes.geom::geometry) or\
					ST_Intersects(odl.destination_geography::geometry, hexes.geom::geometry))"
			dates_sql=f" (odl.delivery_date \
				BETWEEN '{date1.year}-{date1.month}-{date1.day}' AND '{date2.year}-{date2.month}-{date2.day}' OR \
					odl.delivery_date \
				BETWEEN '{date1.year}-{date1.month}-{date1.day}' AND '{date2.year}-{date2.month}-{date2.day}' ) "
			st_ct_sql=f"odl.origin_state IN ({origin_st}) AND \
							odl.origin_city IN ({origin_ct}) "
		elif going=='in':
			intersect=" ST_Intersects(odl.destination_geography::geometry, hexes.geom::geometry) "
			dates_sql=f" odl.delivery_date \
			BETWEEN '{date1.year}-{date1.month}-{date1.day}' AND '{date2.year}-{date2.month}-{date2.day}' "
			st_ct_sql=f"odl.destination_state IN ({origin_st}) AND \
							odl.destination_city IN ({origin_ct}) "
		elif going=='out':
			intersect=" ST_Intersects(odl.origin_geography::geometry, hexes.geom::geometry) "
			dates_sql=f" odl.pickup_date \
			BETWEEN '{date1.year}-{date1.month}-{date1.day}' AND '{date2.year}-{date2.month}-{date2.day}' "
			st_ct_sql=f"odl.origin_state IN ({origin_st}) AND \
							odl.origin_city IN ({origin_ct}) "
		else:
			intersect="(ST_Intersects(odl.origin_geography::geometry, hexes.geom::geometry) or \
				ST_Intersects(odl.destination_geography::geometry, hexes.geom::geometry))"
			dates_sql=f" (odl.delivery_date \
				BETWEEN '{date1.year}-{date1.month}-{date1.day}' AND '{date2.year}-{date2.month}-{date2.day}' OR \
					odl.delivery_date \
			BETWEEN '{date1.year}-{date1.month}-{date1.day}' AND '{date2.year}-{date2.month}-{date2.day}' ) "
	else:
		intersect="(ST_Intersects(odl.origin_geography::geometry, hexes.geom::geometry) or\
				ST_Intersects(odl.destination_geography::geometry, hexes.geom::geometry))"
		dates_sql=f" (odl.delivery_date \
			BETWEEN '{date1.year}-{date1.month}-{date1.day}' AND '{date2.year}-{date2.month}-{date2.day}' OR \
				odl.delivery_date \
			BETWEEN '{date1.year}-{date1.month}-{date1.day}' AND '{date2.year}-{date2.month}-{date2.day}' ) "

	df=pd.read_sql(f"SELECT odl.*,hexes.tile_id,ST_AsText(hexes.geom) as geom, \
		ST_AsText(odl.lane_line_str) as lane_geom, \
			carr.legal_name, carr.c411_trucks \
		FROM \
		usa_hex_3 AS hexes \
		LEFT JOIN \
		otr_data_loads AS odl \
		ON {intersect} \
		LEFT JOIN carrier_otr AS carr ON  odl.carrier_id=carr.id   \
			where  odl.status='RELEASED' AND {dates_sql} \
			AND ( {st_ct_sql} \
			);",conn)


	# times=response.GET.get('times',None)
	# if times:
	# 	date=times
	# 	date1=date.split(" ")[0]
	# 	date2=date.split(" ")[2]
	# 	datesss='05/31/2020 xxxxx 05/31/2021'
	# 	date1=datetime.strptime(date1, '%m/%d/%Y')
	# 	date2=datetime.strptime(date2, '%m/%d/%Y')
	# 	df=pd.read_sql(f"SELECT odl.*,hexes.tile_id,ST_AsText(hexes.geom) as geom, \
	# 		ST_AsText(odl.lane_line_str) as lane_geom, \
	# 			carr.legal_name, carr.c411_trucks \
	# 		FROM \
	# 		usa_hex_3 AS hexes \
	# 		LEFT JOIN \
	# 		otr_data_loads AS odl \
	# 		ON {intersect} \
	# 		LEFT JOIN carrier_otr AS carr ON  odl.carrier_id=carr.id   \
	# 			where odl.delivery_date \
	# 		BETWEEN '{date1.year}-{date1.month}-{date1.day}' AND '{date2.year}-{date2.month}-{date2.day}' \
	# 			AND ( \
	# 				odl.origin_state IN ({origin_st}) AND \
	# 				odl.origin_city IN ({origin_ct}) \
	# 			);",conn)
	# 	if len(df)<10:
	# 		date_now=datetime.now()
	# 		date_ago = datetime.today() - timedelta(days=45)
	# 		df=pd.read_sql(f"SELECT odl.*,hexes.tile_id,ST_AsText(hexes.geom) as geom, \
	# 		ST_AsText(odl.lane_line_str) as lane_geom, \
	# 			carr.legal_name, carr.c411_trucks \
	# 		FROM \
	# 		usa_hex_3 AS hexes \
	# 		LEFT JOIN \
	# 		otr_data_loads AS odl \
	# 		ON {intersect} \
	# 		LEFT JOIN carrier_otr AS carr ON  odl.carrier_id=carr.id   \
	# 			where odl.delivery_date \
	# 			BETWEEN '{date_ago.year}-{date_ago.month}-{date_ago.day}' AND '{date_now.year}-{date_now.month}-{date_now.day}' AND ( \
	# 				odl.origin_state IN ({origin_st}) AND \
	# 				odl.origin_city IN ({origin_ct}) \
	# 			);",conn)
	# else:
	# 	date_now=datetime.now()
	# 	date_ago = datetime.today() - timedelta(days=45)
	# 	df=pd.read_sql(f"SELECT odl.*,hexes.tile_id,ST_AsText(hexes.geom) as geom, \
	# 				ST_AsText(odl.lane_line_str) as lane_geom, \
	# 					carr.legal_name, carr.c411_trucks \
	# 	FROM \
	# 	usa_hex_3 AS hexes \
	# 	LEFT JOIN \
	# 	otr_data_loads AS odl \
	# 	ON {intersect} \
	# 	LEFT JOIN carrier_otr AS carr ON  odl.carrier_id=carr.id   \
	# 		where odl.delivery_date \
	# 			BETWEEN '{date_ago.year}-{date_ago.month}-{date_ago.day}' AND '{date_now.year}-{date_now.month}-{date_now.day}' AND ( \
	# 				odl.origin_state IN ({origin_st}) AND \
	# 				odl.origin_city IN ({origin_ct}) \
	# 			);",conn)
	# if times:
	# 	date=times
	# 	date1=date.split(" ")[0]
	# 	date2=date.split(" ")[2]
	# 	datesss='05/31/2020 xxxxx 05/31/2021'
	# 	date1=datetime.strptime(date1, '%m/%d/%Y')
	# 	date2=datetime.strptime(date2, '%m/%d/%Y')
	# 	df1=pd.read_sql(f"SELECT odl.*,hexes.tile_id,ST_AsText(hexes.geom) as geom, \
	# 		ST_AsText(odl.lane_line_str) as lane_geom, \
	# 			carr.legal_name, carr.c411_trucks \
	# 		FROM \
	# 		usa_hex_3 AS hexes \
	# 		LEFT JOIN \
	# 		otr_data_loads AS odl \
	# 		ON {intersect} \
	# 		LEFT JOIN carrier_otr AS carr ON  odl.carrier_id=carr.id   \
	# 			where odl.delivery_date \
	# 		BETWEEN '{date1.year}-{date1.month}-{date1.day}' AND '{date2.year}-{date2.month}-{date2.day}' \
	# 			 AND \
    #                  odl.pickup_date \
    #     		NOT BETWEEN '{date1.year}-{date1.month}-{date1.day}' AND '{date2.year}-{date2.month}-{date2.day}' AND ( \
	# 				odl.origin_state IN ({origin_st}) AND \
	# 				odl.origin_city IN ({origin_ct}) \
	# 			);",conn)
	# 	if len(df)<10:
	# 		date_now=datetime.now()
	# 		date_ago = datetime.today() - timedelta(days=45)
	# 		df1=pd.read_sql(f"SELECT odl.*,hexes.tile_id,ST_AsText(hexes.geom) as geom, \
	# 		ST_AsText(odl.lane_line_str) as lane_geom, \
	# 			carr.legal_name, carr.c411_trucks \
	# 		FROM \
	# 		usa_hex_3 AS hexes \
	# 		LEFT JOIN \
	# 		otr_data_loads AS odl \
	# 		ON {intersect} \
	# 		LEFT JOIN carrier_otr AS carr ON  odl.carrier_id=carr.id   \
	# 			where odl.delivery_date \
	# 			BETWEEN '{date_ago.year}-{date_ago.month}-{date_ago.day}' AND '{date_now.year}-{date_now.month}-{date_now.day}' \
	# 			 AND \
    #                  odl.pickup_date \
    #     		NOT BETWEEN '{date_ago.year}-{date_ago.month}-{date_ago.day}' AND '{date_now.year}-{date_now.month}-{date_now.day}' AND ( \
	# 				odl.origin_state IN ({origin_st}) AND \
	# 				odl.origin_city IN ({origin_ct}) \
	# 			);",conn)
	# else:
	# 	date_now=datetime.now()
	# 	date_ago = datetime.today() - timedelta(days=45)
	# 	df1=pd.read_sql(f"SELECT odl.*,hexes.tile_id,ST_AsText(hexes.geom) as geom, \
	# 				ST_AsText(odl.lane_line_str) as lane_geom, \
	# 					carr.legal_name, carr.c411_trucks \
	# 	FROM \
	# 	usa_hex_3 AS hexes \
	# 	LEFT JOIN \
	# 	otr_data_loads AS odl \
	# 	ON {intersect} \
	# 	LEFT JOIN carrier_otr AS carr ON  odl.carrier_id=carr.id   \
	# 		where odl.delivery_date \
	# 			BETWEEN '{date_ago.year}-{date_ago.month}-{date_ago.day}' AND '{date_now.year}-{date_now.month}-{date_now.day}' \
	# 								 AND \
    #                  odl.pickup_date \
    #     		NOT BETWEEN '{date_ago.year}-{date_ago.month}-{date_ago.day}' AND '{date_now.year}-{date_now.month}-{date_now.day}' AND ( \
	# 				odl.origin_state IN ({origin_st}) AND \
	# 				odl.origin_city IN ({origin_ct}) \
	# 			);",conn)

	df['legal_name'] = df['legal_name'].fillna('INDEPENDENT')
	df['c411_trucks'] = df['c411_trucks'].fillna(0)
	df['geom'] = gp.GeoSeries.from_wkt(df['geom'])
	gdf = gp.GeoDataFrame(df, geometry='geom')
	df_map=df.groupby(['tile_id']).agg({"id": "count","geom":"first","destination_city":"first"}).reset_index()
	# df1['legal_name'] = df1['legal_name'].fillna('INDEPENDENT')
	# df1['c411_trucks'] = df1['c411_trucks'].fillna(0)
	# df_map1=df1.groupby(['tile_id']).agg({"id": "count","geom":"first","destination_city":"first"}).reset_index()

	lst = range(1,80+1)
	ranges=np.array_split(lst, 10)
	chart_colors=['#f21111','#884EA0','#3498DB','#1ABC9C','#1E8449','#F1C40F','#F39C12','#E67E22','#BA4A00','#00b300','#82E0AA','#f02ef0']
	chart_colors=["#1F78B4",
			"#00278C",
			"#B2DF8A",
			"#33A02C",
			"#FB9A99",
			"#E31A1C",
			"#FDBF6F",
			"#FF7F00",
			"#CAB2D6",
			"#6A3D9A",
			"#949D00",
			"#666666"]
	chart_colors=["#491D8B",
				"#7B49BC",
				"#8A3FFC",
				"#BE95FF",
				"#E8DAFF",
				"#F6F2FF",
				"#D9FBFB",
				"#9EF0F0",
				"#3DDBD9",
				"#009D9A",
				"#005D5D",
				"#00464E"]
	hexagons=[]
	for i in df_map.itertuples():
		tl=i[2]
		# tmp=df_map1[df_map1['tile_id']==i[1]]
		# if len(tmp)>0:
		# 	tmp_c=tmp['id'].values[0]
		# else:
		# 	tmp_c=None
		# if tmp_c:
		# 	ddl=tl-tmp_c
		# 	pdl=tmp_c
		# else:
		# 	ddl=0
		# 	pdl=i[2]
		clr_ind=None
		for k in enumerate(ranges):
			if i[2] in k[1]:
				clr_ind=k[0]
				break
		if clr_ind!=0 and not clr_ind:
			clr_ind=11
		hexagons.append({
			"type": "Feature",
			"properties": {"id":i[1],"pop":i[2],"color":chart_colors[clr_ind],
						"delivery":0,"pickup":0},
			"geometry": i[3].__geo_interface__
		})
		
	hexes_not_in_map=[x for x in zip(hexes['tile_id'],hexes['geom']) if x[0] not in df_map['tile_id'].values.tolist()]

	for i in hexes_not_in_map:
		hexagons.append({
			"type": "Feature",
			"properties": {"id":i[0],"pop":0,"color":"#696969"},
			"geometry": i[1].__geo_interface__
		})
	deetz={
	    "type": "FeatureCollection",
	    "features": hexagons
	}
	return JsonResponse({"feats":deetz})

@xframe_options_exempt
def just_map_carrier_api(response):
	origin_st=response.GET.getlist('origin_st[]',None)
	if origin_st:
		origin_st=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in origin_st]
	if not origin_st:
		origin_st=states_list
	origin_ct=response.GET.getlist('origin_ct[]',None)
	if origin_ct:
		origin_ct=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in origin_ct]
	if not origin_ct:
		origin_ct=cities_list
		
	destination_st=response.GET.getlist('destination_st[]',None)
	if destination_st:
		destination_st=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in destination_st]
	if not destination_st:
		destination_st=states_list
	destination_ct=response.GET.getlist('destination_ct[]',None)
	if destination_ct:
		destination_ct=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in destination_ct]
	if not destination_ct:
		destination_ct=cities_list

	# dfx=pd.read_sql(f"select carr.legal_name from otr_data_loads AS odl \
	# LEFT JOIN carrier_otr AS carr ON  odl.carrier_id=carr.id\
	# where  \
	# 			odl.origin_state IN ({str(origin_st)[1:-1]}) AND \
	# 				odl.origin_city IN ({str(origin_ct)[1:-1]}) AND\
	# 					odl.destination_state IN ({str(destination_st)[1:-1]}) AND\
	# 						odl.destination_city IN ({str(destination_ct)[1:-1]}) LIMIT 100;",conn)

	# origin_ct=[x.replace("'","").replace('"',"") for x in origin_ct]
	# destination_ct=[x.replace("'","").replace('"',"") for x in destination_ct]
	# origin_st=str(origin_st)[1:-1]
	# origin_ct=str(origin_ct)[1:-1]
	# destination_st=str(destination_st)[1:-1]
	# destination_ct=str(destination_ct)[1:-1]
	df=df_gd.copy()
	dfx=df[(df['origin_state_province'].isin(origin_st)) & \
		(df['origin_city'].isin(origin_ct)) & \
		(df['destination_state_province'].isin(destination_st)) & \
		(df['destination_city'].isin(destination_ct))]
	# dfx=pd.read_sql(f'select customer,shipper,receiver from gold_oldnew \
	# where  \
	# 			origin_state_province IN ({origin_st}) AND \
	# 				origin_city IN ({origin_ct}) AND \
	# 					destination_state_province IN ({destination_st}) AND \
	# 						destination_city IN ({destination_ct}) LIMIT 100;',conn)
	return JsonResponse({"customer":sorted(list(set(dfx['customer'].values.tolist()))),
	"shipper":sorted(list(set(dfx['shipper'].values.tolist()))),
	"receivers":sorted(list(set(dfx['receiver'].values.tolist())))})

@xframe_options_exempt
def just_map_v16(response):
	deetz={
	    "type": "FeatureCollection",
	    "features": features
	} 
	df=df_gd.copy()

	return render(response ,'blogs/just_map_v21.html',{"feats":deetz,
		"origin_st":[us_state_abbrev_codes[x]+f" ({x})" for x in sorted(df['origin_state_province'].unique().tolist())],
		"destination_st":[us_state_abbrev_codes[x]+f" ({x})" for x in sorted(df['destination_state_province'].unique().tolist())],
		"origin_ct":sorted(df['origin_city'].unique().tolist()),
		"destination_ct":sorted(df['destination_city'].unique().tolist())})

@xframe_options_exempt
def just_map_carrier_api2(response):
	origin_st=response.GET.getlist('origin_st[]',None)
	if origin_st:
		origin_st=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in origin_st]
	if not origin_st:
		origin_st=states_list
	origin_ct=response.GET.getlist('origin_ct[]',None)
	if origin_ct:
		origin_ct=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in origin_ct]
	if not origin_ct:
		origin_ct=cities_list
		
	destination_st=response.GET.getlist('destination_st[]',None)
	if destination_st:
		destination_st=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in destination_st]
	if not destination_st:
		destination_st=states_list
	destination_ct=response.GET.getlist('destination_ct[]',None)
	if destination_ct:
		destination_ct=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in destination_ct]
	if not destination_ct:
		destination_ct=cities_list

	origin_ct=[x.replace("'","").replace('"',"") for x in origin_ct]
	destination_ct=[x.replace("'","").replace('"',"") for x in destination_ct]
	origin_st=str(origin_st)[1:-1]
	origin_ct=str(origin_ct)[1:-1]
	destination_st=str(destination_st)[1:-1]
	destination_ct=str(destination_ct)[1:-1]
	dfx=pd.read_sql(f"select carr.legal_name  as legal_name from otr_data_loads AS odl \
	LEFT JOIN carrier_otr AS carr ON  odl.carrier_id=carr.id \
	where   odl.status='RELEASED' AND \
				odl.origin_state IN ({origin_st}) AND \
					odl.origin_city IN ({origin_ct}) AND\
						odl.destination_state IN ({destination_st}) AND\
							odl.destination_city IN ({destination_ct}) LIMIT 1000;",conn)

	return JsonResponse({"customer":list(set(dfx['legal_name'].values.tolist()))})

@xframe_options_exempt
def just_map_tile_id(response):
	# going=response.GET.get('going',None)
	# if going:
	# 	if going=='both':
	# 		intersect="(ST_Intersects(odl.origin_geography::geometry, hexes.geom::geometry) or\
	# 			ST_Intersects(odl.destination_geography::geometry, hexes.geom::geometry))"
	# 	elif going=='in':
	# 		intersect="ST_Intersects(odl.destination_geography::geometry, hexes.geom::geometry)"
	# 	elif going=='out':
	# 		intersect="ST_Intersects(odl.origin_geography::geometry, hexes.geom::geometry)"
	# 	else:
	# 		intersect="(ST_Intersects(odl.origin_geography::geometry, hexes.geom::geometry) or\
	# 			ST_Intersects(odl.destination_geography::geometry, hexes.geom::geometry))"
	# else:
	# 	intersect="(ST_Intersects(odl.origin_geography::geometry, hexes.geom::geometry) or\
	# 			ST_Intersects(odl.destination_geography::geometry, hexes.geom::geometry))"
	tile_id=response.GET.get('tile_id',None)
	date2=datetime.now()
	date1 = datetime.today() - timedelta(days=120)
	going=response.GET.get('going',None)
	if going:
		if going=='both':
			intersect="(ST_Intersects(odl.origin_geography::geometry, hexes.geom::geometry) or\
					ST_Intersects(odl.destination_geography::geometry, hexes.geom::geometry))"
			dates_sql=f" (odl.delivery_date \
				BETWEEN '{date1.year}-{date1.month}-{date1.day}' AND '{date2.year}-{date2.month}-{date2.day}' OR \
					odl.delivery_date \
				BETWEEN '{date1.year}-{date1.month}-{date1.day}' AND '{date2.year}-{date2.month}-{date2.day}' ) "
		elif going=='in':
			intersect=" ST_Intersects(odl.destination_geography::geometry, hexes.geom::geometry) "
			dates_sql=f" odl.delivery_date \
			BETWEEN '{date1.year}-{date1.month}-{date1.day}' AND '{date2.year}-{date2.month}-{date2.day}' "
			orderby_sql=" ORDER BY delivery_date desc LIMIT 4000 "
		elif going=='out':
			intersect=" ST_Intersects(odl.origin_geography::geometry, hexes.geom::geometry) "
			dates_sql=f" odl.pickup_date \
			BETWEEN '{date1.year}-{date1.month}-{date1.day}' AND '{date2.year}-{date2.month}-{date2.day}' "
			orderby_sql=" ORDER BY pickup_date desc LIMIT 4000 "
		else:
			intersect="(ST_Intersects(odl.origin_geography::geometry, hexes.geom::geometry) or \
				ST_Intersects(odl.destination_geography::geometry, hexes.geom::geometry))"
			dates_sql=f" (odl.delivery_date \
				BETWEEN '{date1.year}-{date1.month}-{date1.day}' AND '{date2.year}-{date2.month}-{date2.day}' OR \
					odl.delivery_date \
			BETWEEN '{date1.year}-{date1.month}-{date1.day}' AND '{date2.year}-{date2.month}-{date2.day}' ) "
	else:
		intersect="(ST_Intersects(odl.origin_geography::geometry, hexes.geom::geometry) or\
				ST_Intersects(odl.destination_geography::geometry, hexes.geom::geometry))"
		dates_sql=f" (odl.delivery_date \
			BETWEEN '{date1.year}-{date1.month}-{date1.day}' AND '{date2.year}-{date2.month}-{date2.day}' OR \
				odl.delivery_date \
			BETWEEN '{date1.year}-{date1.month}-{date1.day}' AND '{date2.year}-{date2.month}-{date2.day}' ) "
	# intersect="(ST_Intersects(odl.origin_geography::geometry, hexes.geom::geometry) or\
	# 			ST_Intersects(odl.destination_geography::geometry, hexes.geom::geometry))"
	# df=pd.read_sql(f"SELECT odl.id as id,odl.description as description,odl.equipment_type_id as equipment_type_id, \
	# 	hexes.tile_id,ST_AsText(hexes.geom) as geom, odl.origin_data, odl.destination_data,\
	# 		ST_AsText(odl.lane_line_str) as lane_geom, \
	# 			carr.legal_name, carr.c411_trucks, COALESCE(carr.dat_fleet_refreshed_at, odl.delivery_date) AS delivery_date \
	# 		FROM \
	# 		usa_hex_3 AS hexes \
	# 		LEFT JOIN \
	# 		otr_data_loads AS odl \
	# 		ON {intersect} \
	# 		FULL JOIN carrier_otr AS carr ON  odl.carrier_id=carr.id   \
	# 			where hexes.tile_id='{tile_id}' AND \
	# 				{dates_sql};",conn,
	# 			parse_dates={'booked_on': {'format': '%Y-%m-%d'},
	# 		'picked_up_by': {'format': '%Y-%m-%d'},
	# 		'delivery_date': {'format': '%Y-%m-%d'}})

	df=pd.read_sql(f"SELECT odl.id as id,odl.description as description,eg.name AS equipment_type_id, odl.equipment_type_id as equipment_type, \
		 odl.origin_data, odl.destination_data,\
			ST_AsText(odl.lane_line_str) as lane_geom, \
				carr.legal_name, carr.c411_trucks, COALESCE(carr.dat_fleet_refreshed_at, odl.delivery_date) AS delivery_date \
			FROM \
			usa_hex_3 AS hexes \
			LEFT JOIN \
			otr_data_loads AS odl \
			ON {intersect} \
               LEFT JOIN otr_loads_eq_type et ON odl.equipment_type_id = et.id \
                   LEFT JOIN otr_loads_eq_group eg ON et.equipment_group_id = eg.id \
			FULL JOIN carrier_otr AS carr ON  odl.carrier_id=carr.id   \
				where odl.status='RELEASED' AND hexes.tile_id='{tile_id}' AND \
					{dates_sql} {orderby_sql} ;",conn,
				parse_dates={'booked_on': {'format': '%Y-%m-%d'},
			'picked_up_by': {'format': '%Y-%m-%d'},
			'delivery_date': {'format': '%Y-%m-%d'}})
	desc=df['description'].values.tolist()
	desc=[x.replace(" ","-").upper() for x in desc if x]
	desc =sorted(list(desc))
	desc=str(desc)[1:-1].replace(","," ")
	
	df['equipment_type_id']=df['equipment_type_id'].fillna('UNKNOWN')
	df['legal_name']=df['legal_name'].fillna('INDEPENDENT')
	df=df[~df['delivery_date'].astype(str).str.startswith('N')]
	df['created_week']=df['delivery_date'].apply(lambda x : x.strftime("%U"))#%U#%W
	df['created_week']=df['created_week'].astype(int)
	df['created_year']=df['delivery_date'].apply(lambda x : x.strftime("%Y"))
	df['created_year']=df['created_year'].astype(int)
	df['created_month']=df['delivery_date'].apply(lambda x : x.strftime("%B"))
	df['created_month_num']=df['delivery_date'].apply(lambda x : x.strftime("%m"))
	df['created_month_num']=df['created_month_num'].astype(int)
	df['created_year']=df['created_year'].astype(str)
	df['created_week']=df['created_week'].astype(str)
	df['year_week_str']=df[['created_year', 'created_week']].agg(' Week '.join, axis=1)
	df['created_year']=df['created_year'].astype(int)
	df['created_week']=df['created_week'].astype(int)

	df_select2=df.groupby(['delivery_date','legal_name']).agg({"id": "count"}).reset_index()
	df_select2=df_select2.sort_values(by=['id'],ascending=False)
	df_select=df.groupby(['legal_name']).agg({"id": "count"}).reset_index()
	df_select=df_select.sort_values(by=['id'],ascending=False)
	df=df[df['legal_name'].isin(df_select['legal_name'][0:11])]
	df_map=df.groupby(['legal_name','year_week_str']).agg({"id": "count",
														"created_year":"first",
														"created_month_num":"first",
														"created_week":"first"}).reset_index()
	df_map=df_map.sort_values(by=['created_year','created_month_num','created_week'])
	labels=df_map['year_week_str'].unique().tolist()[0:5]
	# df_map=df_map[df_map['year_week_str'].isin(labels)]
	all_data=[]
	chart_colors=['#E74C3C','#884EA0','#3498DB','#1ABC9C','#1E8449','#F1C40F','#F39C12','#E67E22','#BA4A00','#2E4053','#82E0AA','#17202A']

	for i in enumerate(df_map['legal_name'].unique().tolist()):
		df_tmp=df_map[df_map['legal_name']==i[1]]
		deet=[]
		for l in labels:
			p=df_tmp[df_tmp['year_week_str']==l]['id'].values
			if len(p)>0:
				deet.append(int(p[0]))
			else:
				deet.append(0)
		if i[0]>10:
			ind=11
		else:
			ind=i[0]
		dct={
		'label': i[1],
		'data': deet,
		'borderColor': chart_colors[ind],
		'backgroundColor': chart_colors[ind],
		'tension':0.5
		}
		all_data.append(dct)
	final_data={
		"labels": labels,
		"datasets": all_data
	}
	am_cht1=[]
	lblamt1=df_map['legal_name'].unique().tolist()[0:5]
	for i in enumerate(labels):
		df_tmp=df_map[df_map['year_week_str']==i[1]]
		dct={}
		dct["year"]=i[1]
		for j in enumerate(lblamt1):
			p=df_tmp[df_tmp['legal_name']==j[1]]['id'].values
			if len(p)>0:
				dct[j[1]]=int(p[0])
			else:
				dct[j[1]]=0
		am_cht1.append(dct)
	# desc=df['description'].values.tolist()
	
	df_map1=df.groupby(['equipment_type_id']).agg({"id": "count"}).reset_index()
	amt_chart2=[]
	for i in df_map1.itertuples():
		amt_chart2.append({"equipment_type_id":i[1],
		"value":i[2]})

	line_data=[]
	for i in enumerate(df_select2['legal_name'].unique().tolist()):
		df_tmp=df_select2[df_select2['legal_name']==i[1]]
		df_tmp=df_tmp.sort_values(by=['delivery_date'],ascending=False)
		loads=df_tmp['id'].values.tolist()
		df_tmp['dd_year']=df_tmp['delivery_date'].apply(lambda x: x.strftime('%Y'))
		df_tmp['dd_month']=df_tmp['delivery_date'].apply(lambda x: x.strftime('%m'))
		df_tmp['dd_day']=df_tmp['delivery_date'].apply(lambda x: x.strftime('%d'))
		years=df_tmp['dd_year'].values.tolist()
		months=df_tmp['dd_month'].values.tolist()
		days=df_tmp['dd_day'].values.tolist()
		dct=[{"year":x[1],"month":x[2],"day":x[3],"value":x[0]} for x in zip(loads,years,months,days)]
		line_data.append([i[0],i[1],dct])
	
	df=df[df['origin_data'].notnull()]
	df=df[df['destination_data'].notnull()]
	df_map=df.groupby(['origin_data','destination_data']).agg({"id": "count"}).reset_index()
	df_map=df_map.sort_values(by=['id'],ascending=False)
	df_map=df_map[0:12]
	chord_data=[]
	for i in df_map.itertuples():
		chord_data.append({"from":i[1],
							"to":i[2],
							"value":i[3]})
	tile_df=pd.read_sql(f"select ST_AsText(geom) as geom from usa_hex_3 where tile_id='{tile_id}'",conn)
	tile_df['geom'] = gp.GeoSeries.from_wkt(tile_df['geom'])
	if len(tile_df)>0:
		highlight_poly = [{
		"type": "Feature",
		"geometry": tile_df['geom'].values[0].__geo_interface__
		}]
	else:
		highlight_poly=[{
		"type": "Feature",
		"geometry": {"d":"d"}
		}]
	return JsonResponse({"error":[False],
		"myChart1":final_data,
		"words":desc,
		"amt_chart1":am_cht1,
		"amt_chart1_labels":lblamt1,
		"amt_chart2":amt_chart2,
		"line_data":line_data,
		"chord_data":chord_data,
		"highlight_poly":highlight_poly})

@xframe_options_exempt
def just_map_deadhead(response):
	lon=response.GET.get('lon',None)
	lat=response.GET.get('lat',None)
	dist=response.GET.get('dist',None)
	dist=int(dist)
	dist=804.5 * dist#80450
	date_now=datetime.now()
	date_ago = datetime.today() - timedelta(days=60)
	"""
	df=pd.read_sql("SELECT asset_assetId,\
		asset_equipment_destination_place_namedcoordinates_latitude,\
		asset_equipment_destination_place_namedcoordinates_longitude,\
		asset_equipment_origin_namedcoordinates_latitude,\
		asset_equipment_origin_namedcoordinates_longitude\
	 FROM import.trucks_raw where cast(created_week as int)>12 and \
		cast(created_week as int)<17 and origin_zone!='x'",con=conn) 
	"""
	# df=pd.read_sql(f"SELECT odl.*, ST_AsText(odl.destination_geography) as destination_geom, \
	# 		ST_AsText(odl.lane_line_str) as lane_geom, \
	# 			carr.legal_name, carr.c411_trucks,otr_cust.name as customer_name \
	# 		FROM \
	# 		otr_data_loads AS odl \
	# 		LEFT JOIN carrier_otr AS carr ON  odl.carrier_id=carr.id   \
	# 			INNER JOIN otr_data_customers AS otr_cust ON  odl.customer_id=otr_cust.id   \
	# 			where odl.status='RELEASED' AND ST_DWithin(odl.destination_geography::geography, 'SRID=4326;POINT({lon} {lat})'::geography, {dist}) \
	# 				AND odl.delivery_date \
	# 				BETWEEN '{date_ago.year}-{date_ago.month}-{date_ago.day}' AND \
	# 					'{date_now.year}-{date_now.month}-{date_now.day}';",conn,
	# 			parse_dates={'booked_on': {'format': '%Y-%m-%d'},
	# 		'picked_up_by': {'format': '%Y-%m-%d'},
	# 		'delivery_date': {'format': '%Y-%m-%d'}})
	df=pd.read_sql(f"SELECT odl.delivery_date,odl.destination_geography,odl.id, \
				odl.carrier_id,odl.carrier_total_rate as rate, \
					ST_AsText(odl.destination_geography) as destination_geom, \
			ST_AsText(odl.lane_line_str) as lane_geom, \
				carr.legal_name, carr.c411_trucks,otr_cust.name as customer_name \
			FROM \
			otr_data_loads AS odl \
			LEFT JOIN carrier_otr AS carr ON  odl.carrier_id=carr.id   \
				INNER JOIN otr_data_customers AS otr_cust ON  odl.customer_id=otr_cust.id   \
				where odl.status='RELEASED' AND ST_DWithin(odl.destination_geography::geography, 'SRID=4326;POINT({lon} {lat})'::geography, {dist}) \
					AND odl.delivery_date \
					BETWEEN '{date_ago.year}-{date_ago.month}-{date_ago.day}' AND \
						'{date_now.year}-{date_now.month}-{date_now.day}';",conn,
				parse_dates={'booked_on': {'format': '%Y-%m-%d'},
			'picked_up_by': {'format': '%Y-%m-%d'},
			'delivery_date': {'format': '%Y-%m-%d'}})
	df['legal_name'] = df['legal_name'].fillna('INDEPENDENT')
	df['rate'] = df['rate'].fillna(0)

	df=df[~df['delivery_date'].astype(str).str.startswith('N')]
	df['created_week']=df['delivery_date'].apply(lambda x : x.strftime("%U"))#%U#%W
	df['created_week']=df['created_week'].astype(int)
	df['created_year']=df['delivery_date'].apply(lambda x : x.strftime("%Y"))
	df['created_year']=df['created_year'].astype(int)
	df['created_month']=df['delivery_date'].apply(lambda x : x.strftime("%B"))
	df['created_month_num']=df['delivery_date'].apply(lambda x : x.strftime("%m"))
	df['created_month_num']=df['created_month_num'].astype(int)
	df['created_year']=df['created_year'].astype(str)
	df['created_week']=df['created_week'].astype(str)
	df['year_week_str']=df[['created_year', 'created_week']].agg(' Week '.join, axis=1)
	df['created_year']=df['created_year'].astype(int)
	df['created_week']=df['created_week'].astype(int)

	df['destination_geom'] = gp.GeoSeries.from_wkt(df['destination_geom'])
	# df_select=df.groupby(['destination_geography','year_week_str']).agg({"id": "count",'destination_geom':'first'}).reset_index()
	df_select=df.groupby(['destination_geography']).agg({"id": "count",'destination_geom':'first'}).reset_index()
	# df_select=df_select.groupby(['destination_geography']).agg({"id": "sum",'destination_geom':'first'}).reset_index()
	df_select=df_select.sort_values(by=['id'],ascending=False)
	df_select=df_select[0:20]
	destination_geography=df_select['destination_geography']

	# lst = range(1,10)
	# ranges=np.array_split(lst, 3)
	# chart_colors=['#f21111','#884EA0','#3498DB','#1ABC9C','#1E8449','#F1C40F','#F39C12','#E67E22','#BA4A00','#00b300','#82E0AA','#f02ef0']
 
	# lines=[]
	# for i in df_select['destination_geography'].unique().tolist():
	# 	df_tmp=df_select[df_select['destination_geography']==i]
	# 	df_tmp1=df[df['destination_geography']==i]['legal_name'].values.tolist()
	# 	if len(df_tmp1)>0:
	# 		df_tmp1=[x for x in df_tmp1 if x]
	# 		df_tmp1=sorted(list(set(df_tmp1)))
	# 	if len(df_tmp)>0:
	# 		avg=df_tmp['id'].mean()
	# 		lat2=df_tmp['destination_geom'].values[0].y
	# 		lon2=df_tmp['destination_geom'].values[0].x
	# 	else:
	# 		lat2=0.0
	# 		lon2=0.0
	# 		avg=1
	# 	clr_ind=None
	# 	for k in enumerate(ranges):
	# 		if int(avg) in k[1]:
	# 			clr_ind=k[0]
	# 			break
	# 	if clr_ind!=0 and not clr_ind:
	# 		clr_ind=11
	# 	point1 = Point(float(lon),float(lat))#lon.lat
	# 	point2 = Point(float(lon2),float(lat2))
	# 	angle1,angle2,distance = geod.inv(point1.x, point1.y, point2.x, point2.y)
	# 	lines.append([[lat,lon],[lat2,lon2],int(avg),chart_colors[clr_ind],int(distance/1000),df_tmp1])
	lines=[]
	for i in df_select.itertuples():
		tmp=df[df['destination_geography']==i[1]]
		tmp_map=tmp.groupby(['legal_name']).agg({'rate':"mean","id": "count",}).reset_index()
		tmp_map=tmp_map[0:10]
		tmp_map['rate']=tmp_map['rate'].astype(int)
		if len(tmp)>0:
			avg=1#tmp['delivery_date'].mean()
			lat2=tmp['destination_geom'].values[0].y
			lon2=tmp['destination_geom'].values[0].x
		else:
			lat2=0.0
			lon2=0.0
			avg=1
		point1 = Point(float(lon),float(lat))#lon.lat
		point2 = Point(float(lon2),float(lat2))
		angle1,angle2,distance = geod.inv(point1.x, point1.y, point2.x, point2.y)
		lines.append([0,[lat2,lon2],int(avg),0,int(distance/1000),tmp_map.values.tolist(),int(i[2])])
	data={"lines":lines}
	return JsonResponse(data)

@xframe_options_exempt
def test(response):
	data={"lines":"lines"}
	return JsonResponse(data)

@xframe_options_exempt
def just_map_loads_deadhead1(response):
	lon=response.GET.get('lon',None)
	lat=response.GET.get('lat',None)
	dist=response.GET.get('dist',None)
	date_now=datetime.now()
	date_ago = datetime.today() - timedelta(days=60)

	# df=pd.read_sql(f"SELECT odl.*, ST_AsText(odl.origin_geography) as origin_geom, \
	# 		ST_AsText(odl.lane_line_str) as lane_geom, \
	# 			carr.legal_name, carr.c411_trucks,otr_cust.name as customer_name \
	# 		FROM \
	# 		otr_data_loads AS odl \
	# 		LEFT JOIN carrier_otr AS carr ON  odl.carrier_id=carr.id   \
	# 			INNER JOIN otr_data_customers AS otr_cust ON  odl.customer_id=otr_cust.id   \
	# 			where ST_DWithin(odl.origin_geography::geography, 'SRID=4326;POINT({lon} {lat})'::geography, 80450) \
	# 				AND odl.delivery_date \
	# 				BETWEEN '{date_ago.year}-{date_ago.month}-{date_ago.day}' AND \
	# 					'{date_now.year}-{date_now.month}-{date_now.day}';",conn,
	# 			parse_dates={'booked_on': {'format': '%Y-%m-%d'},
	# 		'picked_up_by': {'format': '%Y-%m-%d'},
	# 		'delivery_date': {'format': '%Y-%m-%d'}})
	# df['legal_name'] = df['legal_name'].fillna('INDEPENDENT')

	# df=df[~df['delivery_date'].astype(str).str.startswith('N')]
	# df['created_week']=df['delivery_date'].apply(lambda x : x.strftime("%U"))#%U#%W
	# df['created_week']=df['created_week'].astype(int)
	# df['created_year']=df['delivery_date'].apply(lambda x : x.strftime("%Y"))
	# df['created_year']=df['created_year'].astype(int)
	# df['created_month']=df['delivery_date'].apply(lambda x : x.strftime("%B"))
	# df['created_month_num']=df['delivery_date'].apply(lambda x : x.strftime("%m"))
	# df['created_month_num']=df['created_month_num'].astype(int)
	# df['created_year']=df['created_year'].astype(str)
	# df['created_week']=df['created_week'].astype(str)
	# df['year_week_str']=df[['created_year', 'created_week']].agg(' Week '.join, axis=1)
	# df['created_year']=df['created_year'].astype(int)
	# df['created_week']=df['created_week'].astype(int)

	# df['origin_geom'] = gp.GeoSeries.from_wkt(df['origin_geom'])
	# df['lane_geom'] = gp.GeoSeries.from_wkt(df['lane_geom'])
	# df_select=df.groupby(['origin_geography','year_week_str']).agg({"id": "count",
	# 'origin_geom':'first','lane_geom':'first'}).reset_index()
	# df_select=df_select.groupby(['origin_geography']).agg({"id": "mean",
	# 'origin_geom':'first','lane_geom':'first'}).reset_index()
	# df_select=df_select.sort_values(by=['id'],ascending=False)
	# df_select=df_select[0:20]
	# df_select=df_select.reset_index()

	# lst = range(1,10)
	# ranges=np.array_split(lst, 3)
	# chart_colors=['#f21111','#884EA0','#3498DB','#1ABC9C','#1E8449','#F1C40F','#F39C12','#E67E22','#BA4A00','#00b300','#82E0AA','#f02ef0']
 
	# lines=[]
	# for i in df_select['origin_geography'].unique().tolist():
	# 	df_tmp=df_select[df_select['origin_geography']==i]
	# 	df_tmp1=df[df['origin_geography']==i]['legal_name'].values.tolist()
	# 	if len(df_tmp1)>0:
	# 		df_tmp1=[x for x in df_tmp1 if x]
	# 		# df_tmp1=sorted(list(set(df_tmp1)))
	# 		desc=df_tmp1
	# 		desc=[x.replace(" ","-") for x in desc if x]
	# 		desc =sorted(list(desc))
	# 		desc=str(desc)[1:-1].replace(","," ")
	# 	if len(df_tmp)>0:
	# 		avg=df_tmp['id'].mean()
	# 		lat2=df_tmp['origin_geom'].values[0].y
	# 		lon2=df_tmp['origin_geom'].values[0].x
	# 		lat11=df_tmp['lane_geom'].values[0].coords[0][1]
	# 		lon11=df_tmp['lane_geom'].values[0].coords[0][0]
	# 		lat22=df_tmp['lane_geom'].values[0].coords[1][1]
	# 		lon22=df_tmp['lane_geom'].values[0].coords[1][0]
	# 	else:
	# 		lat2=0.0
	# 		lon2=0.0
	# 		lat11=0.0
	# 		lon11=0.0
	# 		lat22=0.0
	# 		lon22=0.0
	# 		avg=1
	# 	# clr_ind=None
	# 	# for k in enumerate(ranges):
	# 	# 	if int(avg) in k[1]:
	# 	# 		clr_ind=k[0]
	# 	# 		break
	# 	# if clr_ind!=0 and not clr_ind:
	# 	# 	clr_ind=11
	# 	clr_ind = 0
	# 	point1 = Point(float(lon),float(lat))#lon.lat
	# 	point2 = Point(float(lon2),float(lat2))
	# 	angle1,angle2,distance = geod.inv(point1.x, point1.y, point2.x, point2.y)
	# 	lines.append([[lat,lon],[lat2,lon2],int(avg),chart_colors[clr_ind],int(distance/1000),desc])
	# 	# point1 = Point(float(lon11),float(lat11))#lon.lat
	# 	# point2 = Point(float(lon22),float(lat22))
	# 	# angle1,angle2,distance = geod.inv(point1.x, point1.y, point2.x, point2.y)
	# 	# lines.append([[lat11,lon11],[lat22,lon22],int(avg),chart_colors[1],int(distance/1000),desc])

	lines=[]
	df=pd.read_sql(f"SELECT odl.*, ST_AsText(odl.origin_geography) as origin_geom, \
			ST_AsText(odl.lane_line_str) as lane_geom, \
				carr.legal_name, carr.c411_trucks,otr_cust.name as customer_name \
			FROM \
			otr_data_loads AS odl \
			LEFT JOIN carrier_otr AS carr ON  odl.carrier_id=carr.id   \
				INNER JOIN otr_data_customers AS otr_cust ON  odl.customer_id=otr_cust.id   \
				where odl.status='RELEASED' AND ST_DWithin(odl.origin_geography::geography, 'SRID=4326;POINT({lon} {lat})'::geography, 80450) \
					AND odl.delivery_date \
					BETWEEN '{date_ago.year}-{date_ago.month}-{date_ago.day}' AND \
						'{date_now.year}-{date_now.month}-{date_now.day}';",conn,
				parse_dates={'booked_on': {'format': '%Y-%m-%d'},
			'picked_up_by': {'format': '%Y-%m-%d'},
			'delivery_date': {'format': '%Y-%m-%d'}})
	df['legal_name'] = df['legal_name'].fillna('INDEPENDENT')

	df=df[~df['delivery_date'].astype(str).str.startswith('N')]
	df['created_week']=df['delivery_date'].apply(lambda x : x.strftime("%U"))#%U#%W
	df['created_week']=df['created_week'].astype(int)
	df['created_year']=df['delivery_date'].apply(lambda x : x.strftime("%Y"))
	df['created_year']=df['created_year'].astype(int)
	df['created_month']=df['delivery_date'].apply(lambda x : x.strftime("%B"))
	df['created_month_num']=df['delivery_date'].apply(lambda x : x.strftime("%m"))
	df['created_month_num']=df['created_month_num'].astype(int)
	df['created_year']=df['created_year'].astype(str)
	df['created_week']=df['created_week'].astype(str)
	df['year_week_str']=df[['created_year', 'created_week']].agg(' Week '.join, axis=1)
	df['created_year']=df['created_year'].astype(int)
	df['created_week']=df['created_week'].astype(int)

	df['origin_geom'] = gp.GeoSeries.from_wkt(df['origin_geom'])
	df['lane_geom'] = gp.GeoSeries.from_wkt(df['lane_geom'])
	df_select=df.groupby(['origin_geography','year_week_str']).agg({"id": "count",
	'origin_geom':'first','lane_geom':'first'}).reset_index()
	df_select=df_select.groupby(['origin_geography']).agg({"id": "mean",
	'origin_geom':'first','lane_geom':'first'}).reset_index()
	df_select=df_select.sort_values(by=['id'],ascending=False)
	df_select=df_select[0:20]
	df_select=df_select.reset_index()

	lst = range(1,10)
	ranges=np.array_split(lst, 3)
	chart_colors=['#f21111','#884EA0','#3498DB','#1ABC9C','#1E8449','#F1C40F','#F39C12','#E67E22','#BA4A00','#00b300','#82E0AA','#f02ef0']
 
	for i in df_select['origin_geography'].unique().tolist():
		df_tmp=df_select[df_select['origin_geography']==i]
		df_tmp1=df[df['origin_geography']==i]['legal_name'].values.tolist()
		if len(df_tmp1)>0:
			df_tmp1=[x for x in df_tmp1 if x]
			# df_tmp1=sorted(list(set(df_tmp1)))
			desc=df_tmp1
			desc=[x.replace(" ","-") for x in desc if x]
			desc =sorted(list(desc))
			desc=str(desc)[1:-1].replace(","," ")
		if len(df_tmp)>0:
			avg=df_tmp['id'].mean()
			lat2=df_tmp['origin_geom'].values[0].y
			lon2=df_tmp['origin_geom'].values[0].x
			lat11=df_tmp['lane_geom'].values[0].coords[0][1]
			lon11=df_tmp['lane_geom'].values[0].coords[0][0]
			lat22=df_tmp['lane_geom'].values[0].coords[1][1]
			lon22=df_tmp['lane_geom'].values[0].coords[1][0]
		else:
			lat2=0.0
			lon2=0.0
			lat11=0.0
			lon11=0.0
			lat22=0.0
			lon22=0.0
			avg=1
		# clr_ind=None
		# for k in enumerate(ranges):
		# 	if int(avg) in k[1]:
		# 		clr_ind=k[0]
		# 		break
		# if clr_ind!=0 and not clr_ind:
		# 	clr_ind=11
		clr_ind = 0
		point1 = Point(float(lon),float(lat))#lon.lat
		point2 = Point(float(lon2),float(lat2))
		angle1,angle2,distance = geod.inv(point1.x, point1.y, point2.x, point2.y)
		lines.append([[lat,lon],[lat2,lon2],int(avg),chart_colors[clr_ind],int(distance/1000),desc])
		# point1 = Point(float(lon11),float(lat11))#lon.lat
		# point2 = Point(float(lon22),float(lat22))
		# angle1,angle2,distance = geod.inv(point1.x, point1.y, point2.x, point2.y)
		# lines.append([[lat11,lon11],[lat22,lon22],int(avg),chart_colors[2],int(distance/1000),desc])
	data={"lines":lines}
	return JsonResponse(data)

@xframe_options_exempt
def just_heat_chart_v2_api(response):
	# df = df_gd.copy()
	customer=response.GET.getlist('customer[]',None)
	if customer:
		customer=[x.replace("'","").replace('"',"") for x in customer]
		cust=str(customer)[1:-1]
		cusotmer_sql=f"odl.customer IN ({cust}) AND  "
	else:
		cusotmer_sql=""
	selector=response.GET.get('week_month',None)
	if not selector:
		selector='year_month'
	selector0=response.GET.get('selector0',None)
	if not selector0:
		selector0='customer'
	origin_st=response.GET.getlist('origin_st[]',None)
	if origin_st:
		origin_st=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in origin_st]
		origin_st=str(origin_st)[1:-1]
		origin_st_sql=f" AND odl.origin_state_province IN ({origin_st}) "
	if not origin_st:
		origin_st_sql=""
	

	destination_st=response.GET.getlist('destination_st[]',None)
	if destination_st:
		destination_st=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in destination_st]
		destination_st=str(destination_st)[1:-1]
		destination_st_sql=f" AND odl.destination_state_province IN ({destination_st}) "
	if not destination_st:
		destination_st_sql=""

	origin_ct=response.GET.getlist('origin_ct[]',None)
	if origin_ct:
		origin_ct=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in origin_ct]
		origin_ct=[x.replace("'","").replace('"',"") for x in origin_ct]
		origin_ct=str(origin_ct)[1:-1]
		origin_ct_sql=f" AND odl.origin_city IN ({origin_ct}) "
	if not origin_ct:
		origin_ct_sql=""
	
	destination_ct=response.GET.getlist('destination_ct[]',None)
	if destination_ct:
		destination_ct=[x.split(" ")[-1].replace("(","").replace(")","").strip() for x in destination_ct]
		destination_ct=[x.replace("'","").replace('"',"") for x in destination_ct]
		destination_ct=str(destination_ct)[1:-1]
		destination_ct_sql=f" AND odl.destination_city IN ({destination_ct}) "
	if not destination_ct:
		destination_ct_sql=""

	# # selector='year_month'
	# # selector0='customer'
	# origin_ct=[x.replace("'","").replace('"',"") for x in origin_ct]
	# destination_ct=[x.replace("'","").replace('"',"") for x in destination_ct]
	# origin_st=str(origin_st)[1:-1]
	# origin_ct=str(origin_ct)[1:-1]
	# destination_st=str(destination_st)[1:-1]
	# destination_ct=str(destination_ct)[1:-1]

	date_now=datetime.now()
	date_ago = datetime.today() - timedelta(days=190)
	df1=pd.read_sql(f"select odl.id,odl.booked_on,odl.customer_rate, \
		odl.customer,odl.shipper,odl.receiver,odl.origin_data,odl.destination_data  \
		 from gold_oldnew AS odl \
	where {cusotmer_sql} \
		 (booked_on \
					BETWEEN '{date_ago.year}-{date_ago.month}-{date_ago.day}' AND '{date_now.year}-{date_now.month}-{date_now.day}') \
				{origin_st_sql} \
					{origin_ct_sql} \
						{destination_st_sql} \
							{destination_ct_sql} ORDER BY booked_on DESC LIMIT 1000;",conn,parse_dates=['booked_on'])
		
	if len(df1)<1:
		return JsonResponse({"error":[True]})
	df1=df1[~df1['booked_on'].astype(str).str.startswith('N')]
	# df['created_at'] = df['booked_on'].map(lambda x: x.strftime('%Y-%m-%d'))
	df1['created_week']=df1['booked_on'].apply(lambda x : x.strftime("%U"))#%U#%W
	df1['created_week']=df1['created_week'].astype(int)
	df1['created_year']=df1['booked_on'].apply(lambda x : x.strftime("%Y"))
	df1['created_year']=df1['created_year'].astype(int)
	df1['created_month']=df1['booked_on'].apply(lambda x : x.strftime("%B"))
	df1['created_month_num']=df1['booked_on'].apply(lambda x : x.strftime("%m"))
	df1['created_month_num']=df1['created_month_num'].astype(int)
	df1['created_year']=df1['created_year'].astype(str)
	df1['created_week']=df1['created_week'].astype(str)
	df1['year_week_str']=df1[['created_year', 'created_week']].agg(' Week '.join, axis=1)
	df1['created_year']=df1['created_year'].astype(int)
	df1['created_week']=df1['created_week'].astype(int)
	df1['created_year']=df1['created_year'].astype(str)
	df1['created_week']=df1['created_week'].astype(str)
	df1['year_month']=df1[['created_year', 'created_month']].agg(' '.join, axis=1)
	df1['travel_data']=df1[['origin_data', 'destination_data']].agg('->'.join, axis=1)
	df1['year_week_str']=df1[['created_year', 'created_week']].agg(' Week '.join, axis=1)
	df1['created_year']=df1['created_year'].astype(int)
	df1['created_week']=df1['created_week'].astype(int)
	df1['year_week']=df1['created_year'].astype(str)+df1['created_week'].astype(str)
	# selector='year_month'
	# selector='year_week_str'
	# selector0='customer'
	carr=df1.groupby([selector0,selector]).agg({'id':'count',
												'year_week':'max',
												'created_year':'max',
												'created_week':'max',
												'created_month_num':'max',
												'customer_rate':['min', 'max', 'mean']}).reset_index()
	carr_columns=[]
	for x in carr.columns.ravel():
		if x[0]=="customer_rate":
			carr_columns.append("_".join(x))
		else:
			carr_columns.append(x[0])

	carr.columns = carr_columns
	if selector=='year_week_str':
		carr.sort_values(by=['created_year','created_week'],ascending=True,inplace=True)
	else:
		carr.sort_values(by=['created_year','created_month_num'],ascending=True,inplace=True)

	lanes=carr.groupby([selector0]).count().sort_values(by=['id'],
					ascending=False)['id'][:20].index.tolist()
	carr=carr[carr[selector0].isin(lanes)]
	year_weeks=carr[selector].unique().tolist()
	if selector=='year_week_str':
		year_weeks=year_weeks[-14:]

	heats=[]
	for i in lanes:
		tmp=carr[carr[selector0]==i]
		for j in year_weeks:
			tmp1=tmp[tmp[selector]==j]
			if len(tmp1)>0:
				heats.append({"selector0":i,"selector":j,
						"value":int(tmp1['id'].values[0]),
						"customer_rate":int(tmp1['customer_rate_mean'].values[0])})
			else:
				heats.append({"selector0":i,"selector":j,
						"value":0,
						"customer_rate":0})

	return JsonResponse({"error":[False],
		"heat_series":heats})

@xframe_options_exempt
def just_map_deadhead_rig_lines(response):
	lon=response.GET.get('lon',None)
	lat=response.GET.get('lat',None)
	date_now=datetime.now()
	date_ago = datetime.today() - timedelta(days=60)
	# outgoing_sql=f" (ST_DWithin(odl.origin_geography::geography, 'SRID=4326;POINT({lon} {lat})'::geography, 6045) \
	# 	OR ST_DWithin(odl.destination_geography::geography, 'SRID=4326;POINT({lon} {lat})'::geography, 100)) "
	# outgoing_sql=f" ST_DWithin(odl.destination_geography::geography, 'SRID=4326;POINT({lon} {lat})'::geography, 100) "
	# df1=pd.read_sql(f"SELECT MAX(odl.delivery_date) AS delivery_date, \
	# 	COALESCE(ST_AsText(odl.lane_line_str)) as lane_geom  \
	# 	FROM \
	# 	otr_data_loads AS odl \
	# 		where odl.status='RELEASED' AND {outgoing_sql} AND odl.lane_line_str IS NOT NULL \
	# 				group by odl.lane_line_str \
	# 				order by count(odl.id) desc LIMIT 50 ;",conn)
	# df1['lane_geom'] = gp.GeoSeries.from_wkt(df1['lane_geom'])
	# chart_colors=["#1F78B4",
	# 		"#00278C",
	# 		"#B2DF8A",
	# 		"#33A02C",
	# 		"#FB9A99",
	# 		"#E31A1C",
	# 		"#FDBF6F",
	# 		"#FF7F00",
	# 		"#CAB2D6",
	# 		"#6A3D9A",
	# 		"#949D00",
	# 		"#666666"]
	# lines=[]
	# for i in df1.itertuples():
	# 	c=i[2].coords
	# 	point1 = Point(float(c[0][0]),float(c[0][1]))#lon.lat
	# 	point2 = Point(float(c[1][0]),float(c[1][1]))
	# 	angle1,angle2,distance = geod.inv(point1.x, point1.y, point2.x, point2.y)
	# 	# lines.append([[float(lat),float(lon)],[c[1][1],c[1][0]],0,"#5035fc",int(distance/1000),"desc"])
	# 	lines.append([[c[0][1],c[0][0]],[c[1][1],c[1][0]],0,"#5035fc",int(distance/1000),"desc"])
	outgoing_sql=f" ST_DWithin(odl.destination_geography::geography, 'SRID=4326;POINT({lon} {lat})'::geography, 100) "
	df1=pd.read_sql(f"SELECT odl.id,odl.delivery_date, \
					odl.origin_data,odl.destination_data, \
		COALESCE(ST_AsText(odl.lane_line_str)) as lane_geom  \
		FROM \
		otr_data_loads AS odl \
			where odl.status='RELEASED' AND {outgoing_sql} AND odl.lane_line_str IS NOT NULL \
				AND odl.delivery_date \
					BETWEEN '{date_ago.year}-{date_ago.month}-{date_ago.day}' AND \
						'{date_now.year}-{date_now.month}-{date_now.day}' LIMIT 100;",conn)
	df1['lane_geom_str'] = df1['lane_geom']
	df1['lane_geom'] = gp.GeoSeries.from_wkt(df1['lane_geom'])
	# 	df=df[~df['delivery_date'].astype(str).str.startswith('N')]
	df_map=df1.groupby(['lane_geom_str']).agg({'lane_geom':"first","id": "count",
											"origin_data":"first","destination_data":"first"}).reset_index()
	df_map=df_map[0:20]
	lines=[]
	for i in df_map.itertuples():
		c=i[2].coords
		point1 = Point(float(c[0][0]),float(c[0][1]))#lon.lat
		point2 = Point(float(c[1][0]),float(c[1][1]))
		angle1,angle2,distance = geod.inv(point1.x, point1.y, point2.x, point2.y)
		# lines.append([[float(lat),float(lon)],[c[1][1],c[1][0]],0,"#5035fc",int(distance/1000),"desc"])
		lines.append([[c[0][1],c[0][0]],[c[1][1],c[1][0]],0,"#5035fc",int(distance/1000),[i[4],i[5]]])

	data={"lines":lines}
	return JsonResponse(data)

@xframe_options_exempt
def just_map_deadhead_lines1(response):
	lon=response.GET.get('lon',None)
	lat=response.GET.get('lat',None)
	outgoing_sql=f" (ST_DWithin(odl.origin_geography::geography, 'SRID=4326;POINT({lon} {lat})'::geography, 6045) \
		OR ST_DWithin(odl.destination_geography::geography, 'SRID=4326;POINT({lon} {lat})'::geography, 100)) "
	outgoing_sql=f" ST_DWithin(odl.origin_geography::geography, 'SRID=4326;POINT({lon} {lat})'::geography, 100) "
	df1=pd.read_sql(f"SELECT MAX(odl.delivery_date) AS delivery_date, \
		COALESCE(ST_AsText(odl.lane_line_str)) as lane_geom  \
		FROM \
		otr_data_loads AS odl \
			where odl.status='RELEASED' AND {outgoing_sql} AND odl.lane_line_str IS NOT NULL \
					group by odl.lane_line_str \
					order by count(odl.id) desc LIMIT 50 ;",conn)
	df1['lane_geom'] = gp.GeoSeries.from_wkt(df1['lane_geom'])
	chart_colors=["#1F78B4",
			"#00278C",
			"#B2DF8A",
			"#33A02C",
			"#FB9A99",
			"#E31A1C",
			"#FDBF6F",
			"#FF7F00",
			"#CAB2D6",
			"#6A3D9A",
			"#949D00",
			"#666666"]
	lines=[]
	for i in df1.itertuples():
		c=i[2].coords
		point1 = Point(float(c[0][0]),float(c[0][1]))#lon.lat
		point2 = Point(float(c[1][0]),float(c[1][1]))
		angle1,angle2,distance = geod.inv(point1.x, point1.y, point2.x, point2.y)
		# lines.append([[float(lat),float(lon)],[c[1][1],c[1][0]],0,"#5035fc",int(distance/1000),"desc"])
		lines.append([[c[0][1],c[0][0]],[c[1][1],c[1][0]],0,"#5035fc",int(distance/1000),"desc"])

	data={"lines":lines}
	return JsonResponse(data)

@xframe_options_exempt
def just_map_loads_deadhead(response):
	lon=response.GET.get('lon',None)
	lat=response.GET.get('lat',None)
	dist=response.GET.get('dist',None)
	print(dist)
	dist=int(dist)
	dist=804.5 * dist#80450
	date_now=datetime.now()
	date_ago = datetime.today() - timedelta(days=90)
	"""
	df=pd.read_sql("SELECT asset_assetId,\
		asset_equipment_origin_place_namedcoordinates_latitude,\
		asset_equipment_origin_place_namedcoordinates_longitude,\
		asset_equipment_origin_namedcoordinates_latitude,\
		asset_equipment_origin_namedcoordinates_longitude\
	 FROM import.trucks_raw where cast(created_week as int)>12 and \
		cast(created_week as int)<17 and origin_zone!='x'",con=conn) 
	"""
	# df=pd.read_sql(f"SELECT odl.*, ST_AsText(odl.origin_geography) as origin_geom, \
	# 		ST_AsText(odl.lane_line_str) as lane_geom, \
	# 			carr.legal_name, carr.c411_trucks,otr_cust.name as customer_name \
	# 		FROM \
	# 		otr_data_loads AS odl \
	# 		LEFT JOIN carrier_otr AS carr ON  odl.carrier_id=carr.id   \
	# 			INNER JOIN otr_data_customers AS otr_cust ON  odl.customer_id=otr_cust.id   \
	# 			where odl.status='RELEASED' AND ST_DWithin(odl.origin_geography::geography, 'SRID=4326;POINT({lon} {lat})'::geography, {dist}) \
	# 				AND odl.delivery_date \
	# 				BETWEEN '{date_ago.year}-{date_ago.month}-{date_ago.day}' AND \
	# 					'{date_now.year}-{date_now.month}-{date_now.day}';",conn,
	# 			parse_dates={'booked_on': {'format': '%Y-%m-%d'},
	# 		'picked_up_by': {'format': '%Y-%m-%d'},
	# 		'delivery_date': {'format': '%Y-%m-%d'}})
	df=pd.read_sql(f"SELECT odl.delivery_date,odl.origin_geography,odl.id, \
				odl.carrier_id,odl.customer_rate as rate, \
					ST_AsText(odl.origin_geography) as origin_geom, \
			ST_AsText(odl.lane_line_str) as lane_geom, \
				carr.legal_name, carr.c411_trucks,otr_cust.name as customer_name \
			FROM \
			otr_data_loads AS odl \
			LEFT JOIN carrier_otr AS carr ON  odl.carrier_id=carr.id   \
				INNER JOIN otr_data_customers AS otr_cust ON  odl.customer_id=otr_cust.id   \
				where odl.status='RELEASED' AND ST_DWithin(odl.origin_geography::geography, 'SRID=4326;POINT({lon} {lat})'::geography, {dist}) \
					AND odl.delivery_date \
					BETWEEN '{date_ago.year}-{date_ago.month}-{date_ago.day}' AND \
						'{date_now.year}-{date_now.month}-{date_now.day}';",conn,
				parse_dates={'booked_on': {'format': '%Y-%m-%d'},
			'picked_up_by': {'format': '%Y-%m-%d'},
			'delivery_date': {'format': '%Y-%m-%d'}})
	df['legal_name'] = df['legal_name'].fillna('INDEPENDENT')
	df['rate'] = df['rate'].fillna(0)
	df=df[~df['delivery_date'].astype(str).str.startswith('N')]
	df['created_week']=df['delivery_date'].apply(lambda x : x.strftime("%U"))#%U#%W
	df['created_week']=df['created_week'].astype(int)
	df['created_year']=df['delivery_date'].apply(lambda x : x.strftime("%Y"))
	df['created_year']=df['created_year'].astype(int)
	df['created_month']=df['delivery_date'].apply(lambda x : x.strftime("%B"))
	df['created_month_num']=df['delivery_date'].apply(lambda x : x.strftime("%m"))
	df['created_month_num']=df['created_month_num'].astype(int)
	df['created_year']=df['created_year'].astype(str)
	df['created_week']=df['created_week'].astype(str)
	df['year_week_str']=df[['created_year', 'created_week']].agg(' Week '.join, axis=1)
	df['created_year']=df['created_year'].astype(int)
	df['created_week']=df['created_week'].astype(int)

	df['origin_geom'] = gp.GeoSeries.from_wkt(df['origin_geom'])
	# df_select=df.groupby(['origin_geography','year_week_str']).agg({"id": "count",'origin_geom':'first'}).reset_index()
	df_select=df.groupby(['origin_geography']).agg({"id": "count",'origin_geom':'first'}).reset_index()
	# df_select=df_select.groupby(['origin_geography']).agg({"id": "sum",'origin_geom':'first'}).reset_index()
	df_select=df_select.sort_values(by=['id'],ascending=False)
	df_select=df_select[0:20]
	origin_geography=df_select['origin_geography']

	# lst = range(1,10)
	# ranges=np.array_split(lst, 3)
	# chart_colors=['#f21111','#884EA0','#3498DB','#1ABC9C','#1E8449','#F1C40F','#F39C12','#E67E22','#BA4A00','#00b300','#82E0AA','#f02ef0']
 
	# lines=[]
	# for i in df_select['origin_geography'].unique().tolist():
	# 	df_tmp=df_select[df_select['origin_geography']==i]
	# 	df_tmp1=df[df['origin_geography']==i]['legal_name'].values.tolist()
	# 	if len(df_tmp1)>0:
	# 		df_tmp1=[x for x in df_tmp1 if x]
	# 		df_tmp1=sorted(list(set(df_tmp1)))
	# 	if len(df_tmp)>0:
	# 		avg=df_tmp['id'].mean()
	# 		lat2=df_tmp['origin_geom'].values[0].y
	# 		lon2=df_tmp['origin_geom'].values[0].x
	# 	else:
	# 		lat2=0.0
	# 		lon2=0.0
	# 		avg=1
	# 	clr_ind=None
	# 	for k in enumerate(ranges):
	# 		if int(avg) in k[1]:
	# 			clr_ind=k[0]
	# 			break
	# 	if clr_ind!=0 and not clr_ind:
	# 		clr_ind=11
	# 	point1 = Point(float(lon),float(lat))#lon.lat
	# 	point2 = Point(float(lon2),float(lat2))
	# 	angle1,angle2,distance = geod.inv(point1.x, point1.y, point2.x, point2.y)
	# 	lines.append([[lat,lon],[lat2,lon2],int(avg),chart_colors[clr_ind],int(distance/1000),df_tmp1])
	lines=[]
	for i in df_select.itertuples():
		tmp=df[df['origin_geography']==i[1]]
		tmp_map=tmp.groupby(['customer_name']).agg({'rate':"mean","id": "count",}).reset_index()
		tmp_map=tmp_map[0:10]
		tmp_map['rate']=tmp_map['rate'].astype(int)
		if len(tmp)>0:
			avg=1#tmp['delivery_date'].mean()
			lat2=tmp['origin_geom'].values[0].y
			lon2=tmp['origin_geom'].values[0].x
		else:
			lat2=0.0
			lon2=0.0
			avg=1
		point1 = Point(float(lon),float(lat))#lon.lat
		point2 = Point(float(lon2),float(lat2))
		angle1,angle2,distance = geod.inv(point1.x, point1.y, point2.x, point2.y)
		lines.append([0,[lat2,lon2],int(avg),0,int(distance/1000),tmp_map.values.tolist(),int(i[2])])
	data={"lines":lines}
	return JsonResponse(data)

@xframe_options_exempt
def just_map_deadhead_lines(response):
	lon=response.GET.get('lon',None)
	lat=response.GET.get('lat',None)
	date_now=datetime.now()
	date_ago = datetime.today() - timedelta(days=90)
	# outgoing_sql=f" (ST_DWithin(odl.origin_geography::geography, 'SRID=4326;POINT({lon} {lat})'::geography, 6045) \
	# 	OR ST_DWithin(odl.origin_geography::geography, 'SRID=4326;POINT({lon} {lat})'::geography, 100)) "
	# outgoing_sql=f" ST_DWithin(odl.origin_geography::geography, 'SRID=4326;POINT({lon} {lat})'::geography, 100) "
	# df1=pd.read_sql(f"SELECT MAX(odl.delivery_date) AS delivery_date, \
	# 	COALESCE(ST_AsText(odl.lane_line_str)) as lane_geom  \
	# 	FROM \
	# 	otr_data_loads AS odl \
	# 		where odl.status='RELEASED' AND {outgoing_sql} AND odl.lane_line_str IS NOT NULL \
	# 				group by odl.lane_line_str \
	# 				order by count(odl.id) desc LIMIT 50 ;",conn)
	# df1['lane_geom'] = gp.GeoSeries.from_wkt(df1['lane_geom'])
	# chart_colors=["#1F78B4",
	# 		"#00278C",
	# 		"#B2DF8A",
	# 		"#33A02C",
	# 		"#FB9A99",
	# 		"#E31A1C",
	# 		"#FDBF6F",
	# 		"#FF7F00",
	# 		"#CAB2D6",
	# 		"#6A3D9A",
	# 		"#949D00",
	# 		"#666666"]
	# lines=[]
	# for i in df1.itertuples():
	# 	c=i[2].coords
	# 	point1 = Point(float(c[0][0]),float(c[0][1]))#lon.lat
	# 	point2 = Point(float(c[1][0]),float(c[1][1]))
	# 	angle1,angle2,distance = geod.inv(point1.x, point1.y, point2.x, point2.y)
	# 	# lines.append([[float(lat),float(lon)],[c[1][1],c[1][0]],0,"#5035fc",int(distance/1000),"desc"])
	# 	lines.append([[c[0][1],c[0][0]],[c[1][1],c[1][0]],0,"#5035fc",int(distance/1000),"desc"])
	outgoing_sql=f" ST_DWithin(odl.origin_geography::geography, 'SRID=4326;POINT({lon} {lat})'::geography, 100) "
	df1=pd.read_sql(f"SELECT odl.id,odl.delivery_date, \
					odl.origin_data,odl.destination_data, \
		COALESCE(ST_AsText(odl.lane_line_str)) as lane_geom  \
		FROM \
		otr_data_loads AS odl \
			where odl.status='RELEASED' AND {outgoing_sql} AND odl.lane_line_str IS NOT NULL \
				AND odl.delivery_date \
					BETWEEN '{date_ago.year}-{date_ago.month}-{date_ago.day}' AND \
						'{date_now.year}-{date_now.month}-{date_now.day}' LIMIT 100;",conn)
	df1['lane_geom_str'] = df1['lane_geom']
	df1['lane_geom'] = gp.GeoSeries.from_wkt(df1['lane_geom'])
	# 	df=df[~df['delivery_date'].astype(str).str.startswith('N')]
	df_map=df1.groupby(['lane_geom_str']).agg({'lane_geom':"first","id": "count",
											"origin_data":"first","destination_data":"first"}).reset_index()
	df_map=df_map[0:20]
	lines=[]
	for i in df_map.itertuples():
		c=i[2].coords
		point1 = Point(float(c[0][0]),float(c[0][1]))#lon.lat
		point2 = Point(float(c[1][0]),float(c[1][1]))
		angle1,angle2,distance = geod.inv(point1.x, point1.y, point2.x, point2.y)
		# lines.append([[float(lat),float(lon)],[c[1][1],c[1][0]],0,"#5035fc",int(distance/1000),"desc"])
		lines.append([[c[0][1],c[0][0]],[c[1][1],c[1][0]],0,"#5035fc",int(distance/1000),[i[4],i[5]]])

	data={"lines":lines}
	return JsonResponse(data)

@xframe_options_exempt
def just_map_heat_chart_click(response):
	lane=response.GET.get('lane',None)
	date_str=response.GET.get('date_str',None)
	df=df_gd.copy()
	df=df_gd[df_gd['travel_data']==lane]

	shipper=df.groupby(['shipper']).agg({"id": "count",
										'duration':'mean',
										'buy_cost':'mean'}).reset_index()

	customer=df.groupby(['customer']).agg({"id": "count",
										'duration':'mean',
										'customer_rate':'mean'}).reset_index()
	carrier=df.groupby(['carrier']).agg({"id": "count",
										'duration':'mean',
										'buy_cost':'mean'}).reset_index()
	carrier=carrier.sort_values(by=['id'],ascending=False)[0:6]
	customer['duration']=customer['duration'].astype(int)
	customer['customer_rate']=customer['customer_rate'].astype(int)
	shipper['duration']=shipper['duration'].astype(int)
	shipper['buy_cost']=shipper['buy_cost'].astype(int)
	carrier['duration']=carrier['duration'].astype(int)
	carrier['buy_cost']=carrier['buy_cost'].astype(int)
	data={"data":customer.values.tolist(),
		"customer":customer.values.tolist(),
		"shipper":shipper.values.tolist(),
		"carrier":carrier.values.tolist(),}
	return JsonResponse(data)







