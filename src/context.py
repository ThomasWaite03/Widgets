import argparse

from retrievers.s3 import S3RequestRetriever
from processors.s3 import S3RequestProcessor
from processors.dynamodb import DynamoDBRequestProcessor


def get_strategies():
    # Parse the commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-rb', '--readbucket', help='S3 bucket to retrieve widget requests from')
    parser.add_argument('-wb', '--writebucket', help='')
    parser.add_argument('-wt', '--writetable', help='')
    args = parser.parse_args()

    # Use parsed arguments to create the resource specific objects that will be used
    if args.readbucket is not None:
        retriever = S3RequestRetriever(args.readbucket)
    else:
        parser.error('Resource containing requests must be specified using --readbucket')

    if args.writebucket is not None and args.writetable is not None:
        parser.error('Can only store widgets in a single resource.')
    elif args.writebucket is not None:
        processor = S3RequestProcessor(args.writebucket)
    elif args.writetable is not None:
        processor = DynamoDBRequestProcessor(args.writetable)
    else:
        parser.error('You must specify a resource where the widgets can be stored')

    return retriever, processor
