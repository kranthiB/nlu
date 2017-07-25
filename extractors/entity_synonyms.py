from nlu.extractors import EntityExtractor

import os
import io
import json
import six

class EntitySynonymMapper(EntityExtractor):
    name = "ner_synonyms"

    provides = ["entities"]

    def __init__(self, synonyms=None):
        self.synonyms = synonyms if synonyms else {}
        
    def process(self, message, **kwargs):
    	updated_entities = message.get("entities", [])[:]
    	self.replace_synonyms(updated_entities)
    	message.set("entities", updated_entities, add_to_output=True)
    	
    def replace_synonyms(self, entities):
    	for entity in entities:
    		entity_value = entity["value"]
    		if entity_value.lower() in self.synonyms:
    			entity["value"] = self.synonyms[entity_value.lower()]
    			self.add_processor_name(entity)
    			
    @classmethod
    def load(cls, model_dir, model_metadata, cached_component, **kwargs):
    	if model_dir and model_metadata.get("entity_synonyms"):
    		entity_synonyms_file = os.path.join(model_dir, model_metadata.get("entity_synonyms"))
    		if os.path.isfile(entity_synonyms_file):
    			with io.open(entity_synonyms_file, encoding='utf-8') as f:
    				synonyms = json.loads(f.read())
    			return EntitySynonymMapper(synonyms)
    		else:
    			warnings.warn("Failed to load synonyms file from '{}'".format(entity_synonyms_file))
    	return EntitySynonymMapper()
    	
    def add_entities_if_synonyms(self, entity_a, entity_b):
    	if entity_b is not None:
    		original = entity_a if isinstance(entity_a, six.text_type) else six.text_type(entity_a)
    		original = original.lower()
    		replacement = entity_b if isinstance(entity_b, six.text_type) else six.text_type(entity_b)
    		if original != replacement:
    			self.synonyms[original] = replacement
    
    def train(self, training_data, config, **kwargs):
    	for key, value in list(training_data.entity_synonyms.items()):
    		self.add_entities_if_synonyms(key, value)
    	for example in training_data.entity_examples:
    		for entity in example.get("entities", []):
    			entity_val = example.text[entity["start"]:entity["end"]]
    			self.add_entities_if_synonyms(entity_val, entity.get("value"))
    			
    def persist(self, model_dir):
    	if self.synonyms:
    		entity_synonyms_file = os.path.join(model_dir, "entity_synonyms.json")
    		with io.open(entity_synonyms_file, 'w') as f:
    			f.write(str(json.dumps(self.synonyms)))
    		return {"entity_synonyms": "entity_synonyms.json"}
    	else:
    		return {"entity_synonyms": None}