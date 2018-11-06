import os

from hose_app.app import create_app

application = create_app()

if __name__ == '__main__':
    application.run(
        # host=os.environ.get('SERVICE_HOST'),
        # port=os.environ.get('SERVICE_PORT'),
        debug=True
    )

