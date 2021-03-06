# django/tastypie
from tastypie.test import ResourceTestCase

# snapable
from api.auth import DatabaseAuthentication
from data.models import PasswordNonce, User


class Private_v1__UserResourceTest(ResourceTestCase):
    fixtures = ['api_accounts_and_keys.json', 'accounts_and_users.json', 'events.json', 'guests.json']

    def setUp(self):
        super(Private_v1__UserResourceTest, self).setUp()
        # we need a custom serializer for multipart uploads
        self.api_key = 'key123'
        self.api_secret = 'sec123'

        self.users = User.objects.all()
        self.user_1 = self.users[0]

        # The data we'll send on POST requests
        self.post_data = {
            'billing_zip': '00000',
            'email': 'john.doe@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'terms': True,
        }

    def get_credentials(self, method, uri):
        return DatabaseAuthentication.create_signature(self.api_key, self.api_secret, method, uri)

    def test_get_auth(self):
        uri = '/private_v1/user/auth/'
        extra_valid = {
            'HTTP_X_SNAP_USER': '{0}:{1}'.format(self.user_1.email, self.user_1.password.split('$')[-1]),
        }
        resp_valid = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri), **extra_valid)

        # assert that the valid auth check works
        self.assertValidJSONResponse(resp_valid)

        # setup some invalid headers that should cause the request to fail
        extra_invalid = {
            'HTTP_X_SNAP_USER': '{0}:{1}'.format(self.user_1.email, self.user_1.password.split('$')[-1][:-5]),
        }
        resp_invalid = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri), **extra_invalid)

        self.assertHttpBadRequest(resp_invalid)

    def test_get_users(self):
        uri = '/private_v1/user/'
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource is valid
        self.assertValidJSONResponse(resp)

        # make sure we have the right number of objects
        self.assertEqual(self.deserialize(resp)['meta']['total_count'], self.users.count())

    def test_get_user(self):
        uri = '/private_v1/user/{0}/'.format(self.user_1.pk)
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource is valid
        self.assertValidJSONResponse(resp)

        # test to make sure all the keys are in the response
        self.assertKeys(self.deserialize(resp), [
            'accounts',
            'billing_zip',
            'created',
            'created_at',
            'creation_date',
            'email',
            'first_name',
            'last_name',
            'last_login',
            'password_algorithm',
            'password_iterations',
            'password_salt',
            'resource_uri',
            'terms',
        ])

    def test_get_user_email(self):
        uri = '/private_v1/user/?email={0}'.format(self.user_1.email)
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource is valid
        self.assertValidJSONResponse(resp)

        # test to make sure all the keys are in the response
        self.assertKeys(self.deserialize(resp), [
            'meta',
            'objects',
        ])

    def test_post_user(self):
        uri = '/private_v1/user/'
        resp = self.api_client.post(uri, data=self.post_data, format='json', authentication=self.get_credentials('POST', uri))

        # make sure the resource was created
        self.assertHttpCreated(resp)

        # test to make sure all the keys are in the response
        self.assertKeys(self.deserialize(resp), [
            'accounts',
            'billing_zip',
            'created',
            'created_at',
            'creation_date',
            'email',
            'first_name',
            'last_name',
            'last_login',
            'resource_uri',
            'terms',
        ])

    def test_password_nonce(self):
        # setup variables
        user = User.objects.get(pk=1)
        password_nonce = PasswordNonce.objects.get(pk=1)

        # get the nonce
        uri = '/private_v1/user/passwordreset/{0}/'.format(password_nonce.nonce)
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))
        self.assertValidJSONResponse(resp)

        uri = '/private_v1/user/{0}/passwordreset/'.format(user.pk)
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))
        self.assertValidJSONResponse(resp)

    def test_password_reset_with_pk(self):
        # get nonce
        user_before = User.objects.get(pk=1)
        nonce = PasswordNonce.objects.get(pk=1)
        password_before = user_before.password

        # update the password
        patch_uri = '/private_v1/user/{0}/passwordreset/'.format(user_before.pk)
        patch_data = {
            'nonce': nonce.nonce,
            'password': 'my1337password',
        }

        # test nonce response
        patch_resp = self.api_client.patch(patch_uri, data=patch_data, format='json', authentication=self.get_credentials('PATCH', patch_uri))
        self.assertHttpAccepted(patch_resp)

        # shouldn't work the second time
        patch_resp = self.api_client.patch(patch_uri, data=patch_data, format='json', authentication=self.get_credentials('PATCH', patch_uri))
        self.assertHttpNotFound(patch_resp)

        # test password
        user_after = User.objects.get(pk=1)
        password_after = user_after.password
        self.assertNotEqual(password_after, password_before)

    def test_password_reset(self):
        # get nonce
        user_before = User.objects.get(pk=1)
        nonce = PasswordNonce.objects.get(pk=1)
        password_before = user_before.password

        # update the password
        patch_uri = '/private_v1/user/passwordreset/'
        patch_data = {
            'nonce': nonce.nonce,
            'password': 'my1337password',
        }

        # test nonce response
        patch_resp = self.api_client.patch(patch_uri, data=patch_data, format='json', authentication=self.get_credentials('PATCH', patch_uri))
        self.assertHttpAccepted(patch_resp)

        # shouldn't work the second time
        patch_resp = self.api_client.patch(patch_uri, data=patch_data, format='json', authentication=self.get_credentials('PATCH', patch_uri))
        self.assertHttpNotFound(patch_resp)

        # test password
        user_after = User.objects.get(pk=1)
        password_after = user_after.password
        self.assertNotEqual(password_after, password_before)
