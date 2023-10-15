# Social Networking Site

## Login
To access the social media site, users need to log in with their credentials. This feature ensures the security and privacy of user accounts.

![Login](https://github.com/Masoudvahid/SocialNetworkingSite/blob/main/examples/login.png)
*Image: Login page of the social media site.*

## Chat
Users can communicate with each other through the chat feature. They can send messages, images, and multimedia files, fostering real-time conversations and connections.

![Chat](https://github.com/Masoudvahid/SocialNetworkingSite/blob/main/examples/chat.png)
*Image: Chat interface of the social media site.*

## Search
The search feature allows users to find other users, posts, and content relevant to their interests. It enhances user experience by enabling efficient and quick exploration of the platform.

![Search](https://github.com/Masoudvahid/SocialNetworkingSite/blob/main/examples/search.png)
*Image: Search functionality of the social media site.*

## Posts
Users can create, edit, and share posts on the platform. They can write text, attach images, and share their thoughts, experiences, and multimedia content with their followers.

![Posts](https://github.com/Masoudvahid/SocialNetworkingSite/blob/main/examples/posts.png)
*Image: Posts section of the social media site.*

## Friend Requests
Users send and recieve friend requests and restrict their profile to the people whom they want to

![Friend_requests](https://github.com/Masoudvahid/SocialNetworkingSite/blob/main/examples/friend_request.png)
*Image: Friend request section of the social media site.*



### Work done:

- [x] Login implemented
- [x] Implemented register page
- [x] Change structure of login urls
- [x] Register shows errors
- [x] Register and Login use Django forms instead of HTML
- [x] Added friends and friend requests
- [x] Added profile page
- [x] Fix avatar issue
- [x] Fix inheritance of templates
- [x] Use postgresql instead of sqlite
- [x] Add posts
- [x] Add comments
- [x] Add likes

### Notes:

- To create user for admin, use 'createsuperuser'
- Remember to make migrations to DB.
- Other less important fixes noted in files.

commands for initiating the app:  
`python manage.py collectstatic`  
`python manage.py makemigrations`  
`python manage.py migrate`  

to run the app you only need this:  
`python manage.py runserver`  
