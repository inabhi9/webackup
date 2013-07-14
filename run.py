#!/usr/bin/env python

from app import webackup
webackup.run(host='0.0.0.0', debug=True, port=2587, threaded=True)  # Start the server
