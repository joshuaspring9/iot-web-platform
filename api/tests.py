from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from oauth2_provider.models import Application
from .models import DataCapturingDevice, DataFile, SmartHomeDevice


# Create your tests here.
class DataFileTestCase(TestCase):
    '''
    Tests the DataFile model
    '''

    def setUp(self):
        self.application = Application.objects.create(client_id='blah', client_secret='blah', client_type='confidential', authorization_grant_type='client-credentials')
        self.capture_device = DataCapturingDevice.objects.create(name="Generic capture device")
        self.captured_device = SmartHomeDevice.objects.create(name='Amazon Alexa')
        self.data_file = DataFile.objects.create(data_file=SimpleUploadedFile(name='blah.pcap', content="blank".encode()), data_capturing_device=self.capture_device, processed=False)
        self.data_file.devices_captured.set([self.captured_device,])
        self.data_file_processed = DataFile.objects.create(data_file=SimpleUploadedFile(name='blah.pcap', content="another blank".encode()), data_capturing_device=self.capture_device, processed=True)
        self.data_file_processed.devices_captured.set([self.captured_device,])

    def test_capture_device_name(self):
        self.assertEqual(str(self.capture_device), "Generic capture device")

    def test_is_processed(self):
        self.assertEqual(self.data_file.is_processed(), False)
        self.assertEqual(self.data_file_processed.is_processed(), True)

    def test_data_file_name(self):
        self.assertTrue('blah' in str(self.data_file))
