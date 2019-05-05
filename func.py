from pymongo import MongoClient
import random
import re


# function to generate random id of length 22
def generate_id():
	characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_'
	randomstring = ''
	for i in range(0, 21):
		randomstring += random.choice(characters)
	return randomstring


# function to retrieve connection with db
def get_client_db():
	client = MongoClient("ec2-54-215-246-81.us-west-1.compute.amazonaws.com", 27021)
	db = client.yelpdb
	return db


# use case 1
def write_review_by_user():
	user_id = input("Enter User Id: ")
	business_id = input("Enter Business Id: ")
	db = get_client_db()
	count_user = db.userInfo.find({"user_id": user_id}).count()
	count_business = db.businessInfo.find({"business_id": business_id}).count()
	if count_user == 0:
		print("User Id does not exist...!")
	elif count_business == 0:
		print("Business Id does not exist...!")
	else:
		text = input("Enter review: ")
		stars = float(input("Enter no. of stars:(0-5) "))
		while True:
			review_id = generate_id()
			count_review = db.reviewInfo.find({"review_id": review_id}).count()
			if count_review > 0:
				continue
			else:
				break
		new_review = {"review_id": review_id, "user_id": user_id, "business_id": business_id, "text": text, "stars": stars}

		insert_id = db.reviewInfo.insert_one(new_review).inserted_id
		if insert_id is not None:
			print("Review added successfully...!\nReview Id: %s" % review_id)
		else:
			print("Error in adding review...! Add review again...!")
	print()
	

# use case 2
def search_business_by_ratings():
	rating = int(input("Enter rating: "))
	db = get_client_db()
	count_business = db.businessInfo.find({"stars": rating}, {"name": 1}).count()
	if count_business > 0:
		print("There are %d business with rating %.1f." % (count_business, rating))
		cursor = db.businessInfo.find({"stars": rating}, {"_id": 0, "name": 1}).limit(15)
		i = 1
		for row in cursor:
			print("%d. %s " % (i, row["name"]))
			i += 1
	else:
		print("No business with rating %.1f...!" % rating)
	print()


# use case 3
def search_business_by_type():
	category = input("Enter type of business: ")
	db = get_client_db()
	regx = re.compile(category, re.IGNORECASE)
	count_business = db.businessInfo.find({"categories": {'$regex': regx}}).count()
	if count_business > 0:
		print("There are %d business with category %s." % (count_business, category))
		cursor = db.businessInfo.find({"categories": {'$regex': regx}}).limit(15)
		i = 1
		for row in cursor:
			print("%d. %s " % (i, row["name"]))
			i += 1
	else:
		print("No business with category %s...!" % category)
	print()


# use case 4
def get_review_by_date():
	date = input("Enter date in YYYY-MM-DD: ")
	db = get_client_db()
	regx = re.compile("^"+date, re.IGNORECASE)
	count_review = db.reviewInfo.find({"date": {'$regex': regx}}).count()
	if count_review > 0:
		print("There are %d reviews with date %s." % (count_review, date))
		cursor = db.reviewInfo.find({"date": {'$regex': regx}}).limit(15)
		i = 1
		for row in cursor:
			print("%d. %s - %d" % (i, row["text"][:100], row["stars"]))
			i += 1
	else:
		print("No review with %s...!" % date)
	print()


# use case 5
def search_business_by_local_area():
	city = input("Enter City: ")
	state = input("Enter State: ")
	db = get_client_db()
	count_business = db.businessInfo.find({"city": city, "state": state}, {"name": 1}).count()
	if count_business > 0:
		print("There are %d business in  city %s and state %s." % (count_business, city, state))
		cursor = db.businessInfo.find({"city": city, "state": state}, {"name": 1}).limit(15)
		i = 1
		for row in cursor:
			print("%d. %s " % (i, row["name"]))
			i += 1
	else:
		print("No business in city %s and state %s...!" % (city, state))
	print()


# use case 6
def delete_review_by_user():
	user_id = input("Enter User Id: ")
	review_id = input("Enter Review Id: ")
	db = get_client_db()
	count_user = db.userInfo.find({"user_id": user_id}).count()
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
			print("Error in Deleting Review...! Delete Review again..!")
	print()


# use case 7
def update_characteristic_by_business():
	business_id = input("Enter Business Id: ")
	attr = input("Enter New Characteristic: ")
	db = get_client_db()
	count_business = db.businessInfo.find({"business_id": business_id}).count()
	cursor = db.businessInfo.find({"business_id": business_id}, {"postal_code": 1})
	for row in cursor:
		postal_code = row["postal_code"]
	if count_business == 0:
		print("Business Id does not exist...!")
	else:
		u = db.businessInfo.update_one({"postal_code": postal_code,"business_id": business_id}, {"$set": {"attributes."+attr: "True"}})
		if u is not None:
			print("Characteristic update successfully...!")
		else:
			print("Error in updating business characteristic...! Update again...!")	
	print()


