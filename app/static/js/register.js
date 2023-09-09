$( document ).ready(function() {
  $( "#tabs1" ).on("click", function( event ) {
	var v1 = "<div id=\"#replaced\">{{ form.username.label }}<br>{{ form.username(size=64) }}<br>{% for error in  form.username.errors %}<span style=\"color: red;\">[{{ error }}]</span>{% endfor %}{{ form.email.label }}<br>{{ form.email(size=120) }}<br>{% for error in form.email.errors %}<span style=\"color: red;\">[{{ error }}]</span>{% endfor %}{{ form.phone.label }}<br>{{ form.phone(size=20) }}<br>{% for error in form.phone.errors %}<span style=\"color:  red;\">[{{ error }}]</span>{% endfor %}{{ form.address.label }}<br>{{ form.address(size=120) }}<br>{% for error in  form.address.errors %}<span style=\"color: red;\">[{{ error }}]</span>{% endfor %}{{ form.about.label }}<br>{{  form.about(size=140) }}<br>{% for error in form.about.errors %}<span style=\"color: red;\">[{{ error }}]</span>{% endfor %}</div>";
    $("#replaced").replaceWith (v1);
    event.stopPropagation();
	alert( v1 );
  });
//});

//$(document).ready(function() {
  $( "#tabs2, #tabs3" ).on("click", function( event ) {
	var v23 = "<div id=\"#replaced\">{{ form.username.label }}<br>{{ form.username(size=64) }}<br>{% for error in form.username.errors %}<span style=\"color: red;\">[{{ error }}]</span>{% endfor %}{{ form.email.label }}<br>{{ form.email(size=120) }}<br>{% for error in form.email.errors %}<span style=\"color: red;\">[{{ error }}]</span>{% endfor %}{{ form.phone.label }}<br>{{ form.phone(size=20) }}<br>{% for error in form.phone.errors %}<span style=\"color: red;\">[{{ error }}]</span>{% endfor %}{{ form.address.label }}<br>{{ form.address(size=120) }}<br>{% for error in form.address.errors %}<span style=\"color: red;\">[{{ error }}]</span>{% endfor %}</div>";
    $("#replaced").replaceWith(v23);
    event.stopPropagation();
	alert( v23 );
  });
//});
  
//$(document).ready(function() {
  $( "#tabs4" ).on("click", function( event ) {
	var v4 = "<div id=\"#replaced\">{{ form.username.label }}<br>{{ form.username(size=64) }}<br>{% for error in  form.username.errors %}<span style=\"color: red;\">[{{ error }}]</span>{% endfor %}{{ form.email.label }}<br>{{ form.email(size=120) }}<br>{% for error in form.email.errors %}<span style=\"color: red;\">[{{ error }}]</span>{% endfor %}</div>";
    $("#replaced").replaceWith(v4);
    event.stopPropagation();
    alert( v4 );
  });
});
