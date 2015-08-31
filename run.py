from mrsurvey import main
import os
import MySQLdb

port = int(os.getenv("PORT"))
main.app.run(host='0.0.0.0', port=port,debug=True)
