import $stateProvider from 'angular';
import authPage from 'auth';
import app from 'index';

export default app.config(['$stateProvider', $stateProvider => {
    $stateProvider.state('auth', {
        url: '/auth',
        component: 'authPage'
    });
}]);
