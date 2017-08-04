from django.core.urlresolvers import reverse


def test_page_title(client):
    response = client.get(reverse('home'))
    assert '<h1>Taar Api</h1>' in response.content.decode('utf-8')


def test_contribute_json(client):
    response = client.get('/contribute.json')
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'
