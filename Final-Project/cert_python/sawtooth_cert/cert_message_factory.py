# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

from sawtooth_processor_test.message_factory import MessageFactory


class CertMessageFactory:
    def __init__(self, signer=None):
        self._factory = MessageFactory(
            family_name="cert",
            family_version="1.0",
            namespace=MessageFactory.sha512("cert".encode("utf-8"))[0:6],
            signer=signer)

    def _certificate_to_address(self, certificate):
        return self._factory.namespace + \
            self._factory.sha512(certificate.encode())[0:64]

    def create_tp_register(self):
        return self._factory.create_tp_register()

    def create_tp_response(self, status):
        return self._factory.create_tp_response(status)

    def _create_txn(self, txn_function, certificate, action, space=None):
        payload = ",".join([
            str(certificate), str(action), str(space)
        ]).encode()

        addresses = [self._certificate_to_address(certificate)]

        return txn_function(payload, addresses, addresses, [])

    def create_tp_process_request(self, action, certificate, space=None):
        txn_function = self._factory.create_tp_process_request
        return self._create_txn(txn_function, certificate, action, space)

    def create_transaction(self, certificate, action, space=None):
        txn_function = self._factory.create_transaction
        return self._create_txn(txn_function, certificate, action, space)

    def create_get_request(self, game):
        addresses = [self._certificate_to_address(game)]
        return self._factory.create_get_request(addresses)

    # Todo: change
    def create_get_response(
        self, game, board="---------", state="P1-NEXT", player1="", player2=""
    ):
        address = self._certificate_to_address(game)

        data = None
        if board is not None:
            data = ",".join([game, board, state, player1, player2]).encode()
        else:
            data = None

        return self._factory.create_get_response({address: data})

    def create_set_request(
        self, game, board="---------", state="P1-NEXT", player1="", player2=""
    ):
        address = self._certificate_to_address(game)

        if state is not None:
            data = ",".join([game, board, state, player1, player2]).encode()
        else:
            data = None

        return self._factory.create_set_request({address: data})

    def create_set_response(self, certificate):
        addresses = [self._certificate_to_address(certificate)]
        return self._factory.create_set_response(addresses)

    def get_public_key(self):
        return self._factory.get_public_key()
