import argparse

from retrievers.s3 import S3RequestRetriever
from retrievers.sqs import SQSRequestRetriever
from processors.s3 import S3RequestProcessor
from processors.dynamodb import DynamoDBRequestProcessor


def get_strategies():
    # Parse the commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-rb', '--readbucket', help='S3 bucket to retrieve widget requests from.')
    parser.add_argument('-rq', '--readqueue', help='SQS queue to retrieve widget requests from.')
    parser.add_argument('-wb', '--writebucket', help='S3 bucket to store widgets in.')
    parser.add_argument('-wt', '--writetable', help='DynamoDB table to store widgets in.')
    args = parser.parse_args()

    # Use parsed arguments to create the resource specific objects that will be used
    if args.readbucket is not None and args.readqueue is not None:
        parser.error('You can only retrieve requests from a single resource.')
    elif args.readbucket is not None:
        retriever = S3RequestRetriever(args.readbucket)
    elif args.readqueue is not None:
        retriever = SQSRequestRetriever(args.readqueue)
    else:
        parser.error('You must specify a resource where widget requests can be retrieved from.')

    if args.writebucket is not None and args.writetable is not None:
        parser.error('You can only store widgets in a single resource.')
    elif args.writebucket is not None:
        processor = S3RequestProcessor(args.writebucket)
    elif args.writetable is not None:
        processor = DynamoDBRequestProcessor(args.writetable)
    else:
        parser.error('You must specify a resource where the widgets can be stored.')

    return retriever, processor
