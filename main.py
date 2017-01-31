import webapp2
import cgi
import re
from string import letters

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User SignUp</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">FlickList</a>
    </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PW_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PW_RE.match(password)

Email_RE = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
def valid_email(email):
    return Email_RE.match(email)


class Index(webapp2.RequestHandler):

    def get(self):

        SignUp_header = "<h3>SignUp</h3>"

        # SignUp Form
        SignUp_form = """
        <form action="/Welcome" method="post">
            <label>
                Username:
                <input type="text" name="username"/>
            </label>
            <br>
             <label>
                Email (optional):
                <input type="text" name="Email"/>
            </label>
            <br>
            <label>
                Password:
                <input type="password" name="PW"/>
            </label>
            <br>
            <label>
                Verify Password:
                <input type="password" name="VPW"/>
            </label>
            <br>
            <input type="submit" value="Submit"/>
        </form>
        """

        # if we have an error, make a <p> to display it
        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""

        # combine all the pieces to build the content of our response
        main_content = SignUp_header + SignUp_form + error_element
        content = page_header + main_content + page_footer
        self.response.write(content)


class SignUp(webapp2.RequestHandler):

    def post(self):
        # look inside the request to figure out what the user typed
        # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
        # if the user wants to add a password that doesnt work
        username = self.request.get("username")
        username = cgi.escape(username, quote=True)
        PW = self.request.get("PW")
        VPW = self.request.get("VPW")
        PW = cgi.escape(PW, quote=True)
        VPW = cgi.escape(VPW, quote=True)
        Email = self.request.get("Email")
        Email = cgi.escape(Email, quote=True)
        params = dict(username = username, Email = Email)

        # if the user typed nothing at all, redirect and yell at them
        if username == "":
            errormessage = "Username"
            self.redirect("/?error=" + errormessage)
        
        # check username capatability
        if not valid_username(username):
            errormessage = "That username doesn't work"
            self.redirect("/?error=" + errormessage)



        params = dict(username = username, Email = Email)
        #check for a password
        if PW == "":
            errormessage = "Password"
            self.redirect("/?error=" + errormessage)
        
        #make sure passwords match
        if PW != VPW:
            errormessage = "Passwords do not match!"
            self.redirect("/?error=" + errormessage)

        #validate password
        if not valid_password(PW):
            errormessage = "That password doesn't work"
            have_error = True
            self.redirect("/?error=" + errormessage, **params)

        #validate email
        if not valid_email(Email):
            errormessage = "That email doesn't work"
            self.redirect("/?error=" + errormessage, **params)


        # build response content
        Welcome = "<strong>Welcome!</strong>"
        content = page_header + "<p>" + Welcome + "</p>" + page_footer
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/Welcome', SignUp),
], debug=True)

