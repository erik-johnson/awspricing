import urllib 
import json
import awspricing.mapper
from awspricing.base import Base

class Ebs(Base):
    """ Class for EBS pricing. """
    def __init__(self):
        Base.__init__(self)
        self.json_data = self.get_json("http://a0.awsstatic.com/pricing/1/ebs/pricing-ebs.min.js")
        self.currency = self.json_data['config']['currencies'][0]
        self.rate = self.json_data['config']['rate']

    def getSQL(self):
        """ Returns a list of SQL statements.

        :returns: a list of SQL statemnets that contains pricing data.
        :rtype: list
        """
        queries = []
        volume_product_id = self.start_id
        pricing_threshold = 0
        name="EBS Storage"
        description="Storage costs for an allocated EBS volume."
        for region in self.json_data['config']['regions']:
            region_id = awspricing.mapper.getRegionID(region['region'])
            if region_id == 'us-gov-west-1':
                continue
            for ebs_type in region['types']:
                if ebs_type['name'] == 'Amazon EBS Magnetic volumes':
                    provider_volume_product_id = 'standard'
                    max_iops = "NULL"
                    min_iops = "NULL"
                    iops_cost = float(ebs_type['values'][1]['prices'][self.currency])
                elif ebs_type['name'] == 'Amazon EBS General Purpose (SSD) volumes':
                    provider_volume_product_id = 'gp2'
                    max_iops = 3000
                    min_iops = 3000
                    iops_cost = "NULL"
                elif ebs_type['name'] == 'Amazon EBS Provisioned IOPS (SSD) volumes':
                    provider_volume_product_id = 'io1'
                    max_iops = 4000
                    min_iops = 100
                    iops_cost = float(ebs_type['values'][1]['prices'][self.currency])
                elif ebs_type['name'] == 'ebsSnapsToS3':
                    continue
                pricing = float(ebs_type['values'][0]['prices'][self.currency])
                query = "INSERT INTO volume_product (volume_product_id, cloud_id, provider_region_id, " \
                        "provider_volume_product_id, active, currency, name, description, pricing_threshold, " \
                        "volume_pricing, iops_cost, max_iops, min_iops)" \
                        "VALUES(%i, %i, '%s', '%s', '%s', '%s', '%s', '%s', %i, %.3f, %s, %s, %s);" %\
                        (volume_product_id, self.cloud_id, region_id, provider_volume_product_id, 'Y',
                         self.currency, name, description, pricing_threshold, pricing, iops_cost, max_iops, min_iops)
                queries.append(query)
                volume_product_id = volume_product_id + 1

        return queries

    def getCSV(self):
        """ Returns a list of CSV.

        Keyword arguments:

        :returns: a list of CSV that contains pricing data.
        :rtype: list
        """
        csv = []
        csv.append("RegionID, Storage Type, Currency, Pricing, Rate")
        for region in self.json_data['config']['regions']:
            region_id = awspricing.mapper.getRegionID(region['region'])
            for ebs_type in region['types']:
                try:
                    pricing = "%.3f" % float(ebs_type['values'][0]['prices'][self.currency])
                except ValueError:
                    pricing = "N/A"
                row = "%s, %s, %s, %s, %s" % (region_id, ebs_type['name'], self.currency, pricing, self.rate)
                csv.append(row)

        return csv
