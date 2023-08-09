import torch

def load_model(model, path):
    model_dict = model.state_dict()
    pretrained_dict = torch.load(path, map_location=torch.device('cpu'))
    pretrained_dict = {k: v for k, v in pretrained_dict.items() if k in model_dict}
    model_dict.update(pretrained_dict)
    model.load_state_dict(model_dict)
    return model