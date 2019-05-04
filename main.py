from func import *

if __name__ == "__main__":
	options_string = '''<-------What would you like to do? Choose from below options---------->
	1. Users write and publish reviews
	2. Search business by ratings
	3. Search business by type
	4. Search rating(????) by date
	5. Users can search local area
	6. Ability to delete reviews made by users
	7. Business wants to update characteristics
	8. Search by hours of operation
	9. Review that is most usefu;
	10. Search user with highest stars
	11. Delete/Update a review
	12. Delete a User account
	13. Year when most users joined
	14. Review that contains “good”, “amazing”
	15. Business currently open in particular postal code.
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
			write_publish_review_by_user()
		elif choice == 2:
			search_business_by_ratings()
		elif choice == 3:
			search_business_by_type()
		elif choice == 4:
			search_rating_by_date()
		elif choice == 5:
			search_business_by_local_area()
		elif choice == 6:
			delete_review_by_user()
		elif choice == 7:
			update_characteristic_by_business()
		elif choice == 8:
			search_by_hours_of_operation()
		elif choice == 9:
			get_most_useful_review()
		elif choice == 10:
			search_user_with_highest_star()
		elif choice == 11:
			delete_or_update_review()
		elif choice == 12:
			delete_user_account()
		elif choice == 13:
			get_year_when_most_user_joined()
		elif choice == 14:
			get_review_good_amazing()
		elif choice == 15:
			get_business_by_postal_code()
		else:
			pass