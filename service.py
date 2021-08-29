from gen import Tree
from flask import Flask, jsonify, request
import demo_trees;
from demo_trees import trees
import reingold_thread;
from reingold_thread import reingold_tilford as rt
# from reingold_naive import reingold_tilford as rt
import buchheim;
from buchheim import buchheim
import importlib
from flask_cors import CORS


def mirror(t):
    if len(t.children) > 1:
        t.children = tuple(reversed(t.children))
    for c in t.children:
        mirror(c)
    return t


resArr = []

r = 100
rh = r * 1.4
rw = r * 1.1


def drawt(root, depth):
    global r
    # oval(root.x * rw, depth * rh, r, r)
    # fill(0)
    # fontsize(10)
    try:
        # print(root.x * rw + 4, depth * rh + rh / 5)
        resArr.append([-(depth * rh + rh / 5), root.x * rw + 4])
        # text("  %s\n%s,%s" % (root.tree, round(root.x, 2), round(root.mod)),
        # root.x * rw + 4, depth * rh + rh/5)
    except:
        pass
    # fill(1)
    for child in root.children:
        drawt(child, depth + 1)

def cleanRes():
    resArr.clear()


def drawconn(root, depth):
    for child in root.children:
        line(root.x * rw + (r / 2), depth * rh + (r / 2),
             child.x * rw + (r / 2), (depth + 1) * rh + (r / 2))
        drawconn(child, depth + 1)


def sign(x):
    if x == 0: return 0
    if x > 0:
        return 1
    else:
        return -1


from math import atan, sin, cos, pi


def dottedline(x1, y1, x2, y2):
    segment = 5
    if x2 == x1:
        theta = pi / 2
    elif x2 - x1 > 0:
        theta = atan(float(y2 - y1) / float(x2 - x1))
    else:
        theta = pi + atan(float(y2 - y1) / float(x2 - x1))

    dx = cos(theta) * segment
    dy = sin(theta) * segment
    xdir = x1 < x2
    ydir = y1 < y2

    while 1:
        if xdir != (x1 < x2) or ydir != (y1 < y2): break
        # line(x1, y1, x1 + dx, y1 + dy)
        x1, y1 = x1 + 2 * dx, y1 + 2 * dy


def drawthreads(root, depth):
    for child in root.children:
        c = child.thread
        if c:
            dottedline(child.x * rw + (r / 2), (depth + 1) * rh + (r / 2),
                       c.x * rw + (r / 2), (depth + 2) * rh + (r / 2))
        drawthreads(child, depth + 1)


# size(1200, 550)
# translate(2, 2)
# drawconn(t, 0)
# stroke(0,.4,.6)
# drawthreads(t, 0)
# stroke(0)
# fill(1,1,1)


app = Flask(__name__)  # 创建一个服务，赋值给APP
CORS(app, supports_credentials=True)


@app.route('/get_user', methods=['post'])  # 指定接口访问的路径，支持什么请求方式get，post
# key_values方式传参
def get_user():
    username = request.get_json()  # 获取接口请求中form-data的username参数传入的值
    str = username["command"]
    print(str)

    t = eval(str)

    t = buchheim(t)
    cleanRes()
    drawt(t, 0)
    return jsonify(resArr)


app.run(host='0.0.0.0', port=8802, debug=True)
'''
resArr = []
str = "Tree(\"root\",Tree(\"m\",Tree(\"leave1\"),Tree(\"leave2\")))"
t = eval(str)
t = buchheim(t)
drawt(t, 0)
print(resArr)
'''

