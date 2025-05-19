import pickle

def serialize(data):
    return pickle.dumps(data)

def deserialize(serialized_data):
    return pickle.loads(serialized_data)