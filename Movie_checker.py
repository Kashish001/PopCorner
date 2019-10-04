from  urllib.request import urlopen , Request
from bs4 import BeautifulSoup
import imdb
import re
import getpass
def Debit_checker(db_n):
	odd_sum=0
	even_sum=0
	for i in range(0,16):
		if((i+1)%2==0):
			even_sum+=int(db_n[i])
		else:
			y=int(db_n[i])*2
			a=y%10
			b=y//10
			odd_sum+=a+b
	if (odd_sum+even_sum)%10==0:
		print()
		passwd = getpass.getpass("Enter Your Pin : ")
		print()
		if passwd.lower() == 'correct':
			print("Congratulations!! Your Ticket Is Booked.")
			print()
		else:
			print("Pin is Incorrect!")
			print()
	else:
		print("Wrong! Debit Card Number ")
		print()
		
def cities():
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	req = Request(url='https://in.bookmyshow.com/', headers=headers) 
	html = urlopen(req).read() 
	bs = BeautifulSoup(html,'lxml')
	cities = bs.findAll('li',{'class':'city-name'})
	citys = []
	for i in cities:
		citys.append(re.sub(r'\s','',i.a.get_text()))
	return citys

def movies(city,lang):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	req = Request(url='https://in.bookmyshow.com/'+str(city.lower())+'/movies/'+str(lang), headers=headers) 
	html = urlopen(req).read() 
	bs = BeautifulSoup(html,'lxml')
	data = bs.findAll('div',{'class':'card-title'})
	ls = bs.findAll('div',{'class':'card-container wow fadeIn movie-card-container'},'a')
	list_of_movies = []
	for i in data:
		list_of_movies.append(i.h4.get_text())

	return list_of_movies

def __links_of_movies(city,lang):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	req = Request(url='https://in.bookmyshow.com/'+str(city.lower())+'/movies/'+str(lang.lower()), headers=headers) 
	html = urlopen(req).read() 
	bs = BeautifulSoup(html,'lxml')
	ls = bs.findAll('div',{'class':'card-container wow fadeIn movie-card-container'},'a')
	links_of_movies = {}
	for link in ls:
		x = link.a.get('title')
		y = link.a.get('href')
		links_of_movies[x] = y

	return links_of_movies

def ratings(li = []):
	rating = []
	db = imdb.IMDb()
	for i in li:
		search = db.search_movie(i)
		id = search[0].getID()
		movie = db.get_movie(id)
		rating.append([i,movie['rating']])
	print("This is a list of movies in your City with their specific ratings : "+str(rating))
	return rating

def link_of_that_movie_to_ticket(links_of_movies,movie):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	req = Request(url='https://in.bookmyshow.com'+str(links_of_movies[movie]), headers=headers) 
	html = urlopen(req).read() 
	bs = BeautifulSoup(html,'lxml')
	link = bs.findAll('div',{'class':'format-dimensions'})
	for l in link:
		link_to_ticket = l.a.get('href')
	return link_to_ticket

def cinemas(link):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	req = Request(url='https://in.bookmyshow.com'+str(link), headers=headers) 
	html = urlopen(req).read() 
	bs = BeautifulSoup(html,'lxml')
	cinema = bs.findAll('li',{'class':'list'})
	cinemas_and_codes = {}
	for i in cinema:
		cinemas_and_codes[i.get('data-name')] = i.get('data-id')
	return cinemas_and_codes

def __timings(link,cinema_code):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	req = Request(url='https://in.bookmyshow.com'+str(link), headers=headers) 
	html = urlopen(req).read() 
	bs = BeautifulSoup(html,'lxml')
	timing = bs.findAll('a',{'class':'__showtime-link time_vrcenter'})
	timing_dict = {}
	for i in timing:
		if i.get('data-venue-code') not in timing_dict:
			timing_dict[i.get('data-venue-code')] = [re.sub(r'\s','',i.get_text())]
		else:
			_y = re.sub(r'\s','',i.get_text())
			timing_dict[i.get('data-venue-code')].append(_y)
	return timing_dict[cinema_code]

def __seats(link,time,l_o_t,c_c):

	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	req = Request(url='https://in.bookmyshow.com'+str(link), headers=headers) 
	html = urlopen(req).read() 
	bs = BeautifulSoup(html,'lxml')
	seats_avail = bs.findAll('a',{'class':'__showtime-link time_vrcenter'})
	dict_of_VC_and_seats = {}
	for i in seats_avail:
		if i.get('data-venue-code') not in dict_of_VC_and_seats:
			dict_of_VC_and_seats[i.get('data-venue-code')] = [i.get('data-cat-popup')]
		else:
			dict_of_VC_and_seats[i.get('data-venue-code')].append(i.get('data-cat-popup'))

	for i in range(len(l_o_t)):
		if l_o_t[i] is time: 
			break
	list_of_seats = eval(dict_of_VC_and_seats[c_c][i][1:-1])
	dic_of_seats = {}
	print("Seats available at "+str(time)+" are : ",end="")
	for k in range(len(list_of_seats)):
		_x = eval(str(list_of_seats[k]))
		dic_of_seats[_x['desc']] = _x['price']
		print(str(_x['desc'])+" : "+str(_x['price'])+" : "+str(_x['availabilityText']) )
		print("                                 ",end="")
	print()
	return dic_of_seats

print()	
lang = input("Enter the Specific Language : ")
print()
city = input("Enter the City : ")
print()
movies_list = movies(city,lang)
ratings(movies_list)
print()
links = __links_of_movies(city,lang)
movie = input("Enter the Name of Movie : ")
print()
link = link_of_that_movie_to_ticket(links,movie)
cinemas = cinemas(link)
_j = 1
for i in cinemas.keys():
	if i is not None:
		print("Cinema Number "+str(_j)+" : "+str(i))
		_j += 1
print()
cinema = input("Enter the Name of Cinema : ")

timing_list = __timings(link,cinemas[cinema])
print()
print("Timings of "+str(cinema)+" are : "+str(timing_list))
print()
time = input("Enter the time of the Show : ")
print()
seat_price = __seats(link,time,timing_list,cinemas[cinema])
Selected_seat = input("Enter the Seat Brand you Want to Choose : ")
print()
no_of_seats = int(input("Enter No of Seats You Want : "))
print()
bill = 0
for i in range(no_of_seats):
	bill += float(seat_price[Selected_seat])
print("Your Total Bill is : "+str(bill))
print()
print("Mode of Payments : 1. Cash\t2. Debit Card\t3. Paytm\t4. UPI")
print()
pay_option = input("Enter the Mode of Payment : ")
print()
if pay_option == 'Cash':
	Print("Ticket Booked!!!! ")
	print()
elif pay_option == 'Debit Card':
	db_num = int(input("Enter Your Debit Card Number : "))
	Debit_checker(str(db_num))
	print()
elif pay_option == 'Paytm':
	Print("Ticket Booked!!!! ")
	print()
elif pay_option == 'UPI':
	Print("Ticket Booked!!!! ")
	print()


#---------------------------------------------------------------END-----------------------------------------------------











	




