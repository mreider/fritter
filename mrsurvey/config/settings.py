# -*- coding: utf-8 -*-

ROUTES = {
    'routes.index': {
        'endpoint': 'index',
        'route': '/',
        'methods': ['GET']
    },

    'routes.authorized': {
        'endpoint': 'authorized',
        'route': '/authorized',
        'methods': ['GET']
    },

    'routes.home': {
        'endpoint': 'home',
        'route': '/home',
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