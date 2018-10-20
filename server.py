#!/bin/env/python


from app import *

if __name__ == "__main__":
    print("Running Flask Development Server on port 5000")
    rafael.jinja_env.auto_reload = True
    rafael.config["TEMPLATES_AUTO_RELOAD"] = True
    rafael.run(use_reloader=True)