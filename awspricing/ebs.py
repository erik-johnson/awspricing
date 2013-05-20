import urllib 
import json
import awspricing.mapper
from awspricing.base import Base

class Ebs(Base):
    def __init__(self):
        Base.__init__(self)
        self.json_data = json.loads(urllib.urlopen("http://aws.amazon.com/ec2/pricing/pricing-ebs.json").read())
        self.currency = self.json_data['config']['currencies'][0]
        self.rate = self.json_data['config']['rate']

    def getSQL(self):
        queries = []
        volume_product_id = self.start_id
        pricing_threshold = 0
        name="EBS Storage"
        description="Storage costs for an allocated EBS volume."
        for region in self.json_data['config']['regions']:
            region_id = awspricing.mapper.getRegionID(region['region'])
            for ebs_type in region['types']:
                if ebs_type['name'] == 'ebsVols':
                    pricing = float(ebs_type['values'][0]['prices'][self.currency])
                    query = "INSERT INTO volume_product VALUES(%i, %i, '%s', '%s', '%s', '%s', '%s', '%s', %i, %.3f);" %\
                            (volume_product_id, self.cloud_id, region_id, 'standard', 'Y',
                             self.currency, name, description, pricing_threshold, pricing)
                    queries.append(query)
                    volume_product_id = volume_product_id + 1

        return queries

    def getCSV(self, selected_type='ebsVols'):
        csv = []
        name="EBS Storage"
        csv.append("RegionID, Storage Type, Currency, Pricing, Rate")
        for region in self.json_data['config']['regions']:
            region_id = awspricing.mapper.getRegionID(region['region'])
            for ebs_type in region['types']:
                if ebs_type['name'] == selected_type:
                    try:
                        pricing = "%.3f" % float(ebs_type['values'][0]['prices'][self.currency])
                    except ValueError:
                        pricing = "N/A"
                    row = "%s, %s, %s, %s, %s" % (region_id, name, self.currency, pricing, self.rate)
                    csv.append(row)

        return csv
