# -*- coding: utf-8 -*-

ROUTES = {
    'routes.authorized': {
        'endpoint': 'authorized',
        'route': '/authorized',
        'methods': ['GET']
    },

    'routes.home': {
        'endpoint': 'home',
        'route': '/',
        'methods': ['GET']
    },

    'routes.login': {
        'endpoint': 'login',
        'route': '/login',
        'methods': ['GET']
    },

    'routes.logout': {
        'endpoint': 'logout',
        'route': '/logout',
        'methods': ['GET']
    },

    'routes.survey': {
        'endpoint': 'survey',
        'route': '/survey',
        'methods': ['GET', 'POST']
    },

    'routes.loadyaml': {
        'endpoint': 'loadyaml',
        'route': '/loadyaml',
        'methods': ['GET', 'POST']
    },


}