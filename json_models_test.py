"""
Copyright 2009 Chris Tarttelin and Point2 Technologies

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of
conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this list
of conditions and the following disclaimer in the documentation and/or other materials
provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE FREEBSD PROJECT ``AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE FREEBSD PROJECT OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the
authors and should not be interpreted as representing official policies, either expressed
or implied, of the FreeBSD Project.
"""

import unittest, json
from datetime import datetime
from mock import patch
from StringIO import StringIO
from json_models import *
from common_models import *

class Address(Model):
    number = IntField(path='number')
    street = CharField(path='street')
    city = CharField(path='city')
    foobars = Collection(CharField, path='foobars')

    finders = { (number,): "http://address/number/%s",
            (number, street): "http://address/number/%s/street/%s",
            (city,): "http://localhost:8998/address/%s",
            (street, 'stringfield'): "http://address/street/%s/stringfield/%s"
          }


class MyModel(Model):
    muppet_name = CharField(path='kiddie.value')
    muppet_type = CharField(path='kiddie.type', default='frog')
    muppet_hair = CharField(path='kiddie.looks.head.hair', default='fuzzy')
    muppet_nose = CharField(path='kiddie.looks.head.nose')
    muppet_names = Collection(CharField, path='kiddie.names')
    muppet_ages = Collection(IntField, path='kiddie.ages')
    muppet_addresses = Collection(Address, path='kiddie.address', order_by='number')

    finders = {
                (muppet_name,): "http://foo.com/muppets/%s"
              }

class Simple(Model):
    field1 = CharField(path='field1')

    finders = {
               (field1,): "http://foo.com/simple/%s"
              }
    headers = {'user': 'user1', 'password': 'pwd1'}

class SimpleWithoutFinder(Model):
    field1 = CharField(path='field1')

class MyValidatingModel(Model):
    muppet_name = CharField(path='kiddie.value')
    muppet_type = CharField(path='kiddie.type', default='frog')
    muppet_names = Collection(CharField, path='kiddie.names')
    muppet_ages = Collection(IntField, path='kiddie.ages')
    muppet_addresses = Collection(Address, path='kiddie.address', order_by='number')

    def validate_on_load(self):
        if not self.muppet_name:
            raise ValidationError("What, no muppet name?")

    finders = {
                (muppet_name,): "http://foo.com/muppets/%s"
              }
    


