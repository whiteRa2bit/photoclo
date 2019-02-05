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
* Photos:
    * /api/photos/ - return photos
        * GET: offset, limit and size.
            * HTTP\_CODE: 200 - STATUS: OK, return amount of photos in `count` and list of photos in needed size, where is heights, width and urls.
            * HTTP\_CODE: 411 - STATUS: error LENGTH\_REQUIRED, no limit was sent.
            * HTTP\_CODE: 416 - STATUS: error REQUESTED\_RANGE\_NOT\_SATISFIABLE, offset is grater than amount of photos in a server.
        * POST: photo
            * HTTP\_CODE: 201 - STATUS: OK, return nothing.
            * HTTP\_CODE: 400 - STATUS: error BAD\_REQUEST, bad photo to upload.
            * HTTP\_CODE: 500 - STATUS: error INTERNAL\_SERVER\_ERROR, error not in the saving process.
            * HTTP\_CODE: 507 - STATUS: error INSUFFICIENT\_STORAGE, error in saving photo at the server.(After adding cloud support it can be changed)
    * /api/photos/\<id\>/ - open or delete photo by id
        * GET: nothing
            * HTTP\_CODE: 200 - STATUS: OK, return url for full-size photo.
            * HTTP\_CODE: 404 - STATUS: error NOT\_FOUND, there is no photo with this id.
            * HTTP\_CODE: 423 - STATUS: error LOCKED, photo is locked.
        * DELETE: nothing
            * HTTP\_CODE: 200 - STATUS: OK, return nothing.
            * HTTP\_CODE: 404 - STATUS: error NOT\_FOUND, there is no photo with this id.
            * HTTP\_CODE: 423 - STATUS: error LOCKED, photo is locked for delete.
    * /api/photos/\<id\>/download/ - download photos by id
        * GET: nothing
            * HTTP\_CODE: 200 - STATUS: OK, return url to download original.
            * HTTP\_CODE: 404 - STATUS: error NOT\_FOUND, there is no photo with this id.
            * HTTP\_CODE: 507 - STATUS: error INSUFFICIENT\_STORAGE, cannot reach original. 