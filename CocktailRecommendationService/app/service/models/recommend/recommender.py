import torch
import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


class CocktailRecommender:
    def __init__(self, model_path, vectorizer_path, data_path):
        self.data, self.idx_to_label = self._load_data(data_path)

        self.vectorizer = self._load_vectorizer(vectorizer_path)

        self.model = self._load_model(model_path)


    def _load_model(self, model_path):
        model = self._get_model()
        model.load_state_dict(torch.load(model_path))
        model.eval()
        return model

    def _load_vectorizer(self, vectorizer_path):
        with open(vectorizer_path, "rb") as f:
            return pickle.load(f)

    def _load_data(self, data_path):
        data = pd.read_csv(data_path)
        cocktail_labels = {name: idx for idx, name in enumerate(data['name'].unique())}
        idx_to_label = {idx: name for name, idx in cocktail_labels.items()}
        return data, idx_to_label

    def _get_model(self):
        class MultiLabelModel(torch.nn.Module):
            def __init__(self, input_size, num_classes):
                super(MultiLabelModel, self).__init__()
                self.fc1 = torch.nn.Linear(input_size, 128)
                self.relu = torch.nn.ReLU()
                self.fc2 = torch.nn.Linear(128, num_classes)
                self.sigmoid = torch.nn.Sigmoid()

            def forward(self, x):
                x = self.relu(self.fc1(x))
                x = self.sigmoid(self.fc2(x))
                return x

        input_size = len(self.vectorizer.get_feature_names_out())
        num_classes = len(self.idx_to_label)
        return MultiLabelModel(input_size, num_classes)

    def recommend(self, ingredients, top_n=5):
        input_vector = self.vectorizer.transform([' '.join(ingredients)]).toarray()
        input_tensor = torch.tensor(input_vector, dtype=torch.float32)

        with torch.no_grad():
            outputs = self.model(input_tensor).flatten()

        scores = outputs / outputs.sum()
        top_indices = torch.topk(scores, k=top_n).indices.numpy()

        recommendations = [(self.idx_to_label[idx], scores[idx].item()) for idx in top_indices]
        return recommendations
