import app from 'index';

class AuthPage {
    static factory(...injections) {
        return new AuthPage(...injections);
    }

    constructor($http) {
        this.$http = $http;
        this.signIn = {};
        this.signUp = {};
    }

    enter($http, user) {
        console.log(user);
        $http({
            method: 'POST',
            url: 'http://localhost:8000/' + 'api/rest-auth/login/',
            headers: {
                'Content-Type': 'application/json'
            },
            data: {
                email: user.email,
                password: user.password
            }
        }).then(response => {
          console.log(response);
        });
    }

    registration($http, newUser) {
        $http({
            method: 'POST',
            url: 'http://localhost:8000/' + 'api/users/register/',
            headers: {
                'Content-Type': 'application/json'
            },
            data: {
                email: newUser.email,
                first_name: newUser.first,
                last_name: newUser.last,
                birth_date: newUser.bD,
                gender: Number(newUser.gender),
                password: newUser.password
            }
        }).then(response => {
            console.log(response);
        });
    }
}

AuthPage.factory.$inject = [
  '$http'
];

export default app.component('authPage', {
    templateUrl: 'pages/auth/auth.html',
    controller: AuthPage.factory
});
