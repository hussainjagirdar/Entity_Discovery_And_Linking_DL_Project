from bs4 import BeautifulSoup as BS
import sys
import io
import os
import pickle
import shutil

reload(sys)
sys.setdefaultencoding("utf-8")

em_dict = {}

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def get_entity_dict(file):
	fd = io.open(ERE_data_path+file,"r",encoding='utf-8')
	xml_file = fd.read()

	xml_soup = BS(xml_file, 'xml')
	# print xml_soup
	
	entity_dict = {}
	# print len(xml_soup.find_all('entity'))
	for entity in xml_soup.find_all('entity'):
		entity_id = entity.get("id")
		entity_type = entity.get("type")
		entity_specificity = entity.get("specificity")
		# print entity_id, entity_type, entity_specificity
		# if entity_id not in entity_dict:
		# 	entity_dict[entity_id] = {'entity_type': entity_type, 'entity_specificity': entity_specificity, 'mention_dict':{} }
		# print entity_dict['ent-8']['entity_type']
		# break
		entity_mention_list = entity.find_all('entity_mention')
		for entity_mention in entity_mention_list:
			entity_mention_id = entity_mention.get("id")
			entity_mention_noun_type = entity_mention.get("noun_type")
			entity_mention_offset = int(entity_mention.get("offset"))
			entity_mention_length = int(entity_mention.get("length"))
			entity_mention_text = entity_mention.find("mention_text").get_text()
			# if entity_mention_id not in entity_dict[entity_id]['mention_dict']:
			# 	entity_dict[entity_id]['mention_dict'][entity_mention_id] = {'entity_mention_noun_type':entity_mention_noun_type, 'entity_mention_offset': entity_mention_offset, 'entity_mention_length':entity_mention_length, 'entity_mention_text':entity_mention_text}
			if len(entity_mention_text.split(" "))>1:
				text_list = entity_mention_text.split(" ")
				for text in text_list:
					if text.lower() not in em_dict:
						em_dict[text.lower()] = [entity_type]
					else:
						if entity_type not in em_dict[text.lower()]:
							em_dict[text.lower()].append(entity_type)
						# if em_dict[text.lower()] != entity_type:
						# 	print "found missmatch for",text.lower(),em_dict[text.lower()],entity_type
				pass
			else:
				if entity_mention_text.lower() not in em_dict:
					em_dict[entity_mention_text.lower()] = [entity_type]
				else:
					if entity_type not in em_dict[entity_mention_text.lower()]:
						em_dict[entity_mention_text.lower()].append(entity_type)
				pass
	# print len(entity_dict.keys())
	fd.close()
	return entity_dict

ERE_data_path = "../dataset/ere/"
ERE_dict_path = "../ere_dict_new/"
if os.path.exists(ERE_data_path):
	if os.path.exists(ERE_dict_path):
		# shutil.rmtree(ERE_dict_path)
		# os.makedirs(ERE_dict_path)
		pass
	else:
		os.makedirs(ERE_dict_path)
else:
	print "ERE Data not found"
	exit(0)

file_list = os.listdir(ERE_data_path)
for file in file_list:
	entity_dict = get_entity_dict(file)
save_obj(em_dict, ERE_dict_path+"_entity_dict_seperate")
print "Entity Dictionary Saved"
for em in em_dict:
	print em, ":",em_dict[em]




