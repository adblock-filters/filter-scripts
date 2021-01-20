 # see: https://github.com/MajkiIT/polish-ads-filter/issues

 # curl -i -H "Accept: application/json" -H "Content-Type: application/json" https://api.github.com/repos/MajkiIT/polish-ads-filter/issues?labels=reklama&state=all&page=1

 # LIMIT: 60 reuest per hour

import requests, json

data = []

START 			= 31
NUM_OF_PAGES 	= 10
extract_name 	= 'title' # check: https://developer.github.com/v3/issues/#list-repository-issues
label 			= 'reklama'  
state	 		= 'all' # closed / open / all
baseurl			= 'https://api.github.com/repos/MajkiIT/polish-ads-filter/issues'


def query(url, extract):
	headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
	response = requests.get(url, headers=headers)
	issues = json.loads(response.text)

	for issue in issues:
		data.append(issue[extract])


def make_requests(start, pages):
	for page in range(start, start+pages):
		p = str(page+1)
		url = f'{baseurl}?labels={label}&state={state}&page={p}'
		print(' :query:\t', url)
		query(url, extract_name)


def main():
	print(' :start:')
	make_requests(START, NUM_OF_PAGES)
	print(' :end:')
	print('\n')

	for i in data: print(i)


if __name__ == "__main__":
    main()