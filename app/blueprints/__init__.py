
from blueprints.auth import auth
from blueprints.conversation import chat
from blueprints.customer import customer
from blueprints.merchant import merchant
from blueprints.case import case
from blueprints.case_status import case_status

def register_blueprints(app):
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(case, url_prefix='/case')
    app.register_blueprint(case_status, url_prefix='/case_status')
    app.register_blueprint(chat, url_prefix='/chat')
    app.register_blueprint(customer, url_prefix='/customer')
    app.register_blueprint(merchant, url_prefix='/merchant')