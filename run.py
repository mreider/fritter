from mrsurvey import main
import os

port = int(os.getenv("PORT", 5000))
main.app.run(host='0.0.0.0', port=port,debug=True)
