import urllib 
import json
import awspricing.mapper
from awspricing.base import Base
from pprint import pprint

class Rds(Base):
    """ Class for RDBMS pricing. """
    def __init__(self):
        Base.__init__(self)
        rds_pricing_js = {
            "mysql_std": "http://a0.awsstatic.com/pricing/1/rds/mysql/pricing-standard-deployments.min.js",
            "mysql_std_previous": "http://a0.awsstatic.com/pricing/1/rds/mysql/previous-generation/pricing-standard-deployments.min.js",
            "postgresql_std": "http://a0.awsstatic.com/pricing/1/rds/postgresql/pricing-standard-deployments.min.js",
            "postgresql_std_previous": "http://a0.awsstatic.com/pricing/1/rds/postgresql/previous-generation/pricing-standard-deployments.min.js",
            "oracle_std": "http://a0.awsstatic.com/pricing/1/rds/oracle/pricing-li-standard-deployments.min.js",
            "oracle_std_previous": "http://a0.awsstatic.com/pricing/1/rds/oracle/previous-generation/pricing-li-standard-deployments.min.js",
            "oracle_byol": "http://a0.awsstatic.com/pricing/1/rds/oracle/pricing-byol-standard-deployments.min.js",
            "oracle_byol_previous": "http://a0.awsstatic.com/pricing/1/rds/oracle/previous-generation/pricing-byol-standard-deployments.min.js",
            "mssql_ex_std": "http://a0.awsstatic.com/pricing/1/rds/sqlserver/sqlserver-li-ex-ondemand.min.js",
            "mssql_ex_std_previous": "http://a0.awsstatic.com/pricing/1/rds/sqlserver/previous-generation/sqlserver-li-ex-ondemand.min.js",
            "mssql_web_std": "http://a0.awsstatic.com/pricing/1/rds/sqlserver/sqlserver-li-web-ondemand.min.js",
            "mssql_web_std_previous": "http://a0.awsstatic.com/pricing/1/rds/sqlserver/previous-generation/sqlserver-li-web-ondemand.min.js",
            "mssql_se_std": "http://a0.awsstatic.com/pricing/1/rds/sqlserver/sqlserver-li-se-ondemand.min.js",
            "mssql_se_std_previous": "http://a0.awsstatic.com/pricing/1/rds/sqlserver/previous-generation/sqlserver-li-se-ondemand.min.js",
            "mssql_byol": "http://a0.awsstatic.com/pricing/1/rds/sqlserver/sqlserver-byol-ondemand.min.js",
            "mssql_byol_previous": "http://a0.awsstatic.com/pricing/1/rds/sqlserver/previous-generation/sqlserver-byol-ondemand.min.js"
        }
        self.byol_licences = "oracle_byol"
        self.io_json = self.get_json("http://a0.awsstatic.com/pricing/1/rds/oracle/pricing-provisioned-db-standard-deploy.min.js")
        self.rds_json = dict()
        for pricing_type in rds_pricing_js:
            self.rds_json[pricing_type] = self.get_json(rds_pricing_js[pricing_type])

#        self.rds_json = {
#            'mysql_std': json.loads(urllib.urlopen("http://aws.amazon.com/rds/pricing/mysql/pricing-standard-deployments.json").read()),
#            'oracle_std': json.loads(urllib.urlopen("http://aws.amazon.com/rds/pricing/oracle/pricing-li-standard-deployments.json").read()),
#            'oracle_byol': json.loads(urllib.urlopen("http://aws.amazon.com/rds/pricing/oracle/pricing-byol-standard-deployments.json").read()),
#            'mssql_std': json.loads(urllib.urlopen("http://aws.amazon.com/rds/pricing/sqlserver/sqlserver-li-se-ondemand.json").read())
#        }
        self.rds_dbengine = {
            'mysql_std': ['MYSQL'],
            'mysql_std_previous': ['MYSQL'],
            'postgresql_std': ['POSTGRES'],
            'postgresql_std_previous': ['POSTGRES'],
            'oracle_std': ['ORACLE_SE1'],
            'oracle_std_previous': ['ORACLE_SE1'],
            'oracle_byol': ['ORACLE_EE', 'ORACLE_SE', 'ORACLE_SE1'],
            'oracle_byol_previous': ['ORACLE_EE', 'ORACLE_SE', 'ORACLE_SE1'],
            'mssql_ex_std': ['SQLSERVER_EX'],
            'mssql_ex_std_previous': ['SQLSERVER_EX'],
            'mssql_web_std': ['SQLSERVER_WEB'],
            'mssql_web_std_previous': ['SQLSERVER_WEB'],
            'mssql_se_std': ['SQLSERVER_SE'],
            'mssql_se_std_previous': ['SQLSERVER_SE'],
            'mssql_byol': ['SQLSERVER_SE', 'SQLSERVER_EE'],
            'mssql_byol_previous': ['SQLSERVER_SE', 'SQLSERVER_EE']
        }
        self.minimum_storage = {
            'MYSQL': 5,
            'POSTGRES': 5,
            'ORACLE_SE1': 10,
            'ORACLE_SE': 10,
            'ORACLE_EE': 10,
            'SQLSERVER_WEB': 20,
            'SQLSERVER_EX': 20,
            'SQLSERVER_SE': 200,
            'SQLSERVER_EE': 200,
        }
        self.maximum_storage = {
            'MYSQL': 3072,
            'POSTGRES': 3072,
            'ORACLE_SE1': 3072,
            'ORACLE_SE': 3072,
            'ORACLE_EE': 3072,
            'SQLSERVER_WEB': 1024,
            'SQLSERVER_EX': 1024,
            'SQLSERVER_SE': 1024,
            'SQLSERVER_EE': 1024,
        }
        self.license = {
            'mysql_std': 'GENERAL_PUBLIC_LICENSE',
            'mysql_std_previous': 'GENERAL_PUBLIC_LICENSE',
            'postgresql_std': 'POSTGRESQL_LICENSE',
            'postgresql_std_previous': 'POSTGRESQL_LICENSE',
            'oracle_std': 'LICENSE_INCLUDED',
            'oracle_std_previous': 'LICENSE_INCLUDED',
            'oracle_byol': 'BRING_YOUR_OWN_LICENSE',
            'oracle_byol_previous': 'BRING_YOUR_OWN_LICENSE',
            'mssql_se_std': 'LICENSE_INCLUDED',
            'mssql_se_std_previous': 'LICENSE_INCLUDED',
            'mssql_ex_std': 'LICENSE_INCLUDED',
            'mssql_ex_std_previous': 'LICENSE_INCLUDED',
            'mssql_web_std': 'LICENSE_INCLUDED',
            'mssql_web_std_previous': 'LICENSE_INCLUDED',
            'mssql_byol': 'BRING_YOUR_OWN_LICENSE',
            'mssql_byol_previous': 'BRING_YOUR_OWN_LICENSE',
        }

