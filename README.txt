We have upgraded from our beta version where we had a very crude face detection algorithm and 
were just able to confirm that we were able establish a communication between devices.

In this branch, we have upgraded our face recognition at the camera door-lock system and provided a web based interface.
Added features include:
	- Creating a log of unrecognized faces,
	-	Switched to SMS using Twilio for notification
	-	Have a remote camera (not directly connected to the main system)
	-       Used Sqlite and Flask for the backend.
