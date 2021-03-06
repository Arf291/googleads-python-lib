#!/usr/bin/env python
#
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This code example creates a new line item to serve to video content.

This feature is only available to DFP premium solution networks. To determine
which line items exist, run get_all_line_items.py. To determine which orders
exist, run get_all_orders.py. To create a video ad unit, run
create_video_ad_unit.py. To create criteria for categories, run
create_custom_targeting_keys_and_values.py.
"""


import datetime
import uuid

# Import appropriate modules from the client library.
from googleads import dfp
import pytz

# Set order that all created line item will belong to and the video ad unit id
# to target.
ORDER_ID = 'INSERT_ORDER_ID_HERE'
TARGETED_VIDEO_AD_UNIT_ID = 'INSERT_TARGETED_VIDEO_AD_UNIT_ID_HERE'

# Set the custom targeting value ID representing the metadata
# on the content to target. This would typically be from a key representing
# a "genre" and the value representing something like "comedy". The value
# must be from a key in a content metadata key hierarchy.
CONTENT_CUSTOM_TARGETING_VALUE_ID = (
    'INSERT_CONTENT_CUSTOM_TARGETING_VALUE_ID_HERE')


def main(client, order_id, targeted_video_ad_unit_id,
         content_custom_targeting_value_id):
  # Initialize appropriate service.
  line_item_service = client.GetService('LineItemService', version='v201802')

  end_datetime = datetime.datetime.now(tz=pytz.timezone('America/New_York'))
  end_datetime += datetime.timedelta(days=365)

  # Create line item object.
  line_item = {
      'name': 'Line item #%s' % uuid.uuid4(),
      'orderId': order_id,
      'targeting': {
          'contentTargeting': {
              'targetedContentMetadata': [
                  {'customTargetingValueIds': [
                      content_custom_targeting_value_id]}
              ]
          },
          'inventoryTargeting': {
              'targetedAdUnits': [{'adUnitId': targeted_video_ad_unit_id,
                                   'includeDescendants': 'true'}]
          },
          'videoPositionTargeting': {
              'targetedPositions': [
                  {
                      'videoPosition': {
                          'positionType': 'PREROLL'
                      }
                  }
              ]
          }
      },
      'creativePlaceholders': [
          {
              'size': {
                  'width': '400',
                  'height': '300'
              },
              'companions': [
                  {
                      'size': {
                          'width': '300',
                          'height': '250'
                      },
                  },
                  {
                      'size': {
                          'width': '728',
                          'height': '90'
                      },
                  }
              ]
          }
      ],
      'environmentType': 'VIDEO_PLAYER',
      'companionDeliveryOption': 'OPTIONAL',
      'startDateTimeType': 'IMMEDIATELY',
      'lineItemType': 'SPONSORSHIP',
      'endDateTime': end_datetime,
      'costType': 'CPM',
      'costPerUnit': {
          'currencyCode': 'USD',
          'microAmount': '2000000'
      },
      'primaryGoal': {
          'units': '50',
          'unitType': 'IMPRESSIONS',
          'goalType': 'DAILY'
      },
      'contractedUnitsBought': '100',
      'creativeRotationType': 'OPTIMIZED',
      'discountType': 'PERCENTAGE',
      'allowOverbook': 'true'
  }

  # Add line item.
  line_item = line_item_service.createLineItem(line_item)

  # Display results.
  print ('Video line item with id "%s", belonging to order id "%s", and '
         'named "%s" was created.' % (line_item['id'], line_item['orderId'],
                                      line_item['name']))

if __name__ == '__main__':
  # Initialize client object.
  dfp_client = dfp.DfpClient.LoadFromStorage()
  main(dfp_client, ORDER_ID, TARGETED_VIDEO_AD_UNIT_ID,
       CONTENT_CUSTOM_TARGETING_VALUE_ID)
