from flask import Flask

from .ip_pool import ip_pool_routes
from .misc import misc_routes
from .ne import ne_routes
from .unblock import unblock_routes
from .users import users_routes

main_routes = Flask(__name__, template_folder="../templates", static_folder="../static")
main_routes.config['SECRET_KEY'] = 'dc70c01d79c0afa0cb8b2f8b0f083f014457eb24fdc1f83fc87d33b2f47213ff'

main_routes.register_blueprint(ip_pool_routes)
main_routes.register_blueprint(misc_routes)
main_routes.register_blueprint(ne_routes)
main_routes.register_blueprint(unblock_routes)
main_routes.register_blueprint(users_routes)
