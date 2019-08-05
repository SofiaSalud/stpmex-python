import pytest
from requests import HTTPError

from stpmex.client import Client
from stpmex.exc import InvalidPassphrase

PKEY = (
    'Bag Attributes\n    friendlyName: prueba\n    localKeyID:'
    ' 54 69 6D 65 20 31 33 32 34 35 39 35 30 31 35 33 '
    '33 30 \nKey Attributes: <No Attributes>\n'
    '-----BEGIN ENCRYPTED PRIVATE KEY-----\n'
    'MIICxjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIAPOngEipSGICA'
    'ggA\nMBQGCCqGSIb3DQMHBAi3RX0'
    '+96FhJASCAoAGX5N8jxBqlyKk8MTz/Q3a/V4fnCNA\n'
    'IlPYybMbO00HbMNXw20Kn+WzK73VZtBdEf'
    '+8CBcqZMwuC0gqn5pdnOVqP0wz8MU5\n'
    'AlWu0ZJpLo8npjQyV5Smrk1OvFREQ9skuJRBgYjPPTgdYmVN77ZGeFwJlf+'
    'OqOIM\nJWZIFZY6z3cXn6CnaAvQ6L+/smRt1Us0gEMe1m7rln0M6m64EbOF'
    'sOonzp7/CRTd\nMmlsk93Lg8G/uwGrL3gf1TDep1yM1KKMu6pWZ'
    '+6zT26ykwNsdUg0NUCpeWeYWzDZ\nKLzQ90U+/XlBPbPg/'
    '8gK6tc1dresvPbRcvNu+IJq8HbKuUkjrDeFor5Wezic3CyO\n/g'
    '//2LJbJGy7Ak4V4W9J46GLD8B3fqyDz0itCBRcmlrtAXiV0azb1isD+j8LdOXN\n'
    'vo/EPjLJnVdbP2RHiKKdp0Kq2FyRbigP86UujxwxfOxNN/w6m48agmVsj1u'
    'B6zBp\nhn0D/MLkMtoV7NmGhayRxFXs5sO1G'
    '/lWOoR96PgNzOur8xnPzvG7ysPv9qKRO1XS\n'
    'JEaGZXUUQ/sq2d6nLWMz9YLh7YVaVsRfIcUGPnmFh/bj30Pk52PodF6kN3JY'
    'ftvn\nZaXgOf6E4NLpHjtYRTzyVZQamenDAlvHQwZE284hDPShuJwxFr6FOSR'
    '/GrgqbN4d\ncOK898ofM'
    '+ZxkNkm5LrU3RAXR3336HU9XMky4UCV9L3CA51IlTMqt/CkddFhsjrw\n'
    'W4Zo1Aj8G7FaoDm7XhkLGDwVjf0Ua1O4YHRpSgVSkrXeBgW7P4Tc+5'
    '3nFns3rwxs\nuzF/x9tl2'
    '+BdiDjPOhSRuoa1ypilODdpOGKNKuf0vu2jAbbzDILBYOfw\n'
    '-----END ENCRYPTED PRIVATE KEY-----\n '
)


@pytest.mark.vcr
def test_client():
    pkey_passphrase = '12345678'
    empresa = 'TAMIZI'
    client = Client(
        empresa=empresa,
        priv_key=PKEY,
        priv_key_passphrase=pkey_passphrase,
        demo=True,
    )
    assert client.soap_client.get_type('ns0:ordenPagoWS')


@pytest.mark.vcr
def test_forbidden_without_vpn():
    pkey_passphrase = '12345678'
    empresa = 'TAMIZI'
    with pytest.raises(HTTPError) as exc_info:
        Client(
            empresa=empresa, priv_key=PKEY, priv_key_passphrase=pkey_passphrase
        )
    assert exc_info.value.response.status_code == 403


def test_incorrect_passphrase():
    pkey_passphrase = 'incorrect'
    empresa = 'TAMIZI'
    with pytest.raises(InvalidPassphrase):
        Client(
            empresa=empresa, priv_key=PKEY, priv_key_passphrase=pkey_passphrase
        )