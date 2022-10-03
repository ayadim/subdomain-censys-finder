#!/usr/bin/env python3
""" 
    Author : ayadi mohammed
    Github account : ayadim
    script title : subdomain-censys-finder
    discription : this script get certificates records collected from censys search engine to extract subdomains


    How it works 
    1- you should have an API-key,api-secret for censys 
    2- install dependencies : pip install -r requirements.txt
    3- change api_id and api_secret variables values 
    4- python3 subdomain-censys-finder.py domain.com

 """
from censys.search import CensysCertificates
import sys



def getSubdomains(domainTarget,apiId,apiSecret):
  c = CensysCertificates(api_id=apiId,api_secret=apiSecret)
  domain=domainTarget
  certificate_query = 'parsed.names: %s' % domain
  fields = ["parsed.names"]
  subdomainsList =[]
  try:
    certificates_search_results = c.search(certificate_query, fields)#max_records=200 field can be added
    for item in certificates_search_results:
      #print(item["parsed.names"])
      subdomainsList.extend(item["parsed.names"])
      
    return set(subdomainsList)
  except censys.base.CensysUnauthorizedException:
    sys.stderr.write('[-] Your Censys credentials look invalid.\n')
    exit(1)
  except censys.base.CensysRateLimitExceededException:
    sys.stderr.write('[-] Looks like you exceeded your Censys account limits rate. Exiting\n')
    return set(subdomainsList)
  except censys.base.CensysException as e:
    # catch the Censys Base exception, example "only 1000 first results are available"
    sys.stderr.write('[-] Something bad happened, ' + repr(e))
    return set(subdomainsList)

def filter_subdomains(domain, subdomains):
	return [ subdomain for subdomain in subdomains if '*' not in subdomain and subdomain.endswith(domain) ]

if __name__ == "__main__":

  #Check if the input command is correct
  if len(sys.argv) != 2:
      print("python subdomain-censys-finder.py target.com")
      sys.exit(1)

  #API KEY       
  api_id="" #change here
  api_secret="" #change here

  #Start the script
  domain = sys.argv[1]
  subdomains = getSubdomains(domain,api_id,api_secret)
  subdomains = filter_subdomains(domain,subdomains)
  print("\n".join(subdomains))

