curl --request PUT \
  --url 'http://127.0.0.1:5000/key_sample' \
  --data 'Ehi, come va?'

curl --request GET \
  --url 'http://127.0.0.1:5000/key_sample' \

curl --request GET \
  --url 'http://127.0.0.1:5000/'\ 