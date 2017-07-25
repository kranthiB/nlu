from nlu.utils.spacy_utils import SpacyNLP
from nlu.tokenizers.spacy_tokenizer import SpacyTokenizer
from nlu.featurizers.spacy_featurizer import SpacyFeaturizer
from nlu.featurizers.regex_featurizer import RegexFeaturizer
from nlu.extractors.crf_entity_extractor import CRFEntityExtractor
from nlu.extractors.entity_synonyms import EntitySynonymMapper
from nlu.classifiers.sklearn_intent_classifier import SklearnIntentClassifier

registered_pipeline_templates = {
    "spacy_sklearn": [
        "nlp_spacy",
        "tokenizer_spacy",
        "intent_featurizer_spacy",
        "intent_entity_featurizer_regex",
        "ner_crf",
        "ner_synonyms",
        "intent_classifier_sklearn",
    ],
    "mitie": [
        "nlp_mitie",
        "tokenizer_mitie",
        "ner_mitie",
        "ner_synonyms",
        "intent_entity_featurizer_regex",
        "intent_classifier_mitie",
    ],
    "mitie_sklearn": [
        "nlp_mitie",
        "tokenizer_mitie",
        "ner_mitie",
        "ner_synonyms",
        "intent_entity_featurizer_regex",
        "intent_featurizer_mitie",
        "intent_classifier_sklearn",
    ],
    "keyword": [
        "intent_classifier_keyword",
    ],
    # this template really is just for testing
    # every component should be in here so train-persist-load-use cycle can be tested
    # they still need to be in a useful order - hence we can not simply generate this automatically
    "all_components": [
        "nlp_spacy",
        "nlp_mitie",
        "tokenizer_whitespace",
        "tokenizer_mitie",
        "tokenizer_spacy",
        "intent_featurizer_mitie",
        "intent_featurizer_spacy",
        "intent_featurizer_ngrams",
        "intent_entity_featurizer_regex",
        "ner_mitie",
        "ner_crf",
        "ner_spacy",
        "ner_duckling",
        "ner_synonyms",
        "intent_classifier_keyword",
        "intent_classifier_sklearn",
        "intent_classifier_mitie",
    ]
}

component_classes = [
	SpacyNLP,
	SpacyTokenizer,
	SpacyFeaturizer,
	RegexFeaturizer,
	CRFEntityExtractor,
	EntitySynonymMapper,
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