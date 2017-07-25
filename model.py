import io
import os
import json
import copy
import logging
import datetime

from nlu.training_data import Message
from nlu import components
from nlu.utils import create_dir

from builtins import object

logger = logging.getLogger(__name__)

class InvalidModelError(Exception):
    """Raised when a model failed to load.

    Attributes:
        message -- explanation of why the model is invalid
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
        
class Metadata:
	
	@staticmethod
	def load(model_dir):
		try:
			with io.open(os.path.join(model_dir, 'metadata.json'), encoding="utf-8") as f:
				data = json.loads(f.read())
			return Metadata(data, model_dir)
		except Exception as e:
			raise InvalidModelError("Failed to load model metadata. {}".format(e))
			
	def __init__(self, metadata, model_dir):
		self.metadata = metadata
		self.model_dir = model_dir
		
	def get(self, property_name, default=None):
		return self.metadata.get(property_name, default)
		
	@property
	def language(self):
		return self.get('language')
		
	@property
	def pipeline(self):
		return self.get('pipeline', [])
	
	def persist(self, model_dir):
		metadata = self.metadata.copy()
		metadata.update({
			"trained_at": datetime.datetime.now().strftime('%Y%m%d-%H%M%S'),
			"nlu_version": '1.0',
		})
		with io.open(os.path.join(model_dir, 'metadata.json'), 'w') as f:
			f.write(str(json.dumps(metadata, indent=4)))
		
class Interpreter:

	@staticmethod
	def default_output_attributes():
		return {"intent": {"name": "", "confidence": 0.0}, "entities": []}

	@staticmethod
	def load(model_metadata, config, component_builder=None, skip_valdation=False):
		context = {}
		pipeline = []
		if component_builder is None:
			component_builder = components.ComponentBuilder()
		for component_name in model_metadata.pipeline:
			component = component_builder.load_component(component_name, model_metadata.model_dir, model_metadata, **context)
			try:
				updates = component.provide_context()
				if updates:
					context.update(updates)
				pipeline.append(component)
			except components.MissingArgumentError as e:
				raise Exception("Failed to initialize component '{}'. {}".format(component.name, e))
		return Interpreter(pipeline, context, model_metadata)
	
	def __init__(self, pipeline, context, model_metadata=None):
		self.pipeline = pipeline
		self.context = context if context is not None else {}
		self.model_metadata = model_metadata
		
	def parse(self, text, time=None):
		message = Message(text, self.default_output_attributes(), time=time)
		for component in self.pipeline:
			component.process(message, **self.context)
		output = self.default_output_attributes()
		output.update(message.as_dict(only_output_properties=True))
		return output
		
class Trainer(object):
	SUPPORTED_LANGUAGES = ["en"]
	
	def __init__(self, config, component_builder=None, skip_validation=False):
		self.config = config
		self.skip_validation = skip_validation
		self.training_data = None
		self.pipeline = []
		if component_builder is None:
			component_builder = components.ComponentBuilder()
		for component_name in config.pipeline:
			component = component_builder.create_component(component_name, config)
			self.pipeline.append(component)
			
	def train(self, data):
		self.training_data = copy.deepcopy(data)
		context = {} 
		for component in self.pipeline:
			updates = component.provide_context()
			if updates:
				context.update(updates)
		for i, component in enumerate(self.pipeline):
			logger.info("Starting to train component {}".format(component.name))
			component.prepare_partial_processing(self.pipeline[:i], context)
			updates = component.train(data, self.config, **context)
			logger.info("Finished training component.")
			if updates:
				context.update(updates)
				
		return Interpreter(self.pipeline, context)
		
	def persist(self, path, persistor=None, model_name=None):
		timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
		metadata = {
			"language": self.config["language"],
			"pipeline": [component.name for component in self.pipeline],
		}
		if model_name is None:
			dir_name = os.path.join(path, "model_" + timestamp)
		else:
			dir_name = os.path.join(path, model_name)
		create_dir(dir_name)
		if self.training_data:
			metadata.update(self.training_data.persist(dir_name))
		for component in self.pipeline:
			update = component.persist(dir_name)
			if update:
				metadata.update(update)
		Metadata(metadata, dir_name).persist(dir_name)
		logger.info("Successfully saved model into '{}'".format(os.path.abspath(dir_name)))
		return dir_name