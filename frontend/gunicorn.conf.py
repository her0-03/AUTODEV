# Gunicorn Configuration for Render
# Optimized for long-running SSE connections

import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"
backlog = 2048

# Worker processes
workers = 2  # Free tier: 512MB RAM, 2 workers max
worker_class = "sync"
worker_connections = 1000
timeout = 300  # 5 minutes
keepalive = 300  # 5 minutes
graceful_timeout = 300  # 5 minutes

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "autodev-frontend"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (Render handles this)
keyfile = None
certfile = None