# use case 8
def get_elite_user_by_year():
	year = input("Enter year: ")
	db = get_client_db()
	regx = re.compile(year, re.IGNORECASE)
	elite_count = db.userInfo.find({"elite": {'$regex': regx}}).count()
	if elite_count == 0:
		print("No elite user in %d." % year)
	else:
		print("There are %d elite users." % elite_count)
		cursor = db.userInfo.find({"elite": {'$regex': regx}}, {"name": 1}).limit(15)
		i = 1
		print("Elite user details: ")
		for row in cursor:
			print("%d. %s" % (i, row["name"]))
			i += 1
	print()


# use case 9
def get_most_useful_review():
	db = get_client_db()
	cursor = db.reviewInfo.find({}, {"review_id": 1, "stars": 1, "text": 1}).sort("useful", -1).limit(15)
	i = 1
	print("Top Useful Reviews: ")
	for row in cursor:
		print("%d. %s %s %s" % (i, row["review_id"], row["stars"], row["text"][:50]))
		i += 1
	print()


# use case 10
def search_user_with_highest_star():
	db = get_client_db()

	cursor = db.userInfo.find({}, {"name": 1}).sort("average_stars", -1).limit(15)
	i = 1
	print("Top highest star user: ")
	for row in cursor:
		print("%d. %s" % (i, row["name"]))
		i += 1
	print()


# use case 11
def update_review():
	review_id = input("Enter review_id: ")
	db = get_client_db()
	count_review = db.reviewInfo.find({"review_id": review_id}).count()
	cursor = db.reviewInfo.find({"review_id": review_id}, {"user_id": 1})
	for row in cursor:
		user_id = row["user_id"]
	if count_review == 0:
		print("Review Id does not exist...!")
	else:
		text = input("Enter review: ")
		cursor = db.reviewInfo.update_one({"user_id": user_id,"review_id": review_id}, {"$set": {"text": text}})
		if cursor.modified_count > 0:
			print("Review update successfully...!")
		else:
			print("Error in updating review...! Update again...!")
	print()


# use case 12
def delete_user_account():
	user_id = input("Enter user id: ")
	db = get_client_db()
	count_user = db.userInfo.find({"user_id": user_id}).count()
	cursor = db.userInfo.find({"user_id": user_id}, {"name": 1})
	for row in cursor:
		name = row["name"]
	if count_user == 0:
		print("User does not exist...!")
	else:
		cursor = db.userInfo.delete_one({"name": name,"user_id": user_id})
		if cursor.deleted_count == 0:
			print("Error in deleting user...! Delete again...!")
		else:
			print("User deleted successfully...!")
	print()


# use case 13
def get_cities_by_no_of_business():
	db = get_client_db()
	pipeline = [{"$group": {"_id": {"city": "$city", "state": "$state"}, "business_count": {"$sum": 1}}}, {
		"$sort": {"business_count": -1}}, {"$limit": 10}]
	cursor = db.businessInfo.aggregate(pipeline)
	print("List of businesses: ")
	for row in cursor:
		print("%s, %s has %d business." % (row["_id"]["city"], row["_id"]["state"], row["business_count"]))
	print()


# use case 14
def get_review_good_amazing():
	db = get_client_db()
	regx1 = re.compile("good", re.IGNORECASE)
	regx2 = re.compile("amazing", re.IGNORECASE)
	count_review = db.reviewInfo.find({"$or": [{"text": {'$regex': regx1}}, {"text": {'$regex': regx2}}]}).count()
	if count_review > 0:
		print("There are %d review that are %s or %s" % (count_review, "good", "amazing"))
		cursor = db.reviewInfo.find({"$or": [{"text": {'$regex': regx1}}, {"text": {'$regex': regx2}}]}).limit(15)
		i = 1
		for row in cursor:
			print("%d. %s " % (i, row["text"][:100]))
			i += 1
	else:
		print("No review that are %s or %s" % ("good", "amazing"))	
	print()


# use case 15
def get_business_by_postal_code():
	zipcode = input("Enter Postal Code: ")
	db = get_client_db()
	count_business = db.businessInfo.find({"postal_code": zipcode, "is_open": 1}, {"name": 1}).count()
	if count_business > 0:
		print("There are %d business open in zipcode %s." % (count_business, zipcode))
		cursor = db.businessInfo.find({"postal_code": zipcode, "is_open": 1}, {"_id": 0, "name": 1}).limit(15)
		i = 1
		for row in cursor:
			print("%d. %s " % (i, row["name"]))
			i += 1
	else:
		print("No business open in zipcode %s...!" % zipcode)
	print()
