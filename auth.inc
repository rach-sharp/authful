error_page 401 = /login;

location /auth {
  internal;
  proxy_pass http://auth:5000/verify;
  proxy_pass_request_body off;
  proxy_set_header Content-Length "";
  proxy_set_header X-Original-URI $request_uri;
}

location /login {
  auth_request off;
  proxy_pass http://auth:5000/login?redirect=$scheme://$http_host$request_uri;
}

location = /authful/callback {
  auth_request off;
  proxy_pass http://auth:5000/callback;
}

location = /authful/logout {
  auth_request off;
  proxy_pass http://auth:5000/logout;
}