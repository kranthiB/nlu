import os
import logging

from nlu.components import Component

logger = logging.getLogger(__name__)

MAX_CV_FOLDS = 5
INTENT_RANKING_LENGTH = 10

class SklearnIntentClassifier(Component):
    """Intent classifier using the sklearn framework"""

    name = "intent_classifier_sklearn"

    provides = ["intent", "intent_ranking"]

    requires = ["text_features"]

    def __init__(self, clf=None, le=None):
        from sklearn.preprocessing import LabelEncoder

        if le is not None:
            self.le = le
        else:
            self.le = LabelEncoder()
        self.clf = clf
        
    @classmethod
    def required_packages(cls):
    	return ["numpy", "sklearn"]
    	
    def transform_labels_str2num(self, labels):
    	return self.le.fit_transform(labels)
    
    def transform_labels_num2str(self, y):
    	return self.le.inverse_transform(y)
    	
    def train(self, training_data, config, **kwargs):
    	from sklearn.model_selection import GridSearchCV
    	from sklearn.svm import SVC
    	labels = [e.get("intent") for e in training_data.intent_examples]
    	if len(set(labels)) < 2:
    		logger.warn("Can not train an intent classifier. Need at least 2 different classes. " +
    					"Skipping training of intent classifier.")
    	else:
    		import numpy as np
    		y = self.transform_labels_str2num(labels)
    		X = np.stack([example.get("text_features") for example in training_data.intent_examples])
    		tuned_parameters = [{'C': [1, 2, 5, 10, 20, 100], 'kernel': [str('linear')]}]
    		cv_splits = max(2, min(MAX_CV_FOLDS, np.min(np.bincount(y)) // 5))
    		self.clf = GridSearchCV(SVC(C=1, probability=True, class_weight='balanced'),
    								param_grid=tuned_parameters, n_jobs=config["num_threads"],
    								cv=cv_splits, scoring='f1_weighted', verbose=1)
    		self.clf.fit(X, y)
        
    def process(self, message, **kwargs):
    	if not self.clf:
    		intent = None
    		intent_ranking = []
    	else:
    		X = message.get("text_features").reshape(1, -1)
    		intent_ids, probabilities = self.predict(X)
    		intents = self.transform_labels_num2str(intent_ids)
    		intents, probabilities = intents.flatten(), probabilities.flatten()
    		if intents.size > 0 and probabilities.size > 0:
    			ranking = list(zip(list(intents), list(probabilities)))[:INTENT_RANKING_LENGTH]
    			intent = {"name": intents[0], "confidence": probabilities[0]}
    			intent_ranking = [{"name": intent_name, "confidence": score} for intent_name, score in ranking]
    		else:
    			intent = {"name": None, "confidence": 0.0}
    			intent_ranking = []
    	message.set("intent", intent, add_to_output=True)
    	message.set("intent_ranking", intent_ranking, add_to_output=True)	
    	
    def predict_prob(self, X):
    	return self.clf.predict_proba(X)
    	
    def predict(self, X):
    	import numpy as np
    	pred_result = self.predict_prob(X)
    	sorted_indices = np.fliplr(np.argsort(pred_result, axis=1))
    	return sorted_indices, pred_result[:, sorted_indices]
    	
    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):
    	from sklearn.externals import joblib
    	if model_dir and model_metadata.get("intent_classifier_sklearn"):
    		clf = joblib.load(os.path.join(model_dir, model_metadata.get("intent_classifier_sklearn")))
    		le = joblib.load(os.path.join(model_dir, model_metadata.get("label_encoder_sklearn")))
    		return SklearnIntentClassifier(clf,le)
    	return SklearnIntentClassifier()
    				
    def persist(self, model_dir):
    	from sklearn.externals import joblib
    	classifier_file = os.path.join(model_dir, "intent_classifier.pkl")
    	label_encoder_file = os.path.join(model_dir, "label_encoder.pkl")
    	joblib.dump(self.clf, classifier_file)
    	joblib.dump(self.le, label_encoder_file)
    	return {
    		"intent_classifier_sklearn": "intent_classifier.pkl",
    		"label_encoder_sklearn": "label_encoder.pkl"
    	}