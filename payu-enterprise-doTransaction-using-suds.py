#!/usr/bin/env python
import os
import random
from traceback import print_exc
from suds.client import Client
from suds.client import Client, sys
from suds.sax.element import Element
from suds.sax.attribute import Attribute
from suds.xsd.sxbasic import Import
from suds.wsse import UsernameToken, Security, Token, Timestamp
import logging


def payuMeaDoTransactionApiCall(args):	

	urlToQuery = 'https://secure.payu.co.za/service/PayUAPI?wsdl'
	if	(args['store']['environment'] == 'staging')	:
		urlToQuery = 'https://staging.payu.co.za/service/PayUAPI?wsdl'

	#------------------------------------- CREATING CLIENT OBJECT--------------------------------------
	client = Client(urlToQuery, faults=False)
	
	#------------------------------------- CREATING CUSTOM HEADER--------------------------------------
	wsse = ('wsse','http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd')

	mustAttributeSecurity = Attribute('SOAP-ENV:mustUnderstand', '1')
	addressAttributeSecurity = Attribute('xmlns:wsse', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd')
	AttributeUsernameToken1 = Attribute('wsu:Id','UsernameToken-9')
	addressAttributeUsernameToken = Attribute('xmlns:wsu','http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd')
	addressAttributePassword = Attribute('Type','http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText')

	msgUsername = Element('Username', ns=wsse).setText(args['store']['soapUsername'])
	msgPassword = Element('Password', ns=wsse).setText(args['store']['soapPassword']).append(addressAttributePassword)

	msgUsernameToken = Element('UsernameToken', ns=wsse)
	msgUsernameToken.append(AttributeUsernameToken1)
	msgUsernameToken.append(addressAttributeUsernameToken)
	msgUsernameToken.insert(msgPassword).insert(msgUsername)
	
	msgSecurity = Element('Security', ns=wsse).addPrefix(p='SOAP-ENC', u='http://www.w3.org/2003/05/soap-encoding')
	msgSecurity.append(mustAttributeSecurity)
	msgSecurity.append(addressAttributeSecurity)
	msgSecurity.insert(msgUsernameToken)

	client.set_options(soapheaders=[msgSecurity])

	#------------------------------------- CREATING SOAP CALL DETAILS HERE--------------------------------------	
	transaction = {}
	transaction['Api'] = 'ONE_ZERO';
	transaction['Safekey'] = args['store']['safekey'];
	transaction['TransactionType'] = 'PAYMENT';	
	transaction['AdditionalInformation'] = args['additionalInformation']
	transaction['Basket'] = args['basket']	
	transaction['Customer'] = args['customer']	
	transaction['Creditcard'] = args['creditcard']	
	
	#------------------------------------- DOING SOAP CALL HERE--------------------------------------
	try:
		setTransaction = client.service.doTransaction(** transaction)
	except Exception, e:
		print "----------------"		
		print 'type is:', e.__class__.__name__
		print_exc()
		print "----------------"	
		
	print "--------------	RESPONSE	----------------"
	print client.last_sent()
	
	print "\r\n"
	
	print "--------------	RESPONSE	----------------"
	print client.last_received()
	

if __name__ == '__main__':
	try:	
		
		doTransactionDetails = {}	
		doTransactionDetails['store'] = {}
		doTransactionDetails['store']['soapUsername'] = 'Staging Integration Store 1'
		doTransactionDetails['store']['soapPassword'] = '78cXrW1W'
		doTransactionDetails['store']['safekey'] = '{45D5C765-16D2-45A4-8C41-8D6F84042F8C}'
		doTransactionDetails['store']['environment'] = 'staging'

		doTransactionDetails['additionalInformation'] = {}
		doTransactionDetails['additionalInformation']['merchantReference'] = random.randrange(1,10+1)
		doTransactionDetails['additionalInformation']['payUReference'] = 11999149347
		
		doTransactionDetails['basket'] = {}
		doTransactionDetails['basket']['description'] = "Product Description"
		doTransactionDetails['basket']['amountInCents'] = "10000"
		doTransactionDetails['basket']['currencyCode'] = 'ZAR'
		
		doTransactionDetails['creditcard'] = {}
		doTransactionDetails['creditcard']['nameOnCard'] = "Mr John Doe"		
		doTransactionDetails['creditcard']['cardNumber'] = "4000000000000234"
		doTransactionDetails['creditcard']['cardExpiry'] = "042014"
		doTransactionDetails['creditcard']['cvv'] = "123"
		doTransactionDetails['creditcard']['amountInCents'] = doTransactionDetails['basket']['amountInCents']

		doTransactionDetails['customer'] = {}
		doTransactionDetails['customer']['email'] = "john@doe.com"
		doTransactionDetails['customer']['firstName'] = 'John'
		doTransactionDetails['customer']['lastName'] = 'Doe'
		doTransactionDetails['customer']['mobile'] = '0211234567'

		payuMeaDoTransactionApiCall(doTransactionDetails)
		
	except Exception, e:
		print 'type is:', e.__class__.__name__
		print_exc()


		