from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from app.grpc_client import GRPCClient
from app.kafka_client import KafkaClient

db = SQLAlchemy()
grpcClient = GRPCClient()
kafkaClient = KafkaClient()


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    config = config_by_name[env or "test"]

    app = Flask(__name__)
    app.config.from_object(config)
    api = Api(app, title="UdaConnect API", version="0.1.0")

    CORS(app)  # Set CORS for development

    grpcClient.config(config.GRPC_LOCATION_HOST, config.GRPC_LOCATION_PORT, config.GRPC_PERSON_HOST, config.GRPC_PERSON_PORT)
    kafkaClient.config(config.KAFKA_HOST, config.KAFKA_PORT)

    register_routes(api, app)
    db.init_app(app)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
