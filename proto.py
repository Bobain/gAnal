import argparse

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
KEY_FILE_LOCATION = './ulule.p12'
SERVICE_ACCOUNT_EMAIL = '901681681616-p3h8ciugv6l057g4r2v6j9cbpld8u3fb@developer.gserviceaccount.com'
VIEW_ID = '30518954' # '86954238'


def initialize_analyticsreporting():
  """Initializes an analyticsreporting service object.

  Returns:
    analytics an authorized analyticsreporting service object.
  """

  credentials = ServiceAccountCredentials.from_p12_keyfile(
    SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION, scopes=SCOPES)

  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)

  return analytics


def get_report(analytics):
  # Use the Analytics Service Object to query the Analytics Reporting API V4.
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:sessions'}]
        }]
      }
  ).execute()


def print_response(response):
  """Parses and prints the Analytics Reporting API V4 response"""

  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    rows = report.get('data', {}).get('rows', [])

    for row in rows:
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        print header + ': ' + dimension

      for i, values in enumerate(dateRangeValues):
        print 'Date range (' + str(i) + ')'
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          print metricHeader.get('name') + ': ' + value


def get_my_report(analytics):
  # Use the Analytics Service Object to query the Analytics Reporting API V4.
  return analytics.reports().batchGet(
      body=get_request_for_page_views()
  ).execute()

def get_request_for_page_views():
    return {
        'reportRequests': [
        {
          'viewId': VIEW_ID,
            # 'samplingLevel': 'HIGHER_PRECISION',
            'pageSize': 10,
          'dateRanges': [{'startDate': "2016-04-18", 'endDate': "2016-05-18"}],
            'metrics': [{'expression': 'ga:uniquepageviews'}], # , {'expression': 'ga:pageviews'}
            'dimensions': [{'name': 'ga:pagePath'}],
            'orderBys': [{"fieldName": "ga:uniquepageviews", 'sortOrder': 'DESCENDING'}]
        }]
      }

def main():

    analytics = initialize_analyticsreporting()
    # response = get_report(analytics)
    response = get_my_report(analytics)
    print_response(response)

if __name__ == '__main__':
  main()
