# Event Logging
This package is meant to facilitate the easy logging of all events and errors that may occur in your software while it is running. Instructions for it's use and implementation may are contained within this README. Guidelines for what needs to be logged can be found in the [Payload Software Standards](https://docs.google.com/document/d/1vicnkUB_dqbaCpopz8N8pzhCTJqari4AZ5WBYJJv5HY/edit#heading=h.yexhmihjoetb).

## log.py
This package is run by the log.py module. The commands supplied by this module can be imported using:

```python
from Logs.log import log, open_experiment
```

### Opening an Experiment
The open experiment method may not be required by the module you are writing. It is to be included and called within the control loop at the start of each experiment.

```python
open_experiment(experiment_num:int)
```

When called, this method will create a log file for the experiment you are running. Log files will be named YYYY-MM-DD_Exp-#.log where the # is a count of the number of experiments run that day.
For example:
- The first experiment run on 4/12/2024 will be called 2024-4-12_Exp-1.log 
- The fourth experiment run on 4/12/2024 will be called 2024-4-12_Exp-4.log 

The experiment number passed to this method will indicate which experiment from the experiment table is being run. This number will be include in the header of the log file, and is different than the number in the file name.

Every time a new event is logged, it will be recorded in the most recent log file. **Opening the log at the start of each experiment is imperative.**

### Logging Events
All events and errors must be logged in accordance to the guidelines provided in the [Payload Software Standards](https://docs.google.com/document/d/1vicnkUB_dqbaCpopz8N8pzhCTJqari4AZ5WBYJJv5HY/edit#heading=h.yexhmihjoetb). This can be done with the log module's built in command:

```python
log(code:str, extra='')
```

The code passed should match the event happening as noted in the [Payload Software Specifications](https://docs.google.com/document/d/1LpYGc71wTcKrt5TmQpS8grCHC3RCom-TDyZihmUt6Bg/edit#heading=h.tvzqshglh107). The code itself and a description of the event should be included in the codes.txt file. If you wish to include information other than what is already provided (ex. the error message if an error occurs) you have the ability to do so using the optional `extra` parameter. 

Actions logged with this method will include a timestamp. 

## Payload Software Documentation 

- [Payload Software Standards](https://docs.google.com/document/d/1vicnkUB_dqbaCpopz8N8pzhCTJqari4AZ5WBYJJv5HY/edit#heading=h.yexhmihjoetb)
- [Payload Software Flowchart](https://drive.google.com/file/d/1rOezNYC_cjR_Z52rbMSgPSSvkrbp2D6H/view?usp=sharing)

## Authors

- [@simon-kowerski](https://github.com/simon-kowerski)


