from nlu.utils.spacy_utils import SpacyNLP
from nlu.tokenizers.spacy_tokenizer import SpacyTokenizer
from nlu.featurizers.spacy_featurizer import SpacyFeaturizer
from nlu.featurizers.regex_featurizer import RegexFeaturizer
from nlu.classifiers.sklearn_intent_classifier import SklearnIntentClassifier

registered_pipeline_templates = {
    "spacy_sklearn": [
        "nlp_spacy",
        "tokenizer_spacy",
        "intent_featurizer_spacy",
        "intent_entity_featurizer_regex",
        "intent_classifier_sklearn"
    ]
}

component_classes = [
	SpacyNLP,
	SpacyTokenizer,
	SpacyFeaturizer,
	RegexFeaturizer,
	SklearnIntentClassifier
]

registered_components = {
    component.name: component for component in component_classes}
    
def get_component_class(component_name):
	return registered_components[component_name]

def load_component_by_name(component_name, model_dir, metadata, cached_component, **kwargs):
	component_clz = get_component_class(component_name)
	return component_clz.load(model_dir, metadata, cached_component, **kwargs)
	
def create_component_by_name(component_name, config):
	component_clz = get_component_class(component_name)
	return component_clz.create(config)