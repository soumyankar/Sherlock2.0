import re
import urllib.request, urllib.error

def  URLValidator(url):
	if URLMalformity(url) == True and URLReachable(url) == 200:
		return True
	return False

def URLMalformity(url):
	regex = re.compile(
	        r'^(?:http|ftp)s?://' # http:// or https://
	        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
	        r'localhost|' #localhost...
	        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
	        r'(?::\d+)?' # optional port
	        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	return (re.match(regex, url) is not None)
	# print(re.match(regex, "http://www.example.com") is not None) # True
	# print(re.match(regex, "example.com") is not None)            # False

def URLReachable(url):
	try:
		conn = urllib.request.urlopen(url)
	except (urllib.error.HTTPError) as e:
		return (format(e.code))
	except (urllib.error.URLError) as e:
		return (format(e.reason))
	else:
		return (urllib.request.urlopen(url).getcode())
	return False