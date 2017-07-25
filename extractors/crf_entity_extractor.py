from nlu.extractors import EntityExtractor

import logging
import os

logger = logging.getLogger(__name__)

class CRFEntityExtractor(EntityExtractor):
    name = "ner_crf"

    provides = ["entities"]

    requires = ["spacy_doc", "tokens"]

    function_dict = {
        'low': lambda doc: doc[0].lower(),
        'title': lambda doc: doc[0].istitle(),
        'word3': lambda doc: doc[0][-3:],
        'word2': lambda doc: doc[0][-2:],
        'pos': lambda doc: doc[1],
        'pos2': lambda doc: doc[1][:2],
        'bias': lambda doc: 'bias',
        'upper': lambda doc: doc[0].isupper(),
        'digit': lambda doc: doc[0].isdigit(),
        'pattern': lambda doc: str(doc[3]) if doc[3] is not None else 'N/A',
    }
    
    def __init__(self, ent_tagger=None, entity_crf_features=None, entity_crf_BILOU_flag=True):
    
        self.ent_tagger = ent_tagger
        self.BILOU_flag = entity_crf_BILOU_flag

        if not entity_crf_features:
            self.crf_features = [
                ['low', 'title', 'upper', 'pos', 'pos2'],
                ['bias', 'low', 'word3', 'word2', 'upper', 'title', 'digit', 'pos', 'pos2', 'pattern'],
                ['low', 'title', 'upper', 'pos', 'pos2']
            ]
        else:
            self.crf_features = entity_crf_features
            
    def process(self, message, **kwargs):
    	extracted = self.add_extractor_name(self.extract_entities(message))
    	message.set("entities", message.get("entities", []) + extracted, add_to_output=True)
    	
    def extract_entities(self, message):
    	if self.ent_tagger is not None:
    		text_data = self._from_text_to_crf(message)
    		features = self._sentence_to_features(text_data)
    		ents = self.ent_tagger.predict_single(features)
    		return self._from_crf_to_json(message, ents)
    	else:
    		return []
    		
    def _from_text_to_crf(self, message, entities=None):
    	crf_format = []
    	for i, token in enumerate(message.get("spacy_doc")):
    		pattern = self.__pattern_of_token(message, i)
    		entity = entities[i] if entities else "N/A"
    		crf_format.append((token.text, token.tag_, entity, pattern))
    	return crf_format
    	
    def __pattern_of_token(self, message, i):
    	if message.get("tokens"):
    		return message.get("tokens")[i].get("pattern")
    	else:
    		return None
    
    def _sentence_to_features(self, sentence):
    	sentence_features = []
    	for word_idx in range(len(sentence)):
    		prefixes = ['-1', '0', '+1']
    		word_features = {}
    		for i in range(3):
    			if word_idx == len(sentence) - 1 and i == 2:
    				word_features['EOS'] = True
    			elif word_idx == 0 and i == 0:
    				word_features['BOS'] = True
    			else:
    				word = sentence[word_idx - 1 + i]
    				prefix = prefixes[i]
    				features = self.crf_features[i]
    				for feature in features:
    					word_features[prefix + ":" + feature] = self.function_dict[feature](word)
    		sentence_features.append(word_features)
    	return sentence_features
    	
    def _from_crf_to_json(self, message, entities):
    	sentence_doc = message.get("spacy_doc")
    	json_ents = []
    	if len(sentence_doc) != len(entities):
    		raise Exception('Inconsistency in amount of tokens between crfsuite and spacy')
    	if self.BILOU_flag:
    		for word_idx in range(len(sentence_doc)):
    			entity = entities[word_idx]
    			word = sentence_doc[word_idx]
    			if entity.startswith('U-'):
    				ent = {'start': word.idx, 'end': word.idx + len(word),
    						'value': word.text, 'entity': entity[2:]}
    				json_ents.append(ent)
    			elif entity.startswith('B-'):
    				ent_word_idx = word_idx + 1
    				finished = False
    				while not finished:
    					if len(entities) > ent_word_idx and entities[ent_word_idx][2:] != entity[2:]:
    						logger.debug(
    								"Inconsistent BILOU tagging found, B- tag, L- tag pair encloses multiple " +
    								"entity classes.i.e. ['B-a','I-b','L-a'] instead of ['B-a','I-a','L-a'].\n" +
    								"Assuming B- class is correct.")
    					if len(entities) > ent_word_idx and entities[ent_word_idx].startswith('L-'):
    						finished = True
    					elif len(entities) > ent_word_idx and entities[ent_word_idx].startswith('I-'):
    						ent_word_idx += 1
    					else:
    						finished = True	
    						ent_word_idx -= 1
    						logger.debug(
    								"Inconsistent BILOU tagging found, B- tag not closed by L- tag, " +
    								"i.e ['B-a','I-a','O'] instead of ['B-a','L-a','O'].\nAssuming last tag is L-")
    				ent = {'start': word.idx,
    						'end': sentence_doc[word_idx:ent_word_idx + 1].end_char,
    						'value': sentence_doc[word_idx:ent_word_idx + 1].text,
    						'entity': entity[2:]}
    				json_ents.append(ent)
    	elif not self.BILOU_flag:
    		for word_idx in range(len(sentence_doc)):
    			entity = entities[word_idx]
    			word = sentence_doc[word_idx]
    			if entity != 'O':
    				ent = {'start': word.idx,
    						'end': word.idx + len(word),
    						'value': word.text,
    						'entity': entity}
    				json_ents.append(ent)
    	return json_ents
    
    @classmethod
    def load(cls, model_dir, model_metadata, cached_component, **kwargs):
    	from sklearn.externals import joblib
    	
    	if model_dir and model_metadata.get("entity_extractor_crf"):
    		meta = model_metadata.get("entity_extractor_crf")
    		ent_tagger = joblib.load(os.path.join(model_dir, meta["model_file"]))
    		return CRFEntityExtractor(ent_tagger=ent_tagger,
    									entity_crf_features=meta['crf_features'],
    									entity_crf_BILOU_flag=meta['BILOU_flag'])
    	else:
    		return CRFEntityExtractor()
    		
    def _convert_example(self, example):
    	def convert_entity(ent):
    		return ent["start"], ent["end"], ent["entity"]
    	return [convert_entity(ent) for ent in example.get("entities", [])]
    	
    def _from_json_to_crf(self, message, entity_offsets):
    	from spacy.gold import GoldParse
    	doc = message.get("spacy_doc")
    	gold = GoldParse(doc, entities=entity_offsets)
    	ents = [l[5] for l in gold.orig_annot]
    	if '-' in ents:
    		logger.warn("Misaligned entity annotation in sentence '{}'. ".format(doc.text) +
    					"Make sure the start and end values of the annotated training " +
    					"examples end at token boundaries (e.g. don't include trailing whitespaces).")
    	if not self.BILOU_flag:
    		for i, entity in enumerate(ents):
    			if entity.startswith('B-') or \
    					entity.startswith('I-') or \
    					entity.startswith('U-') or \
    					entity.startswith('L-'):
    				ents[i] = entity[2:]
    				
    	return self._from_text_to_crf(message, ents)
    
    def _create_dataset(self, examples):
    	dataset = []
    	for example in examples:
    		entity_offsets = self._convert_example(example)
    		dataset.append(self._from_json_to_crf(example, entity_offsets))
    	return dataset
    	
    def _sentence_to_labels(self, sentence):
    	return [label for _, _, label, _ in sentence]
		
    def _train_model(self, df_train):
    	import sklearn_crfsuite
    	X_train = [self._sentence_to_features(sent) for sent in df_train]
    	y_train = [self._sentence_to_labels(sent) for sent in df_train]
    	self.ent_tagger = sklearn_crfsuite.CRF(
    			algorithm='lbfgs',
    			c1=1.0,
    			c2=1e-3,
    			max_iterations=50,
    			all_possible_transitions=True
    	)
    	self.ent_tagger.fit(X_train, y_train)
    		
    def train(self, training_data, config, **kwargs):
    	self.BILOU_flag = config["entity_crf_BILOU_flag"]
    	self.crf_features = config["entity_crf_features"]
    	if training_data.entity_examples:
    		dataset = self._create_dataset(training_data.entity_examples)
    		self._train_model(dataset)
    
    def persist(self, model_dir):
    	from sklearn.externals import joblib
    	if self.ent_tagger:
    		model_file_name = os.path.join(model_dir, "crf_model.pkl")
    		joblib.dump(self.ent_tagger, model_file_name)
    		return {"entity_extractor_crf": {"model_file": "crf_model.pkl",
    										"crf_features": self.crf_features,
    										"BILOU_flag": self.BILOU_flag,
    										"version": 1}}
    	else:
    		return {"entity_extractor_crf": None}