# Widgets
This was a project I completed in my CS5260 Cloud Development course at Utah State University. The project includes a command-line application written in Python 
that can manage "widget" objects that are stored in AWS S3 buckets or AWS DyanmoDB tables. It performs create, update, and delete operations on these widgets by 
reading widget requests from a designated source. Widget requests are formatted in JSON and can be read from an S3 bucket or an SQS queue. This command-line tool 
is called the consumer, since it will try to read as many requests from a resource as possible until its time limit is reached. In order to easily add new widget 
requests, I set up an API that triggers a lambda function which transforms API requests into widget requests. It then stores them in an SQS queue where they can be 
read by the consumer program.

## Design & Architecture
A UML diagram for the project can be found in the `docs` directory.

#### The following is a diagram of the AWS architecture used in this project:
<img src="./docs/AWS Architecture.png" width="50%" />

## Testing
The unit tests for the consumer program were implemented using the unittest framework from Python's standard library. Many of the unit tests interact with AWS services 
using the boto3 sdk, so they cover some aspects of integration testing in addition to the testing of individual components.

#### Directories
* `src/tests` - contains unit tests for all the modules that compose the consumer program.
* `src/tests/data` - contains test data with both valid and invalid widget requests.
* `src/tests/lambda_events` - contains JSON files used for testing API events in the Lambda console.

#### How to run tests
To run all the unit tests, simply run the command `python -m unittest discover`.<br>
[More instructions](https://docs.python.org/3/library/unittest.html#command-line-interface)

## Logs
Logs will be automatically written to the `src/logs` directory each time the consumer program is run. They provide information about each operation performed by the 
program. When known errors are caught, appropriate messages are displayed for use in debugging.

## Docker
A dockerfile has been provided, so the consumer program can be packaged into a docker image. This allows the consumer program to be deployed in a cluster of containers 
for better scalability.
