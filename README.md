Log in address and view:

![alt text](readme_images/log_in.png)


Superuser navbar & logout:

![alt text](readme_images/superuser_view.png)


Common user navbar & logout:

![alt text](readme_images/other_user_view.png)


Page to see devices that are not available or need calibration:

**On top there is a button to send a summary by email to all users.

![alt text](readme_images/device_status.png)


Page to see all devices. PENDING: Option to filtter.

![alt text](readme_images/all_tools.png)


Small form for "renting users" to update device's properties:

*Controled_by field will authomaticatly update:

**IF user logged in changes location or device's avaliability to false THEN controled_by=user.authentified

**IF DEVICE'S location is (in this case Valencia, Spain) AND device's avaliability is True OR device's is_calibrating is True THEN controled_by=None
Temporal small form that opens when update device button is pressed:

![alt text](readme_images/form.png)


