config = {}

aws_s3 = {}
database = {}

aws_s3['access_key'] = ''
aws_s3['secret_key'] = ''
aws_s3['bucket_name'] = ''

database['host'] = ''
database['user'] = ''
database['password'] = ''
database['database'] = ''
database['port'] = 0  # should be an int

config['aws_s3'] = aws_s3
config['database'] = database


def get_config_var(type, key):
    return config[type][key]
