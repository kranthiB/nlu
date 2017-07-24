from pkrm_nlu.components import Component

import logging

logger = logging.getLogger(__name__)

class SpacyNLP(Component):
	
	name = "nlp_spacy"
	provides = ["spacy_doc", "spacy_nlp"]
	def __init__(self, nlp, language, spacy_model_name):
		self.nlp = nlp
		self.language = language
		self.spacy_model_name = spacy_model_name
		
	@classmethod
	def cache_key(cls, model_metadata):
		spacy_model_name = model_metadata.metadata.get("spacy_model_name")
		if spacy_model_name is None:
			spacy_model_name = model_metadata.language
		return cls.name + "-" + spacy_model_name
		
	
	@classmethod
	def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):
		import spacy
		if cached_component:
			return cached_component
		nlp = spacy.load(model_metadata.get("spacy_model_name"), parser=False)
		cls.ensure_proper_language_model(nlp)
		return SpacyNLP(nlp, model_metadata.get("language"), model_metadata.get("spacy_model_name"))
		
	@classmethod
	def create(cls, config):
		import spacy
		spacy_model_name = config["spacy_model_name"]
		if spacy_model_name is None:
			 spacy_model_name = config["language"]
		logger.info("Trying to load spacy model with name '{}'".format(spacy_model_name))
		nlp = spacy.load(spacy_model_name, parser=False)
		cls.ensure_proper_language_model(nlp)
		return SpacyNLP(nlp, config["language"], spacy_model_name)
		
	@staticmethod
	def ensure_proper_language_model(nlp):
		if nlp is None:
			raise Exception("Failed to load spacy language model. Loading the model returned 'None'.")
		if nlp.path is None:
			raise Exception("Failed to load spacy language model for lang '{}'. ".format(nlp.lang) +
							"Make sure you have downloaded the correct model (https://spacy.io/docs/usage/).")
							
	def provide_context(self):
		return {"spacy_nlp": self.nlp}
		
	def process(self, message, **kwargs):
		message.set("spacy_doc", self.nlp(message.text))
		
	def train(self, training_data, config, **kwargs):
		for example in training_data.training_examples:
			example.set("spacy_doc", self.nlp(example.text))
			
	def persist(self, model_dir):
		return {
			"spacy_model_name": self.spacy_model_name,
			"language": self.language
		}