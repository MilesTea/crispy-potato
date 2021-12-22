import unittest
from unittest.mock import patch, call
import app
import yandex


class TestBaseFunctional(unittest.TestCase):

	@classmethod
	def setUpClass(cls) -> None:
		cls.sample_document = ['1234567890', 'test_doc', 'test_owner', '1']  # тестовый документ

	@patch('builtins.print')  # перехват print
	def test_getting_doc_info(self, mocked_print):
		expected_document_info = [doc for doc in app.documents[0].values()]
		expected_document = '{} "{}" "{}"'.format(*expected_document_info)
		test_document = app.documents[0]
		app.show_document_info(test_document)
		self.assertEqual(mocked_print.mock_calls, call(expected_document).call_list(), 'invalid info')

	@patch('builtins.input')  # перехват input
	def test_document_adding(self, mocked_input):
		inputs = self.sample_document
		mocked_input.side_effect = inputs  # подставляет элементы inputs вместо input
		app.add_new_doc()
		test_document = None
		found = 0
		for doc in app.documents:
			if doc['number'] == inputs[0]:
				found += 1
				test_document = doc
		self.assertTrue(found <= 1, 'Multiple documents found')
		self.assertEqual(test_document, {'type': inputs[1], 'number': inputs[0], 'name': inputs[2]}, 'No such document')
		self.assertIn(inputs[0], app.directories[inputs[3]], 'No such document in directory')
		mocked_input.side_effect = [inputs[0]]
		app.delete_doc()

	@patch('builtins.input')  # перехват input
	def test_document_deleting(self, mocked_input):
		inputs = self.sample_document
		test_doc = self.sample_document[0]
		inputs.append(test_doc)
		mocked_input.side_effect = inputs  # подставляет элементы inputs вместо input
		app.add_new_doc()
		app.delete_doc()
		doc_exists = False
		doc_shelf = None
		for i, directory in enumerate(app.directories):
			if test_doc in app.directories[directory]:
				doc_exists = True
				doc_shelf = i
		self.assertFalse(doc_exists, f'document exists in {doc_shelf} directory')


class TestYandex(unittest.TestCase):
	with open('token.txt', mode='r', encoding='utf-8') as file:
		token = file.read().strip('\n')
	test_client = yandex.YaDisk(token)

	def test_folder_creation(self):
		folder = 'test'
		self.test_client.delete_folder(folder)  # удаление папки(на случай, если уже была создана)

		# тест при создании папки
		response = self.test_client.create_folder(folder)
		self.assertNotEqual(response, 400, 'incorrect data')
		self.assertNotEqual(response, 401, 'unauthorized')
		self.assertNotEqual(response, 403, 'API temporarily unavailable')
		self.assertNotEqual(response, 404, 'resource not found')
		self.assertNotEqual(response, 406, 'invalid data format')
		self.assertNotEqual(response, 423, 'resource blocked; maybe another operation in progress')
		self.assertNotEqual(response, 429, 'too much requests')
		self.assertNotEqual(response, 503, 'service temporarily unavailable')
		self.assertEqual(response, 201, 'unexpected error')

		# тест при проверке папки
		check_disk = self.test_client.check_folder(folder)
		self.assertNotEqual(check_disk, 400, 'incorrect data')
		self.assertNotEqual(check_disk, 401, 'unauthorized')
		self.assertNotEqual(check_disk, 403, 'API temporarily unavailable')
		self.assertNotEqual(check_disk, 404, 'folder not found')
		self.assertNotEqual(check_disk, 406, 'invalid data format')
		self.assertNotEqual(check_disk, 429, 'too much requests')
		self.assertNotEqual(check_disk, 403, 'service temporarily unavailable')
		self.assertEqual(check_disk, 200, 'unexpected error')
