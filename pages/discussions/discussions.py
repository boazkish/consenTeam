from flask import Blueprint, render_template, redirect, url_for, request, session
from datetime import datetime
# discussions blueprint definition
from markupsafe import Markup
from utilities.db.quries import DBQuery

discussions = Blueprint('discussions', __name__, static_folder='static', static_url_path='/discussions',
                        template_folder='templates')


# Routes
@discussions.route('/discussions')
def redirect_discussions():
    query = DBQuery()
    discussions = query.get_all_discussions()
    list = []
    if session['logged_in']:
        favorites = query.get_favorites(session['email'])
        for f in favorites:
            list.append(f[0])

    return render_template('discussions.html', discussions=discussions, list=list)


@discussions.route('/discussions/insert', methods=['GET', 'POST'])
def insert_discussions():
    if request.method == 'POST':
        topic = request.form['title']
        description = request.form['description']
        d_date = request.form['date']
        query = DBQuery()
        max_id = query.get_max_id_discuss()
        discussion = query.insert_discuss(max_id, topic, description, d_date, session['email'])
    return redirect('/discussions')


@discussions.route('/discussions/insert_comments/<discussion_id>/<parent_id>', methods=['GET', 'POST'])
def insert_comments(discussion_id, parent_id):
    if request.method == 'POST':
        topic = request.form['title']
        query = DBQuery()
        node_level = query.get_node_id_level(parent_id)
        node_level = int(node_level) + 1
        inserted_comment = query.insert_node_comment(discussion_id, parent_id, topic, session['email'], node_level)
    return redirect('/discussions/' + discussion_id)


@discussions.route('/discussions/insert_favorite/<discussion_id>')
def insert_favorite(discussion_id):
    query = DBQuery()
    if session['logged_in']:
        query.insert_favorite(session['email'], discussion_id)
    return redirect('/discussions')


@discussions.route('/discussions/delete_favorite/<discussion_id>')
def delete_favorite(discussion_id):
    query = DBQuery()
    query.delete_favorite(session['email'], discussion_id)
    return redirect('/discussions')


@discussions.route('/discussions/<discussion_id>')
def discussion_page_main(discussion_id):
    query = DBQuery()
    discussion = query.get_discussions_by_id(discussion_id)
    comments = query.get_all_comments_list(discussion_id)
    graph = {}
    counter = 1
    level = [1]

    for s in comments:
        mylist = []
        node_id = s[0]
        counter = counter + 1
        for j in comments:
            parent_id = (j[2])
            if parent_id == node_id:
                level.append(counter)
                mylist.append(str(j[0]))
                graph[str(node_id)] = mylist
        if str(node_id) not in graph:
            graph[str(node_id)] = []

    global html_string
    status = discussion[0][6]
    html_string = []
    visited = dfs(graph, str(comments[0][0]), [], html_string, comments, status)
    str1 = ''.join(html_string)
    user = ''
    merge_comments = ''
    joined = ''
    big_dict = {}
    for c in comments:
        parent_id = c[2]
        parent_content = c[3]
        value_list = []
        if parent_id is None:
            value_list.insert(0, parent_content)
            big_dict[c[0]] = value_list
        else:
            while parent_id is not None:
                value_list.insert(0, parent_content)
                big_dict[c[0]] = value_list
                parent_id, parent_content = query.get_parent_id(parent_id)
    print(big_dict)
    user_score_discussion = ''
    if session['logged_in']:
        user = query.get_user_details(session['email'])
        user_score_discussion = query.get_user_vote_details_discussion(discussion_id, session['email'])
        merge_comments = query.get_merge_list(discussion_id)
        joined = query.check_if_joined(discussion_id, session['email'])

    return render_template('discussion_page.html', discussion=discussion, comments=comments,
                           main=True, tree=False, html_string=Markup(str1), user=user, merge_list=merge_comments,
                           joined=joined, user_score_discussion=user_score_discussion, big_dict=big_dict)


@discussions.route('/discussions/<discussion_id>/info')
def discussion_page_info(discussion_id):
    query = DBQuery()
    discussion = query.get_discussions_by_id(discussion_id)
    comments = query.get_all_comments_list(discussion_id)
    user = ''
    joined = ''
    user_score_discussion = ''
    big_dict = {}
    for c in comments:
        parent_id = c[2]
        parent_content = c[3]
        value_list = []
        while parent_id is not None:
            value_list.insert(0, parent_content)
            big_dict[c[0]] = value_list
            parent_id, parent_content = query.get_parent_id(parent_id)
    if session['logged_in']:
        user = query.get_user_details(session['email'])
        joined = query.check_if_joined(discussion_id, session['email'])
        user_score_discussion = query.get_user_vote_details_discussion(discussion_id, session['email'])

    return render_template('discussion_page.html', discussion=discussion, comments=comments, main=False, user=user,
                           joined=joined, user_score_discussion=user_score_discussion, big_dict=big_dict)


