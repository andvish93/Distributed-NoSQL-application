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
	# client = MongoClient("ec2-3-14-86-28.us-east-2.compute.amazonaws.com", 27021)
	db = client.yelpdb
	return db

def write_publish_review_by_user():
	(user_id, business_id) = input("Enter space separated valuess: ").split(" ")
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

def search_business_by_local_area():
	(city, state) = input("Enter city and state space separated: ").split(" ")
	db = get_client_db()
	count_business = db.businessInfo.find({"city": city, "state": state}, {"name": 1}).count()
	if count_business > 0:
		print("There are %d business in  city %s and state %s" % (count_business, city, state))
		cursor = db.businessInfo.find({"city": city, "state": state}, {"name": 1}).limit(15)
		i = 1
		for row in cursor:
			print("%d. %s " % (i, row["name"]))
			i += 1
	else:
		print("No business in  city %s and state %s" % (city, state))

def delete_review_by_user():
	(user_id, review_id) = input("Enter space separated values: ").split(" ")
	db = get_client_db()
	count_user = db.userInfo.find({"user_id" : user_id}).count()
	count_review = db.reviewInfo.find({"review_id": review_id}).count()
	if count_user == 0:
		print("Invalid User")
	elif count_review == 0:
		print("Invalid Review")
	else:
		x = db.reviewInfo.delete_one({"review_id": review_id, "user_id": user_id})
		if x.deleted_count > 0:
			print("Review deleted successfully")
		else:
			print("Error in deleting review...delete review again..!")

def update_characteristic_by_business():
	business_id = input("Enter business_id: ")
	attr = input("Enter new characteristic: ")
	db = get_client_db()
	count_business = db.businessInfo.find({"business_id" : business_id}).count()
	if count_business == 0:
		print("Invalid business")
	else:
		u = db.businessInfo.update_one({"business_id": business_id}, {"$set": {"attributes."+attr: "true"}})
		if u is not None:
			print("Characteristic update successfully")
		else:
			print("Error in updating business characteristic...update again...!")	

def search_by_hours_of_operation():
	pass

def get_most_useful_review():
	db = get_client_db()
	cursor = db.reviewInfo.find({}, {"review_id" : 1}).sort("useful", -1).limit(10)
	i = 1
	print("Top Useful review: ")
	for row in cursor:
		print("%d. %s %s %s" % (i, row["review_id"], row["stars"], row["text"]))
		i += 1


def search_user_with_highest_star():
	db = get_client_db()

	cursor = db.userInfo.find({}, {"name" : 1}).sort("average_stars", -1).limit(10)
	i = 1
	print("Top highest star user: ")
	for row in cursor:
		print("%d. %s" % (i, row["name"]))
		i += 1

def update_review():
	review_id = input("Enter review_id: ")
	db = get_client_db()
	count_review = db.reviewInfo.find({"review_id": review_id}).count()
	if count_review == 0:
		print("Invalid review id")
	else:
		text = input("Enter review: ")
		cursor = db.reviewInfo.update_one({"review_id": review_id}, {"$set": {"text": text}})
		if cursor.modified_count > 0:
			print("Review update successfully...!")
		else:
			print("Error in updating review..update again...!")

def delete_user_account():
	pass

def get_year_when_most_user_joined():
	pass

def get_review_good_amazing():
	pass

def get_business_by_postal_code():
	pass