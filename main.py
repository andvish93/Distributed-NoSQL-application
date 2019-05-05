from func import *

if __name__ == "__main__":
	options_string = '''<-------What would you like to do? Choose from below options---------->
	1. Write review on a particular business by a registered user.
	2. Search businesses by ratings(0 - 5).
	3. Search business by type(Eg. Mexican, Burgers, etc.).
	4. Get reviews given on a particular date.
	5. Retrieve businesses in a particular city and state.
	6. Delete a particular review made by that user.
	7. Update characteristics of a business(Eg: Vegan, For Children, Valet Parking, etc.).
	8. Get list of all elite user in a specified year.
	9. Fetch review that has received most useful votes.
	10. Obtain user names who has been rated with highest stars.
	11. Update the review made by user.
	12. Deletion of a user account.
	13. Get top cities by number of business in a city of a particular state.
	14. Obtain review that contains “good” and “amazing” as a keyword.
	15. Get list of business currently open in a particular postal code.
	16. To exit the menu options'''
	
	while True:
		print(options_string)
		choice = input("Enter your choice: ")
		if not choice.isnumeric():
			print("Bad Input....!")
			continue
		else:
			choice = int(choice)
		if choice == 16:
			break
		elif choice not in range(1, 16):
			print("Wrong Input...!")
		elif choice == 1:
			write_review_by_user()
		elif choice == 2:
			search_business_by_ratings()
		elif choice == 3:
			search_business_by_type()
		elif choice == 4:
			get_review_by_date()
		elif choice == 5:
			search_business_by_local_area()
		elif choice == 6:
			delete_review_by_user()
		elif choice == 7:
			update_characteristic_by_business()
		elif choice == 8:
			get_elite_user_by_year()
		elif choice == 9:
			get_most_useful_review()
		elif choice == 10:
			search_user_with_highest_star()
		elif choice == 11:
			update_review()
		elif choice == 12:
			delete_user_account()
		elif choice == 13:
			get_cities_by_no_of_business()
		elif choice == 14:
			get_review_good_amazing()
		elif choice == 15:
			get_business_by_postal_code()
		else:
			pass
