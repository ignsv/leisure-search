import app from 'index';

class HeaderSection {
    static factory(...injections) {
        return new HeaderSection(...injections);
    }

    constructor($state, $http) {
        this.$state = $state;
        this.$http = $http;

        this.token = localStorage.getItem('token');
    }

    signOut($state, $http) {
        localStorage.removeItem('token');
        localStorage.removeItem('email');
        $state.go('auth');
    }
}

HeaderSection.factory.$inject = [
    '$state',
    '$http'
];

export default app.component('headerSection', {
    templateUrl: 'components/header-section/header-section.html',
    controller: HeaderSection.factory
});
