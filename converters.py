from pkrm_nlu import utils
from pkrm_nlu.training_data import TrainingData, Message

import io
import json

PKRM_FILE_FORMAT = "pkrm_nlu"

def resolve_data_files(resource_name):
	try:
		return utils.recursively_find_files(resource_name)
	except ValueError as e:
		raise ValueError("Invalid training data file / folder specified. {}".format(e))
		
def guess_format(files):
	return PKRM_FILE_FORMAT

def pkrm_nlu_data_schema():
	training_example_schema = {
		"type": "object",
		"properties": {
			"text": {"type": "string"},
			"intent": {"type": "string"},
			"entities": {
				"type": "array",
				"items": {
					"type": "object",
					"properties": {
						"start": {"type": "number"},
						"end": {"type": "number"},
						"value": {"type": "string"},
						"entity": {"type": "string"}
					},
					"required": ["start", "end", "entity"]
				}
			}
		},
		"required": ["text"]
	}
	
	regex_feature_schema = {
		"type": "object",
		"properties": {
			"name": {"type": "string"},
			"pattern": {"type": "string"}
		}
	}
	
	return {
		"type": "object",
		"properties": {
			"pkrm_nlu_data": {
				"type": "object",
				"properties": {
					"regex_features": {
						"type": "array",
						"items": regex_feature_schema
					},
					"common_examples": {
						"type": "array",
						"items": training_example_schema
					}
				}
			}
		},
		"additionalProperties": False
	}
	
def validate_pkrm_nlu_data(data):
	from jsonschema import validate
	from jsonschema import ValidationError
	try:
		validate(data, pkrm_nlu_data_schema())
	except ValidationError as e:
		 e.message += \
		 	". Failed to validate training data, make sure your data is valid. "
		 raise e

def load_pkrm_data(filename):
	with io.open(filename, encoding="utf-8-sig") as f:
		data = json.loads(f.read())
	validate_pkrm_nlu_data(data)
	
	all_examples = data['pkrm_nlu_data'].get("common_examples", list())
	regex_features = data['pkrm_nlu_data'].get("regex_features", list())
	synonyms = data['pkrm_nlu_data'].get("entity_synonyms", list())
	
	entity_synonyms = {}
	for s in synonyms:
		if "value" in s and "synonyms" in s:
			for synonym in s["synonyms"]:
				entity_synonyms[synonym] = s["value"]
				
	training_examples = []
	for e in all_examples:
		data = {}
		if e.get("intent"):
			data["intent"] = e["intent"]
		if e.get("entities") is not None:
			data["entities"] = e["entities"]
		training_examples.append(Message(e["text"], data))
	
	return TrainingData(training_examples, entity_synonyms, regex_features)
		
def load_data(resource_name, fformat=None):
	files = resolve_data_files(resource_name)
	return load_pkrm_data(files[0])