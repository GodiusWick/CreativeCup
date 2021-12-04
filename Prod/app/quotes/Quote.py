from flask import request
from sentinel_data_loader import DataLoader
from resnet import resnet32

import torch
import torch.nn.functional as F
import torchvision.transforms as transforms

import numpy as np
from PIL import Image
import base64


def PostStartDefine():
    resp = {
        'rgb':          None,
        'filter':       None,
        'size':         None,
        'result':       None,
        'exception':    None,
    }

    transform = transforms.Compose([transforms.Resize([224, 224]),
                                    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                         std=[0.229, 0.224, 0.225])])
    try:
        data = {
            'coordinates':      request.json['coordinates'],
            'resolution':       request.json['resolution'],
            'time_interval':    request.json['time_interval'],
        }

        dl = DataLoader(data)
        rgb, oil_filter = dl.Load()

        if not rgb.any():
            return resp, 400

        resp['rgb'] = base64.b64encode(Image.fromarray(np.uint8(rgb * 255), 'RGB').tobytes()).decode()
        resp['filter'] = base64.b64encode(Image.fromarray(np.uint8(oil_filter * 255), 'RGB').tobytes()).decode()
        resp['size'] = (rgb.shape[1], rgb.shape[0])

        tensor = np.transpose(oil_filter, (2, 0, 1))
        tensor = torch.from_numpy(tensor).unsqueeze(0)
        tensor = transform(tensor)

        model = resnet32(3, 2)
        model.load_state_dict(torch.load('resnet18.pth'))
        model.eval()
        with torch.no_grad():
            out_data = F.softmax(model(tensor), dim=1)[0]
            resp['result'] = {'no': float(out_data[0]), 'yes': float(out_data[1])}

        return resp, 200
    except Exception as ex:
        resp['exception'] = str(ex)
        return resp, 400
