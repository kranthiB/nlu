from builtins import object
class Component(object):
	name = ""
	provides = []
	requires = []
	def __init__(self):
		self.partial_processing_pipeline = None
		self.partial_processing_context = None
		
	@classmethod
	def cache_key(cls, model_metadata):
		return None
	
	@classmethod
	def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):
		return cached_component if cached_component else cls()
		
	@classmethod
	def create(cls, config):
		return cls()
		
	def provide_context(self):
		pass
	
	def prepare_partial_processing(self, pipeline, context):
		self.partial_processing_pipeline = pipeline
		self.partial_processing_context = context
	
	def persist(self, model_dir):
		pass
		
class MissingArgumentError(ValueError):

    def __init__(self, message):
        super(MissingArgumentError, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message
        
class ComponentBuilder(object):
	
	def __init__(self, use_cache=True):
		self.use_cache = use_cache
		self.component_cache = {}
	
	def __get_cached_component(self, component_name, model_metadata):
		from nlu import registry
		component_class = registry.get_component_class(component_name)
		cache_key = component_class.cache_key(model_metadata)
		if cache_key is not None and self.use_cache and cache_key in self.component_cache:
			return self.component_cache[cache_key], cache_key
		else:
			return None, cache_key
	
	def load_component(self, component_name, model_dir, model_metadata, **context):
		from nlu import registry
		try:
			cached_component, cache_key = self.__get_cached_component(component_name, model_metadata)
			component = registry.load_component_by_name(component_name, model_dir,model_metadata, cached_component, **context)
			if not cached_component:
				self.__add_to_cache(component, cache_key)
			return component
		except MissingArgumentError as e:   # pragma: no cover
			raise Exception("Failed to load component '{}'. {}".format(component_name, e))
			
	def __add_to_cache(self, component, cache_key):
		if cache_key is not None and self.use_cache:
			self.component_cache[cache_key] = component
			
	def create_component(self, component_name, config):
		from nlu import registry
		from nlu.model import Metadata
		try:
			component, cache_key = self.__get_cached_component(component_name, Metadata(config.as_dict(), None))
			if component is None:
				component = registry.create_component_by_name(component_name, config)
				self.__add_to_cache(component, cache_key)
			return component
		except MissingArgumentError as e:
			raise Exception("Failed to create component '{}'. {}".format(component_name, e))