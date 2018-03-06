# -*- coding: utf-8 -*-
"""KB Manager
"""
import os
import json
from flask import request, session, send_from_directory
from werkzeug import secure_filename
from .app import app, files
from .graph import Database
# from .sql import Database
from .semantic import get_tag

# 初始化知识库
database = Database(password="train", userid="A0001")

img_formats = {'png', 'jpg', 'jpeg', 'gif', 'xls'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in img_formats

def get_username():
    user = database.selector.select("User").where("_.userid ='A0001'").first()
    return user['robotname']

def get_available_kb():
    kb = []
    match_str = "MATCH (user:User {userid: 'A0001'})\
        -[r:has {available:1}]->(config:Config) RETURN config.name as name"
    for item in database.graph.run(match_str):
        kb.append(item['name'])
    return kb

def get_selected_kb():
    kb = []
    match_str = "MATCH (user:User {userid: 'A0001'})-[r:has {bselected:1, available:1}] \
        ->(config:Config) RETURN config.name as name"
    for item in database.graph.run(match_str):
        kb.append(item['name'])
    return kb

@app.route("/data/<path:path>")
def root_data(path):
    """Root path of data reference. 数据资源引用路径。
    
    1.出于安全原因，该函数不允许客户端直接读取任何*.py代码文件；
    2.所有其他类型的文件将被映射到项目的 data 目录中。
    """
    state = {
        'success' : 0,
        'message' : "不允许客户端直接读取任何*.py代码文件"
    }
    if path.rfind('py') > (len(path)-4):
        return json.dumps(state)
    data_path = os.environ.get("ApiData") # 该API服务的数据源
    return send_from_directory(data_path, path)

def __user_kb(request):
    """Get session kb. 获取 session 的已选知识库名称。
    """
    return session.get('kb', '')

def __is_login():
    """Return user login status. 返回用户登录状态。
    """
    return session.get('islogin', False)

def __check_login(_kb):
    """Check kb. 验证用户名和密码。
    """
    _state = {
        'success' : False,
        'message' : ''
    }
    try:
        if _kb:
            _state['success']  = True
        else:
            _state['message'] = 'KB incorrect.'
    except:
        _state['message'] = 'KB does not exist.'
    return _state

def __do_login(_kb):
    """登录核心操作。
    """
    _state = __check_login(_kb)
    if _state['success']:
        session['islogin'] = True
        session['kb'] = _kb
    return _state

# ==============================API 接口================================
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """登录：获取可用知识库列表并选择要维护的知识库。
    """
    data = {
        'akb': get_available_kb(),
        'skb': database.skb
    }
    if request.method == 'POST':
        pdata = request.form.to_dict()
        data.update(pdata)
        if data['skb']:
            database.skb = data['skb']
    return json.dumps(data)

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    """Signout. 退出。
    """
    session.pop('kb', None)
    session.pop('islogin', None)
    database.skb = ''
    state = {
        'success' : 1,
        'message' : "退出成功"
    }
    return json.dumps(state)

@app.route('/skb', methods=['GET'])
def get_skb():
    """获取当前知识库名称
    """
    data = {
        'skb': database.skb
    }
    return json.dumps(data)

@app.route("/user/edit", methods=['GET', 'POST'])
def user_edit():
    """编辑用户信息
    """
    data = database.selector.select("User").where("_.userid ='A0001'").first()
    if request.method == 'POST':
        pdata = request.form.to_dict()
        data.update(pdata)
        database.graph.push(data)
        state = {
            'success' : 1,
            'message' : "修改信息成功"
        }
        return json.dumps(state)
    return json.dumps(data)

@app.route("/scene/error", methods=['GET', 'POST'])
def scene_error():
    """场景 error_page
    """
    user = database.selector.select("User").where("_.userid ='A0001'").first()
    data = {
        'error_page': user['error_page']
    }
    if request.method == 'POST':
        pdata = request.form.to_dict()
        user.update(pdata)
        database.graph.push(user)
        state = {
            'success' : 1,
            'message' : "修改错误提示成功"
        }
        return json.dumps(state)
    return json.dumps(data)

@app.route('/reset', methods=['POST'])
def reset():
    """Reset 用用户上传的知识库重置用户所有已有知识库。
    """
    if request.method == 'POST':
        state = {
            'success' : 0,
            'message' : "上传知识库文件后缀应该是.xls"
        }
        f = request.files['file']
        if allowed_file(f.filename):
            filename = 'C:/nlu/data/upload/' + secure_filename(f.filename)
            f.save(filename)
            # 删除配置
            database.graph.run("MATCH (n:Config) DETACH DELETE n")
            # 重新导入
            database.reset(filename=filename)
            state['success'] = 1
            state['message'] = "重置知识库成功"
        return json.dumps(state)

@app.route('/upload', methods=['POST'])
def upload():
    """Upload 上传
    对已存在的节点覆盖，对不存在的追加。
    TODO：只对该用户有权限的知识库有效，无权限的知识库导入无效。
    """
    if request.method == 'POST':
        state = {
            'success' : 0,
            'message' : "上传知识库文件后缀应该是.xls"
        }
        f = request.files['file']
        if allowed_file(f.filename):
            # 采用绝对路径
            filename = 'C:/nlu/data/upload/' + secure_filename(f.filename)
            f.save(filename)
            # 对已存在的节点覆盖，对不存在的追加
            database.handle_excel(filename=filename)
            state['success'] = 1
            state['message'] = "上传知识库成功"
        return json.dumps(state)

@app.route('/upload/img', methods=['POST'])
def upload_img():
    """Upload img. 上传图片
    """
    if request.method == 'POST':
        state = {
            'success' : 0,
            'message' : "上传图片后缀支持 png, jpg, jpeg, gif 格式",
            'url': ""
        }
        f = request.files['file']
        if allowed_file(f.filename):
            # 采用绝对路径
            filename = 'C:/nlu/data/img/' + secure_filename(f.filename)
            f.save(filename)
            state['success'] = 1
            state['message'] = "上传图片成功"
            state['url'] = filename
        return json.dumps(state)

@app.route('/download/img', methods=['POST'])
def download_img():
    """Download img. 下载图片
    """
    if request.method == 'POST':
        pdata = request.form.to_dict()
        state = {
            'success' : 0,
            'message' : "找不到图片"
        }
        filepath, filename = os.path.split(pdata['url'])
        if allowed_file(filename):
            return send_from_directory(filepath, filename)
        return json.dumps(state)

@app.route('/download', methods=['GET', 'POST'])
def download():
    """Download 下载
    Get   获取全部知识库的 xls 文件
    POST 获取所选知识库的 xls 文件
    """
    if request.method == 'POST':
        database.dkb = request.form.to_dict()['skb'].split()
    if not database.dkb:
        database.dkb = get_available_kb()
    database.download(filename='C:/nlu/data/download/kb.xls', names=database.dkb)
    return send_from_directory('C:/nlu/data/download', 'kb.xls')

@app.route('/config/manage', methods=['GET', 'POST'])
def config_manage():
    """Config manage. 知识库配置。
    """
    akb = get_available_kb()
    skb = get_selected_kb()
    data = {'bkb': {k: 1 if k in skb else 0 for k in akb}}
    if request.method == 'POST':
        state = {
            'success' : 0,
            'message' : "参数传递错误"
        }
        pdata = request.form.to_dict()
        try:
            skb = pdata['skb'].split()
        except:
            return json.dumps(state)
        fkb = list(set(akb).difference(set(skb)))
        for name in skb:
            match_str = "MATCH (user:User {userid: 'A0001'})-[r:has {available: 1}]\
                ->(config:Config {name: '" + name + "'}) SET r.bselected=1"
            database.graph.run(match_str)
        for name in fkb:
            match_str = "MATCH (user:User {userid: 'A0001'})-[r:has {available: 1}]\
                ->(config:Config {name: '" + name + "'}) SET r.bselected=0"
            database.graph.run(match_str)
        state['success'] = 1
        state['message'] = "挂接知识库成功"
        return json.dumps(state)
    return json.dumps(data)

@app.route("/config/add", methods=['GET', 'POST'])
def config_add():
    """添加知识库
    """
    akb = get_available_kb()
    skb = get_selected_kb()
    data = {'bkb': {k: 1 if k in skb else 0 for k in akb}}
    if request.method == 'POST':
        state = {
            'success' : 0,
            'message' : "新建知识库不能为空或者与已有知识库重名"
        }
        name = request.form.to_dict()['kb']
        # 确保节点唯一性
        if not name or database.selector.select("Config").where("_.name ='" + name + "'").first():
            return json.dumps(state)
        match_str = "MATCH (user:User {userid: 'A0001'}) \
            MERGE (user)-[r:has {bselected:1, available:1}]->\
            (config:Config {name: '" + name + "', topic: ''})"
        database.graph.run(match_str)
        state['success'] = 1
        state['message'] = "新建知识库成功"
        return json.dumps(state)
    return json.dumps(data)

@app.route("/config/delete", methods=['GET', 'POST'])
def config_delete():
    """用户删除知识库/知识库权限
    """
    akb = get_available_kb()
    skb = get_selected_kb()
    data = {'bkb': {k: 1 if k in skb else 0 for k in akb}}
    if request.method == 'POST':
        state = {
            'success' : 0,
            'message' : "要删除的知识库名不能为空或不存在"
        }
        name = request.form.to_dict()['kb']
        # 删除该用户有权限的知识库，无权限的同名知识库不能删除
        if not name or not name in akb:
            return json.dumps(state)
        config = database.selector.select("Config", name=name).first()
        # 删除该 Config 节点属性 topic 对应的所有 NluCell 节点
        database.graph.run("MATCH (n:NluCell) WHERE '" + config['topic'] \
            + "' CONTAINS n.topic DELETE n")
        # 删除该 Config 节点及其关系
        match_str = "MATCH (user:User {userid: 'A0001'})-[r:has]->\
            (config:Config {name: '" + name + "'}) DELETE r, config"
        database.graph.run(match_str)
        state['success'] = 1
        state['message'] = "删除知识库成功"
        return json.dumps(state)
    return json.dumps(data)

@app.route("/config/delete/admin", methods=['GET', 'POST'])
def config_delete_admin():
    """管理员删除知识库
    多知识库管理由管理员统一对用户权限进行操作，不支持用户删除知识库。
    """
    pass

@app.route("/search/nlucell", methods=['GET', 'POST'])
def search_nlucell():
    """Search NluCell 搜索问答节点
    Get：返回所有问答节点
    POST：返回所有包含搜索关键词的问答节点
    """
    data = {
        'skb': database.skb,
        'result': []
    }
    state = {
        'success' : 0,
        'message' : "请先选择知识库再搜索节点"
    }
    if not database.skb:
        return json.dumps(state)
    if request.method == 'POST':
        pdata = request.form.to_dict()
        subgraph = database.graph.run(
            "MATCH (n:NluCell) WHERE n.name CONTAINS '" \
            + pdata['name'] + "' and n.topic='" + database.skb + \
            "' and n.tid='' RETURN n").data()
    else:
        subgraph = database.graph.run("MATCH (n:NluCell) WHERE n.topic='" + \
            database.skb + "' and n.tid='' RETURN n").data()
    data['result'] = [each['n'] for each in subgraph]
    return json.dumps(data)

@app.route("/search/scene", methods=['GET', 'POST'])
def search_scene():
    """Search Scene 搜索场景节点
    Get：返回所有场景根节点
    POST：返回所有包含搜索关键词的场景节点
    """
    data = {
        'skb': database.skb,
        'result': []
    }
    state = {
        'success' : 0,
        'message' : "请先选择知识库再搜索节点"
    }
    skb = database.selector.select("Config").where("_.name ='" + database.skb + "'").first()
    if not skb:
        return json.dumps(state)
    if request.method == 'POST':
        pdata = request.form.to_dict()
        if not pdata['name']:
            state['message'] = "问题不能为空"
            return json.dumps(state)
        subgraph = database.graph.run("MATCH (n:NluCell) WHERE n.name CONTAINS '" \
            + pdata['name'] + "' and '" + skb['topic'] + "' CONTAINS n.topic and n.tid<>'' RETURN n").data()
    else:
        subgraph = database.graph.run("MATCH (n:NluCell) WHERE '" + skb['topic'] \
            + "' CONTAINS n.topic and n.tid=0 RETURN n").data()
    data['result'] = [each['n'] for each in subgraph]
    return json.dumps(data)
    
@app.route("/nlucell/item", methods=['GET', 'POST'])
def nlucell_item():
    """根据 name 获取问答节点列表
    Get：返回所有问答节点
    POST：返回所有 name 包含关键词的问答节点
    """
    data = {
        'skb': database.skb,
        'result': []
    }
    state = {
        'success' : 0,
        'message' : "请先选择知识库再搜索节点"
    }
    if not database.skb:
        return json.dumps(state)
    if request.method == 'POST':
        pdata = request.form.to_dict()
        subgraph = database.graph.run(
            "MATCH (n:NluCell) WHERE n.name CONTAINS '" \
            + pdata['name'] + "' and n.topic='" + database.skb + \
            "' and n.tid='' RETURN n").data()
    else:
        subgraph = database.graph.run("MATCH (n:NluCell) WHERE n.topic='" + \
            database.skb + "' and n.tid='' RETURN n").data()
    data['result'] = [each['n'] for each in subgraph]
    return json.dumps(data)

@app.route("/nlucell/add", methods=['GET', 'POST'])
def nlucell_add():
    """添加问答节点
    """
    data = {
        'akb': get_available_kb(),
        'skb': database.skb
    }
    if request.method == 'POST':
        state = {
            'success' : 0,
            'message' : "问题不能为空"
        }
        pdata = request.form.to_dict()
        if not pdata['name']:
            return json.dumps(state)
        skb = database.selector.select("Config", name=database.skb).first()
        # 追加并更新可用话题集(问答 topic=database.skb)
        if skb:
            match_str = "MATCH (n:NluCell {name:'"+ pdata['name'] + "'}) WHERE '" \
                + skb['topic'] + "' CONTAINS n.topic RETURN n"
            node = list(database.graph.run(match_str).data())
            if node:
                state['message'] = "问题已存在"
                return json.dumps(state)
            topics = skb['topic'].split(",") if skb['topic'] else []
            topics.append(database.skb)
            skb['topic'] = ",".join(set(topics))
            database.graph.push(skb)
            database.add_nlucell(
                name=pdata['name'],
                content=pdata['content'],
                topic=database.skb,
                delimiter="|"
            )
            state['success'] = 1
            state['message'] = "添加问答成功"
            return json.dumps(state)
        else:
            state['message'] = "请先选择知识库再添加问答"
            return json.dumps(state)
    return json.dumps(data)

@app.route("/nlucell/edit", methods=['GET', 'POST'])
def nlucell_edit():
    """编辑问答节点
    """
    data = {
        'akb': get_available_kb(),
        'skb': database.skb
    }
    if request.method == 'POST':
        state = {
            'success' : 0,
            'message' : "问题不能为空"
        }
        pdata = request.form.to_dict()
        name = pdata['pre_name']
        if not name or not pdata['name']:
            return json.dumps(state)
        node = database.selector.select("NluCell").where("_.name ='" + name + "'", \
            "_.topic ='" + database.skb + "'").first()
        if node:
            node['name'] = pdata['name']
            node['content'] = pdata['content']
            database.graph.push(node)

        else:
            # 问答不存在时直接创建新问答，topic=database.skb
            database.add_nlucell(
                name=pdata['name'],
                content=pdata['content'],
                topic=database.skb,
                delimiter="|"
            )
        state['success'] = 1
        state['message'] = "编辑问答成功"
        return json.dumps(state)
    return json.dumps(data)

@app.route("/nlucell/delete", methods=['GET', 'POST'])
def nlucell_delete():
    """删除问答节点
    """
    data = {
        'akb': get_available_kb(),
        'skb': database.skb
    }
    if request.method == 'POST':
        state = {
            'success' : 0,
            'message' : "问题不能为空"
        }
        pdata = request.form.to_dict()
        name = pdata['name']
        if not name:
            return json.dumps(state)
        node = database.selector.select("NluCell").where("_.name ='" + name + "'", \
            "_.topic ='" + database.skb + "'").first()
        if node:
            database.graph.delete(node)
            state['success'] = 1
            state['message'] = "删除问答成功"
            return json.dumps(state)
        else:
            state['message'] = "该问答不存在"
            return json.dumps(state)
    return json.dumps(data)

@app.route("/scene/topic", methods=['GET', 'POST'])
def scene_topic():
    """GET 返回当前所选知识库所有场景根节点
    POST：根据 topic, name, tid, ftid 获取唯一场景节点及其下一层子节点 Modify: 2018-1-30
    """
    data = {
        'skb': database.skb,
        'result': []
    }
    state = {
        'success' : 0,
        'message' : "请先选择知识库再搜索节点"
    }
    if not database.skb:
        return json.dumps(state)
    skb = database.selector.select("Config").where("_.name ='" + database.skb + "'").first()
    if request.method == 'POST':
        pdata = request.form.to_dict()
        match_node = "MATCH (n:NluCell) WHERE n.topic='" + pdata['topic'] + \
            "' and '" + skb['topic'] + "' CONTAINS n.topic and n.tid=" + \
            str(pdata['tid']) + " and n.ftid=" + str(pdata['ftid']) + " RETURN n"
        match_child = "MATCH (n:NluCell) WHERE n.topic='" + pdata['topic'] + \
            "' and '" + skb['topic'] + "' CONTAINS n.topic and n.tid<>n.ftid and n.ftid=" + \
            str(pdata['tid']) + " RETURN n"
        subgraph = database.graph.run(match_node).data()
        data['child'] = [each['n'] for each in database.graph.run(match_child).data()]
    else:
        subgraph = database.graph.run("MATCH (n:NluCell) WHERE '" + skb['topic'] \
            + "' CONTAINS n.topic and n.tid=0 RETURN n").data()
    data['result'] = [each['n'] for each in subgraph]
    return json.dumps(data)

@app.route("/scene/item", methods=['GET', 'POST'])
def scene_item():
    """根据 name 获取场景节点列表
    Get：返回所有场景节点
    POST：返回所有 name 包含关键词的场景节点
    """
    data = {
        'skb': database.skb,
        'result': []
    }
    state = {
        'success' : 0,
        'message' : "请先选择知识库再搜索节点"
    }
    if not database.skb:
        return json.dumps(state)
    skb = database.selector.select("Config").where("_.name ='" + database.skb + "'").first()
    if request.method == 'POST':
        pdata = request.form.to_dict()
        subgraph = database.graph.run(
            "MATCH (n:NluCell) WHERE n.name CONTAINS '" \
            + pdata['name'] + "' and '" + skb['topic'] + \
            "' CONTAINS n.topic and n.tid<>'' RETURN n").data()
    else:
        subgraph = database.graph.run("MATCH (n:NluCell) WHERE '" + skb['topic'] \
            + "' CONTAINS n.topic and n.tid<>'' RETURN n").data()
    data['result'] = [each['n'] for each in subgraph]
    return json.dumps(data)

@app.route("/scene/add", methods=['POST'])
def scene_add():
    """添加场景节点
    """
    if request.method == 'POST':
        state = {
            'success' : 0,
            'message' : "问题不能为空"
        }
        pdata = request.form.to_dict()
        if not pdata['name']:
            return json.dumps(state)
        # 确保新场景标签是全局唯一的
        all_topics = []
        for config in database.selector.select("Config"):
            all_topics.extend(config['topic'].split(',') if config["topic"] else [])
        if pdata['topic'] in all_topics:
            state['message'] = "该场景已存在，请重命名场景标签"
            return json.dumps(state)
 
        skb = database.selector.select("Config", name=database.skb).first()
        if skb:
            # 追加并更新可用话题集
            topics = skb["topic"].split(",") if skb["topic"] else []
            topics.append(pdata['topic'])
            skb["topic"] = ",".join(set(topics))
            database.graph.push(skb)
            
            etids_data = database.graph.run("MATCH (n:NluCell) WHERE n.topic='"\
                + pdata['topic'] + "' RETURN n.tid as t").data()
            etids = [each['t'] for each in etids_data]
            count = len(etids)
            if pdata['tid'] == '': # 子节点先生成 tid 再添加
                # 若之前删除过其它子树，tid 应选取 <=count 范围内与其它节点 tid 不重复的值
                atid = list(set(range(0, count+1)) - set(etids))
                tid = int(atid[0])
            elif int(pdata['tid']) == 0: # 根节点直接添加
                if count > 0:
                    state['message'] = "根节点已存在"
                    return json.dumps(state)
                tid = int(pdata['tid'])

            database.add_nlucell(
                name=pdata['name'],
                content=pdata['content'],
                topic=pdata['topic'],
                tid=tid,
                ftid=int(pdata['ftid']),
                behavior='0x1500',
                parameter=pdata['parameter'], # str
                txt=pdata['txt'],
                img=pdata['img'],              # str
                button=pdata['button'],
                description=pdata['description'],
                delimiter="|"
            )
            state['success'] = 1
            state['message'] = "添加场景节点成功"
            return json.dumps(state)
        else:
            state['message'] = "请先选择知识库再添加场景节点"
            return json.dumps(state)

@app.route("/scene/edit", methods=['GET', 'POST'])
def scene_edit():
    """编辑场景节点
    """
    data = {
        'akb': get_available_kb(),
        'skb': database.skb
    }
    if request.method == 'POST':
        state = {
            'success' : 0,
            'message' : "问题不能为空"
        }
        pdata = request.form.to_dict()
        name = pdata['pre_name']
        if not name or not pdata['name']:
            return json.dumps(state)
        # TODO：需确保 pdata['topic'] 和原 topic 一致
        node = database.selector.select("NluCell").where("_.name ='" + name + "'", \
            "_.topic ='" + pdata['topic'] + "'", "_.tid =" + str(pdata['tid'])).first()
        if node:
            # TODO：加入格式检查
            node['name'] = pdata['name']
            node['content'] = pdata['content']
            # topic 不能编辑或者编辑后必须调整对应知识库 Config 节点的 topic 属性
            # node['topic']=pdata['topic']
            node['tid']=int(pdata['tid'])
            node['ftid']=int(pdata['ftid'])
            # node['behavior']=pdata['behavior'] # behavior 不能编辑
            node['parameter']=pdata['parameter']
            if pdata['pre_name'] != pdata['name']: # Modify 2018-2-7
                node['tag'] = get_tag(node['name'], database.user)
            node['txt']=pdata['txt']
            node['img']=pdata['img']
            node['button']=pdata['button']
            node['description']=pdata['description']
            database.graph.push(node)
            state['success'] = 1
            state['message'] = "编辑场景节点成功"
            return json.dumps(state)
        else:
            state['message'] = "该场景节点不存在，您可以添加"
            return json.dumps(state)
    return json.dumps(data)

@app.route("/scene/delete", methods=['GET', 'POST'])
def scene_delete():
    """删除场景节点及其所有子节点
    """
    data = {
        'akb': get_available_kb(),
        'skb': database.skb
    }
    if request.method == 'POST':
        state = {
            'success' : 0,
            'message' : "问题不能为空"
        }
        pdata = request.form.to_dict()
        name = pdata['name']
        if not name:
            return json.dumps(state)
        # 循环删除当前节点及其所有子节点
        tids = []
        childs = list(database.selector.select("NluCell").where("_.name ='" + name + "'", \
            "_.topic ='" + pdata['topic'] + "'", "_.tid =" + str(pdata['tid'])))
        if childs:
            while childs:
                for child in childs:
                    tids.append(child['tid'])
                    database.graph.delete(child)
                childs = []
                for tid in tids:
                    childs.extend(list(database.selector.select("NluCell").where("_.topic ='" + \
                        pdata['topic'] + "'", "_.ftid =" + str(tid))))
                tids = []
            state['success'] = 1
            state['message'] = "删除场景节点成功"
            return json.dumps(state)
        else:
            state['message'] = "该场景节点不存在"
            return json.dumps(state)
    return json.dumps(data)

@app.route("/scene/add/single", methods=['GET', 'POST'])
def scene_add_single():
    """添加单节点场景
    单节点场景的 content='', topic=database.skb, tid=0, behavior='0x1500'
    """
    data = {
        'akb': get_available_kb(),
        'skb': database.skb
    }
    if request.method == 'POST':
        state = {
            'success' : 0,
            'message' : "问题不能为空"
        }
        pdata = request.form.to_dict()
        if not pdata['name']:
            return json.dumps(state)
        skb = database.selector.select("Config", name=database.skb).first()
        # 追加并更新可用话题集
        if skb:
            match_str = "MATCH (n:NluCell {name:'"+ pdata['name'] + "'}) WHERE '" \
                + skb['topic'] + "' CONTAINS n.topic RETURN n"
            node = list(database.graph.run(match_str).data())
            if node:
                state['message'] = "问题已存在"
                return json.dumps(state)
            topics = skb["topic"].split(",") if skb["topic"] else []
            topics.append(database.skb)
            skb["topic"] = ",".join(set(topics))
            database.graph.push(skb)
            database.add_nlucell(
                name=pdata['name'],
                content='',
                topic=database.skb,
                tid=0,
                ftid=0,
                behavior='0x1500',
                description=pdata['description'],
                delimiter="|"
            )
            state['success'] = 1
            state['message'] = "添加单节点场景成功"
            return json.dumps(state)
        else:
            state['message'] = "请先选择知识库再添加单节点场景"
            return json.dumps(state)
    return json.dumps(data)

@app.route("/scene/edit/single", methods=['GET', 'POST'])
def scene_edit_single():
    """编辑单节点场景
    """
    data = {
        'akb': get_available_kb(),
        'skb': database.skb
    }
    if request.method == 'POST':
        state = {
            'success' : 0,
            'message' : "问题不能为空"
        }
        pdata = request.form.to_dict()
        name = pdata['pre_name']
        if not name or not pdata['name']:
            return json.dumps(state)
        node = database.selector.select("NluCell").where("_.name ='" + name + "'", \
            "_.topic ='" + database.skb + "'", "_.tid =0").first()
        if node:
            # TODO：加入格式检查
            node['name'] = pdata['name']
            node['content'] = pdata['content']
            node['description']=pdata['description']
            database.graph.push(node)
        else:
            database.add_nlucell(
                name=pdata['name'],
                content=pdata['content'],
                topic=database.skb,
                tid=0,
                ftid=0,
                behavior='0x1500',
                description=pdata['description'],
                delimiter="|"
            )
        state['success'] = 1
        state['message'] = "编辑场景节点成功"
        return json.dumps(state)
    return json.dumps(data)

@app.route("/scene/delete/single", methods=['GET', 'POST'])
def scene_delete_single():
    """删除单节点场景
    """
    data = {
        'akb': get_available_kb(),
        'skb': database.skb
    }
    if request.method == 'POST':
        state = {
            'success' : 0,
            'message' : "问题不能为空"
        }
        pdata = request.form.to_dict()
        name = pdata['name']
        if not name:
            return json.dumps(state)
        node = database.selector.select("NluCell").where("_.name ='" + name + "'", \
            "_.topic ='" + database.skb + "'", "_.tid =0").first()
        if node:
            database.graph.delete(node)
            state['success'] = 1
            state['message'] = "删除单节点场景成功"
            return json.dumps(state)
        else:
            state['message'] = "该单节点场景不存在"
            return json.dumps(state)
    return json.dumps(data)

def start(port=5000):
    app.run(debug=True, port=port, threaded=True)

if __name__ == '__main__':
    # start(port=getConfig("kmserver", "port"))
    start()
