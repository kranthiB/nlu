from nlu.featurizers import Featurizer

class SpacyFeaturizer(Featurizer):
	name = "intent_featurizer_spacy"
	provides = ["text_features"]
	requires = ["spacy_doc"]
	
	def process(self, message, **kwargs):
		features = self.features_for_doc(message.get("spacy_doc"))
		message.set("text_features", self._combine_with_existing_text_features(message, features))
	
	def features_for_doc(self, doc):
		return doc.vector
	
	def train(self, training_data, config, **kwargs):
		for example in training_data.intent_examples:
			features = self.features_for_doc(example.get("spacy_doc"))
			example.set("text_features", self._combine_with_existing_text_features(example, features))