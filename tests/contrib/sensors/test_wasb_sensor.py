# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import unittest

import datetime

from airflow import DAG, configuration
from airflow.contrib.sensors.wasb_sensor import WasbBlobSensor
from airflow.contrib.sensors.wasb_sensor import WasbPrefixSensor

try:
    from unittest import mock
except ImportError:
    try:
        import mock
    except ImportError:
        mock = None


class TestWasbBlobSensor(unittest.TestCase):
    _config = {
        'container_name': 'container',
        'blob_name': 'blob',
        'wasb_conn_id': 'conn_id',
        'timeout': 100,
    }

    def setUp(self):
        configuration.load_test_config()
        args = {
            'owner': 'airflow',
            'start_date': datetime.datetime(2017, 1, 1)
        }
        self.dag = DAG('test_dag_id', default_args=args)

    def test_init(self):
        sensor = WasbBlobSensor(
            task_id='wasb_sensor',
            dag=self.dag,
            **self._config
        )
        self.assertEqual(sensor.container_name, self._config['container_name'])
        self.assertEqual(sensor.blob_name, self._config['blob_name'])
        self.assertEqual(sensor.wasb_conn_id, self._config['wasb_conn_id'])
        self.assertEqual(sensor.check_options, {})
        self.assertEqual(sensor.timeout, self._config['timeout'])

        sensor = WasbBlobSensor(
            task_id='wasb_sensor',
            dag=self.dag,
            check_options={'timeout': 2},
            **self._config
        )
        self.assertEqual(sensor.check_options, {'timeout': 2})

    @mock.patch('airflow.contrib.sensors.wasb_sensor.WasbHook',
                autospec=True)
    def test_poke(self, mock_hook):
        mock_instance = mock_hook.return_value
        sensor = WasbBlobSensor(
            task_id='wasb_sensor',
            dag=self.dag,
            check_options={'timeout': 2},
            **self._config
        )
        sensor.poke(None)
        mock_instance.check_for_blob.assert_called_once_with(
            'container', 'blob', timeout=2
        )


class TestWasbPrefixSensor(unittest.TestCase):
    _config = {
        'container_name': 'container',
        'prefix': 'prefix',
        'wasb_conn_id': 'conn_id',
        'timeout': 100,
    }

    def setUp(self):
        configuration.load_test_config()
        args = {
            'owner': 'airflow',
            'start_date': datetime.datetime(2017, 1, 1)
        }
        self.dag = DAG('test_dag_id', default_args=args)

    def test_init(self):
        sensor = WasbPrefixSensor(
            task_id='wasb_sensor',
            dag=self.dag,
            **self._config
        )
        self.assertEqual(sensor.container_name, self._config['container_name'])
        self.assertEqual(sensor.prefix, self._config['prefix'])
        self.assertEqual(sensor.wasb_conn_id, self._config['wasb_conn_id'])
        self.assertEqual(sensor.check_options, {})
        self.assertEqual(sensor.timeout, self._config['timeout'])

        sensor = WasbPrefixSensor(
            task_id='wasb_sensor',
            dag=self.dag,
            check_options={'timeout': 2},
            **self._config
        )
        self.assertEqual(sensor.check_options, {'timeout': 2})

    @mock.patch('airflow.contrib.sensors.wasb_sensor.WasbHook',
                autospec=True)
    def test_poke(self, mock_hook):
        mock_instance = mock_hook.return_value
        sensor = WasbPrefixSensor(
            task_id='wasb_sensor',
            dag=self.dag,
            check_options={'timeout': 2},
            **self._config
        )
        sensor.poke(None)
        mock_instance.check_for_prefix.assert_called_once_with(
            'container', 'prefix', timeout=2
        )


if __name__ == '__main__':
    unittest.main()
