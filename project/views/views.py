# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from flask import request, jsonify
from flask_jwt_extended import (create_access_token,create_refresh_token,
    get_jwt_identity,jwt_required)
from project.views import views_bp
from project.views.oauth import jwt, authenticate


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

        access_token = create_access_token(identity=user.id)
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
