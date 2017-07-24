from pkrm_nlu.featurizers import Featurizer

import re
import os
import io
import json

class RegexFeaturizer(Featurizer):
    name = "intent_entity_featurizer_regex"

    provides = ["text_features"]

    requires = ["tokens"]
    
    def __init__(self, known_patterns=None):
    	self.known_patterns = known_patterns if known_patterns else []
    
    def process(self, message, **kwargs):
    	updated = self._text_features_with_regex(message)
    	message.set("text_features", updated)
    	
    def _text_features_with_regex(self, message):
    	if self.known_patterns is not None:
    		extras = self.features_for_patterns(message)
    		return self._combine_with_existing_text_features(message, extras)
    	else:
    		return message.get("text_features")
    		
    def features_for_patterns(self, message):
    	import numpy as np
    	found = []
    	for i, exp in enumerate(self.known_patterns):
    		match = re.search(exp["pattern"], message.text)
    		if match is not None:
    			for t in message.get("tokens", []):
    				if t.offset < match.end() and t.end > match.start():
    					t.set("pattern", i)
    			found.append(1.0)
    		else:
    			found.append(0.0)
    	return np.array(found)
    
    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):
    	if model_dir and model_metadata.get("regex_featurizer"):
    		regex_file = os.path.join(model_dir, model_metadata.get("regex_featurizer"))
    		if os.path.isfile(regex_file):
    			with io.open(regex_file, encoding='utf-8') as f:
    				known_patterns = json.loads(f.read())
    			return RegexFeaturizer(known_patterns)
    		else:
    			warnings.warn("Failed to load regex pattern file '{}'".format(regex_file))
    	return RegexFeaturizer()
    	
    def train(self, training_data, config, **kwargs):
    	for example in training_data.regex_features:
    		self.known_patterns.append(example)
    	for example in training_data.training_examples:
    		updated = self._text_features_with_regex(example)
    		example.set("text_features", updated)
    		
    def persist(self, model_dir):
    	if self.known_patterns:
    		regex_file = os.path.join(model_dir, "regex_featurizer.json")
    		with io.open(regex_file, 'w') as f:
    			f.write(str(json.dumps(self.known_patterns, indent=4)))
    		return {"regex_featurizer": "regex_featurizer.json"}
    	else:
    		return {"regex_featurizer": None}