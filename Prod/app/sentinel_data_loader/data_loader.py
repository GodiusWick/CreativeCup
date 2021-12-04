import datetime
from typing import Dict
import numpy as np

from sentinelhub import DataCollection, SHConfig

from eolearn.core import FeatureType, LinearWorkflow
from eolearn.io import SentinelHubInputTask, SentinelHubDemTask

from geojson.utils import coords

from .utils import *

CLIENT_ID = 'e492dd55-2010-4e1d-8068-e03eb6e06996'
CLIENT_SECRET = 'esDP>D3B.V@u.YU_Ja%Tsm9ps(x48L+?wH>9O:Mx'

MAX_CLOUDS_COVERAGE = .2
TIME_DIFFERENCE = datetime.timedelta(hours=2)
BANDS = ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B8A', 'B09', 'B10', 'B11', 'B12']


class DataLoader(object):
    def __init__(self, data: Dict):
        self.bbox = getBbox(list(coords(data['coordinates'])))
        self.resolution = data['resolution']
        self.time_interval = data['time_interval']

    def Load(self):
        config = SHConfig()
        if CLIENT_ID and CLIENT_SECRET:
            config.sh_client_id = CLIENT_ID
            config.sh_client_secret = CLIENT_SECRET
        else:
            raise ValueError('CLIENT_ID or CLIENT_SECRET is null')

        input_task = SentinelHubInputTask(
            data_collection=DataCollection.SENTINEL2_L1C,
            bands=BANDS,
            bands_feature=(FeatureType.DATA, 'L2A'),
            additional_data=[(FeatureType.MASK, 'dataMask')],
            resolution=self.resolution,
            maxcc=MAX_CLOUDS_COVERAGE,
            time_difference=TIME_DIFFERENCE,
            config=config,
            max_threads=3
        )

        add_dem = SentinelHubDemTask(
            data_collection=DataCollection.DEM_COPERNICUS_30,
            resolution=self.resolution,
            config=config
        )

        workflow = LinearWorkflow(input_task, add_dem)

        result = workflow.execute({
            input_task: {'bbox': self.bbox, 'time_interval': self.time_interval},
        })

        patch = result.eopatch()

        B02 = patch.data['L2A'][0][..., [1]]
        B03 = patch.data['L2A'][0][..., [2]]
        B04 = patch.data['L2A'][0][..., [3]]
        B05 = patch.data['L2A'][0][..., [4]]
        B06 = patch.data['L2A'][0][..., [5]]
        B07 = patch.data['L2A'][0][..., [6]]
        B08 = patch.data['L2A'][0][..., [7]]
        B11 = patch.data['L2A'][0][..., [11]]
        B12 = patch.data['L2A'][0][..., [12]]

        return (patch.data['L2A'][0][...,[3, 2, 1]]*3.5).clip(0, 1), \
               (np.concatenate(((B05+B06)/(B07+1e-5)/3,
                                (B03+B04)/(B02+1e-5)/3,
                                (B11+B12)/(B08+1e-5)/3), axis=2)).clip(0, 1)
