import sys
import _ast

methods = ['get', 'post', 'put', 'delete']
router =  [] # (http method, route, func) tuples

def get(url):    route('get',    url)
def post(url):   route('post',   url)
def put(url):    route('put',    url)
def delete(url): route('delete', url)

def route(m, url):
  # http://github.com/sinatra/sinatra/blob/master/test/routing_test.rb
  for (method, route, func) in router:
    if method != m: continue
    if route == url:
      return getattr(davis_jr, func)()

def recompile(filename):
  ast = compile(open(filename).read(), filename, 'exec', _ast.PyCF_ONLY_AST)

  # find top level http verb methods
  for function in ast.body:
    if not type(function) is _ast.FunctionDef: continue
    if not function.name in methods: continue
    
    # hack args; extract url='route', inject params={}
    args = dict([(a[0].id, a[1]) for a in zip(function.args.args, function.args.defaults)])
    if not args.has_key('url'):
      continue
    route = args['url'].s

    if not args.has_key('params'):
      function.args.args.append(_ast.Name('params', _ast.Param(), lineno=0, col_offset=0))
      function.args.defaults.append(_ast.Dict(keys=[], values=[], lineno=0, col_offset=0))

    # rename method based on route
    name = function.name + route
    name = name.replace('*', ':splat')
    name = name.replace('/', '__')
    name = name.replace(':', 'param_')
    router.append((function.name, route, name))
    function.name = name
  
  return router, compile(ast, filename, 'exec')

def caller_filename():
  """Force an error, walk traceback to get caller's caller's frame"""
  try:
    1 + ''
  except:
    frame = sys.exc_traceback.tb_frame.f_back.f_back
    return frame.f_locals['__file__']

if __name__ != '__main__':
  """On import, recompile and exec the caller"""
  router, code = recompile(caller_filename())
  exec code
