from flask import Flask, jsonify,request,render_template
from flask import make_response
from flask_cors import CORS
import json
import requests
import numpy as np
import pickle
from game import Board, Game
from mcts_pure import MCTSPlayer as MCTS_Pure
from mcts_alphaZero import MCTSPlayer
from policy_value_net_numpy import PolicyValueNetNumpy
import pandas as pd

app = Flask(__name__)
CORS(app)
width, height = 8, 8
model_file = 'best_policy_8_8_5.model'
policy_param = pickle.load(open(model_file, 'rb'))
best_policy = PolicyValueNetNumpy(width, height, policy_param)
mcts_player = MCTSPlayer(best_policy.policy_value_fn,
 c_puct=5, n_playout=40)



def get_action(data, mcts_player):
    # return [x,y]
    #print (data)
    board = Board(1,data)
    board.get_current_player()
    move = mcts_player.get_action(board)
    i = move/8
    j = move%8
    print (i,j)
    i = 7-i
    #j = 7-j
    return [j,i]

def generate_score_board(j):
    print(sorted(j.items(),key=lambda item:item[1]))

    dict ={'id':[],'number-of-step':[]}
    for item in sorted(j.items(),key=lambda item:item[1]):
        dict['id'].append(item[0])
        dict['number-of-step'].append(item[1])
    df = pd.DataFrame(dict)
    HEADER = '''
        <html>
            <head>
                <style>
                    .df tbody tr:last-child { background-color: #FF0000; }
                </style>
            </head>
            <body>
        '''

    FOOTER = '''
        </body>
    </html>
    '''
    with open('scoreboard/index.html', 'w') as f:
        f.write(HEADER)
        f.write(df.to_html(classes='df'))
        f.write(FOOTER)

def update_score_board(id,step_number):
    with open('scoreboard/score.json') as f:
        j=json.load(f)
    with open('scoreboard/score.json','w') as f:
        if id in j.keys():
            if j[id] > step_number:
                j[id] = step_number
        else:
            j[id] = step_number
        f.write(json.dumps(j))
        generate_score_board(j)


@app.route('/post/', methods=['GET', 'POST'])
def real_time_api():
    if request.method == 'POST':

        #print(dir(request.values))
        dict=request.values.to_dict()
        data=np.zeros([8,8])
        for i in range(len(dict.keys())/3):
            x=int(dict['data[%d][x]'%i])
            y=int(dict['data[%d][y]'%i])
            player=dict['data[%d][player]'%i]
            if player == u'true':
                data[y][x]=1
            else:
                data[y][x]=2
        print(data) 

        response={}
        response['result']=get_action(data,mcts_player)
        
        return jsonify(response)

@app.route('/scoreboard/', methods=['GET', 'POST'])
def real_time_api_2():
    if request.method == 'POST':

        #print(dir(request.values))
        dict=request.values.to_dict()
        print(dict)
        update_score_board(dict['id'],(len(dict.keys())-1)/3);
        
        response={'23':'23232'}
        
        return jsonify(response)


if __name__ == '__main__':
    app.run(host= '192.168.1.104',port=8080,debug=True)
