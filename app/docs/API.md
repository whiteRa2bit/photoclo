# API
* Authorization:
	* /api/sign_in/ - sign in account, requires username and password.
		* POST: username and password
			* HTTP\_CODE: 200 - STATUS: OK, return token in data.
			* HTTP\_CODE: 400 - STATUS: error BAD\_REQUEST, no username or password.
			* HTTP\_CODE: 404 - STATUS: error NOT\_FOUND, username or password are incorrect.
	* /api/sign_up/ - sign up account, requires username, email and password.
		* POST: username, password and email
			* HTTP\_CODE: 200 - STATUS: OK, return token in data.
			* HTTP\_CODE: 400 - STATUS: error BAD\_REQUEST, no username, password or email.
			* HTTP\_CODE: 409 - STATUS: error CONFLICT, user with this username already exists.
			* HTTP\_CODE: 500 - STATUS: error INTERNAL\_SERVER\_ERROR, error in saving user, it don't relate with usernames conflict.
	* /api/sign_out/ - sign out account. If there is no open session, return HTTP code 200.
		* POST: nothing
			* HTTP\_CODE: 200 - STATUS: OK, return nothing.