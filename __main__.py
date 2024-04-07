import logging
from api import app
import uvicorn


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                               ' - (Line: %(lineno)d [%(filename)s - %(funcName)s])')
    try:
        uvicorn.run(app)
    except KeyboardInterrupt:
        print('Exit')
