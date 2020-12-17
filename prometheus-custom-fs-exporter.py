from prometheus_client import make_wsgi_app, Gauge
from wsgiref.simple_server import make_server
import os, subprocess
import re


host = os.uname()[1]
g = Gauge('fs_disk_shortage', 'Check files system disk used percentage', ['host','file_system', 'disk_used_percentage',
                                                                          'mount_path'])


def generate():
    free_threshold = 0
    cmd_param = "0+$5 >= {} {{print $1, $5, $6}}".format(free_threshold)
    proc1 = subprocess.Popen(['df', '-h'], stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(['awk', cmd_param], stdin=proc1.stdout, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

    proc1.stdout.close()  # Allow proc1 to receive a SIGPIPE if proc2 exits.

    out, err = proc2.communicate()
    out = out.decode('utf-8')
    rows = out.strip().split('\n')

    for r in rows:
        # Skip header
        if not "Filesystem" in r :

            cols = re.split(' +', r)
            fsystem = cols[0]
            # disk_used_percent = int(cols[1])
            disk_used_percent = int(re.search(r'\d+', cols[1]).group())
            mount_path = cols[2]
            # print("aaa %s, %s" % (fsystem, disk_used_percent))
            if disk_used_percent > 90:
                g.labels(host, fsystem, disk_used_percent, mount_path).set(3)
                print("%s, %s" % (fsystem, "set to 3"))
            elif disk_used_percent > 80:
                g.labels(host, fsystem, disk_used_percent, mount_path).set(2)
                print("%s, %s" % (fsystem, "set to 2"))
            else:
                g.labels(host, fsystem, disk_used_percent, mount_path).set(0)
                print("%s, %s" % (fsystem, "set to 0"))


metrics_app = make_wsgi_app()


def my_app(environ, start_fn):
    if environ['PATH_INFO'] == '/metrics':
            generate()
            return metrics_app(environ, start_fn)


httpd = make_server('', 8000, my_app)
httpd.serve_forever()
