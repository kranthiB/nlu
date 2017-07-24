from pkrm_nlu.tokenizers import Tokenizer, Token
from pkrm_nlu.components import Component

class SpacyTokenizer(Tokenizer, Component):
	name = "tokenizer_spacy"
	provides = ["tokens"]
	
	def process(self, message, **kwargs):
		message.set("tokens", self.tokenize(message.get("spacy_doc")))
		
	def tokenize(self, doc):
		return [Token(t.text, t.idx) for t in doc]
		
	def train(self, training_data, config, **kwargs):
		for example in training_data.training_examples:
			example.set("tokens", self.tokenize(example.get("spacy_doc")))