class JsonModelsTest(unittest.TestCase):
    def test_char_returns_value_for_item_passed_in(self):
        json_data = AttrDict(json.loads('{"kiddie":{"value":"Muppets rock"}}'))
        field = CharField(path="kiddie.value")
        response = field.parse(json_data)
        self.assertEquals('Muppets rock', response)
        
    def test_int_returns_value_for_item_passed_in(self):
        json_data = AttrDict(json.loads('{"kiddie":{"value":30}}'))
        field = IntField(path="kiddie.value")
        response = field.parse(json_data)
        self.assertEquals(30,response)

    def test_int_field_raises_exception_when_non_int_value_is_parsed(self):
        json_data = AttrDict(json.loads('{"kiddie":{"value":"NaN"}}'))
        field = IntField(path="kiddie.value")
        try:
            response = field.parse(json_data)
            self.fail('Should have raised an exception')
        except:
            pass
            # Exception raised, all is right with the world

    def test_date_returns_value_for_item_passed_in(self):
        json_data = AttrDict(json.loads('{"kiddie":{"value":135}}'))
        field = DateField(path="kiddie.value")
        response = field.parse(json_data)
        self.assertEquals(datetime(1970,1,1,0,0,0,135000), response)

    def test_date_returns_None_for_item_not_in(self):
        json_data = AttrDict(json.loads('{"kiddie":{"value":null}}'))
        field = DateField(path="kiddie.value")
        response = field.parse(json_data)
        self.assertEquals(None, response)

    def test_bool_returns_false_for_item_passed_in_when_false(self):
        json_data = AttrDict(json.loads('{"kiddie":{"value":false}}'))
        field = BoolField(path="kiddie.value")
        response = field.parse(json_data)
        self.assertFalse(response)

    def test_bool_returns_true_for_item_passed_in_when_true(self):
        json_data = AttrDict(json.loads('{"kiddie":{"value":false}}'))
        field = BoolField(path="kiddie.value")
        response = field.parse(json_data)
        self.assertFalse(response)

    def test_can_retrieve_attribute_value_from_json_model(self):
        my_model = MyModel('{"kiddie":{"value":"Rowlf"}}')
        self.assertEquals('Rowlf', my_model.muppet_name)

    def test_returns_none_if_non_required_attribute_not_in_json_and_no_default(self):
        my_model = MyModel('{"kiddie":{"valuefoo":"Rowlf"}}')
        self.assertEquals(None, my_model.muppet_name)

    def test_returns_default_if_non_required_attribute_not_in_json_and_default_specified(self):
        my_model = MyModel('{"kiddie":{"value":"Rowlf"}}')
        self.assertEquals('frog', my_model.muppet_type)

    def test_returns_none_if_non_required_nested_attribute_not_in_json_and_no_default(self):
        my_model = MyModel('{"kiddie":{"valuefoo":"Rowlf"}}')
        self.assertEquals(None, my_model.muppet_nose)

    def test_returns_default_if_non_required_nested_attribute_not_in_json_and_default_specified(self):
        my_model = MyModel('{"kiddie":{"value":"Rowlf"}}')
        self.assertEquals('fuzzy', my_model.muppet_hair)


    def test_collection_returns_expected_number_of_correcty_typed_results(self):
        my_model = MyModel('{"kiddie":{"names": ["Rowlf","Kermit","Ms.Piggy"]}}')
        self.assertTrue('Rowlf' in my_model.muppet_names)
        self.assertTrue('Kermit' in my_model.muppet_names)
        self.assertTrue('Ms.Piggy' in my_model.muppet_names)

    def test_collection_returns_expected_number_of_integer_results(self):
        my_model = MyModel('{"kiddie":{"ages":[5,12,3,8]}}')
        self.assertTrue(5 in my_model.muppet_ages)
        self.assertTrue(12 in my_model.muppet_ages)
        self.assertTrue(3 in my_model.muppet_ages)
        self.assertTrue(8 in my_model.muppet_ages)

    def test_collection_returns_user_model_types(self):
        my_model = MyModel('{"kiddie":{ "address": [{"number" :10,"street": "1st Ave. South", "city": "MuppetVille", "foobars" : ["foo","bar"]},{"number": 5, "street": "Mockingbird Lane", "city": "Bedrock"}]}}')
        self.assertEquals(2,len(my_model.muppet_addresses))
        address1 = my_model.muppet_addresses[0]
        self.assertEquals(5, address1.number)
        self.assertEquals('Mockingbird Lane', address1.street)
        self.assertEquals('Bedrock', address1.city)
        address2 = my_model.muppet_addresses[1]
        self.assertEquals(10, address2.number)
        self.assertEquals('1st Ave. South', address2.street)
        self.assertEquals('MuppetVille', address2.city)
        self.assertEquals('foo', address2.foobars[0])
        self.assertEquals('bar', address2.foobars[1])

    def test_collection_orders_by_supplied_attribute_of_user_model_types(self):
        my_model = MyModel('{"kiddie":{ "address": [{"number" :10,"street": "1st Ave. South", "city": "MuppetVille", "foobars" : ["foo","bar"]},{"number": 5, "street": "Mockingbird Lane", "city": "Bedrock"}]}}')
        self.assertEquals(2,len(my_model.muppet_addresses))
        address1 = my_model.muppet_addresses[0]
        self.assertEquals(5, address1.number)
        address2 = my_model.muppet_addresses[1]
        self.assertEquals(10, address2.number)

    def test_collection_empty_collection_returned_when_json_not_found(self):
        my_model = MyModel('{"kiddie":{ "address": [{"number" :10,"street": "1st Ave. South", "city": "MuppetVille"},{"number": 5, "street": "Mockingbird Lane", "city": "Bedrock"}]}}')
        self.assertEquals([], my_model.muppet_addresses[0].foobars)
        
    def test_can_set_charfield_to_model(self):
        my_model = MyModel('{"kiddie":{"muppet_name":"Gonzo"}}')
        my_model.muppet_name = "Kermit"
        self.assertEquals("Kermit", my_model.muppet_name)

    def test_can_set_datefield_to_model(self):
        my_model = MyModel('{"kiddie":{"opened":123456}}')
        my_model.opened = datetime(1980,1,1,0,0,0,135000)
        self.assertEquals(datetime(1980,1,1,0,0,0,135000), my_model.opened)

    def test_can_set_None_to_datefield(self):
        my_model = MyModel('{"kiddie":{"opened":123456}}')
        my_model.opened = None
        self.assertEquals(None, my_model.opened)

    def test_collection_fields_can_be_appended_to(self):
        my_model = MyModel('{"kiddie":{"names": ["Kermit"]}}')
        my_model.muppet_names.append("Fozzie")
        self.assertTrue('Kermit' in my_model.muppet_names)
        self.assertTrue('Fozzie' in my_model.muppet_names)

    def test_manager_noregisteredfindererror_raised_when_filter_on_non_existent_field(self):
        try:
            MyModel.objects.filter(foo="bar").count()
            self.fail("expected NoRegisteredFinderError")
        except NoRegisteredFinderError, e:
            self.assertTrue("foo" in str(e))

    def test_should_handle_models_with_no_data(self):
        my_model = MyModel()
        my_model.muppet_name

    @patch.object(rest_client.Client, "GET")
    def test_manager_queries_rest_service_when_filtering_for_a_registered_finder(self, mock_get):
        class t:
            content = StringIO('{"root": {"kiddie":{"value":"Gonzo", "address": [{ "number" : 10, "street": "1st Ave. South","city": "MuppetVille"},{"number":5,"street":"Mockingbird Lane","city": "Bedrock"}]}}}')
        mock_get.return_value = t()
        count = MyModel.objects.filter(muppet_name="baz").count()
        self.assertEquals(1, count)
        self.assertTrue(mock_get.called)

    @patch.object(rest_client.Client, "GET")
    def test_manager_counts_child_nodes_when_filtering_a_collection_of_results(self, mock_get):
        class t:
            content = StringIO('{"field1": "hello"}\n{"field1": "goodbye"}')
        mock_get.return_value = t()
        count = Simple.objects.filter(field1="baz").count()
        self.assertEquals(2, count)
        self.assertTrue(mock_get.called)

    @patch.object(rest_client.Client, "GET")
    def test_manager_queries_rest_service_when_getting_for_a_registered_finder(self, mock_get):
        class t:
            content = StringIO('{"kiddie":{"value": "Gonzo", "address": [{ "number" : 10, "street": "1st Ave. South","city": "MuppetVille"},{"number":5,"street":"Mockingbird Lane","city": "Bedrock"}]}}')
            response_code = 200
        mock_get.return_value = t()
        val = MyModel.objects.get(muppet_name="baz")
        self.assertEquals("Gonzo", val.muppet_name)
        self.assertTrue(mock_get.called)

    @patch.object(rest_client.Client, "GET")
    def test_manager_queries_rest_service_when_getting_for_a_multi_field_registered_finder(self, mock_get):
        class t:
            content = StringIO('{"number": 10, "street": "1st Ave. South", "city": "MuppetVille"}')
            response_code = 200
        mock_get.return_value = t()
        val = Address.objects.get(street="foo", number="bar")
        self.assertEquals("1st Ave. South", val.street)
        self.assertTrue(mock_get.called)
        self.assertEquals("http://address/number/bar/street/foo", mock_get.call_args[0][0])


    @patch.object(rest_client.Client, "GET")
    def test_manager_queries_rest_service_accepting_strings_as_finder_keys(self, mock_get):
        class t:
            content = StringIO('{"number": 10, "street": "1st Ave. South", "city": "MuppetVille"}')
            response_code = 200
        mock_get.return_value = t()
        val = Address.objects.get(street="foo", stringfield="bar")
        self.assertEquals("1st Ave. South", val.street)
        self.assertTrue(mock_get.called)
        self.assertEquals("http://address/street/foo/stringfield/bar", mock_get.call_args[0][0])

    @patch.object(rest_client.Client, "GET")
    def test_manager_raises_error_when_getting_for_a_registered_finder_and_repsonse_empty(self, mock_get):
        class t:
            content = StringIO('')
            response_code = 200
        mock_get.return_value = t()
        try:
            MyModel.objects.get(muppet_name="baz")
            self.fail("Expected DoesNotExist")
        except DoesNotExist, e:
            self.assertTrue("DoesNotExist" in str(e))

    @patch.object(rest_client.Client, "GET")
    def test_manager_raises_error_when_getting_for_a_registered_finder_and_repsonse_code_404(self, mock_get):
        class t:
            content = StringIO('<HTML><body>Nothing to see here</body></HTML>')
            response_code = 404
        mock_get.return_value = t()
        try:
            MyModel.objects.get(muppet_name="baz")
            self.fail("Expected DoesNotExist")
        except DoesNotExist, e:
            self.assertTrue("DoesNotExist" in str(e))

    @patch.object(rest_client.Client, "GET")
    def test_manager_raises_validation_error_on_load_when_validation_test_fails_given_bad_json(self, mock_get):
        class t:
            content = StringIO('<HTML><body>Nothing to see here</body></HTML>')
            response_code = 200
        mock_get.return_value = t()
        try:
            MyValidatingModel.objects.get(muppet_name="baz")
            self.fail("Expected ValidationError")
        except ValidationError, e:
            self.assertEquals("Invalid JSON", str(e))

    @patch.object(rest_client.Client, "GET")
    def test_manager_raises_validation_error_on_load_when_validation_test_fails_given_bad_data(self, mock_get):
        class t:
            content = StringIO('{"Weta":true}')
            response_code = 200
        mock_get.return_value = t()
        try:
            MyValidatingModel.objects.get(muppet_name="baz")
            self.fail("Expected ValidationError")
        except ValidationError, e:
            self.assertEquals("What, no muppet name?", str(e))

    @patch.object(rest_client.Client, "GET")
    def test_manager_returns_iterator_for_collection_of_results(self, mock_get):
        class t:
            content = StringIO('{"field1": "hello"}\n{"field1": "goodbye"}')
        mock_get.return_value = t()
        qry = Simple.objects.filter(field1="baz")
        results = []
        for mod in qry:
            results.append(mod)
        self.assertEquals(2, len(results))
        self.assertEquals("hello", results[0].field1)
        self.assertEquals("goodbye", results[1].field1)

    @patch.object(rest_client.Client, "GET")
    def test_manager_returns_iterator_for_collection_of_results_from_custom_query(self, mock_get):
        class t:
            content = StringIO('{"field1": "hello"}\n{"field1": "goodbye"}')
        mock_get.return_value = t()
        qry = SimpleWithoutFinder.objects.filter_custom("http://hard_coded_url")
        results = []
        for mod in qry:
            results.append(mod)
        self.assertEquals(2, len(results))
        self.assertEquals("hello", results[0].field1)
        self.assertEquals("goodbye", results[1].field1)

    @patch.object(rest_client.Client, "GET")
    def test_manager_returns_count_of_collection_of_results_when_len_is_called(self, mock_get):
        class t:
            content = StringIO('{"field1": "hello"}\n{"field1": "goodbye"}')
        mock_get.return_value = t()
        qry = Simple.objects.filter(field1="baz")
        self.assertEquals(2, len(qry))

    @stub(MyModel)
    def test_stub_allows_stubbing_return_values_for_queries(self):
        address1 = Address()
        address1.number = 123
        address1.street = 'Sesame St.'
        address1.city = 'New York'
        address1.foobars = ['foo','bar']
        MyModel.stub().get(muppet_name='Kermit').returns(muppet_name='Kermit', muppet_type='toad', muppet_names=['Trevor', 'Kyle'], muppet_addresses=[address1])
        result = MyModel.objects.get(muppet_name='Kermit')
        self.assertEquals('toad', result.muppet_type)
        self.assertEqual(123, result.muppet_addresses[0].number)
        self.assertEqual('foo', result.muppet_addresses[0].foobars[0])

    @stub(MyValidatingModel)
    def test_stub_allows_validation_to_pass_stubbing_return_values_for_queries(self):
        try:
            MyValidatingModel.stub().get(muppet_name='Kermit').returns(muppet_name='Kermit')
            result = MyValidatingModel.objects.get(muppet_name='Kermit')
            self.assertTrue('Kermit', result.muppet_name)
        except Exception as e:
            self.fail(e.message)


    @stub(MyModel)
    def test_stub_allows_stubbing_filter_requests(self):
        MyModel.stub().filter(muppet_name='Kermit').returns(dict(muppet_name='Kermit', muppet_type='toad', muppet_names=['Trevor', 'Kyle']))
        result = MyModel.objects.filter(muppet_name='Kermit')
        self.assertEquals(1, len(result))
        self.assertEquals('toad',list(result)[0].muppet_type)

    @stub(MyModel)
    def test_stub_allows_stubbing_filter_custom_requests(self):
        MyModel.stub().filter_custom('http://anyurl.com').returns(dict(muppet_name='Kermit', muppet_type='toad', muppet_names=['Trevor', 'Kyle']))
        result = MyModel.objects.filter_custom('http://anyurl.com')
        self.assertEquals(1, len(result))
        self.assertEquals('toad',list(result)[0].muppet_type)

    def test_stub_allows_stubbing(self):
        @stub('MyModel')
        def test_something_to_do_with_mymodel(self):
            pass
        self.assertEquals('test_something_to_do_with_mymodel', test_something_to_do_with_mymodel.__name__)



    @stub(MyModel)
    def test_stub_allows_stubbing_to_raise_exception(self):
        class SesameStreetCharacter(Exception):
            pass
        MyModel.stub().get(muppet_name='Big Bird').raises(SesameStreetCharacter)
        try:
            result = MyModel.objects.get(muppet_name='Big Bird')
            self.fail("Stub should have raised exception")
        except SesameStreetCharacter:
            pass

    def test_headers_field_specified_on_model_is_added_to_the_query_manager(self):
        self.assertTrue(Simple.objects.headers != None)
        self.assertEquals('user1', Simple.objects.headers['user'])
        query = Simple.objects.filter(field1="Rhubarb")
        self.assertTrue(query.headers != None)
        self.assertEquals('pwd1', query.headers['password'])

if __name__=='__main__':
    unittest.main()

