curl -X PUT http://admin:admin@172.17.0.4:5984/_node/couchdb@172.17.0.4/_config/httpd/enable_cors -d '"true"'
curl -X PUT http://admin:admin@172.17.0.4:5984/_node/couchdb@172.17.0.4/_config/cors/origins -d '"*"'
curl -X PUT http://admin:admin@172.17.0.4:5984/_node/couchdb@172.17.0.4/_config/cors/credentials -d '"true"'
curl -X PUT http://admin:admin@172.17.0.4:5984/_node/couchdb@172.17.0.4/_config/cors/methods -d '"GET, PUT, POST, HEAD, DELETE"'
curl -X PUT http://admin:admin@172.17.0.4:5984/_node/couchdb@172.17.0.4/_config/cors/headers -d '"accept, authorization, content-type, origin, referer, x-csrf-token"'
curl -X PUT http://admin:admin@172.17.0.4:5984/_node/couchdb@172.17.0.2/_config/httpd/enable_cors -d '"true"'
curl -X PUT http://admin:admin@172.17.0.4:5984/_node/couchdb@172.17.0.2/_config/cors/origins -d '"*"'
curl -X PUT http://admin:admin@172.17.0.4:5984/_node/couchdb@172.17.0.2/_config/cors/credentials -d '"true"'
curl -X PUT http://admin:admin@172.17.0.4:5984/_node/couchdb@172.17.0.2/_config/cors/methods -d '"GET, PUT, POST, HEAD, DELETE"'
curl -X PUT http://admin:admin@172.17.0.4:5984/_node/couchdb@172.17.0.2/_config/cors/headers -d '"accept, authorization, content-type, origin, referer, x-csrf-token"'
curl -X PUT http://admin:admin@172.17.0.4:5984/_node/couchdb@172.17.0.3/_config/httpd/enable_cors -d '"true"'
curl -X PUT http://admin:admin@172.17.0.4:5984/_node/couchdb@172.17.0.3/_config/cors/origins -d '"*"'
curl -X PUT http://admin:admin@172.17.0.4:5984/_node/couchdb@172.17.0.3/_config/cors/credentials -d '"true"'
curl -X PUT http://admin:admin@172.17.0.4:5984/_node/couchdb@172.17.0.3/_config/cors/methods -d '"GET, PUT, POST, HEAD, DELETE"'
curl -X PUT http://admin:admin@172.17.0.4:5984/_node/couchdb@172.17.0.3/_config/cors/headers -d '"accept, authorization, content-type, origin, referer, x-csrf-token"'