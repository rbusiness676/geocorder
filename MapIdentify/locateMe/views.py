import logging
import os

import googlemaps as googlemaps
import openpyxl
import pandas as pd
import requests
import xlrd

from django.http import HttpResponse
from rest_framework.decorators import api_view


@api_view(['GET'])
def get_location_details(request, google_key, file_out=None, file_in=r'C:\Users\rachagan\Desktop\aditeck\MapIdentify\locateMe\test.xlsx'):
    '''
        Process input location details file and return excel file path,
        which contain corordinates details
    :param request:
    :param file_name_xls:
    :return:
    '''
    try:
        GOOGLE_MAPS_API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'
        params={}
        params['address'] = 'Benguluru'
        params['key'] = google_key

        # validate input file
        if os.path.exists(file_in) != True:
            logging.info("Error, input file not exists")
            return HttpResponse(content="file not exists",status=400)

        if (file_out is None) or (os.path.exists(file_out) != True):
            logging.info("file not exists to write output, creating temp file")
            file_out = os.path.join(os.getcwd(), 'locatio_details.xlsx')

        writer = pd.ExcelWriter(file_out)
        if writer is None:
            logging.error("Error in writing to output file[%s]" % (file_out))
            return HttpResponse(status=400, content="Outfile issues")

        # Read data from input file
        df = pd.DataFrame()
        in_xlsx = pd.ExcelFile(file_in)
        if in_xlsx is None:
            logging.error("Error, check input file [%s]" %(file_in))
            return HttpResponse(status=400, content="input file issues")

        location_sheets = []
        for sheet in in_xlsx.sheet_names:
            location_sheets.append(in_xlsx.parse(sheet))
        data_frames = pd.concat(location_sheets)

        if (data_frames is None) or (len(data_frames) == 0):
            logging.info("No records in input file")
            return HttpResponse(content="Empty file", status=200)

        for index, row in data_frames.iterrows():
            params['address'] = row['Address']

            response = requests.get(GOOGLE_MAPS_API_URL, params=params)

            if response.status_code != 200:
                logging.debug("Request to google failed [%s]" %(response.status_code))
                return HttpResponse(status=response.status_code)

            result = response.json()['results'][0]

            geodata = dict()
            geodata['lat'] = result['geometry']['location']['lat']
            geodata['lng'] = result['geometry']['location']['lng']
            geodata['address'] = result['formatted_address']

            df = pd.DataFrame.from_dict(geodata)
            df.to_excel(writer, 'Sheet1')

        writer.save()
        return HttpResponse(status=200, content=str(file_out) + " contains results")

    except Exception as e:
        logging.error("Error in processing request [%s]" %(e))
        return HttpResponse(status=500)


@api_view(['GET'])
def get_corordinates(request, google_key, file_out=None, file_in=r'C:\Users\rachagan\Desktop\aditeck\MapIdentify\locateMe\test.xlsx'):
    '''
        Process input location details file and return excel file path,
        which contain corordinates details
    :param request:
    :param file_name_xls:
    :return:
    '''
    try:
        googlemaps_key = googlemaps.Client(key=google_key)

        # validate input file
        if os.path.exists(file_in) != True:
            logging.info("Error, input file not exists")
            return HttpResponse(content="file not exists",status=400)

        if (file_out is None) or (os.path.exists(file_out) != True):
            logging.info("file not exists to write output, creating temp file")
            file_out = os.path.join(os.getcwd(), 'locatio_details.xlsx')

        writer = pd.ExcelWriter(file_out)
        if writer is None:
            logging.error("Error in writing to output file[%s]" % (file_out))
            return HttpResponse(status=400, content="Outfile issues")

        # Read data from input file
        df = pd.DataFrame()
        in_xlsx = pd.ExcelFile(file_in)
        if in_xlsx is None:
            logging.error("Error, check input file [%s]" %(file_in))
            return HttpResponse(status=400, content="input file issues")

        location_sheets = []
        for sheet in in_xlsx.sheet_names:
            location_sheets.append(in_xlsx.parse(sheet))
        data_frames = pd.concat(location_sheets)

        if (data_frames is None) or (len(data_frames) == 0):
            logging.info("No records in input file")
            return HttpResponse(content="Empty file", status=200)

        for index, row in data_frames.iterrows():
            address = row['Address']

            response = googlemaps_key.geocode(address)
            result = response['result'][0]

            if response["status"] != "OK":
                logging.debug("Request to google failed [%s]" %(response["status"]))
                return HttpResponse(status=500, content=response["status"])

            geodata = dict()
            geodata['lat'] = result['geometry']['location']['lat']
            geodata['lng'] = result['geometry']['location']['lng']
            geodata['address'] = result['formatted_address']

            df = pd.DataFrame.from_dict(geodata)
            df.to_excel(writer, 'Sheet1')

        writer.save()
        return HttpResponse(status=200, content=str(file_out) + " contains results")

    except Exception as e:
        logging.error("Error in processing request [%s]" %(e))
        return HttpResponse(status=500)


