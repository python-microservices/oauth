# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from flask import request, jsonify
from flask_jwt_extended import (create_access_token,create_refresh_token,
    get_jwt_identity,jwt_required,jwt_refresh_token_required)
from project.views import views_bp
from project.views.oauth import authenticate


class UserNotFoundException(Exception):
    pass


@views_bp.route("/login", methods=["POST"])
def login():
    """
    User authenticate method.
    ---
    description: Authenticate user with supplied credentials.
    parameters:
      - name: username
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
    responses:
      200:
        description: User successfully logged in.
      400:
        description: User login failed.
    """
    # current_app.logger.info("{}".format(request.headers))
    try:
        username = request.form.get("username")
        password = request.form.get("password")

        user = authenticate(username, password)
        if not user:
            raise UserNotFoundException("User not found!")

        access_token = create_access_token(identity=user.id,fresh=False)
        refresh_token = create_refresh_token(user.id)

        resp = jsonify({
          "access_token": str(access_token, "utf-8"),
          "refresh_token": str(refresh_token,"utf-8")
          })
        resp.status_code = 200

        # add token to response headers - so SwaggerUI can use it
        resp.headers.extend({'jwt-token': access_token})

    except UserNotFoundException:
        resp = jsonify({"message": "Bad username and/or password"})
        resp.status_code = 401
    print(resp.headers)
    return resp


@views_bp.route("/check-token", methods=["GET"])
@jwt_required()
def protected():
    """
    Protected content method.
    ---
    description: Protected content method. Can not be seen without valid token.
    security:
      - APIKeyQueryParam: []
      - APIKeyHeader: []
    responses:
      200:
        description: User successfully accessed the content.
    """
    resp = jsonify({"protected": "{}".format(get_jwt_identity())})
    resp.status_code = 200

    return resp

@views_bp.route("/refresh-token",methods=["POST"])
@jwt_refresh_token_required
def refresh_token():
  """
  Refresh Token Method
  ---
  description: Refresh Access Tokens of the user
  responses:
    200:
      description: User has generated new access tokens
  """
  current_user = get_jwt_identity()
  access_token = create_access_token(identity=current_user,fresh=False)
  resp = jsonify({"access_token": str(access_token, "utf-8")})

  resp.status_code = 200
  resp.headers.extend({'jwt-token': access_token})
  return resp

