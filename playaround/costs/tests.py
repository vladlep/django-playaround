import json
from django.core.files.base import ContentFile
# from django.test import TestCase
from rest_framework.test import APITestCase
from django_sites import reverse
from rest_framework import status


class CostApiv2Tests(APITestCase):

    def _get_mobile_cost_json(self):
        """
        Without number but with mandatory fields filled in.
        :return: data
        """
        test_pdf_file = ContentFile("random content for this file", name="Test.file")

        return {
            'number': "Test-0001",
            'amount': 200,
            'description': 'lunch',
            'date': '2015-01-16',
            'cost_lines': [
                {
                    'amount': 150,
                    'tax_rate': 21
                },
                {
                    'amount': 50,
                    'tax_rate': 6
                }],
            'image': test_pdf_file,
        }

    def test_upload_normal_cost(self):
        """ Multipart POST
        This test will FAIL: It creates a cost without cost lines.
        E.g.: {'description': u'lunch', 'image': 'http://testserver/api/costs/costs/1426545309.file',
        'number': u'Test-0001', 'cost_lines': [], 'amount': u'200.00', 'date': '2015-01-16', 'id': 1}
        """
        data = self._get_mobile_cost_json()

        data['cost_lines'] = json.dumps(data['cost_lines']) # need json dumps to simulate the AJAX call

        add_url = reverse('cost-list')
        response = self.client.post(add_url, data, format='multipart')
        print response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cost_lines = response.data['cost_lines']
        self.assertEqual(len(cost_lines), 2) # Fails here. There are not lines saved in the database

    def test_upload_cost_without_file(self):
        data = self._get_mobile_cost_json()
        data.pop('image')
        add_url = reverse('cost-list')
        response = self.client.post(add_url, data, format='json')
        print response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cost_lines = response.data['cost_lines']
        self.assertEqual(len(cost_lines), 2)

