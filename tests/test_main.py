import unittest
import pandas as pd
from src.units import ILAUnit


class TestILAUnit(unittest.TestCase):
    def setUp(self):
        # Mock data for testing
        self.test_data = [
            {'MANUALPOLICYNO': 'PSVAK210072', 'FIRST NAME': 'MATRON', 'SURNAME': 'SIBANDA', 'GENDER': 'Female'},
            {'MANUALPOLICYNO': 'PSVAK210073', 'FIRST NAME': 'JOHN', 'SURNAME': 'DOE', 'GENDER': 'Male'},
            {'MANUALPOLICYNO': 'PSVAK210074', 'FIRST NAME': 'JANE', 'SURNAME': 'SMITH', 'GENDER': 'Female'}
        ]

        # Save test data to a temporary Excel file
        self.test_excel_path = 'test_data.xlsx'
        self.test_df = pd.DataFrame(self.test_data)
        self.test_df.to_excel(self.test_excel_path, index=False)

        # Initialize ILAUnit instance
        self.ila_unit = ILAUnit(source='excel', config={'path': self.test_excel_path})

    def tearDown(self):
        # Remove temporary Excel file after tests
        import os
        os.remove(self.test_excel_path)

    def test_get(self):
        # Test retrieving existing policy
        result = self.ila_unit.get('PSVAK210072')
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'success')
        self.assertEqual(len(result['data']), 1)
        self.assertEqual(result['data'][0]['FIRST NAME'], 'MATRON')

        # Test retrieving non-existing policy
        result = self.ila_unit.get('PSVAK210075')
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['message'], "Policy number 'PSVAK210075' not found")
        self.assertIsNone(result['data'])

    def test_get_all(self):
        result = self.ila_unit.get_all()
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'success')
        self.assertEqual(len(result['data']), len(self.test_data))

    def test_post(self):
        new_policy = {'MANUALPOLICYNO': 'PSVAK210075', 'FIRST NAME': 'ALICE', 'SURNAME': 'WONDERLAND', 'GENDER': 'Female'}
        result = self.ila_unit.post([new_policy])
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'Data has been successfully added to the Excel file.')

        # Check if the new policy is added
        result = self.ila_unit.get('PSVAK210075')
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'success')
        self.assertEqual(len(result['data']), 1)
        self.assertEqual(result['data'][0]['FIRST NAME'], 'ALICE')

    def test_update(self):
        update_data = {'FIRST NAME': 'UPDATED', 'SURNAME': 'UPDATED'}
        result = self.ila_unit.update('PSVAK210072', update_data)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], "Policy with primary key 'PSVAK210072' has been successfully updated.")

        # Check if the policy is updated
        result = self.ila_unit.get('PSVAK210072')
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'success')
        self.assertEqual(len(result['data']), 1)
        self.assertEqual(result['data'][0]['FIRST NAME'], 'UPDATED')
        self.assertEqual(result['data'][0]['SURNAME'], 'UPDATED')

    def test_delete(self):
        result = self.ila_unit.delete('PSVAK210073')
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], "Policy with primary key 'PSVAK210073' has been successfully deleted.")

        # Check if the policy is deleted
        result = self.ila_unit.get('PSVAK210073')
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['message'], "Policy number 'PSVAK210073' not found")
        self.assertIsNone(result['data'])

if __name__ == '__main__':
    unittest.main()
