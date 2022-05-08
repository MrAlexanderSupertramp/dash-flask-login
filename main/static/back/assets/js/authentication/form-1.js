var togglePassword = document.getElementById("toggle-password");

if (togglePassword) {
	togglePassword.addEventListener('click', function() {
	  var x = document.getElementById("password");
	  var y = document.getElementById("password-repeat");
	  if (x.type === "password") {
		  if(x){
			x.type = "text";
		  }
		  if(y){
			y.type = "text";
		  }
	  } else {
		if(x){
			x.type = "password";
		  }
		  if(y){
			y.type = "password";
		  }
	  }
	});
}
