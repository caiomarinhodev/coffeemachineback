from django.contrib.auth.models import User
from pagseguro.api import PagSeguroApiTransparent, PagSeguroItem
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET', 'POST'])
def get_session(request):
    pagseguro_api = PagSeguroApiTransparent()
    data = pagseguro_api.get_session_id()
    print data
    session_id = data['session_id']
    if request.method == 'GET':
        return Response({"message": "Generated Session!", "session_id": session_id})
    return Response({"message": "Generated Session!", "session_id": session_id})


@api_view(['GET', 'POST'])
def payment_card(request):
    api = PagSeguroApiTransparent()
    print '---- api'
    print api
    data = request.POST
    print '-----data'
    print data
    token_card = data['token']
    hash_sender = data['hash']
    # for product in data['items']:
    # item = PagSeguroItem(id=product['id'], description=product['description'], amount=product['amount'],
    #                       quantity=product['quantity'])
    item = PagSeguroItem(id='0001', description='Notebook Prata', amount='24300.00', quantity=1)
    api.add_item(item)
    sender = {'name': 'Jose Comprador', 'area_code': 11, 'phone': 56273440, 'email': 'comprador@uol.com.br',
              'cpf': '22111944785', }
    api.set_sender(**sender)
    shipping = {'street': "Av. Brigadeiro Faria Lima", 'number': 1384, 'complement': '5o andar',
                'district': 'Jardim Paulistano', 'postal_code': '01452002', 'city': 'Sao Paulo', 'state': 'SP',
                'country': 'BRA', }
    api.set_shipping(**shipping)
    api.set_payment_method('creditcard')
    data_card = {'quantity': 5, 'value': 125.22, 'name': 'Jose Comprador', 'birth_date': '27/10/1987',
                 'cpf': '22111944785',
                 'area_code': 11, 'phone': 56273440, }
    api.set_creditcard_data(**data_card)
    billing_address = {'street': 'Av. Brig. Faria Lima', 'number': 1384, 'district': 'Jardim Paulistano',
                       'postal_code': '01452002', 'city': 'Sao Paulo', 'state': 'SP', 'country': 'BRA', }
    api.set_creditcard_billing_address(**billing_address)
    api.set_creditcard_token(token_card)
    api.set_sender_hash(hash_sender)
    data_checkout = api.checkout()
    print data_checkout
    return Response({"message": "payment", "data": data_checkout})
