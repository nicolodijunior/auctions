# README
This project is an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”
The project is developed using Django, SQL, HTML, Bootstrap, CSS, and JavaScript.

#### Project Description

The website allows users to create a listing, make bids, comment, add it to the watchlist and, if the user is the owner of the listing, to end it and see the winner.
  
![CS50_Web__Commerce(1)](https://github.com/nicolodijunior/auctions/assets/101586266/fc2a77e0-26ef-4209-848c-04e7e8c79c8c)

![giphy](https://github.com/nicolodijunior/auctions/assets/101586266/44ccf60d-a2d6-4ab5-8e0d-79b77b6ebe62)

#### How to run the project

    0. Install Django
    run pip3 install Django in your terminal to install Django (you’ll also have to install pip)
    
    1. Clone the repository
    git clone https://github.com/nicolodijunior/auctions.git

    2. Navigate to the project directory
    cd auctions

    3. Create database tables
    python manage.py makemigrations
    python manage.py migrate
    
    4. Run the server
    python manage.py runserver

    5. Open the application 
    In a browser, visit http://127.0.0.1:8000/



#### Additional notes

    The project is developed using Django v3.2.8 and Python v3.9.7.