@discussions.route('/discussions/<discussion_id>/settings')
def discussion_page_settings(discussion_id):
    query = DBQuery()
    discussion = query.get_discussions_by_id(discussion_id)
    comments = query.get_all_comments_list(discussion_id)
    user = ''
    joined = ''
    user_score_discussion = ''
    big_dict = {}
    for c in comments:
        parent_id = c[2]
        parent_content = c[3]
        value_list = []
        while parent_id is not None:
            value_list.insert(0, parent_content)
            big_dict[c[0]] = value_list
            parent_id, parent_content = query.get_parent_id(parent_id)
    user_score_discussion = ''
    if session['logged_in']:
        user = query.get_user_details(session['email'])
        joined = query.check_if_joined(discussion_id, session['email'])
        user_score_discussion = query.get_user_vote_details_discussion(discussion_id, session['email'])
    return render_template('discussion_page.html', discussion=discussion, comments=comments, main=False, user=user,
                           joined=joined, user_score_discussion=user_score_discussion, big_dict=big_dict, settings=True)


@discussions.route('/discussions/<discussion_id>/tree', methods=['GET', 'POST'])
def discussion_page_tree(discussion_id):
    query = DBQuery()
    discussion = query.get_discussions_by_id(discussion_id)
    comments = query.get_all_comments_list(discussion_id)
    graph = {}
    counter = 1
    level = [1]
    # num75 = get_num_75(discussion_id)
    # get_nodes_75(discussion_id, num75)
    for s in comments:
        mylist = []
        node_id = s[0]
        counter = counter + 1
        for j in comments:
            parent_id = (j[2])
            if parent_id == node_id:
                level.append(counter)
                mylist.append(str(j[0]))
                graph[str(node_id)] = mylist
        if str(node_id) not in graph:
            graph[str(node_id)] = []

    global html_string
    html_string = []
    status = discussion[0][6]
    visited = dfs(graph, str(comments[0][0]), [], html_string, comments, status)
    str1 = ''.join(html_string)
    user = ''
    joined = ''
    user_score_discussion = ''
    if session['logged_in']:
        user = query.get_user_details(session['email'])
        joined = query.check_if_joined(discussion_id, session['email'])
        user_score_discussion = query.get_user_vote_details_discussion(discussion_id, session['email'])
    print('bbbbbbbbbb')
    big_dict = {}

    for c in comments:
        parent_id = c[2]
        parent_content = c[3]
        value_list = []
        if parent_id is None:
            value_list.insert(0, parent_content)
            big_dict[c[0]] = value_list
        else:
            while parent_id is not None:
                value_list.insert(0, parent_content)
                big_dict[c[0]] = value_list
                parent_id, parent_content = query.get_parent_id(parent_id)
    print(big_dict)

    return render_template('discussion_page.html', discussion=discussion, comments=comments, html_string=Markup(str1),
                           main=True, tree=True, status=True, user=user, user_score_discussion=user_score_discussion,
                           joined=joined, big_dict=big_dict)


def dfs_voting(graph, node, visited, discussion_id, amount):
    if node not in visited:
        query = DBQuery()
        visited.append(node)
        query.rank_final_decision(session['email'], discussion_id, node, amount)

        for k in graph[node]:
            dfs_voting(graph, k, visited, discussion_id, amount)
    return visited


def dfs(graph, node, visited, html_string, comments, status):
    if node not in visited:
        for c in comments:
            if str(c[0]) == node:
                if status == 'Open':
                    html_string.append(
                        "<li><a id='modalBtn" + str(
                            c[0]) + "' onclick='new_comment(" + str(c[0]) + ")'>" + c[
                            3] + "<i class='fa fa-plus fa-1x'></i></a>")
                else:
                    html_string.append(
                        "<li><a id='modalBtn_rank" + str(c[0]) + "' onclick='rank_comment(" + str(c[0]) + ")'>" + c[
                            3] + "</a>" + "<div class='score'>" "   +" + str(c[6]) + "</div>")
        if len(graph[node]) > 0:
            html_string.append('<ul>')
        visited.append(node)

        for k in graph[node]:
            test_list = [int(i) for i in graph[node]]
            dfs(graph, k, visited, html_string, comments, status)
            html_string.append('</li>')
            if str(max(test_list)) == k:
                html_string.append('</ul></li>')

    return html_string


def get_num_75(discussion_id, percentile):
    query = DBQuery()
    comments = query.get_all_comments_list(discussion_id)
    num_of_rows = len(comments)
    percent = percentile / 100.0
    # print(len(comments))
    table75 = int(num_of_rows * percent + 0.99)
    print(table75)
    return table75


def get_nodes_75(discussion_id, num75):
    query = DBQuery()
    comments = query.get_all_comments_list(discussion_id)
    num_of_rows = len(comments)
    print('this is num of rows')
    print(num_of_rows)
    print('this is num 75')
    print(num75)
    while num_of_rows > num75:
        minimum_node = get_min_rank(discussion_id)
        affect_row = query.delete_min_rank(minimum_node)
        comments = query.get_all_comments_list(discussion_id)
        num_of_rows = len(comments)


