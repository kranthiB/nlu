import logging
import warnings
import os
import io
import json

from nlu.utils import lazyproperty, ordered, list_to_str
from itertools import groupby

logger = logging.getLogger(__name__)

class Message(object):
	
	def __init__(self, text, data=None, output_properties=None, time=None):
		self.text = text
		self.time = time
		self.data = data if data else {}
		self.output_properties = output_properties if output_properties else set()
		
	def set(self, prop, info, add_to_output=False):
		self.data[prop] = info
		if add_to_output:
			self.output_properties.add(prop)
		
	def get(self, prop, default=None):
		return self.data.get(prop, default)
		
	def as_dict(self, only_output_properties=False):
		if only_output_properties:
			d = {key: value for key, value in self.data.items() if key in self.output_properties}
		else:
			d = self.data
		return dict(d, text=self.text)
		
	def __eq__(self, other):
		if not isinstance(other, Message):
			return False
		else:
			return (other.text, ordered(other.data)) == (self.text, ordered(self.data))
	
	def __hash__(self):
		return hash((self.text, str(ordered(self.data))))
		
class TrainingData(object):

	MIN_EXAMPLES_PER_INTENT = 2
	MIN_EXAMPLES_PER_ENTITY = 2
	
	def __init__(self, training_examples=None, entity_synonyms=None, regex_features=None):
		self.training_examples = self.sanitice_examples(training_examples) if training_examples else []
		self.entity_synonyms = entity_synonyms if entity_synonyms else {}
		self.regex_features = regex_features if regex_features else []
		self.validate()
	def sanitice_examples(self, examples):
		for e in examples:
			if e.get("intent") is not None:
				e.set("intent", e.get("intent").strip())
		return examples
	
	@lazyproperty
	def intent_examples(self):
		return [e for e in self.training_examples if e.get("intent") is not None]
	
	@lazyproperty
	def entity_examples(self):
		return [e for e in self.training_examples if e.get("entities") is not None]
		
	def sorted_intent_examples(self):
		return sorted(self.intent_examples, key=lambda e: e.get("intent"))
		
	def sorted_entity_examples(self):
		return sorted([entity for ex in self.entity_examples for entity in ex.get("entities")],
						key=lambda e: e["entity"])
	
	@lazyproperty
	def num_intent_examples(self):
		return len(self.intent_examples)
	
	@lazyproperty
	def num_entity_examples(self):
		return len([e for e in self.training_examples if len(e.get("entities", [])) > 0])
		
	def as_json(self, **kwargs):
		return str(json.dumps({
			"nlu_data": {
				"common_examples": [example.as_dict() for example in self.training_examples],
				"regex_features": self.regex_features
			}
		}, **kwargs))
		
	def persist(self, dir_name):
		data_file = os.path.join(dir_name, "training_data.json")
		with io.open(data_file, 'w') as f:
			f.write(self.as_json(indent=2))
		return {
			"training_data": "training_data.json"
		}
		
	def validate(self):
		logger.debug("Validating training data...")
		examples = self.sorted_intent_examples()
		different_intents = []
		for intent, group in groupby(examples, lambda e: e.get("intent")):
			size = len(list(group))
			different_intents.append(intent)
			if size < self.MIN_EXAMPLES_PER_INTENT:
				template = "Intent '{}' has only {} training examples! minimum is {}, training may fail."
				warnings.warn(template.format(intent, size, self.MIN_EXAMPLES_PER_INTENT))
		different_entities = []
		for entity, group in groupby(self.sorted_entity_examples(), lambda e: e["entity"]):
			size = len(list(group))
			different_entities.append(entity)
			if size < self.MIN_EXAMPLES_PER_ENTITY:
				template = "Entity '{}' has only {} training examples! minimum is {}, training may fail."
				warnings.warn(template.format(entity, size, self.MIN_EXAMPLES_PER_ENTITY))
		logger.info("Training data stats: \n" + 
					"\t- intent examples: {} ({} distinct intents)\n".format(
							self.num_intent_examples, len(different_intents)) +
					"\t- found intents: {}\n".format(list_to_str(different_intents)) +
					"\t- entity examples: {} ({} distinct entities)\n".format(
							self.num_entity_examples, len(different_entities)) +
					"\t- found entities: {}\n".format(list_to_str(different_entities)))