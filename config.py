class Config(object):
    SECRET_KEY = 'some_very_secret_key'
    GROUPS = ['TEST-{:02}-17' for i in range(1, 20)]  # add here real groups
    DEPARTMENTS = ['ИППО', 'ВТ', 'КИС', 'МОСИТ']
    LOGS = 'registration.log'
