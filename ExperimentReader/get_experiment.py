import csv
from pydantic import BaseModel
from typing import Literal, Union

class Experiment(BaseModel):
    experiment_num: int
    phase: Literal['A', 'B', 'C', 'D', 'E']
    experiment_name: str
    angle: int
    velocity: int
    mission_day: int
    maneuver: Literal['1-axis', '2-axis', '3-axis']
    rotation_axis: Literal['X', 'Y', 'Z', 'XY', 'XZ', 'YZ', 'XYZ', 'ZYX']
    camera: bool
    torque_force_sensor: bool
    gyro_read: bool
    mission_phase: Literal['Minimum Success', 'Full Mission']
    objective: Literal['Systems Identification', 'ML Initial training data', 'Excite --> Observe', 'Excite --> Mitigate']
    controller: Literal['BCT', 'Output Feedback', 'ML Controller', 'Reference Governor', 'Output+ML+RG']

def get_experiment(experiment: int) -> Union[Experiment, None]:
    if experiment < 1 or experiment > 231:
        print(f'Experiment number {experiment} not in bounds')
        return None
    with open('ExperimentReader/experiments.csv') as f:
        row = list(csv.reader(f))[experiment]
        output = {}
        output['experiment_num'] = int(row[0])
        output['phase'] = row[1]
        output['experiment_name'] = row[2]
        output['angle'] = int(row[3])
        output['velocity'] = int(row[4])
        output['mission_day'] = int(row[5])
        output['maneuver'] = row[6]
        output['rotation_axis'] = row[7]
        output['camera'] = row[8] == 'On'
        output['torque_force_sensor'] = row[9] == 'On'
        output['gyro_read'] = row[10] == 'On'
        output['mission_phase'] = row[11]
        output['objective'] = row[12]
        output['controller'] = row[13]

        return Experiment(**output)