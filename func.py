import pymongo
from pymongo import MongoClient
import random
import pprint
import re


def generate_id():
	characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_'
	randomstring = ''
	for i in range(0, 21):
		randomstring += random.choice(characters)
	return randomstring

def get_client_db():
	client = MongoClient("mongodb://127.0.0.1:27017/")
	db = client.yelpdb
	return db

def write_publish_review_by_user():
	(user_id, business_id) = input("Enter space separated valuess: ").split(" ")
	# client = MongoClient("ec2-3-14-86-28.us-east-2.compute.amazonaws.com", 27021)
	db = get_client_db()

	count_user = db.userInfo.find({"user_id" : user_id}).count()
	count_business = db.businessInfo.find({"business_id" : business_id}).count()
	if count_user == 0 :
		print("Invalid user id")
	elif count_business == 0 :
		print("Invalid business")
	else:
		text = input("Enter review: ")
		stars = int(input("Enter no. of stars:(0-5) "))
		# characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
		while True:
			review_id = generate_id()
			count_review = db.reviewInfo.find({"review_id" : review_id}).count()
			if count_review > 0:
				continue
			else:
				break
		new_review = {"review_id": review_id, "user_id": user_id, "business_id": business_id, "text": text, "stars": stars}

		insert_id = db.reviewInfo.insert_one(new_review).inserted_id
		if insert_id is not None:
			print("Review added successfully")
		else:
			print("Error in adding review...Add review again..!")
	


def search_business_by_ratings():
	rating = int(input("Enter rating: "))
	db = get_client_db()
	count_business = db.businessInfo.find({"stars": rating}, {"name": 1}).count()
	if count_business > 0:
		print("There are %d business with rating %.1f" % (count_business, rating))
		cursor = db.businessInfo.find({"stars": rating}, {"_id": 0, "name": 1}).limit(15)
		i = 1
		for row in cursor:
			print("%d. %s " % (i, row["name"]))
			i += 1
	else:
		print("No business with rating %.1f" % rating)


def search_business_by_type():
	category = input("Enter type of business: ")
	db = get_client_db()
	regx = re.compile(category, re.IGNORECASE)
	count_business = db.businessInfo.find({"categories" : {'$regex': regx}}).count()
	print(count_business)
	if count_business > 0:
		print("There are %d business with category %s" % (count_business, category))
		cursor = db.businessInfo.find({"categories" : {'$regex': regx}}).limit(15)
		i = 1
		for row in cursor:
			print("%d. %s " % (i, row["name"]))
			i += 1
	else:
		print("No business with category %s" % category)

def search_rating_by_date():
	date = input("Enter date in YYYY-MM-DD: ")
	db = get_client_db()
	regx = re.compile("^"+date, re.IGNORECASE)
	count_review = db.reviewInfo.find({"date" : {'$regex': regx}}).count()
	print(count_review)
	if count_review > 0:
		print("There are %d reviews with date %s" % (count_review, date))
		cursor = db.reviewInfo.find({"date" : {'$regex': regx}}).limit(15)
		i = 1
		for row in cursor:
			print("%d. %s - %d" % (i, row["text"], row["stars"]))
			i += 1
	else:
		print("No review with %s" %date)

def search_local_area_by_user():
	pass

def delete_or_edit_review_by_user():
	pass

def update_characteristic_by_business():
	pass

def search_by_hours_of_operation():
	pass

def get_most_useful_review():
	pass

def search_user_with_highest_star():
	pass

def delete_or_update_review():
	pass

def delete_user_account():
	pass

def get_year_when_most_user_joined():
	pass

def get_review_good_amazing():
	pass

def get_business_by_postal_code():
	pass