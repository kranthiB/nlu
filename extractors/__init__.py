from nlu.components import Component


class EntityExtractor(Component):
    def add_extractor_name(self, entities):
        for entity in entities:
            entity["extractor"] = self.name
        return entities

    def add_processor_name(self, entity):
        if "processors" in entity:
            entity["processors"].append(self.name)
        else:
            entity["processors"] = [self.name]
        return entity