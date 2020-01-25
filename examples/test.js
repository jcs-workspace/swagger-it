/**
 * $File: test.js $
 * $Date: 2020-01-19 00:35:46 $
 * $Revision: $
 * $Creator: Jen-Chieh Shen $
 * $Notice: See LICENSE.txt for modification and distribution information
 *                   Copyright © 2020 by Shen, Jen-Chieh $
 */

"use strict";

/**
 * @swagger
 * @tags accounts
 * @tags.description Everything about your Pets
 * @tags.externalDocs.description Find out more
 * @tags.externalDocs.url http://swagger.io
 */

/**
 * @swagger
 * @summary Show an account
 * @tags accounts
 * @description This is the description to show an account.
 * @accept json
 * @produce json
 * @param id path int true "Account ID"
 * @success 200 object model.Account
 * @failure 400 {object} httputil.HTTPError
 * @failure 404 {object} httputil.HTTPError
 * @failure 500 {object} httputil.HTTPError
 * @verb get
 * @router /accounts/{id}
 */
function showAccount(a, b) {

}

function listAccount(a, b) {

}

/**
 * @swagger
 * @title Swagger Example API
 * @version 1.0
 * @description This is a sample server Petstore server.
 * @termsOfService http://swagger.io/terms/
 *
 * @contact.name API Support
 * @contact.url http://www.swagger.io/support
 * @contact.email support@swagger.io
 *
 * @license.name Apache 2.0
 * @license.url http://www.apache.org/licenses/LICENSE-2.0.html
 *
 * @host petstore.swagger.io
 * @basePath /v2
 *
 * @schemes http, https, ws, wss
 *
 * @externalDocs.description Find out more about Swagger
 * @externalDocs.url http://swagger.io
 */
function main() {

}