#        self.io_json = json.loads(urllib.urlopen("http://aws.amazon.com/rds/pricing/pricing-provisioned-db-standard-deploy.json").read())
        self.currency = self.rds_json['mysql_std']['config']['currencies'][0]

    def getSQL(self):
        """ Returns a list of SQL statements.

        :returns: a list of SQL statemnets that contains pricing data.
        :rtype: list
        """
        queries = []
        std_storage_rate = dict()
        std_io_rate = dict()
        rdbms_product_id = self.start_id
        for region in self.io_json['config']['regions']:
            region_id = awspricing.mapper.getRegionID(region['region'])
            for rate in region['rates']:
                if rate['type'] == 'ioRate':
                    std_io_rate[region_id] = rate['prices'][self.currency]
                elif rate['type'] == 'storageRate':
                    std_storage_rate[region_id] = rate['prices'][self.currency]
        for pricing_type in self.rds_json:
            for region in self.rds_json[pricing_type]['config']['regions']:
                region_id = awspricing.mapper.getRegionID(region['region'])
                for type in region['types']:
                    for tier in type['tiers']:
                        rds_name = "%s" % (tier['name'])
                        rds_spec = awspricing.mapper.getRdsSpec(rds_name)
                        product_size = rds_spec['product_size']
                        name = rds_spec['name']
                        core_count = rds_spec['core_count']
                        cpu_power = rds_spec['cpu_power']
                        memory_in_gb = rds_spec['memory_in_gb']
                        io_units = 1000000
                        description = "64-bit, %s GB RAM, %s x %s GHz CPU Core" %\
                                      (memory_in_gb, core_count, cpu_power)
                        license = self.license[pricing_type]
                        try:
                            pricing = "%.3f" % float(tier['prices'][self.currency])
                        except ValueError:
                            pricing = "0"
                        for dbengine in self.rds_dbengine[pricing_type]:
                            maximum_storage_in_gb = self.maximum_storage[dbengine]
                            minimum_storage_in_gb = self.minimum_storage[dbengine]

                            query = "INSERT INTO rdbms_product VALUES(%i, %i, '%s', '%s', '%s', '%s', %i, %s, '%s', %i, %i, %s, %i, '%s', '%s', '%s', %s, %s, %s, %i, '%s');" %\
                                     (rdbms_product_id, self.cloud_id, region_id, dbengine, 'Y', 'I64',
                                      core_count, cpu_power, description, io_units, maximum_storage_in_gb,
                                      memory_in_gb, minimum_storage_in_gb, name, product_size, self.currency,
                                      pricing, std_io_rate[region_id], std_storage_rate[region_id], 1, license)
                            queries.append(query)
                            rdbms_product_id = rdbms_product_id + 1

        return queries

    def getCSV(self):
        """ Returns a list of CSV.

        :returns: a list of CSV that contains pricing data.
        :rtype: list
        """
        csv = []
        std_storage_rate = dict()
        std_io_rate = dict()
        csv.append("Product Size, DB engine, Region ID, Currency, Pricing, I/O Rate, Storage Rate")
        #for region in self.io_json['config']['regions']:
            #region_id = awspricing.mapper.getRegionID(region['region'])
            #pprint(region)
            #for rate in region['prices']:
                #if rate['type'] == 'ioRate':
                    #std_io_rate[region_id] = rate['prices'][self.currency]
                #elif rate['type'] == 'storageRate':
                    #std_storage_rate[region_id] = rate['prices'][self.currency]
        for pricing_type in self.rds_json:
            for region in self.rds_json[pricing_type]['config']['regions']:
                region_id = awspricing.mapper.getRegionID(region['region'])
                for type in region['types']:
                    for tier in type['tiers']:
                        rds_name = "%s.%s" % (type['name'],tier['name'])
#                        rds_spec = awspricing.mapper.getRdsSpec(rds_name)
                        #product_size = rds_spec['product_size']
                        try:
                            pricing = "%.3f" % float(tier['prices'][self.currency])
                        except ValueError:
                            pricing = "0"
                        row = "%s, %s, %s, %s, %s, %s, %s" % (product_size, pricing_type, region_id,
                                                              self.currency, pricing, std_io_rate[region_id],
                                                              std_storage_rate[region_id])
                        csv.append(row)
        return csv

def strip_jsonp(jsonp):
    print jsonp
    json = jsonp[jsonp.index("(") + 1 : jsonp.rindex(")")]
    print json
    return json
