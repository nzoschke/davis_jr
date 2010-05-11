import davis_jr

def get(url='/'):
  print 'GET /'

def post(url='/'):
  print 'POST /'

def put(url='/'):
  print 'GET /'

def delete(url='/'):
  print 'POST /'

def get(url='/hello/:name'):
  print 'GET hello %s' % params['name']

def get(url='/say/*/to/*'):
  print 'GET %s' % repr(params['splat'])

class helpers(object):
  def bar(name):
    return "%sbar" % name

if __name__ == '__main__':
  davis_jr.get('/')
  davis_jr.post('/')

