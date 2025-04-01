# from Core import Pipeline
# from Core.backend import app
# import config as C


# # Global variable to stop double execution
# _has_executed = False

# # Function safety wrapper for object instantiation only once
# def runPipeline():
#     global _has_executed
#     if not _has_executed:
#         Pipeline(C.DB_CONFIG, C.API_CONFIG, C.REF_SEQS).run()
#         _has_executed = True
#     return None

# # Run with app_context to try to execute on top of app declaration
# with app.app_context():
#     # Run All DB Tests and Ops
#     runPipeline()

# app
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World'


if __name__ == '__main__':
    # Run All DB Tests and Ops
    pass
    # runPipeline()

    # # Serve up flask API
    # app.run(debug = False, use_reloader = False)