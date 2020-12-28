import simplejson as json


def build_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        },
        'body': json.dumps(body)
    }


def return_success(body):
    return build_response(200, body)


def return_failure(body):
    return build_response(500, body)
