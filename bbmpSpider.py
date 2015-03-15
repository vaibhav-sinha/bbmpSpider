from webscraping import common, download, xpath
from lxml import html
import requests
import json


def scrape():
        urls = ['http://bbmp.gov.in/councillors-contact-details?p_p_id=councillors_WAR_councillorsportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-3&p_p_col_count=1&_councillors_WAR_councillorsportlet_keywords=&_councillors_WAR_councillorsportlet_advancedSearch=false&_councillors_WAR_councillorsportlet_andOperator=true&_councillors_WAR_councillorsportlet_resetCur=false&_councillors_WAR_councillorsportlet_delta=75',
	'http://bbmp.gov.in/councillors-contact-details?p_p_id=councillors_WAR_councillorsportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_councillors_WAR_councillorsportlet_delta=75&_councillors_WAR_councillorsportlet_keywords=&_councillors_WAR_councillorsportlet_advancedSearch=false&_councillors_WAR_councillorsportlet_andOperator=true&_councillors_WAR_councillorsportlet_resetCur=false&cur=2',
	'http://bbmp.gov.in/councillors-contact-details?p_p_id=councillors_WAR_councillorsportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_councillors_WAR_councillorsportlet_delta=75&_councillors_WAR_councillorsportlet_keywords=&_councillors_WAR_councillorsportlet_advancedSearch=false&_councillors_WAR_councillorsportlet_andOperator=true&_councillors_WAR_councillorsportlet_resetCur=false&cur=3'
                 ]
	party_url = 'http://www.mybengaluru.com/resources/2999-BBMP-ELection-List-Winning-Candidate.aspx'

	filename = 'bbmp_data.json'
	neta_list = []
	for url in urls:
		page = requests.get(url)
		raw = page.text
		tree = html.fromstring(raw)
		
		data = tree.xpath("//div[@class='aui-column-content  aui-column-content-last ']/text()")
		count = 0
		index = 0
		field = 0
		for j in data:
			if index%2 == 1:
				if field == 0:
					ward_number = j.strip()
				if field == 1:
					ward_name = j.strip()
				if field == 2:
					ward_area_sqkm = j.strip()
				if field == 3:
					ac_name = j.strip()
				if field == 4:
					name = j.strip()
				if field == 5:
					address = j.strip()
				if field == 6:
					phone = j.strip()
				field = field + 1
				photo = 'http://bbmp.gov.in/councillors-contact-details?p_p_id=councillors_WAR_councillorsportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=getimage&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_count=1&_councillors_WAR_councillorsportlet_action=serveResource&_councillors_WAR_councillorsportlet_filename='+str(count+1)+'.jpg&_councillors_WAR_councillorsportlet_keywords=&_councillors_WAR_councillorsportlet_resetCur=false&_councillors_WAR_councillorsportlet_cur=2&_councillors_WAR_councillorsportlet_advancedSearch=false&_councillors_WAR_councillorsportlet_andOperator=true&_councillors_WAR_councillorsportlet_delta=75'
			index = index + 1
			if index%14 == 0:
				neta = {'ward_number':ward_number, 'ward_name':ward_name, 'ward_area_sqkm':ward_area_sqkm, 'ac_name':ac_name, 'name': name, 'address':address, 'photo': photo, 'phone':phone}
				neta_list.append(neta)
				#print neta
				count = count + 1
				field = 0
		
	page = requests.get(party_url)
	raw = page.text
	tree = html.fromstring(raw)
	
	data = tree.xpath("//table[@class='tableizer-table']//tr//td/text()")
	for i in range(0, len(neta_list)):
		neta_list[i]['party'] = data[i*7 + 6]
	#print data
		
	#print neta_list
	print "Scrapped ", str(len(neta_list)), " records"
	with open(filename, 'w') as outfile:
		json.dump(neta_list,outfile)
	print filename+" Done!"

scrape()
