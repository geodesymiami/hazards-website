config = {}

aws_s3 = {}
database = {}

aws_s3['access_key'] = 'AKIA3NOVYUATRLYHYHBL'
aws_s3['secret_key'] = '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'
aws_s3['bucket_name'] = 'hazards-website'

database['localhost'] = 'db'
database['host'] = '129.114.17.74'
database['user'] = 'root'
database['password'] = 'root'
database['database'] = 'hazards'
database['localport'] = 3306
database['port'] = 32000  # should be an int
database['attempts'] = 5
database['attempt_delay'] = 5

config['aws_s3'] = aws_s3
config['database'] = database


def get_config_var(type, key):
    return config[type][key]
