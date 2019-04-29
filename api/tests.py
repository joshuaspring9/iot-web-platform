from django.test import TestCase
from .models import DataCapturingDevice, DataFile, SmartHomeDevice
from oauth2_provider.models import Application


# Create your tests here.
class DataFileTestCase(TestCase):
    '''
    Tests the DataFile model
    '''

    def setUp(self):
        self.application = Application.objects.create(client_id='blah', client_secret='blah', client_type='confidential', authorization_grant_type='client-credentials')
        self.capture_device = DataCapturingDevice.objects.create(oauth_application=self.application)
        self.captured_device = SmartHomeDevice.objects.create(name='Amazon Alexa')
        self.data_file = DataFile.objects.create(data_file='blah', data_capturing_device=self.capture_device, devices_captured=[self.captured_device,])
        self.data_file_processed = DataFile.objects.create(data_file='blah', data_capturing_device=self.capture_device, devices_captured=[self.captured_device,], processed=True)


    def test_is_processed(self):
        self.assertEqual(self.data_file.is_processed(), False)
        self.assertEqual(self.data_file_processed.is_processed(), True)

    def test_data_file_name(self):
        self.assertEqual(str(self.data_file), 'blah')
