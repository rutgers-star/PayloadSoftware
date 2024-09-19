# Event Logging
This package is meant to facilitate the easy logging of all events and errors that may occur in your software while it is running. Instructions for it's use and implementation may are contained within this README. Guidelines for what needs to be logged can be found in the [Payload Software Standards](https://docs.google.com/document/d/1vicnkUB_dqbaCpopz8N8pzhCTJqari4AZ5WBYJJv5HY/edit#heading=h.yexhmihjoetb).

## log.py
This package is run by the log.py module. The commands supplied by this module can be imported using:

```python
from Logs.log import log
```

### Logging Events
All events and errors must be logged in accordance to the guidelines provided in the [Payload Software Standards](https://docs.google.com/document/d/1vicnkUB_dqbaCpopz8N8pzhCTJqari4AZ5WBYJJv5HY/edit#heading=h.yexhmihjoetb). This can be done with the log module's built in command:

```python
log(code:int|str, extra='')
```

The code itself and a description of the event must be included in the 00-event-codes.txt file. See [Payload Software Standards](https://docs.google.com/document/d/1vicnkUB_dqbaCpopz8N8pzhCTJqari4AZ5WBYJJv5HY/edit#heading=h.yexhmihjoetb) for more information, including formatting. When you invoke this method for an event pass an integer to the code parameter. Errors are passed as strings. 

If you wish to include information other than what is already provided (ex. the error message if an error occurs) you have the ability to do so using the optional `extra` parameter. 

Actions logged with this method will include a timestamp in the current days log file. The first time you log an action on any given day, a new file will be created for that day. 

## Logging Errors

All errors for this project should be raised as custom exceptions using the `errors.py` module included in this directory. This can be imported using:

```python
from Logs.errors import ERROR
```

With this you can envoke the built in errors by raising it as a custom exception. 
using:

```python
raise ERROR(code:int, context='')
```
The code is a 4 digit integer which stores the error code you are trying to invoke, and the context functions the same way as the log module's 'extra' .

When you are envoking a custom error, make sure the code your are requesting is found in the appropriate array at the top of the errors module. When you are envoking a custom error, make sure the code your are requesting is found in the appropriate array at the top of the errors module. See [Payload Software Standards](https://docs.google.com/document/d/1vicnkUB_dqbaCpopz8N8pzhCTJqari4AZ5WBYJJv5HY/edit#heading=h.yexhmihjoetb) for more information including how these arrays are assigned.

## Payload Software Documentation 

- [Payload Software Standards](https://docs.google.com/document/d/1vicnkUB_dqbaCpopz8N8pzhCTJqari4AZ5WBYJJv5HY/edit#heading=h.yexhmihjoetb)
- [Payload Software Flowchart](https://drive.google.com/file/d/1rOezNYC_cjR_Z52rbMSgPSSvkrbp2D6H/view?usp=sharing)

## Authors

- [@simon-kowerski](https://github.com/simon-kowerski)


