import app from 'index';

class AuthPage {
    static factory(...injections) {
        return new AuthPage(...injections);
    }

    constructor($http, $state, $route) {
        this.$http = $http;
        this.$state = $state;
        this.signIn = {};
        this.signUp = {};
    }

    enter($http, $state, user) {
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
            localStorage.setItem('token', response.data.key);
            localStorage.setItem('email', user.email);
            $state.go('home');
        });
    }

    registration($http, $state, newUser) {
        let bDMonth = (newUser.bD.getMonth() < 10) ? '-0' : '-';
        bDMonth += newUser.bD.getMonth();
        let bDDate = (newUser.bD.getDate() < 10) ? '-0' : '-';
        bDDate += newUser.bD.getDate()
        const bD = newUser.bD.getFullYear() + bDMonth + bDDate;

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
                birth_date: bD,
                gender: Number(newUser.gender),
                password: newUser.password
            }
        }).then(response => {
            $state.reload();
        });
    }
}

AuthPage.factory.$inject = [
    '$http',
    '$state'
];

export default app.component('authPage', {
    templateUrl: 'pages/auth/auth.html',
    controller: AuthPage.factory
});
