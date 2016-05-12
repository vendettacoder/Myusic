# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 02:12:53 2016

@author: Rohan Kulkarni
@email : rohan.kulkarni@columbia.edu

"""
from flask import Flask,render_template,request,jsonify
import pickle
import operator
import indicoio


clusters = pickle.load(open("../src/clusters.p", "rb"))
app = Flask(__name__,static_url_path='/static')

frequency_list = list()

@app.route('/')
def displayWordCloud():
    return_dict = dict()
    global frequency_list
    frequency_list = []
    for i in xrange(len(clusters)):
        cloud_dict = dict()
        cloud_dict['text'] = clusters[i]['Topic']
        cloud_dict['size'] = clusters[i]['Weight']/2
        frequency_list.append(cloud_dict)
    chart = dict()
    chart['x'] = range(1,len(clusters)+1)
    chart['y'] = [len(cluster['Songs']) for cluster in clusters]
    return_dict['frequency_list'] = frequency_list
    return_dict['chart'] = chart
    return render_template('homepage.html',return_dict=return_dict)

@app.route('/results_on_lyrics', methods=['POST'])
def getSimilarSongsGivenLyrics():
    lyrics = request.form['song_lyrics']
    lyrics = lyrics.strip().lower()
    lyrics_set = set(lyrics.split(' '))
    lyrics_array = list(lyrics_set)
    cluster_score_result = [0,0]
    for i, cluster in enumerate(clusters):
        score = 0
        for lyrics_word in lyrics_array:
            if lyrics_word in cluster['Words']:
                score += 1
        if score > cluster_score_result[1]:
            cluster_score_result[1] = score
            cluster_score_result[0] = i
    cluster_number = cluster_score_result[0]
    print("Cluster number: "+str(cluster_number))
    song_score = []
    name_preference_songs = []
    name_preference = False
    for filename in clusters[cluster_number]['Songs']:
        name_preference = False
        file_array = filename[:-4].split('_')
        for lyric in lyrics_array:
            if lyric in file_array:
                name_preference_songs.append((filename,20))
                name_preference = True
                break
        if name_preference == False:
            with open('../Songs/'+filename, 'r') as f:
                song_data = f.read()
                f.close()
            song_data_set = set(song_data.strip().lower().split(' '))
            score = len(lyrics_set.intersection(song_data_set))
            song_score.append((filename, score))
    result = sorted(song_score, key=operator.itemgetter(1))[-10:]
    result.reverse()
    result = name_preference_songs+result
    result = result[:10]
    return_dict = dict()
    song_list = []
    for filename in result:
        each_song = dict()
        name = filename[0]
        with open('../Songs/'+name, 'r') as f:
            lyrics = f.read()
            f.close()
        each_song['name'] = " ".join(name[:-4].split('_'))
        each_song['lyrics'] = lyrics
        song_list.append(each_song)
    return_dict['song_list'] = song_list
    chart = dict()
    chart['x'] = range(1,len(clusters)+1)
    chart['y'] = [len(cluster['Songs']) for cluster in clusters]
    return_dict['chart'] = chart
    global frequency_list
    return_dict['frequency_list'] = frequency_list
    return render_template("homepage.html",return_dict = return_dict)


@app.route('/results_on_name', methods=['POST'])
def getSimilarSongsGivenFile():
    filename = request.form['song_name'].strip().lower()
    if filename[-4:] != ".txt":
        filename += ".txt"
    filename = filename.replace(" ","_")
    with open('../Songs/'+filename, 'r') as f:
        filename_data = f.read()
        f.close()
    filename_data_set = set(filename_data.strip().lower().split(' '))
    for i,cluster in enumerate(clusters):
        if filename in cluster['Songs']:
            cluster_number = i
            break
    print("Cluster number: "+str(cluster_number))
    song_score = []
    for filename1 in clusters[cluster_number]['Songs']:
        if filename1 == filename:
            continue
        with open('../Songs/'+filename1, 'r') as f:
            song_data = f.read()
            f.close()
        song_data_set = set(song_data.strip().lower().split(' '))
        score = len(filename_data_set.intersection(song_data_set))
        song_score.append((filename1, score))
    result = sorted(song_score, key=operator.itemgetter(1))[-10:]
    result.reverse()
    return_dict = dict()
    song_list = []
    for filename in result:
        each_song = dict()
        name = filename[0]
        with open('../Songs/'+name, 'r') as f:
            lyrics = f.read()
            f.close()
        each_song['name'] = " ".join(name[:-4].split('_'))
        each_song['lyrics'] = lyrics
        song_list.append(each_song)
    return_dict['song_list'] = song_list
    global frequency_list
    return_dict['frequency_list'] = frequency_list
    chart = dict()
    chart['x'] = range(1,len(clusters)+1)
    chart['y'] = [len(cluster['Songs']) for cluster in clusters]
    return_dict['chart'] = chart
    return render_template("homepage.html",return_dict = return_dict)

@app.route('/cluster_songs', methods=['POST'])
def getSongsGivenCluster():
    word_input_set = request.form['data']
    word_input_set = set(word_input_set.split(','))
    for i, cluster in enumerate(clusters):
        cluster_set = set(cluster['Words'])
        if word_input_set.intersection(cluster_set) == word_input_set:
            cluster_number = i
            break
    print("Cluster number: "+str(cluster_number))
    result = clusters[cluster_number]['Songs'][:10]
    return_dict = dict()
    song_list = []
    for name in result:
        each_song = dict()
        with open('../Songs/'+name, 'r') as f:
            lyrics = f.read()
            f.close()
        each_song['name'] = " ".join(name[:-4].split('_'))
        each_song['lyrics'] = lyrics
        song_list.append(each_song)
    return_dict['song_list'] = song_list
    global frequency_list
    return_dict['frequency_list'] = frequency_list
    return render_template("render_songs_template.html",return_dict=return_dict)

@app.route('/search_word_statistics/',methods=['POST'])
def getWordStatistics():
    word = request.form['word'].strip().split(" ")[0]
    word_counts_across_clusters = list()

    for cluster in clusters:
        word_count = 0
        for song in cluster['Songs']:
            with open('../Songs/'+song, 'r') as f:
                lyrics = f.read()
                f.close()
            lyrics_list = lyrics.lower().split()
            word_count += lyrics_list.count(word.lower())
        word_counts_across_clusters.append(word_count)

    return_dict = dict()
    return_dict['x'] = range(1,len(clusters)+1)
    return_dict['y'] = word_counts_across_clusters
    return jsonify(chart=return_dict)

@app.route('/get_song_emotions/',methods=['POST'])
def getSongEmotions():
    indicoio.config.api_key = '781cddf05f6cb0d88449272c8c7768eb'
    filename = request.form['song_name'].strip().lower()
    if filename[-4:] != ".txt":
        filename += ".txt"
    filename = filename.replace(" ","_")
    with open('../Songs/'+filename, 'r') as f:
        filename_data = f.read()
        f.close()
    text = filename_data.strip()
    emotion_dict = indicoio.emotion(text)

    return_dict = dict()
    return_dict['data'] = [[emotion,score] for emotion,score in zip(emotion_dict.keys(),emotion_dict.values())]
    return jsonify(chart=return_dict)


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost',port=8082)
