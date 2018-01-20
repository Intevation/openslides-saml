(function () {

'use strict';

angular.module('OpenSlidesApp.openslides_saml.site', [
    'OpenSlidesApp.openslides_saml',
])

.run([
    'templateHooks',
    '$http',
    function (templateHooks, $http) {
        templateHooks.registerHook({
            Id: 'loginFormButtons',
            // I do not know, why the href attribute does not work here. But with JS setting the
            // window.location works...
            template:   '<a href="/saml/?sso" class="btn btn-primary pull-right" translate ng-click="samlLogin()">' +
                            'Login via SAML' +
                        '</a>',
            noDivWrap: true,
            scope: {
                samlLogin: function () {
                    window.location = "/saml/?sso";
                },
            },
        });
    }
])

})();
