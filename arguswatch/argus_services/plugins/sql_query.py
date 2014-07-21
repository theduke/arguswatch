import datetime 
from pprint import pprint
import re

from django.db import models
from django.utils.translation import ugettext as _

from django_baseline.forms import CrispyModelForm

from . import ServicePlugin, ServiceIsDownException, PluginCheckError, PluginConfiguratinError
from ..models import ServicePluginConfiguration


class SQLQueryPluginConfig(ServicePluginConfiguration):
    DATABASE_MYSQL = 'mysql'
    DATABASE_CHOICES = (
        (DATABASE_MYSQL, 'MySQL'),
    )
    database_type = models.CharField(max_length=50, choices=DATABASE_CHOICES)

    host = models.CharField(max_length=255)
    port = models.PositiveSmallIntegerField(default=3306)
    database = models.CharField(max_length=255, blank=True)

    username = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=255, blank=True)

    query = models.TextField(help_text='The MySQL query to run against the database.')

    query_replace_time = models.BooleanField(default=False, help_text='If enabled, the query will be run through strftime with the current time offest with timedelta. See https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior for format.')
    query_replace_timedelta = models.CharField(max_length=50, blank=True, verbose_name='Timedelta, specified as: +/-1y10m3d10h5m22s')

    query_eval = models.BooleanField(default=False, help_text='If enabled, the given query text will be evald as python code to generate the query.')

    VALIDATION_NUM_ROWS = 'num_rows'
    VALIDATION_EVAL = 'eval'

    VALIDATION_CHOICES = (
        (VALIDATION_NUM_ROWS, 'Number of result rows'),
        (VALIDATION_EVAL, 'Eval - Result will be available as result'),
    )
    validation_mode = models.CharField(max_length=50, choices=VALIDATION_CHOICES)

    help_validation="""
How the result should be validated. 
How the content of this field is interpreted depends on the validation mode setting.

Number of result rows: 
  Enter a comparison expression that checks the number of result rows.
  Supported operands: =,<,>,<=,>=.
  Examples: <=3, >5, >0, =1

Eval:
  Enter python code that will be evald.
  Available variables: 
    * row_count: Number of result rows
    * result: A tuple, with each item being a result row of the query.
  Example: 
    -) row_count >= 1
"""

    validation = models.TextField(help_text=help_validation)

    def get_settings(self):
        return {
            'database_type': self.database_type,
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'username': self.username,
            'password': self.password,
            'query': self.query,
            'query_replace_time': self.query_replace_time,
            'query_replace_timedelta': self.query_replace_timedelta,
            'query_eval': self.query_eval,
            'validation_mode': self.validation_mode,
            'validation': self.validation,
        }

    class Meta:
        verbose_name = _('SQLQueryPluginConfig')
        verbose_name_plural = _('SQLQueryPluginConfigs')
        app_label = "argus_services"


class SQLQueryPluginForm(CrispyModelForm):
    class Meta:
        model = SQLQueryPluginConfig
        fields = ['database_type', 
            'host', 'port', 'database', 'username', 'password',
            'query', 'query_eval',
            'query_replace_time', 'query_replace_timedelta',
          'validation_mode', 'validation']


class SQLQueryService(ServicePlugin):
    name = "SQLQuery"
    description = "Execute a SQL query on a database server and validate the result."
    is_passive = False
    config_class = SQLQueryPluginConfig
    form_class = SQLQueryPluginForm


    def __init__(self, *args, **kwargs):
        super(SQLQueryService, self).__init__(*args, **kwargs)


    def run_check(self, settings):
        log = self.get_logger()

        con = None
        try:
            con = self.get_connection(settings)
        except Exception as e:
            raise ServiceIsDownException("Could not connect to database: " + str(e))

        query = self.get_query(settings)
        log.debug("Running query {q}".format(q=query))

        row_count, result = self.execute_query(settings['database_type'], con, query)
        is_valid = self.validate_result(row_count, result, settings)

        if not is_valid:
            raise ServiceIsDownException("Validation check failed")


    def validate_result(self, row_count, result, settings):
        flag = None

        if settings['validation_mode'] == SQLQueryPluginConfig.VALIDATION_EVAL:
            flag = eval(settings['validation'])
        elif settings['validation_mode'] == SQLQueryPluginConfig.VALIDATION_NUM_ROWS:
            spec = settings['validation'].replace(' ', '')

            if spec[:2] == '>=':
                num = int(spec[2:])
                flag = row_count >= num
            elif spec[:2] == '<=':
                num = int(spec[2:])
                flag = row_count >= num
            elif spec[0] == '=':
                num = int(spec[1:])
                flag = row_count == num
            elif spec[0] == '>':
                num = int(spec[1:])
                flag = row_count > num
            elif spec[0] == '<':
                num = int(spec[1:])
                flag = row_count < num
            else:
                raise PluginConfiguratinError("Could not parse validation spec: " + spec)
        else:
            raise Exception("Unknown validation mode: " + settings['validation_mode'])

        return flag


    def get_connection(self, settings):
        if settings['database_type'] == SQLQueryPluginConfig.DATABASE_MYSQL:
            from pymysql import connect

            args = {
                'host': settings['host'],
                'port': int(settings['port']) if settings['port'] else 3306,
            }

            if settings['database']:
                args['database'] = settings['database']
            if settings['username']:
                args['user'] = settings['username']
                args['passwd'] = settings['password']


            con = connect(**args)
            return con
        else:
            raise Ecxeption("Unknown database type: " + settings['database_type'])


    def execute_query(self, db_type, con, query):
        if db_type == SQLQueryPluginConfig.DATABASE_MYSQL:
            cursor = con.cursor()
            cursor.execute(query)
            #cursor.commit()

            return (cursor.rowcount, cursor.fetchall())
        else:
            raise PluginConfiguratinError("Unknown database type: " + db_type)


    def get_query(self, settings):
        query = settings['query']

        if settings['query_eval']:
            query = eval(settings['query'])
        elif settings['query_replace_time']:
            plus, delta = self.build_timedelta(settings['query_replace_timedelta'])

            date = datetime.datetime.now()
            if plus:
                date += delta
            else:
                date -= delta


            # Handle %s for unix epoch time ourselfes, since it is not 
            # supported by python.
            query = query.replace('%s', str(int(date.timestamp())))
            query = date.strftime(query)

        return query


    def build_timedelta(self, spec):
        plus = None
        if spec[0] == '+':
            pass
        elif spec[0] == '-':
            plus = False
        else:
            raise PluginConfiguratinError("Timedelta specification must start with + or -")
        spec = spec[1:]

        parts = re.subn('([yMdhms])', r'\1 ', spec)[0].strip().split(' ')

        unit_map = {
            's': 1,
            'm': 60,
            'h': 60*60,
            'd': 60*60*24,
            'M': 60*60*24*30,
            'y': 60*60*24*365,
        }

        seconds = 0
        for part in parts:
            unit = part[-1]
            num = int(part[:-1])

            seconds += num * unit_map[unit]

        delta = datetime.timedelta(seconds=seconds)
        return (plus, delta)