def get_min_rank(discussion_id):
    query = DBQuery()
    comments = query.get_all_comments_list(discussion_id)
    min_score = int(comments[0][6])
    # level = int(comments[0][5])
    min_node_id = int(comments[0][0])
    for i in comments:
        print('this is i6')
        print(i[6])
        print(min_score)
        print(i[5])
        print('iteration number')
        print(i)
        level = query.get_level_parent(int(i[0]))
        if int(i[6]) <= min_score and int(i[5]) > level:
            min_score = int(i[6])
            min_node_id = int(i[0])

    return min_node_id


@discussions.route('/discussions/rank_node/<discussion_id>/<parent_id>', methods=['GET', 'POST'])
def rank_node(discussion_id, parent_id):  # parent_id is node_id
    query = DBQuery()
    temp_parent = parent_id
    status = query.get_discussions_by_id(discussion_id)
    if status[0].status == 'Voting':
        if request.method == 'POST':
            amount = request.form['rank']
            query = DBQuery()
            first_time = 0
            last_time = 1
            last_parent = parent_id
            while parent_id is not None:
                print('Boaz')
                print(parent_id)
                rank_node = query.vote_for_comment(session['email'], discussion_id, parent_id, amount, first_time,
                                                   last_time)
                parent_id, parent_content = query.get_parent_id(parent_id)
            first_time = 1
            last_time = 0
            rank_node = query.vote_for_comment(session['email'], discussion_id, last_parent, amount, first_time,
                                               last_time)
    else:
        if request.method == 'POST':
            amount = request.form['rank']
            query = DBQuery()
            discussion = query.get_discussions_by_id(discussion_id)
            comments = query.get_all_comments_list(discussion_id)
            # sub_comments = query.get_all_sub_comments_list(discussion_id)
            graph = {}
            counter = 1
            level = [1]
            # num75 = get_num_75(discussion_id)
            # get_nodes_75(discussion_id, num75)
            for s in comments:
                # if node_id == s[0].node_id
                mylist = []
                node_id = s[0]
                counter = counter + 1
                for j in comments:
                    parent_id = (j[2])
                    if parent_id == node_id:
                        level.append(counter)
                        mylist.append(str(j[0]))
                        graph[str(node_id)] = mylist
                if str(node_id) not in graph:
                    graph[str(node_id)] = []
            visited = dfs_voting(graph, temp_parent, [], discussion_id, amount)
            print('we are printing dfs VOTING VISITED @@@@@@@@@@@@@@@@@@@@@@@')
            print('we are printing dfs VOTING VISITED @@@@@@@@@@@@@@@@@@@@@@@')
            print(visited)
            query.rank_final_decision(session['email'], discussion_id, parent_id, amount)

    return redirect('/discussions/' + discussion_id + '/tree')


@discussions.route('/discussions/<discussion_id>/tree/remove_branches', methods=['GET', 'POST'])
def remove_branches(discussion_id):
    query = DBQuery()
    discussion = query.get_discussions_by_id(discussion_id)
    comments = query.get_all_comments_list(discussion_id)
    graph = {}
    counter = 1
    level = [1]
    if request.method == 'POST':
        percentile = int(request.form['percentile'])
    num75 = get_num_75(discussion_id, percentile)
    get_nodes_75(discussion_id, num75)
    for s in comments:
        mylist = []
        node_id = s[0]
        counter = counter + 1
        for j in comments:
            parent_id = (j[2])
            if parent_id == node_id:
                level.append(counter)
                mylist.append(str(j[0]))
                graph[str(node_id)] = mylist
        if str(node_id) not in graph:
            graph[str(node_id)] = []

    global html_string
    html_string = []
    status = discussion[0][6]
    print(status)
    visited = dfs(graph, str(comments[0][0]), [], html_string, comments, status)
    str1 = ''.join(html_string)
    user = query.get_user_details(session['email'])
    reset_ranking = query.reset_ranking(discussion_id)
    return redirect(url_for('discussions.discussion_page_tree', discussion_id=discussion_id, discussion=discussion,
                            comments=comments, html_string=Markup(str1),
                            main=True, tree=True, status=True, user=user))


@discussions.route('/change_status', methods=['POST', 'GET'])
def change_status():
    query = DBQuery()
    if request.method == 'POST':
        status = request.form['status']
        discussion_id = request.form['discussion_id']
        if status == 'Open' or 'Final Voting':
            score_tokens_update = query.set_default_user_tokens(discussion_id)
        print(status)
        status_update = query.update_discussion_status(discussion_id, status)
    return redirect('/discussions/' + discussion_id + '/tree')


@discussions.route('/join_new_discussion/<discussion_id>', methods=['POST', 'GET'])
def join_new_discuss(discussion_id):
    if request.method == 'POST':
        query = DBQuery()
        email = session['email']
        discuss_id = discussion_id
        joined = query.check_if_joined(discuss_id, email)
        if not joined:
            query.initial_score_for_discussion(discuss_id, email)

    return redirect('/discussions/' + discussion_id)


discussions.route('/final_decision/<discussion_id>', methods=['POST', 'GET'])


def final_decision(discussion_id):
    if request.method == 'POST':
        query = DBQuery()

    return redirect('/discussions/' + discussion_id)
